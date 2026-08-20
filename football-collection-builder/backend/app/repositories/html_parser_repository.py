from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Literal

from app.database.database import DEFAULT_DATABASE_PATH, Database
from app.database.schema import HTML_PARSER_TABLES, SCHEMA_SQL
from app.models.html_parser import (
    HtmlHeading, HtmlImageContext, HtmlImageReference, HtmlLinkReference, HtmlMissingReference,
    HtmlMissingReferencesResponse, HtmlPageDetails, HtmlPageListItem, HtmlPageResult,
    HtmlPagesResponse, HtmlParseError, HtmlParseRun, HtmlParseStatus, HtmlParseSummary,
)


class HtmlParserRepository:
    def __init__(self, database_path: str | Path = DEFAULT_DATABASE_PATH):
        self.database = Database(database_path)

    def create_schema(self) -> None:
        with self.database.connect() as connection:
            connection.executescript(SCHEMA_SQL)
            columns={x['name'] for x in connection.execute('pragma table_info(html_image_contexts)')}
            for name,kind in [('image_container_dom_index','INTEGER'),('description_container_dom_index','INTEGER'),('structural_group_key','TEXT'),('image_container_type','TEXT'),('description_container_type','TEXT'),('structural_order','INTEGER')]:
                if name not in columns:connection.execute(f'alter table html_image_contexts add column {name} {kind}')

    def save_run(
        self, run: HtmlParseRun, pages: list[HtmlPageResult],
        errors: list[HtmlParseError], replace_previous: bool = True,
    ) -> int:
        self.create_schema()
        connection = self.database.connect()
        try:
            connection.execute("PRAGMA foreign_keys = ON")
            connection.execute("BEGIN")
            if replace_previous:
                for table in reversed(HTML_PARSER_TABLES):
                    connection.execute(f"DELETE FROM {table}")
            cursor = connection.execute(
                """INSERT INTO html_parse_runs(
                workspace_path,started_at,finished_at,duration_ms,status,total_pages,parsed_pages,
                failed_pages,image_references,internal_links,external_links,missing_references,message)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (run.workspacePath, run.startedAt, run.finishedAt, run.durationMs, run.status.value,
                 run.totalPages, run.parsedPages, run.failedPages, run.imageReferences,
                 run.internalLinks, run.externalLinks, run.missingReferences, run.message),
            )
            run_id = int(cursor.lastrowid)
            for page in pages:
                page_id = self._save_page(connection, run_id, page)
                self._save_references(connection, page_id, page)
            connection.executemany(
                """INSERT INTO html_parse_errors(run_id,inventory_item_id,relative_path,error_type,message)
                   VALUES(?,?,?,?,?)""",
                [(run_id, e.inventoryItemId, e.relativePath, e.errorType, e.message) for e in errors],
            )
            connection.commit()
            return run_id
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def _save_page(self, connection: sqlite3.Connection, run_id: int, page: HtmlPageResult) -> int:
        cursor = connection.execute(
            """INSERT INTO html_pages(run_id,inventory_item_id,relative_path,absolute_path,filename,
            extension,file_size,created_at,modified_at,encoding_used,title,document_language,
            charset_declared,meta_description,text_preview,parse_status,parse_message)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (run_id, page.inventoryItemId, page.relativePath, page.absolutePath, page.filename,
             page.extension, page.fileSize, page.createdAt, page.modifiedAt, page.encodingUsed,
             page.title, page.documentLanguage, page.charsetDeclared, page.metaDescription,
             page.textPreview, page.parseStatus, page.parseMessage),
        )
        page_id = int(cursor.lastrowid)
        connection.executemany(
            "INSERT INTO html_headings(page_id,level,position,text) VALUES(?,?,?,?)",
            [(page_id, h.level, h.position, h.text) for h in page.headings],
        )
        return page_id

    def _save_references(self, connection: sqlite3.Connection, page_id: int, page: HtmlPageResult) -> None:
        image_ids=[]
        for x in page.imageReferences:
            cursor=connection.execute(
            """INSERT INTO html_image_references(page_id,src_original,src_normalized,alt_text,
            title_text,width_declared,height_declared,is_external,resolved_relative_path,
            resolved_absolute_path,exists_in_inventory,referenced_inventory_item_id,status)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (page_id, x.srcOriginal, x.srcNormalized, x.alt, x.title, x.widthDeclared,
              x.heightDeclared, int(x.isExternal), x.resolvedRelativePath, x.resolvedAbsolutePath,
              int(x.existsInInventory), x.referencedInventoryItemId, x.status.value))
            image_ids.append(int(cursor.lastrowid))
        connection.executemany("""INSERT INTO html_image_contexts(html_page_id,image_reference_id,reference_original,resolved_relative_path,dom_order,container_type,context_text,caption_text,extraction_rule,confidence,status,image_container_dom_index,description_container_dom_index,structural_group_key,image_container_type,description_container_type,structural_order,created_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,datetime('now'))""",[(page_id,image_ids[x.domOrder],x.referenceOriginal,x.resolvedRelativePath,x.domOrder,x.containerType,x.contextText,x.captionText,x.extractionRule,x.confidence,x.status,x.imageContainerDomIndex,x.descriptionContainerDomIndex,x.structuralGroupKey,x.imageContainerType,x.descriptionContainerType,x.structuralOrder) for x in page.imageContexts])
        connection.executemany(
            """INSERT INTO html_link_references(page_id,href_original,href_normalized,visible_text,
            title_text,is_external,is_anchor,is_mailto,is_javascript,resolved_relative_path,
            exists_in_inventory,referenced_inventory_item_id,status) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            [(page_id, x.hrefOriginal, x.hrefNormalized, x.visibleText, x.title, int(x.isExternal),
              int(x.isAnchor), int(x.isMailto), int(x.isJavascript), x.resolvedRelativePath,
              int(x.existsInInventory), x.referencedInventoryItemId, x.status.value)
             for x in page.linkReferences],
        )

    def get_latest_run(self, completed_only: bool = False) -> HtmlParseSummary | None:
        self.create_schema()
        where = "WHERE status IN ('completed','completed_with_errors')" if completed_only else ""
        with self.database.connect() as connection:
            row = connection.execute(f"SELECT * FROM html_parse_runs {where} ORDER BY id DESC LIMIT 1").fetchone()
        return None if row is None else self._run(row)

    @staticmethod
    def _run(row: sqlite3.Row) -> HtmlParseSummary:
        return HtmlParseSummary(
            id=row["id"], workspacePath=row["workspace_path"], startedAt=row["started_at"],
            finishedAt=row["finished_at"], durationMs=row["duration_ms"],
            status=HtmlParseStatus(row["status"]), totalPages=row["total_pages"],
            parsedPages=row["parsed_pages"], failedPages=row["failed_pages"],
            imageReferences=row["image_references"], internalLinks=row["internal_links"],
            externalLinks=row["external_links"], missingReferences=row["missing_references"],
            message=row["message"],
        )

    def get_pages(self, limit: int, offset: int, status: str | None, search: str | None) -> HtmlPagesResponse:
        run = self.get_latest_run(completed_only=True)
        if run is None:
            return HtmlPagesResponse(items=[], total=0, limit=limit, offset=offset)
        conditions, params = ["p.run_id = ?"], [run.id]
        if status:
            conditions.append("p.parse_status = ?"); params.append(status)
        if search:
            conditions.append("(p.relative_path LIKE ? OR p.title LIKE ?)")
            params.extend([f"%{search}%", f"%{search}%"])
        where = " AND ".join(conditions)
        query = f"""SELECT p.*,
          (SELECT count(*) FROM html_image_references i WHERE i.page_id=p.id) image_count,
          (SELECT count(*) FROM html_link_references l WHERE l.page_id=p.id) link_count,
          (SELECT count(*) FROM html_image_references i WHERE i.page_id=p.id AND i.status='missing') +
          (SELECT count(*) FROM html_link_references l WHERE l.page_id=p.id AND l.status='missing') missing_count
          FROM html_pages p WHERE {where} ORDER BY p.relative_path LIMIT ? OFFSET ?"""
        with self.database.connect() as connection:
            total = connection.execute(f"SELECT count(*) count FROM html_pages p WHERE {where}", params).fetchone()["count"]
            rows = connection.execute(query, [*params, limit, offset]).fetchall()
        items = [HtmlPageListItem(
            id=r["id"], relativePath=r["relative_path"], filename=r["filename"], title=r["title"],
            encodingUsed=r["encoding_used"], imageReferences=r["image_count"],
            linkReferences=r["link_count"], missingReferences=r["missing_count"],
            parseStatus=r["parse_status"],
        ) for r in rows]
        return HtmlPagesResponse(items=items, total=total, limit=limit, offset=offset)

    def get_page(self, page_id: int) -> HtmlPageDetails | None:
        self.create_schema()
        with self.database.connect() as connection:
            p = connection.execute("SELECT * FROM html_pages WHERE id=?", (page_id,)).fetchone()
            if p is None:
                return None
            hs = connection.execute("SELECT * FROM html_headings WHERE page_id=? ORDER BY position", (page_id,)).fetchall()
            images = connection.execute("SELECT * FROM html_image_references WHERE page_id=? ORDER BY id", (page_id,)).fetchall()
            links = connection.execute("SELECT * FROM html_link_references WHERE page_id=? ORDER BY id", (page_id,)).fetchall()
            contexts = connection.execute("SELECT * FROM html_image_contexts WHERE html_page_id=? ORDER BY dom_order", (page_id,)).fetchall()
            errors = connection.execute(
                "SELECT * FROM html_parse_errors WHERE run_id=? AND inventory_item_id=?",
                (p["run_id"], p["inventory_item_id"]),
            ).fetchall()
        return HtmlPageDetails(
            id=p["id"], inventoryItemId=p["inventory_item_id"], relativePath=p["relative_path"],
            absolutePath=p["absolute_path"], filename=p["filename"], extension=p["extension"],
            fileSize=p["file_size"], createdAt=p["created_at"], modifiedAt=p["modified_at"],
            encodingUsed=p["encoding_used"], title=p["title"], documentLanguage=p["document_language"],
            charsetDeclared=p["charset_declared"], metaDescription=p["meta_description"],
            textPreview=p["text_preview"], parseStatus=p["parse_status"], parseMessage=p["parse_message"],
            headings=[HtmlHeading(level=x["level"], position=x["position"], text=x["text"]) for x in hs],
            imageReferences=[HtmlImageReference(
                srcOriginal=x["src_original"], srcNormalized=x["src_normalized"], alt=x["alt_text"],
                title=x["title_text"], widthDeclared=x["width_declared"], heightDeclared=x["height_declared"],
                isExternal=bool(x["is_external"]), resolvedRelativePath=x["resolved_relative_path"],
                resolvedAbsolutePath=x["resolved_absolute_path"], existsInInventory=bool(x["exists_in_inventory"]),
                referencedInventoryItemId=x["referenced_inventory_item_id"], status=x["status"],
            ) for x in images],
            imageContexts=[HtmlImageContext(domOrder=x['dom_order'],referenceOriginal=x['reference_original'],resolvedRelativePath=x['resolved_relative_path'],containerType=x['container_type'],contextText=x['context_text'],captionText=x['caption_text'],extractionRule=x['extraction_rule'],confidence=x['confidence'],status=x['status'],imageContainerDomIndex=x['image_container_dom_index'],descriptionContainerDomIndex=x['description_container_dom_index'],structuralGroupKey=x['structural_group_key'],imageContainerType=x['image_container_type'],descriptionContainerType=x['description_container_type'],structuralOrder=x['structural_order']) for x in contexts],
            linkReferences=[HtmlLinkReference(
                hrefOriginal=x["href_original"], hrefNormalized=x["href_normalized"], visibleText=x["visible_text"],
                title=x["title_text"], isExternal=bool(x["is_external"]), isAnchor=bool(x["is_anchor"]),
                isMailto=bool(x["is_mailto"]), isJavascript=bool(x["is_javascript"]),
                resolvedRelativePath=x["resolved_relative_path"], existsInInventory=bool(x["exists_in_inventory"]),
                referencedInventoryItemId=x["referenced_inventory_item_id"], status=x["status"],
            ) for x in links],
            errors=[HtmlParseError(inventoryItemId=x["inventory_item_id"], relativePath=x["relative_path"],
                                   errorType=x["error_type"], message=x["message"]) for x in errors],
        )

    def get_missing_references(
        self, limit: int, offset: int, reference_type: Literal["image", "link"] | None,
    ) -> HtmlMissingReferencesResponse:
        run = self.get_latest_run(completed_only=True)
        if run is None:
            return HtmlMissingReferencesResponse(items=[], total=0, limit=limit, offset=offset)
        parts = []
        if reference_type in (None, "image"):
            parts.append("""SELECT i.id,p.id page_id,p.relative_path,'image' reference_type,
                          i.src_original original,i.resolved_relative_path,i.status
                          FROM html_image_references i JOIN html_pages p ON p.id=i.page_id
                          WHERE p.run_id=? AND i.status='missing'""")
        if reference_type in (None, "link"):
            parts.append("""SELECT l.id,p.id page_id,p.relative_path,'link' reference_type,
                          l.href_original original,l.resolved_relative_path,l.status
                          FROM html_link_references l JOIN html_pages p ON p.id=l.page_id
                          WHERE p.run_id=? AND l.status='missing'""")
        union = " UNION ALL ".join(parts)
        params = [run.id] * len(parts)
        with self.database.connect() as connection:
            total = connection.execute(f"SELECT count(*) count FROM ({union})", params).fetchone()["count"]
            rows = connection.execute(f"SELECT * FROM ({union}) ORDER BY relative_path,id LIMIT ? OFFSET ?",
                                      [*params, limit, offset]).fetchall()
        return HtmlMissingReferencesResponse(
            items=[HtmlMissingReference(
                id=x["id"], pageId=x["page_id"], sourceRelativePath=x["relative_path"],
                referenceType=x["reference_type"], original=x["original"],
                resolvedRelativePath=x["resolved_relative_path"], status=x["status"],
            ) for x in rows], total=total, limit=limit, offset=offset,
        )

