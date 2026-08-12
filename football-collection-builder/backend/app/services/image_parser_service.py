from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter
from PIL import Image, UnidentifiedImageError
from app.models.image_parser import *
from app.repositories.inventory_repository import InventoryRepository
from app.repositories.image_parser_repository import ImageParserRepository

def utc_now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')

class ImageParserService:
    def __init__(self, inventory_repository=None, repository=None):
        self.inventory=inventory_repository or InventoryRepository(); self.repository=repository or ImageParserRepository()
    def status(self):
        workspace=self.inventory.get_workspace_path(); images=self.inventory.get_images() if workspace else []
        return ImageParserStatus(hasRun=self.repository.latest() is not None,inventoryAvailable=workspace is not None,htmlParserAvailable=self.repository.html_available(),availableImages=len(images),lastRun=self.repository.latest())
    def parse(self, request: ImageParseRequest):
        workspace=self.inventory.get_workspace_path()
        if not workspace: raise ValueError('Inventory persistido nao encontrado.')
        if Path(workspace).resolve()!=Path(request.workspacePath).resolve(): raise ValueError('Workspace nao corresponde ao Inventory persistido.')
        if not Path(workspace).is_dir(): raise ValueError('Workspace persistido nao esta disponivel no caminho salvo.')
        started=utc_now(); timer=perf_counter(); items=self.inventory.get_images(); html=self.repository.html_available()
        refs=self.repository.reference_counts() if html else {}; images=[]; errors=[]
        for item in items:
            ref_count=refs.get(item.relativePath.replace('\\','/').casefold(),0); ref_status=ImageReferenceStatus.REFERENCED if ref_count else (ImageReferenceStatus.ORPHAN if html else ImageReferenceStatus.UNRESOLVED_CONTEXT)
            try: meta=self._inspect(item,ref_count,ref_status)
            except Exception as exc:
                meta=ImageMetadata(inventoryItemId=item.id,relativePath=item.relativePath,absolutePath=item.absolutePath,filename=item.filename,extension=item.extension,fileSize=item.size,createdAt=item.createdAt,modifiedAt=item.modifiedAt,readable=False,validImage=False,validationStatus='read_error',validationMessage=str(exc),referenceCount=ref_count,referenceStatus=ref_status)
            images.append(meta)
            if not meta.validImage: errors.append(ImageParseError(inventoryItemId=item.id,relativePath=item.relativePath,errorType=meta.validationStatus,message=meta.validationMessage))
        dims=[x for x in images if x.width is not None and x.height is not None]
        run=ImageParseRun(workspacePath=workspace,startedAt=started,finishedAt=utc_now(),durationMs=round((perf_counter()-timer)*1000),status='completed_with_errors' if errors else 'completed',totalImages=len(images),validImages=sum(x.validImage for x in images),invalidImages=sum(not x.validImage for x in images),referencedImages=sum(x.referenceStatus==ImageReferenceStatus.REFERENCED for x in images),orphanImages=sum(x.referenceStatus==ImageReferenceStatus.ORPHAN for x in images),brokenReferences=self.repository.broken_count() if html else 0,htmlAuditAvailable=html,totalSize=sum(x.fileSize for x in images),averageWidth=(sum(x.width for x in dims)/len(dims) if dims else None),averageHeight=(sum(x.height for x in dims)/len(dims) if dims else None),maxWidth=max((x.width for x in dims),default=None),maxHeight=max((x.height for x in dims),default=None),message='Parser de imagens concluido.')
        rid=self.repository.save_run(run,images,errors,request.replacePrevious)
        return ImageParserResponse(**run.model_dump(),runId=rid,errors=errors)
    def _inspect(self,item,ref_count,ref_status):
        path=Path(item.absolutePath); common=dict(inventoryItemId=item.id,relativePath=item.relativePath,absolutePath=item.absolutePath,filename=item.filename,extension=item.extension,fileSize=item.size,createdAt=item.createdAt,modifiedAt=item.modifiedAt,readable=item.readable,referenceCount=ref_count,referenceStatus=ref_status)
        if item.extension.lower()=='.svg':
            with path.open('rb') as f:
                head=f.read(4096).lstrip()
            valid=b'<svg' in head.lower()
            return ImageMetadata(**common,format='SVG',validImage=valid,validationStatus='valid' if valid else 'invalid_content',validationMessage='SVG valido.' if valid else 'Conteudo SVG nao identificado.')
        try:
            with Image.open(path) as image:
                width,height=image.size; fmt=image.format; mode=image.mode; frames=getattr(image,'n_frames',1); dpi=image.info.get('dpi',(None,None)); image.verify()
            expected={'.jpg':'JPEG','.jpeg':'JPEG','.tif':'TIFF','.tiff':'TIFF'}.get(item.extension.lower(),item.extension[1:].upper())
            mismatch=bool(fmt and fmt.upper()!=expected); status='format_mismatch' if mismatch else 'valid'; message=f'Formato interno {fmt} difere da extensao {item.extension}.' if mismatch else 'Imagem valida.'
            return ImageMetadata(**common,format=fmt,width=width,height=height,aspectRatio=width/height if height else None,mode=mode,hasAlpha=mode in ('RGBA','LA','PA') or 'transparency' in getattr(image,'info',{}),animated=frames>1,frameCount=frames,dpiX=float(dpi[0]) if dpi and dpi[0] else None,dpiY=float(dpi[1]) if dpi and len(dpi)>1 and dpi[1] else None,validImage=True,validationStatus=status,validationMessage=message)
        except (UnidentifiedImageError,OSError,ValueError) as exc:
            return ImageMetadata(**common,validImage=False,validationStatus='invalid_image',validationMessage=str(exc))
