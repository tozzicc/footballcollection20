import json,sqlite3
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.repositories.catalog_view_repository import CatalogViewRepository
from app.services.catalog_public_routes import item_breadcrumbs,public_item_route
from app.services.catalog_view_service import CatalogViewService,VIEW_SCHEMA_VERSION,public_status

def seed(path,duplicate_direct=False):
 repo=CatalogViewRepository(path);repo.create_schema()
 with repo.database.connect() as c:
  c.execute("insert into catalog_build_runs(id,started_at,finished_at,status,message) values(1,'a','b','completed','ok')")
  for i in range(1,5):c.execute("insert into catalog_items(id,build_run_id,team_id,collection_id,source_page_id,original_title,title,relative_path,slug,item_type,confidence,source) values(?,1,1,?,null,?,?,?,?,'shirt','high','html')",(i,1 if i<3 else None,f'Item {i}',f'Item {i}',f'page{i}.htm','same' if i<3 else 'direct'))
  c.execute("insert into catalog_normalization_runs(id,catalog_build_id,started_at,completed_at,status,rules_version,countries_processed,teams_processed,collections_processed,items_processed,duration_ms) values(1,1,'a','b','completed','1.0.1',1,1,2,4,1)")
  c.execute("insert into catalog_normalized_countries values(1,1,'country:key',1,'Brasil','paises/brasil','Brasil','Brasil','brasil','unchanged','original','high','[]','a','a')")
  c.execute("insert into catalog_normalized_teams values(1,1,'team:key',1,'country:key','Time FC','p','Time FC','Time FC','time-fc','unchanged','original','high','[]','a','a')")
  for i,(slug,month) in enumerate([('08-2023',8),('09-2024',9)],1):c.execute("""insert into catalog_normalized_collections(id,normalization_run_id,stable_key,source_entity_id,team_stable_key,country_stable_key,original_name,original_path,normalized_name,display_name,slug,collection_type,inclusion_period,inclusion_month,inclusion_year,normalization_status,normalization_source,confidence,created_at,updated_at) values(?,?,?,?,'team:key','country:key',?,?,?,?,?,'inclusion_period',?,?,2024,'unchanged','original','high','a','a')""",(i,1,f'collection:{i}',i,f'0{month}_24',f'c/{i}',f'0{month}/2024',f'0{month}/2024',slug,f'0{month}/2024',month))
  items=[(1,'collection:1','same','ready title','unchanged'),(2,'collection:2','same','ready title','review_required'),(3,None,'direct','Direct','unchanged')]
  if duplicate_direct:items.append((4,None,'direct','Duplicate','unchanged'))
  for i,col,slug,title,status in items:c.execute("insert into catalog_normalized_items values(?,?,?,?,'team:key','country:key',?,?,?,?,?,?,?,?,?,?,?,?,?)",(i,1,f'item:{i}',i,col,title,f'page{i}.htm',title,title,slug,f'page{i}.htm',status,'original','high','[]','a','a'))
  c.execute("insert into image_metadata(id,run_id,inventory_item_id,relative_path,absolute_path,filename,extension,format,file_size,width,height,aspect_ratio,mode,has_alpha,animated,frame_count,readable,valid_image,validation_status,validation_message,reference_count,reference_status) values(1,1,'media:key','img.jpg','C:\\private\\img.jpg','img.jpg','.jpg','JPEG',10,100,200,.5,'RGB',0,0,1,1,1,'valid','ok',1,'referenced')")
  c.execute("insert into catalog_item_images(id,build_run_id,catalog_item_id,image_metadata_id,reference_original,relative_path,display_order,alt_text,is_primary_candidate) values(1,1,1,1,'img.jpg','img.jpg',2,'secondary',0)")
  c.execute("insert into catalog_item_images(id,build_run_id,catalog_item_id,image_metadata_id,reference_original,relative_path,display_order,alt_text,is_primary_candidate) values(2,1,1,1,'img.jpg','img.jpg',5,'primary',1)")
  c.commit()
 return repo

