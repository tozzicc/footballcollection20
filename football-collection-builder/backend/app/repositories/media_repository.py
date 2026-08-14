from __future__ import annotations
from pathlib import Path
from app.database.database import DEFAULT_DATABASE_PATH,Database
from app.database.schema import SCHEMA_SQL

class MediaRepository:
 def __init__(self,database_path:str|Path=DEFAULT_DATABASE_PATH):self.database=Database(database_path)
 def create_schema(self):
  from app.repositories.catalog_view_repository import CatalogViewRepository
  CatalogViewRepository(self.database.path).create_schema()
 def latest_view(self):
  self.create_schema()
  with self.database.connect() as c:r=c.execute("select id from catalog_view_runs where status='completed' order by id desc limit 1").fetchone()
  return None if r is None else r['id']
 def latest_run_row(self):
  self.create_schema()
  with self.database.connect() as c:r=c.execute("select * from media_build_runs where status='completed' order by id desc limit 1").fetchone()
  return None if r is None else dict(r)
 def load_source(self,view_run_id):
  with self.database.connect() as c:
   workspace=c.execute('select workspace_path from inventory_metadata where id=1').fetchone()
   rows=c.execute('''select v.public_media_key,v.inventory_reference,m.relative_path,m.extension,m.format,m.file_size,m.width,m.height,m.aspect_ratio,m.valid_image,m.readable,m.modified_at from catalog_view_media v join image_metadata m on m.inventory_item_id=v.inventory_reference where v.view_run_id=? order by v.id''',(view_run_id,)).fetchall()
  return (None if workspace is None else workspace['workspace_path'],[dict(x) for x in rows])
 def persist(self,run,assets,relations):
  c=self.database.connect()
  try:
   c.execute('BEGIN');cols=','.join(run);marks=','.join('?' for _ in run);rid=int(c.execute(f'insert into media_build_runs({cols}) values({marks})',tuple(run.values())).lastrowid)
   for row in assets:
    data={'media_run_id':rid,**row};cs=','.join(data);ms=','.join('?' for _ in data);c.execute(f'insert into media_assets({cs}) values({ms})',tuple(data.values()))
   c.executemany('insert into media_asset_relations(media_run_id,view_public_media_key,media_key) values(?,?,?)',[(rid,x['view_public_media_key'],x['media_key']) for x in relations]);c.commit();return rid
  except Exception:c.rollback();raise
  finally:c.close()
 def asset(self,media_key):
  run=self.latest_run_row()
  if not run:return None
  with self.database.connect() as c:r=c.execute('select * from media_assets where media_run_id=? and media_key=?',(run['id'],media_key)).fetchone()
  return None if r is None else dict(r)
 def workspace(self):
  with self.database.connect() as c:r=c.execute('select workspace_path from inventory_metadata where id=1').fetchone()
  return None if r is None else r['workspace_path']
 @staticmethod
 def public_asset(row):
  return {'mediaKey':row['media_key'],'filename':row['filename'],'extension':row['extension'],'format':row['format'],'mimeType':row['mime_type'],'fileSize':row['file_size'],'width':row['width'],'height':row['height'],'aspectRatio':row['aspect_ratio'],'available':bool(row['available']),'valid':bool(row['valid']),'mediaUrl':f"/api/media/assets/{row['media_key']}" if row['available'] and row['valid'] and row['format']!='SVG' else None}
 def page(self,limit,offset,search='',available=None,format=None):
  run=self.latest_run_row();cond=['media_run_id=?'];params=[run['id'] if run else -1]
  if search:cond.append('(media_key like ? or extension like ?)');params += [f'%{search}%',f'%{search}%']
  if available is not None:cond.append('available=?');params.append(int(available))
  if format:cond.append('format=?');params.append(format)
  where=' and '.join(cond)
  with self.database.connect() as c:total=c.execute(f'select count(*) from media_assets where {where}',params).fetchone()[0];rows=c.execute(f'select * from media_assets where {where} order by media_key limit ? offset ?',[*params,limit,offset]).fetchall()
  return {'items':[self.public_asset(dict(x)) for x in rows],'total':total,'limit':limit,'offset':offset,'hasNext':offset+limit<total}
 def summary(self):
  run=self.latest_run_row()
  if not run:return None
  with self.database.connect() as c:
   formats={r['format'] or 'UNKNOWN':r['n'] for r in c.execute('select format,count(*) n from media_assets where media_run_id=? group by format',(run['id'],))};size=c.execute('select coalesce(sum(file_size),0) n from media_assets where media_run_id=?',(run['id'],)).fetchone()['n'];view=run['catalog_view_run_id'];counts={}
   for name,table in [('items','catalog_view_items'),('collections','catalog_view_collections'),('countries','catalog_view_countries'),('teams','catalog_view_teams')]:
    counts[name+'WithPrimaryMedia']=c.execute(f'select count(*) from {table} where view_run_id=? and primary_media_key is not null',(view,)).fetchone()[0];counts[name+'WithoutPrimaryMedia']=c.execute(f'select count(*) from {table} where view_run_id=? and primary_media_key is null',(view,)).fetchone()[0]
  return {'uniqueAssets':run['unique_assets'],'availableAssets':run['available_assets'],'unavailableAssets':run['unavailable_assets'],'invalidAssets':run['invalid_assets'],'totalRelations':run['total_relations'],'formats':formats,'totalSize':size,**counts,'durationMs':run['duration_ms'],'builtAt':run['completed_at'],'schemaVersion':run['schema_version']}
