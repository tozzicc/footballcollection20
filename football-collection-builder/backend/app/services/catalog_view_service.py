from __future__ import annotations
import hashlib,json,time
from datetime import datetime,timezone
from app.repositories.catalog_view_repository import CatalogViewRepository
from app.services.catalog_public_routes import item_breadcrumbs,public_item_route

VIEW_SCHEMA_VERSION='1.4.0'
def now():return datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
def public_status(row,required):
 if any(not row.get(x) for x in required):return 'unavailable'
 return 'review_required' if row.get('normalization_status')=='review_required' else 'ready'
def media_key(value):return 'media-'+hashlib.sha256(value.encode('utf-8')).hexdigest()[:16]

class CatalogViewService:
 def __init__(self,repository=None):self.repository=repository or CatalogViewRepository()
 def status(self):
  normalization=self.repository.latest_normalization();view=self.repository.latest_run()
  return {'normalizationAvailable':normalization is not None,'viewAvailable':view is not None,'lastRun':view,'schemaVersion':VIEW_SCHEMA_VERSION,'status':'available' if view else 'prerequisite_required' if not normalization else 'not_built'}
 def build(self):
  normalization=self.repository.latest_normalization()
  if not normalization:raise ValueError('Normalização concluída necessária.')
  started=now();clock=time.perf_counter();src=self.repository.load_source(normalization['id'])
  countries={x['stable_key']:x for x in src['countries']};teams={x['stable_key']:x for x in src['teams']};collections={x['stable_key']:x for x in src['collections']};items=src['items']
  team_items={k:[] for k in teams};collection_items={k:[] for k in collections};country_items={k:[] for k in countries}
  for x in items:
   team_items.setdefault(x['team_stable_key'],[]).append(x);country_items.setdefault(x.get('country_stable_key'),[]).append(x)
   if x.get('collection_stable_key'):collection_items.setdefault(x['collection_stable_key'],[]).append(x)
  media_by_item={}
  for m in src['media']:media_by_item.setdefault(m['source_item_id'],[]).append(m)
  route_by_item={};breadcrumbs_by_item={};route_set=set()
  for x in items:
   team=teams.get(x['team_stable_key']);country=countries.get(x.get('country_stable_key'));collection=collections.get(x.get('collection_stable_key'))
   if not team or not country:route=''
   else:route=public_item_route(country['slug'],team['slug'],x['slug'],collection['slug'] if collection else None)
   if route and route in route_set:raise ValueError(f'Colisão de rota pública detectada: {route}')
   if route:route_set.add(route)
   route_by_item[x['id']]=route;breadcrumbs_by_item[x['id']]=item_breadcrumbs(country['slug'],country['display_name'],team['slug'],team['display_name'],x['slug'],x['display_title'],collection['slug'] if collection else None,collection['display_name'] if collection else None) if route else []
  media_rows=[];public_media_by_item={}
  for x in items:
   occurrences={};logical=[]
   for m in media_by_item.get(x['source_entity_id'],[]):
    occurrences[m['inventory_item_id']]=occurrences.get(m['inventory_item_id'],0)+1
    key=media_key(f"{m['inventory_item_id']}|{occurrences[m['inventory_item_id']]}")
    row={'item_public_route':route_by_item[x['id']],'public_media_key':key,'inventory_reference':m['inventory_item_id'],'filename':m['filename'],'extension':m['extension'],'width':m['width'],'height':m['height'],'aspect_ratio':m['aspect_ratio'],'format':m['format'],'alt_text':m['alt_text'],'display_order':m['display_order'],'is_primary_candidate':int(bool(m['is_primary_candidate'])),'media_source':'catalog_relation','availability_status':'available' if m['valid_image'] and m['readable'] else 'unavailable'};logical.append(row);media_rows.append(row)
   logical.sort(key=lambda m:(not bool(m['is_primary_candidate']),m['display_order'] is None,m['display_order'] or 0,m['public_media_key']));public_media_by_item[x['id']]=logical
  branding_by_team={}
  for brand in src.get('branding',[]):
   if brand['status']!='matched' or not brand.get('inventory_item_id'):continue
   key=media_key(f"team-logo|{brand['inventory_item_id']}");branding_by_team[brand['team_stable_key']]=key
   media_rows.append({'item_public_route':f"/branding/teams/{key}",'public_media_key':key,'inventory_reference':brand['inventory_item_id'],'filename':brand['filename'],'extension':brand['extension'],'width':brand['width'],'height':brand['height'],'aspect_ratio':brand['aspect_ratio'],'format':brand['format'],'alt_text':None,'display_order':0,'is_primary_candidate':1,'media_source':'team_branding','availability_status':'available' if brand['valid_image'] and brand['readable'] else 'unavailable'})
  branding_by_country={}
  for brand in src.get('country_branding',[]):
   if brand['status']!='matched' or not brand.get('inventory_item_id'):continue
   key=media_key(f"country-logo|{brand['inventory_item_id']}");branding_by_country[brand['country_stable_key']]=key
   media_rows.append({'item_public_route':f"/branding/countries/{key}",'public_media_key':key,'inventory_reference':brand['inventory_item_id'],'filename':brand['filename'],'extension':brand['extension'],'width':brand['width'],'height':brand['height'],'aspect_ratio':brand['aspect_ratio'],'format':brand['format'],'alt_text':None,'display_order':0,'is_primary_candidate':1,'media_source':'country_branding','availability_status':'available' if brand['valid_image'] and brand['readable'] else 'unavailable'})
  def primary_for(entity_items):
   for item in sorted(entity_items,key=lambda z:z['id']):
    available=[m for m in public_media_by_item.get(item['id'],[]) if m['availability_status']=='available']
    if available:return available[0]['public_media_key']
   return None
  country_team_count={k:sum(1 for t in teams.values() if t.get('country_stable_key')==k) for k in countries};country_collection_count={k:sum(1 for co in collections.values() if co.get('country_stable_key')==k) for k in countries}
  output={'countries':[],'teams':[],'collections':[],'items':[]}
  for key,x in countries.items():output['countries'].append({'slug':x['slug'],'name':x['display_name'],'original_name':x['original_name'],'teams_count':country_team_count[key],'collections_count':country_collection_count[key],'items_count':len(country_items.get(key,[])),'primary_media_key':primary_for(country_items.get(key,[])),'logo_media_key':branding_by_country.get(key),'public_status':public_status(x,['slug','display_name'])})
  for key,x in teams.items():
   country=countries.get(x.get('country_stable_key'));own=team_items.get(key,[]);cols=[co for co in collections.values() if co['team_stable_key']==key];latest=sorted([co for co in cols if co.get('inclusion_year') is not None],key=lambda z:(z['inclusion_year'],z.get('inclusion_month') or 0,z.get('inclusion_batch') or 0),reverse=True)
   output['teams'].append({'slug':x['slug'],'country_slug':country['slug'] if country else '','name':x['display_name'],'original_name':x['original_name'],'collections_count':len(cols),'items_count':len(own),'images_count':sum(len(public_media_by_item.get(i['id'],[])) for i in own),'primary_media_key':primary_for(own),'latest_inclusion_period':latest[0]['inclusion_period'] if latest else None,'logo_media_key':branding_by_team.get(key),'public_status':public_status(x,['slug','display_name']) if country else 'unavailable'})
  for key,x in collections.items():
   team=teams.get(x['team_stable_key']);country=countries.get(x.get('country_stable_key'));own=collection_items.get(key,[])
   output['collections'].append({'slug':x['slug'],'country_slug':country['slug'] if country else '','team_slug':team['slug'] if team else '','name':x['display_name'],'original_name':x['original_name'],'collection_type':x['collection_type'],'inclusion_month':x['inclusion_month'],'inclusion_year':x['inclusion_year'],'inclusion_batch':x['inclusion_batch'],'display_period':x['inclusion_period'],'items_count':len(own),'images_count':sum(len(public_media_by_item.get(i['id'],[])) for i in own),'primary_media_key':primary_for(own),'public_status':public_status(x,['slug','display_name']) if team and country else 'unavailable'})
  for x in items:
   team=teams.get(x['team_stable_key']);country=countries.get(x.get('country_stable_key'));collection=collections.get(x.get('collection_stable_key'));logical=public_media_by_item.get(x['id'],[]);available=[m for m in logical if m['availability_status']=='available']
   output['items'].append({'slug':x['slug'],'country_slug':country['slug'] if country else '','team_slug':team['slug'] if team else '','collection_slug':collection['slug'] if collection else None,'title':x['display_title'],'original_title':x['original_title'],'item_type':x['source_item_type'],'source_page_reference':x['source_page'].replace('\\','/'),'images_count':len(logical),'primary_media_key':available[0]['public_media_key'] if available else None,'public_status':public_status(x,['slug','display_title']) if route_by_item[x['id']] else 'unavailable','public_route':route_by_item[x['id']],'breadcrumbs_json':json.dumps(breadcrumbs_by_item[x['id']],ensure_ascii=False),'description':x.get('source_editorial_description')})
  statuses=[x['public_status'] for rows in output.values() for x in rows];duration=int((time.perf_counter()-clock)*1000);run={'normalization_run_id':normalization['id'],'started_at':started,'completed_at':now(),'status':'completed','countries':len(output['countries']),'teams':len(output['teams']),'collections':len(output['collections']),'items':len(output['items']),'media_relations':len(media_rows),'ready':statuses.count('ready'),'review_required':statuses.count('review_required'),'unavailable':statuses.count('unavailable'),'duration_ms':duration,'schema_version':VIEW_SCHEMA_VERSION,'error_message':None}
  rid=self.repository.persist(run,output,media_rows);return {'viewRun':rid,**run,'uniqueRoutes':len(route_set)}
