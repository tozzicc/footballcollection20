from pathlib import Path
from app.database.database import DEFAULT_DATABASE_PATH,Database
from app.database.schema import SCHEMA_SQL

class TeamBrandingRepository:
 def __init__(self,database_path:str|Path=DEFAULT_DATABASE_PATH):self.database=Database(database_path)
 def create_schema(self):
  with self.database.connect() as c:c.executescript(SCHEMA_SQL)
 def source(self):
  self.create_schema()
  with self.database.connect() as c:
   build=c.execute("select id from catalog_build_runs where status='completed' order by id desc limit 1").fetchone()
   if not build:return None
   teams=[dict(x) for x in c.execute("select t.id,t.original_name,t.relative_path,s.stable_key from catalog_teams t join catalog_stable_keys s on s.build_run_id=t.build_run_id and s.entity_type='team' and s.entity_id=t.id where t.build_run_id=? order by t.relative_path",(build['id'],))]
   pages=[dict(x) for x in c.execute("select id,relative_path from html_pages where run_id=(select id from html_parse_runs where status in ('completed','completed_with_errors') order by id desc limit 1)")]
   refs=[dict(x) for x in c.execute("select page_id,resolved_relative_path,referenced_inventory_item_id from html_image_references where lower(replace(coalesce(resolved_relative_path,''),'\\','/')) like 'logos/%'")]
  return build['id'],teams,pages,refs
 def persist(self,run,rows):
  c=self.database.connect()
  try:
   c.execute('begin');cols=','.join(run);marks=','.join('?' for _ in run);rid=int(c.execute(f"insert into team_branding_runs({cols}) values({marks})",tuple(run.values())).lastrowid)
   for row in rows:
    data={'branding_run_id':rid,**row};cs=','.join(data);ms=','.join('?' for _ in data);c.execute(f"insert into team_branding({cs}) values({ms})",tuple(data.values()))
   c.commit();return rid
  except Exception:c.rollback();raise
  finally:c.close()
 def latest(self):
  self.create_schema()
  with self.database.connect() as c:r=c.execute("select * from team_branding_runs where status='completed' order by id desc limit 1").fetchone()
  return None if r is None else dict(r)
