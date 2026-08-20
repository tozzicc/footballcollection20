from __future__ import annotations

from pathlib import Path

from app.database.database import DEFAULT_DATABASE_PATH, Database
from app.database.schema import SCHEMA_SQL


class HistoricalCollectionsRepository:
    def __init__(self, database_path: str | Path = DEFAULT_DATABASE_PATH):
        self.database = Database(database_path)

    def create_schema(self) -> None:
        with self.database.connect() as connection:
            connection.executescript(SCHEMA_SQL)

    def workspace(self) -> str | None:
        with self.database.connect() as connection:
            row = connection.execute("SELECT workspace_path FROM inventory_metadata WHERE id=1").fetchone()
        return None if row is None else row["workspace_path"]

    def image_lookup(self) -> dict[str, dict]:
        with self.database.connect() as connection:
            rows = connection.execute(
                """SELECT inventory_item_id,relative_path,format,file_size,width,height,aspect_ratio,
                          valid_image,readable,extension,modified_at
                   FROM image_metadata
                   WHERE run_id=(SELECT id FROM image_parse_runs WHERE status='completed' ORDER BY id DESC LIMIT 1)"""
            ).fetchall()
        return {row["relative_path"].replace("\\", "/").casefold(): dict(row) for row in rows}

    def persist(self, run: dict, sections: list[dict], items: list[dict]) -> int:
        connection = self.database.connect()
        try:
            connection.execute("BEGIN")
            columns = ",".join(run)
            run_id = int(connection.execute(
                f"INSERT INTO historical_collection_runs({columns}) VALUES({','.join('?' for _ in run)})",
                tuple(run.values()),
            ).lastrowid)
            for section in sections:
                data = {"run_id": run_id, **section}
                columns = ",".join(data)
                connection.execute(
                    f"INSERT INTO historical_collection_sections({columns}) VALUES({','.join('?' for _ in data)})",
                    tuple(data.values()),
                )
            for item in items:
                media = item.pop("media")
                data = {"run_id": run_id, **item}
                columns = ",".join(data)
                item_id = int(connection.execute(
                    f"INSERT INTO historical_collection_items({columns}) VALUES({','.join('?' for _ in data)})",
                    tuple(data.values()),
                ).lastrowid)
                media_data = {"run_id": run_id, "item_id": item_id, **media}
                columns = ",".join(media_data)
                connection.execute(
                    f"INSERT INTO historical_collection_media({columns}) VALUES({','.join('?' for _ in media_data)})",
                    tuple(media_data.values()),
                )
            connection.commit()
            return run_id
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def latest_run(self) -> dict | None:
        self.create_schema()
        with self.database.connect() as connection:
            row = connection.execute(
                "SELECT * FROM historical_collection_runs WHERE status='completed' ORDER BY id DESC LIMIT 1"
            ).fetchone()
        return None if row is None else dict(row)

    def media_source(self) -> list[dict]:
        run = self.latest_run()
        if run is None:
            return []
        with self.database.connect() as connection:
            rows = connection.execute(
                """SELECT 'historical:'||i.stable_key||':primary' public_media_key,
                          m.inventory_reference,im.relative_path,im.extension,im.format,im.file_size,
                          im.width,im.height,im.aspect_ratio,im.valid_image,im.readable,im.modified_at,
                          'historical_collection' source_type
                   FROM historical_collection_media m
                   JOIN historical_collection_items i ON i.id=m.item_id AND i.run_id=m.run_id
                   JOIN image_metadata im ON im.inventory_item_id=m.inventory_reference
                   WHERE m.run_id=? AND m.is_primary=1 ORDER BY i.section,i.source_order""",
                (run["id"],),
            ).fetchall()
        return [dict(row) for row in rows]

    @staticmethod
    def _camel(row: dict) -> dict:
        result = {}
        for key, value in row.items():
            parts = key.split("_")
            result[parts[0] + "".join(part.title() for part in parts[1:])] = value
        return result

    def _media_key(self, connection, run_id: int, stable_key: str) -> str | None:
        row = connection.execute(
            """SELECT r.media_key FROM media_asset_relations r
               WHERE r.media_run_id=(SELECT id FROM media_build_runs WHERE status='completed' ORDER BY id DESC LIMIT 1)
                 AND r.view_public_media_key=?""",
            (f"historical:{stable_key}:primary",),
        ).fetchone()
        return None if row is None else row["media_key"]

    def _public_item(self, connection, run_id: int, row) -> dict:
        value = self._camel(dict(row))
        stable_key = value.pop("stableKey")
        for key in ("id", "runId", "sourceHtml", "sourceOrder"):
            value.pop(key, None)
        key = self._media_key(connection, run_id, stable_key)
        value["mediaUrl"] = None if key is None else f"/api/media/assets/{key}"
        value["route"] = f"/site/colecoes/{'flamulas' if value['section']=='pennants' else 'bandeiras' if value['section']=='flags' else 'memorabilia'}/{value['slug']}"
        return value

    def summary(self) -> dict | None:
        run = self.latest_run()
        if run is None:
            return None
        with self.database.connect() as connection:
            sections = connection.execute(
                "SELECT section,title,description,items_count,ready,review_required,unavailable FROM historical_collection_sections WHERE run_id=? ORDER BY display_order",
                (run["id"],),
            ).fetchall()
        return {
            "schemaVersion": run["schema_version"], "status": run["status"],
            "totalItems": run["total_items"], "ready": run["ready"],
            "reviewRequired": run["review_required"], "unavailable": run["unavailable"],
            "completedAt": run["completed_at"],
            "sections": [self._camel(dict(row)) for row in sections],
        }

    def sections(self) -> list[dict]:
        summary = self.summary()
        return [] if summary is None else summary["sections"]

    def section(self, section: str) -> dict | None:
        run = self.latest_run()
        if run is None:
            return None
        with self.database.connect() as connection:
            row = connection.execute(
                "SELECT section,title,description,items_count,ready,review_required,unavailable FROM historical_collection_sections WHERE run_id=? AND section=?",
                (run["id"], section),
            ).fetchone()
            if row is None:
                return None
            groups = connection.execute(
                "SELECT group_key,count(*) count FROM historical_collection_items WHERE run_id=? AND section=? AND group_key IS NOT NULL GROUP BY group_key ORDER BY min(source_order)",
                (run["id"], section),
            ).fetchall()
        value = self._camel(dict(row))
        value["groups"] = [self._camel(dict(group)) for group in groups]
        return value

    def items(self, section: str, limit: int, offset: int, group: str | None = None, category: str | None = None) -> dict:
        run = self.latest_run()
        run_id = -1 if run is None else run["id"]
        conditions = ["run_id=?", "section=?"]
        params: list = [run_id, section]
        for column, value in (("group_key", group), ("category", category)):
            if value:
                conditions.append(f"{column}=?")
                params.append(value)
        where = " AND ".join(conditions)
        with self.database.connect() as connection:
            total = connection.execute(f"SELECT count(*) FROM historical_collection_items WHERE {where}", params).fetchone()[0]
            rows = connection.execute(
                f"SELECT * FROM historical_collection_items WHERE {where} ORDER BY source_order,id LIMIT ? OFFSET ?",
                [*params, limit, offset],
            ).fetchall()
            values = [self._public_item(connection, run_id, row) for row in rows]
        return {"items": values, "total": total, "limit": limit, "offset": offset, "hasNext": offset + limit < total}

    def item(self, section: str, slug: str) -> dict | None:
        run = self.latest_run()
        if run is None:
            return None
        with self.database.connect() as connection:
            row = connection.execute(
                "SELECT * FROM historical_collection_items WHERE run_id=? AND section=? AND slug=?",
                (run["id"], section, slug),
            ).fetchone()
            return None if row is None else self._public_item(connection, run["id"], row)