def test_route_helper_and_breadcrumbs_are_deterministic():
 assert public_item_route('brasil','time','item','08-2023')=='/items/brasil/teams/time/collections/08-2023/item'
 assert public_item_route('brasil','time','item')=='/items/brasil/teams/time/items/item'
 assert public_item_route('brasil','time','item')==public_item_route('brasil','time','item')
 assert [x['type'] for x in item_breadcrumbs('brasil','Brasil','time','Time','item','Item','c','Collection')]==['country','team','collection','item']
 assert public_status({'normalization_status':'review_required','slug':'x','name':'x'},['slug','name'])=='review_required'
 assert public_status({'normalization_status':'unchanged','slug':'','name':'x'},['slug','name'])=='unavailable'

def test_build_public_models_media_routes_search_latest_and_safety(tmp_path,monkeypatch):
 repo=seed(tmp_path/'view.db');service=CatalogViewService(repo);first=service.build();second=service.build()
 assert first['schema_version']==VIEW_SCHEMA_VERSION and second['viewRun']!=first['viewRun']
 assert first['countries']==1 and first['items']==3 and first['media_relations']==2 and first['uniqueRoutes']==3
 items=repo.page('items',24,0,{})['items'];routes={x['publicRoute'] for x in items};assert len(routes)==3
 assert '/items/brasil/teams/time-fc/collections/08-2023/same' in routes
 assert '/items/brasil/teams/time-fc/collections/09-2024/same' in routes
 assert '/items/brasil/teams/time-fc/items/direct' in routes
 detail=repo.item_detail('brasil','time-fc','same','08-2023');assert detail['primaryMedia']['altText']=='primary' and any(x['isPrimaryCandidate'] for x in detail['media'])
 assert repo.item_detail('brasil','time-fc','direct')['primaryMedia'] is None
 assert repo.page('items',1,0,{})['hasNext']
 assert any(x['publicStatus']=='review_required' for x in items)
 assert repo.page('collections',24,0,{'year':2024})['total']==2
 assert repo.search('Brasil',None,None,24,0)['items'][0]['type']=='country'
 assert repo.search('Time',None,None,24,0)['items'][0]['type']=='team'
 assert repo.search('',None,None,24,0)['total']==0
 assert repo.search('08/2024',None,None,24,0)['total']>=1
 search=repo.search('ready',None,None,24,0);assert all(x['publicRoute'].startswith('/items/') for x in search['items'])
 latest=repo.latest(2);assert latest[0]['publicRoute'].startswith('/items/')
 assert repo.navigation()['countries'][0]['slug']=='brasil'
 payload=json.dumps({'summary':repo.summary(),'items':items,'detail':detail,'search':search,'latest':latest});assert 'absolutePath' not in payload and 'workspacePath' not in payload and 'C:\\' not in payload and 'stableKey' not in payload
 import app.api.routes.catalog_view as routes_module
 monkeypatch.setattr(routes_module,'service',service);client=TestClient(app)
 assert client.get('/api/public/catalog/items/brasil/teams/time-fc/collections/08-2023/same').status_code==200
 assert client.get('/api/public/catalog/items/brasil/teams/time-fc/items/direct').status_code==200
 built=client.post('/api/public/catalog/build',json={}).json();assert 'viewRun' not in built and 'normalizationRunId' not in built

def test_duplicate_direct_route_blocks_build(tmp_path):
 service=CatalogViewService(seed(tmp_path/'collision.db',True))
 with pytest.raises(ValueError,match='Colisão de rota pública'):service.build()

def test_missing_normalization_and_rollback(tmp_path,monkeypatch):
 empty=CatalogViewService(CatalogViewRepository(tmp_path/'empty.db'))
 with pytest.raises(ValueError,match='Normalização'):empty.build()
 repo=seed(tmp_path/'rollback.db');service=CatalogViewService(repo);service.build();before=repo.latest_run()
 original=repo.persist
 def fail(run,entities,media):entities['countries'][0]['bad']='x';return original(run,entities,media)
 monkeypatch.setattr(repo,'persist',fail)
 with pytest.raises(sqlite3.OperationalError):service.build()
 assert repo.latest_run()==before
