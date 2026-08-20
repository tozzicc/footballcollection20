from pathlib import Path
from app.database.database import DEFAULT_DATABASE_PATH, Database
from app.database.schema import IMAGE_PARSER_TABLES, SCHEMA_SQL
from app.models.image_parser import *

class ImageParserRepository:
    def __init__(self, database_path: str | Path = DEFAULT_DATABASE_PATH): self.database = Database(database_path)
    def create_schema(self):
        with self.database.connect() as c: c.executescript(SCHEMA_SQL)
    def html_available(self) -> bool:
        self.create_schema()
        with self.database.connect() as c: return c.execute("SELECT 1 FROM html_parse_runs WHERE status IN ('completed','completed_with_errors') LIMIT 1").fetchone() is not None
    def reference_counts(self) -> dict[str, int]:
        self.create_schema()
        with self.database.connect() as c:
            rows=c.execute("SELECT resolved_relative_path path,count(*) n FROM html_image_references WHERE exists_in_inventory=1 AND resolved_relative_path IS NOT NULL GROUP BY resolved_relative_path").fetchall()
        return {r['path'].replace('\\','/').casefold(): r['n'] for r in rows}
    def broken_count(self) -> int:
        with self.database.connect() as c: return c.execute("SELECT count(*) n FROM html_image_references WHERE status='missing'").fetchone()['n']
    def save_run(self, run: ImageParseRun, images: list[ImageMetadata], errors: list[ImageParseError], replace_previous=True) -> int:
        self.create_schema(); c=self.database.connect()
        try:
            c.execute('PRAGMA foreign_keys=ON'); c.execute('BEGIN')
            if replace_previous:
                dependent=c.execute('SELECT count(*) n FROM catalog_item_images').fetchone()['n']
                if dependent:
                    raise ValueError(
                        f'Image Parser replacement blocked: {dependent} Catalog image relations depend on '
                        'the current image metadata. Rebuild/coordinate the Catalog after the parser run.'
                    )
                for table in reversed(IMAGE_PARSER_TABLES): c.execute(f'DELETE FROM {table}')
            cur=c.execute("""INSERT INTO image_parse_runs(workspace_path,started_at,finished_at,duration_ms,status,total_images,valid_images,invalid_images,referenced_images,orphan_images,broken_references,html_audit_available,total_size,average_width,average_height,max_width,max_height,message) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (run.workspacePath,run.startedAt,run.finishedAt,run.durationMs,run.status,run.totalImages,run.validImages,run.invalidImages,run.referencedImages,run.orphanImages,run.brokenReferences,int(run.htmlAuditAvailable),run.totalSize,run.averageWidth,run.averageHeight,run.maxWidth,run.maxHeight,run.message))
            rid=int(cur.lastrowid)
            c.executemany("""INSERT INTO image_metadata(run_id,inventory_item_id,relative_path,absolute_path,filename,extension,format,file_size,width,height,aspect_ratio,mode,has_alpha,animated,frame_count,dpi_x,dpi_y,created_at,modified_at,readable,valid_image,validation_status,validation_message,reference_count,reference_status) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                [(rid,x.inventoryItemId,x.relativePath,x.absolutePath,x.filename,x.extension,x.format,x.fileSize,x.width,x.height,x.aspectRatio,x.mode,int(x.hasAlpha),int(x.animated),x.frameCount,x.dpiX,x.dpiY,x.createdAt,x.modifiedAt,int(x.readable),int(x.validImage),x.validationStatus,x.validationMessage,x.referenceCount,x.referenceStatus.value) for x in images])
            c.executemany('INSERT INTO image_parse_errors(run_id,inventory_item_id,relative_path,error_type,message) VALUES(?,?,?,?,?)',[(rid,e.inventoryItemId,e.relativePath,e.errorType,e.message) for e in errors])
            c.commit(); return rid
        except Exception: c.rollback(); raise
        finally: c.close()
    def _run(self,r):
        formats=self.formats(r['id'])
        return ImageParseSummary(id=r['id'],workspacePath=r['workspace_path'],startedAt=r['started_at'],finishedAt=r['finished_at'],durationMs=r['duration_ms'],status=r['status'],totalImages=r['total_images'],validImages=r['valid_images'],invalidImages=r['invalid_images'],referencedImages=r['referenced_images'],orphanImages=r['orphan_images'],brokenReferences=r['broken_references'],htmlAuditAvailable=bool(r['html_audit_available']),totalSize=r['total_size'],averageWidth=r['average_width'],averageHeight=r['average_height'],maxWidth=r['max_width'],maxHeight=r['max_height'],formats=formats,message=r['message'])
    def latest(self):
        self.create_schema()
        with self.database.connect() as c: r=c.execute('SELECT * FROM image_parse_runs ORDER BY id DESC LIMIT 1').fetchone()
        return None if r is None else self._run(r)
    def formats(self,run_id):
        with self.database.connect() as c: rows=c.execute('SELECT coalesce(format,\'UNKNOWN\') format,count(*) n FROM image_metadata WHERE run_id=? GROUP BY format ORDER BY n DESC',(run_id,)).fetchall()
        return {r['format']:r['n'] for r in rows}
    @staticmethod
    def _image(r):
        return ImageMetadata(id=r['id'],inventoryItemId=r['inventory_item_id'],relativePath=r['relative_path'],absolutePath=r['absolute_path'],filename=r['filename'],extension=r['extension'],format=r['format'],fileSize=r['file_size'],width=r['width'],height=r['height'],aspectRatio=r['aspect_ratio'],mode=r['mode'],hasAlpha=bool(r['has_alpha']),animated=bool(r['animated']),frameCount=r['frame_count'],dpiX=r['dpi_x'],dpiY=r['dpi_y'],createdAt=r['created_at'],modifiedAt=r['modified_at'],readable=bool(r['readable']),validImage=bool(r['valid_image']),validationStatus=r['validation_status'],validationMessage=r['validation_message'],referenceCount=r['reference_count'],referenceStatus=r['reference_status'])
    def images(self,limit,offset,search=None,status=None,format=None,min_width=None,min_height=None,kind=None):
        run=self.latest(); conditions=['run_id=?']; params=[run.id if run else -1]
        if search: conditions.append('(relative_path LIKE ? OR filename LIKE ?)'); params += [f'%{search}%',f'%{search}%']
        if status: conditions.append('validation_status=?'); params.append(status)
        if format: conditions.append('format=?'); params.append(format.upper())
        if min_width is not None: conditions.append('width>=?'); params.append(min_width)
        if min_height is not None: conditions.append('height>=?'); params.append(min_height)
        if kind=='orphan': conditions.append("reference_status='orphan'")
        if kind=='invalid': conditions.append('valid_image=0')
        where=' AND '.join(conditions)
        with self.database.connect() as c:
            total=c.execute(f'SELECT count(*) n FROM image_metadata WHERE {where}',params).fetchone()['n']
            rows=c.execute(f'SELECT * FROM image_metadata WHERE {where} ORDER BY relative_path LIMIT ? OFFSET ?',[*params,limit,offset]).fetchall()
        return PaginatedImages(items=[self._image(r) for r in rows],total=total,limit=limit,offset=offset)
    def detail(self,image_id):
        with self.database.connect() as c: r=c.execute('SELECT * FROM image_metadata WHERE id=?',(image_id,)).fetchone()
        return None if r is None else self._image(r)
    def broken(self,limit,offset):
        with self.database.connect() as c:
            total=c.execute("SELECT count(*) n FROM html_image_references WHERE status='missing'").fetchone()['n']
            rows=c.execute("""SELECT i.id,p.id page_id,p.relative_path,i.src_original,i.resolved_relative_path,i.status FROM html_image_references i JOIN html_pages p ON p.id=i.page_id WHERE i.status='missing' ORDER BY p.relative_path,i.id LIMIT ? OFFSET ?""",(limit,offset)).fetchall()
        return PaginatedBrokenReferences(items=[BrokenImageReference(id=r['id'],pageId=r['page_id'],pageRelativePath=r['relative_path'],referenceOriginal=r['src_original'],resolvedRelativePath=r['resolved_relative_path'],status=r['status']) for r in rows],total=total,limit=limit,offset=offset)
