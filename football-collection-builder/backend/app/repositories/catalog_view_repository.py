from __future__ import annotations
import json
from pathlib import Path
from app.database.database import DEFAULT_DATABASE_PATH,Database
from app.database.schema import SCHEMA_SQL

TABLES={'countries':'catalog_view_countries','teams':'catalog_view_teams','collections':'catalog_view_collections','items':'catalog_view_items'}
class CatalogViewRepository:
 def __init__(self,database_path:str|Path=DEFAULT_DATABASE_PATH):self.database=Database(database_path)
 def create_schema(self):
  with self.database.connect() as c:
   c.executescript(SCHEMA_SQL)
   if 'inventory_reference' not in {x['name'] for x in c.execute('pragma table_info(catalog_view_media)')}:c.execute('alter table catalog_view_media add column inventory_reference TEXT')
   columns={x['name'] for x in c.execute('pragma table_info(catalog_view_items)')}
   for name,kind in [('season_label','TEXT'),('season_start_year','INTEGER'),('season_end_year','INTEGER'),('description','TEXT'),('competition','TEXT')]:
    if name not in columns:c.execute(f'alter table catalog_view_items add column {name} {kind}')
   team_columns={x['name'] for x in c.execute('pragma table_info(catalog_view_teams)')}
   if 'logo_media_key' not in team_columns:c.execute('alter table catalog_view_teams add column logo_media_key TEXT')
   country_columns={x['name'] for x in c.execute('pragma table_info(catalog_view_countries)')}
   if 'logo_media_key' not in country_columns:c.execute('alter table catalog_view_countries add column logo_media_key TEXT')
 @staticmethod
 def camel(row):
  out={}
  for k,v in dict(row).items():
   p=k.split('_');out[p[0]+''.join(x.title() for x in p[1:])]=v
  return out
 def latest_normalization(self):
  self.create_schema()
  with self.database.connect() as c:r=c.execute("select * from catalog_normalization_runs where status='completed' order by id desc limit 1").fetchone()
  return None if r is None else dict(r)
 def latest_run(self):
  self.create_schema()
  with self.database.connect() as c:r=c.execute("select * from catalog_view_runs where status='completed' order by id desc limit 1").fetchone()
  if not r:return None
  value=self.camel(r);value.pop('id',None);value.pop('normalizationRunId',None);value.pop('errorMessage',None);return value
 def latest_run_id(self):
  with self.database.connect() as c:r=c.execute("select id from catalog_view_runs where status='completed' order by id desc limit 1").fetchone()
  return None if r is None else r['id']
 def load_source(self,normalization_run_id):
  with self.database.connect() as c:
   build=c.execute('select catalog_build_id from catalog_normalization_runs where id=?',(normalization_run_id,)).fetchone()['catalog_build_id']
   result={k:[dict(x) for x in c.execute(f'select * from {t} where normalization_run_id=? order by id',(normalization_run_id,))] for k,t in {'countries':'catalog_normalized_countries','teams':'catalog_normalized_teams','collections':'catalog_normalized_collections'}.items()}
   result['items']=[dict(x) for x in c.execute('''select n.*,i.item_type source_item_type,i.editorial_description source_editorial_description,i.editorial_status source_editorial_status,i.editorial_anchor source_editorial_anchor from catalog_normalized_items n join catalog_items i on i.id=n.source_entity_id and i.build_run_id=? where n.normalization_run_id=? order by n.id''',(build,normalization_run_id))]
   result['media']=[dict(x) for x in c.execute('''select r.catalog_item_id source_item_id,r.image_metadata_id,r.display_order,r.alt_text,r.is_primary_candidate,m.inventory_item_id,m.filename,m.extension,m.width,m.height,m.aspect_ratio,m.format,m.valid_image,m.readable from catalog_item_images r join image_metadata m on m.id=r.image_metadata_id where r.build_run_id=? order by r.catalog_item_id,coalesce(r.display_order,2147483647),r.id''',(build,))]
   result['editorial']=[dict(x) for x in c.execute('''select p.relative_path source_page,r.referenced_inventory_item_id inventory_item_id,x.context_text,x.status from html_image_contexts x join html_pages p on p.id=x.html_page_id join html_image_references r on r.id=x.image_reference_id where p.run_id=(select id from html_parse_runs where status in ('completed','completed_with_errors') order by id desc limit 1)''')]
   result['branding']=[dict(x) for x in c.execute('''select b.team_stable_key,b.status,m.inventory_item_id,m.filename,m.extension,m.width,m.height,m.aspect_ratio,m.format,m.valid_image,m.readable from team_branding b join team_branding_runs r on r.id=b.branding_run_id left join image_metadata m on m.inventory_item_id=b.inventory_reference where r.status='completed' and r.id=(select id from team_branding_runs where status='completed' order by id desc limit 1)''')]
   result['country_branding']=[dict(x) for x in c.execute('''select b.country_stable_key,b.status,m.inventory_item_id,m.filename,m.extension,m.width,m.height,m.aspect_ratio,m.format,m.valid_image,m.readable from country_branding b join country_branding_runs r on r.id=b.branding_run_id left join image_metadata m on m.inventory_item_id=b.inventory_reference where r.status='completed' and r.id=(select id from country_branding_runs where status='completed' order by id desc limit 1)''')]
  return result
 def persist(self,run,entities,media):
  c=self.database.connect()
  try:
   c.execute('BEGIN');cols=','.join(run);marks=','.join('?' for _ in run);rid=int(c.execute(f'insert into catalog_view_runs({cols}) values({marks})',tuple(run.values())).lastrowid)
   media_inventory={x['public_media_key']:x.get('inventory_reference') for x in media}
   for kind,rows in entities.items():
    for row in rows:
     if kind=='items':
      from app.services.catalog_editorial_rules import season_from
      season=season_from(row.get('original_title'),row.get('source_page_reference'));context=None;inventory=media_inventory.get(row.get('primary_media_key'))
      if inventory:
       context=c.execute('''select x.context_text from html_image_contexts x join html_pages p on p.id=x.html_page_id join html_image_references r on r.id=x.image_reference_id where lower(replace(p.relative_path,'\\','/'))=lower(?) and r.referenced_inventory_item_id=? and x.status='matched' order by x.id desc limit 1''',(row.get('source_page_reference'),inventory)).fetchone()
      row={**row,'season_label':season['label'] if season else None,'season_start_year':season['start'] if season else None,'season_end_year':season['end'] if season else None,'description':row.get('description') or (context['context_text'] if context else None),'competition':None}
     data={'view_run_id':rid,**row};cs=','.join(data);ms=','.join('?' for _ in data);c.execute(f'insert into {TABLES[kind]}({cs}) values({ms})',tuple(data.values()))
   for row in media:
    data={'view_run_id':rid,**row};cs=','.join(data);ms=','.join('?' for _ in data);c.execute(f'insert into catalog_view_media({cs}) values({ms})',tuple(data.values()))
   c.commit();return rid
  except Exception:c.rollback();raise
  finally:c.close()
 def _media(self,c,run_id,key):
  if not key:return None
  r=c.execute('select * from catalog_view_media where view_run_id=? and public_media_key=? limit 1',(run_id,key)).fetchone()
  if r is None:return None
  enrichment=self._media_enrichments(c,run_id,[key]).get(key)
  return self._public_media(r,enrichment)
 def _media_enrichments(self,c,run_id,keys):
  if not keys:return {}
  marks=','.join('?' for _ in keys)
  rows=c.execute(f'''select r.view_public_media_key,a.media_key,a.available,a.valid,a.format from media_build_runs b join media_asset_relations r on r.media_run_id=b.id join media_assets a on a.media_run_id=b.id and a.media_key=r.media_key where b.id=(select id from media_build_runs where status='completed' and catalog_view_run_id=? order by id desc limit 1) and r.view_public_media_key in ({marks})''',[run_id,*keys]).fetchall()
  return {x['view_public_media_key']:dict(x) for x in rows}
 def _public_media(self,row,enrichment=None):
  x=self.camel(row)
  for k in ('id','viewRunId','itemPublicRoute','inventoryReference'):x.pop(k,None)
  x['mediaKey']=None if enrichment is None else enrichment['media_key'];x['mediaUrl']=None if enrichment is None or not enrichment['available'] or not enrichment['valid'] or enrichment['format']=='SVG' else f"/api/media/assets/{enrichment['media_key']}"
  x['isPrimaryCandidate']=bool(x.get('isPrimaryCandidate'));return x
 def _public(self,c,run_id,row,media_map=None):
  x=self.camel(row);key=x.pop('primaryMediaKey',None);logo_key=x.pop('logoMediaKey',None)
  for k in ('id','viewRunId'):x.pop(k,None)
  x['primaryMedia']=media_map.get(key) if media_map is not None and key else self._media(c,run_id,key)
  if 'logo_media_key' in row.keys():x['logoMedia']=media_map.get(logo_key) if media_map is not None and logo_key else self._media(c,run_id,logo_key)
  if 'breadcrumbsJson' in x:x['breadcrumbs']=json.loads(x.pop('breadcrumbsJson'))
  return x
 def _public_many(self,c,run_id,rows):
  keys=[r[k] for r in rows for k in ('primary_media_key','logo_media_key') if k in r.keys() and r[k]]
  media_map={}
  if keys:
   marks=','.join('?' for _ in keys)
   enrichments=self._media_enrichments(c,run_id,keys)
   for m in c.execute(f'select * from catalog_view_media where view_run_id=? and public_media_key in ({marks})',[run_id,*keys]).fetchall():media_map[m['public_media_key']]=self._public_media(m,enrichments.get(m['public_media_key']))
  return [self._public(c,run_id,r,media_map) for r in rows]
 def summary(self):
  run=self.latest_run()
  if not run:return None
  return {'countries':run['countries'],'teams':run['teams'],'collections':run['collections'],'items':run['items'],'mediaRelations':run['mediaRelations'],'ready':run['ready'],'reviewRequired':run['reviewRequired'],'unavailable':run['unavailable'],'durationMs':run['durationMs'],'lastBuildAt':run['completedAt'],'schemaVersion':run['schemaVersion']}
 def page(self,kind,limit,offset,filters):
  rid=self.latest_run_id();table=TABLES[kind];cond=['view_run_id=?'];params=[rid or -1]
  mapping={'status':'public_status','country':'country_slug','team':'team_slug','collection':'collection_slug','year':'inclusion_year','month':'inclusion_month','type':'collection_type','itemType':'item_type'}
  for k,col in mapping.items():
   if filters.get(k) not in (None,''):cond.append(col+'=?');params.append(filters[k])
  if filters.get('search'):
   fields=('name','original_name') if kind!='items' else ('title','original_title');cond.append(f'({fields[0]} like ? or {fields[1]} like ?)');params += [f"%{filters['search']}%"]*2
  where=' and '.join(cond);order='inclusion_year desc,inclusion_month desc,coalesce(inclusion_batch,0) desc,id' if kind=='collections' else 'name,id' if kind!='items' else 'title,id'
  with self.database.connect() as c:total=c.execute(f'select count(*) from {table} where {where}',params).fetchone()[0];rows=c.execute(f'select * from {table} where {where} order by {order} limit ? offset ?',[*params,limit,offset]).fetchall();items=self._public_many(c,rid,rows)
  return {'items':items,'total':total,'limit':limit,'offset':offset,'hasNext':offset+limit<total}
 def country_detail(self,slug):
  rid=self.latest_run_id()
  with self.database.connect() as c:r=c.execute('select * from catalog_view_countries where view_run_id=? and slug=?',(rid or -1,slug)).fetchone()
  if not r:return None
  return {'country':self._public(c,rid,r),'summary':{'teams':r['teams_count'],'collections':r['collections_count'],'items':r['items_count']},'teams':self.page('teams',12,0,{'country':slug})['items'],'navigation':{'countrySlug':slug}}
 def team_detail(self,country,team):
  rid=self.latest_run_id()
  with self.database.connect() as c:r=c.execute('select * from catalog_view_teams where view_run_id=? and country_slug=? and slug=?',(rid or -1,country,team)).fetchone();cr=c.execute('select * from catalog_view_countries where view_run_id=? and slug=?',(rid or -1,country)).fetchone()
  if not r or not cr:return None
  return {'team':self._public(c,rid,r),'country':self._public(c,rid,cr),'latestCollections':self.page('collections',12,0,{'country':country,'team':team})['items'],'itemsSummary':{'total':r['items_count']}}
 def collection_detail(self,country,team,collection):
  rid=self.latest_run_id()
  with self.database.connect() as c:r=c.execute('select * from catalog_view_collections where view_run_id=? and country_slug=? and team_slug=? and slug=?',(rid or -1,country,team,collection)).fetchone()
  if not r:return None
  return {'collection':self._public(c,rid,r),'items':self.page('items',24,0,{'country':country,'team':team,'collection':collection})}
 def item_detail(self,country,team,item,collection=None):
  rid=self.latest_run_id();cond='collection_slug=?' if collection else 'collection_slug is null';params=[rid or -1,country,team,*([collection] if collection else []),item]
  with self.database.connect() as c:r=c.execute(f'select * from catalog_view_items where view_run_id=? and country_slug=? and team_slug=? and {cond} and slug=?',params).fetchone()
  if not r:return None
  value=self._public(c,rid,r);rows=c.execute('select * from catalog_view_media where view_run_id=? and item_public_route=? order by coalesce(display_order,2147483647),id',(rid,r['public_route'])).fetchall();enrichments=self._media_enrichments(c,rid,[x['public_media_key'] for x in rows]);value['media']=[self._public_media(x,enrichments.get(x['public_media_key'])) for x in rows];return value
 def season_detail(self,country,team,season):
  rid=self.latest_run_id()
  with self.database.connect() as c:
   tr=c.execute('select * from catalog_view_teams where view_run_id=? and country_slug=? and slug=?',(rid or -1,country,team)).fetchone();cr=c.execute('select * from catalog_view_countries where view_run_id=? and slug=?',(rid or -1,country)).fetchone()
   if not tr or not cr:return None
   rows=c.execute('select * from catalog_view_items where view_run_id=? and country_slug=? and team_slug=? and season_label=? order by id',(rid,country,team,season)).fetchall()
   if not rows:return None
   items=[]
   for row in rows:
    value=self._public(c,rid,row);value.pop('sourcePageReference',None);media=c.execute('select * from catalog_view_media where view_run_id=? and item_public_route=? order by coalesce(display_order,2147483647),id',(rid,row['public_route'])).fetchall();enrichments=self._media_enrichments(c,rid,[x['public_media_key'] for x in media]);value['media']=[self._public_media(x,enrichments.get(x['public_media_key'])) for x in media];items.append(value)
  return {'country':self._public(c,rid,cr),'team':self._public(c,rid,tr),'season':season,'records':items,'summary':{'records':len(items),'images':sum(x['imagesCount'] for x in items)}}
 def navigation(self):
  p=self.page('countries',100,0,{})
  return {'countries':[{'slug':x['slug'],'name':x['name'],'teamsCount':x['teamsCount'],'status':x['publicStatus']} for x in p['items']]}
 def search(self,q,kind,country,limit,offset):
  if not q.strip():return {'items':[],'total':0,'limit':limit,'offset':offset,'hasNext':False}
  rid=self.latest_run_id();types=[kind] if kind in TABLES else list(TABLES);all_rows=[]
  with self.database.connect() as c:
   for k in types:
    table=TABLES[k];title='title' if k=='items' else 'name';cond=['view_run_id=?',f'({title} like ? or '+('original_title' if k=='items' else 'original_name')+' like ?)'];params=[rid or -1,f'%{q}%',f'%{q}%']
    if country and k!='countries':cond.append('country_slug=?');params.append(country)
    rows=c.execute(f"select *,case when lower({title})=lower(?) then 0 when lower({title}) like lower(?) then 1 else 2 end rank from {table} where {' and '.join(cond)} order by rank,{title}",[q,q+'%',*params]).fetchall()
    for r,x in zip(rows,self._public_many(c,rid,rows)):
     all_rows.append({'type':{'countries':'country','teams':'team','collections':'collection','items':'item'}[k],'title':x.get('title',x.get('name')),'subtitle':x.get('originalTitle',x.get('originalName')),'countrySlug':x.get('countrySlug',x.get('slug') if k=='countries' else None),'teamSlug':x.get('teamSlug',x.get('slug') if k=='teams' else None),'collectionSlug':x.get('collectionSlug',x.get('slug') if k=='collections' else None),'itemSlug':x.get('slug') if k=='items' else None,'publicRoute':x.get('publicRoute'),'primaryMedia':x.get('primaryMedia'),'status':x['publicStatus'],'rank':r['rank']})
  all_rows.sort(key=lambda x:(x.pop('rank'),x['title'].casefold()));total=len(all_rows);items=all_rows[offset:offset+limit];return {'items':items,'total':total,'limit':limit,'offset':offset,'hasNext':offset+limit<total}
 def latest(self,limit,country=None,team=None):
  rid=self.latest_run_id();conditions=['i.view_run_id=?'];params=[rid or -1]
  if country:conditions.append('i.country_slug=?');params.append(country)
  if team:conditions.append('i.team_slug=?');params.append(team)
  with self.database.connect() as c:
   rows=c.execute(f'''select i.* from catalog_view_items i left join catalog_view_collections co on co.view_run_id=i.view_run_id and co.country_slug=i.country_slug and co.team_slug=i.team_slug and co.slug=i.collection_slug where {' and '.join(conditions)} order by co.inclusion_year desc,co.inclusion_month desc,co.inclusion_batch desc,i.id limit ?''',[*params,limit]).fetchall()
   return self._public_many(c,rid,rows)
