from __future__ import annotations
import hashlib,time,unicodedata
from datetime import datetime,timezone
from pathlib import Path,PurePosixPath
from app.repositories.media_repository import MediaRepository

MEDIA_SCHEMA_VERSION='1.0.0'
MIME_BY_FORMAT={'JPEG':'image/jpeg','PNG':'image/png','GIF':'image/gif','BMP':'image/bmp','WEBP':'image/webp','TIFF':'image/tiff','SVG':'image/svg+xml'}
def now():return datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
def normalize_relative_path(value):return unicodedata.normalize('NFC','/'.join(PurePosixPath(value.replace('\\','/')).parts)).casefold()
def media_key(value):return hashlib.sha256(normalize_relative_path(value).encode('utf-8')).hexdigest()
class MediaService:
 def __init__(self,repository=None):self.repository=repository or MediaRepository()
 def status(self):
  view=self.repository.latest_view();run=self.repository.latest_run_row()
  return {'viewModelAvailable':view is not None,'mediaLayerAvailable':run is not None,'lastBuild':None if run is None else {'completedAt':run['completed_at'],'durationMs':run['duration_ms'],'status':run['status']},'schemaVersion':MEDIA_SCHEMA_VERSION,'uniqueAssets':0 if run is None else run['unique_assets'],'availableAssets':0 if run is None else run['available_assets'],'unavailableAssets':0 if run is None else run['unavailable_assets'],'invalidAssets':0 if run is None else run['invalid_assets']}
 def build(self):
  view=self.repository.latest_view()
  if not view:raise ValueError('View Model concluído necessário.')
  workspace,rows=self.repository.load_source(view)
  if not workspace:raise ValueError('Workspace persistido necessário para resolver mídias.')
  started=now();clock=time.perf_counter();assets={};relation_map={}
  for row in rows:
   key=media_key(row['relative_path']);existing=relation_map.get(row['public_media_key'])
   if existing and existing['media_key']!=key:raise ValueError('Colisão inconsistente de referência lógica de mídia.')
   relation_map[row['public_media_key']]={'view_public_media_key':row['public_media_key'],'media_key':key}
   if key in assets:continue
   relative_text=row['relative_path'].replace('\\','/');relative=PurePosixPath(relative_text);safe=not relative.is_absolute() and '..' not in relative.parts and ':' not in relative_text and not relative_text.startswith('//')
   available=safe and bool(row['readable']);valid=bool(row['valid_image']);fmt=(row['format'] or '').upper();mime=MIME_BY_FORMAT.get(fmt,'application/octet-stream');stamp=now();assets[key]={'media_key':key,'inventory_reference':row['inventory_reference'],'relative_path':relative_text,'filename':Path(row['relative_path']).name,'extension':row['extension'].lower(),'format':fmt or None,'mime_type':mime,'file_size':row['file_size'],'width':row['width'],'height':row['height'],'aspect_ratio':row['aspect_ratio'],'valid':int(valid),'available':int(available),'modified_at':row['modified_at'],'created_at':stamp,'updated_at':stamp}
  values=list(assets.values());relations=list(relation_map.values());duration=int((time.perf_counter()-clock)*1000);run={'catalog_view_run_id':view,'started_at':started,'completed_at':now(),'status':'completed','total_relations':len(rows),'unique_assets':len(values),'available_assets':sum(x['available'] for x in values),'unavailable_assets':sum(not x['available'] for x in values),'invalid_assets':sum(not x['valid'] for x in values),'duration_ms':duration,'schema_version':MEDIA_SCHEMA_VERSION,'error_message':None};rid=self.repository.persist(run,values,relations);return {'mediaBuild':rid,**run}
