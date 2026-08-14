import json,sqlite3
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.repositories.media_repository import MediaRepository
from app.services.media_resolver import MediaResolutionError,MediaResolver
from app.services.media_service import MEDIA_SCHEMA_VERSION,MIME_BY_FORMAT,MediaService,media_key

def seed(db,workspace,extension='.jpg',fmt='JPEG',exists=True):
 repo=MediaRepository(db);repo.create_schema();relative='images/sample'+extension
 path=workspace/'images'/('sample'+extension);path.parent.mkdir(parents=True)
 if exists:path.write_bytes(b'fake-image')
 with repo.database.connect() as c:
  c.execute("insert into inventory_metadata values(1,'a','v',?,1,'a')",(str(workspace),))
  c.execute("insert into catalog_view_runs(id,normalization_run_id,started_at,completed_at,status,schema_version) values(1,1,'a','b','completed','1.0.0')")
  c.execute("insert into catalog_view_media(view_run_id,item_public_route,public_media_key,inventory_reference,filename,extension,is_primary_candidate,media_source,availability_status) values(1,'/item','view-key','inventory-key',?,?,1,'catalog_relation','available')",(path.name,extension))
  c.execute("insert into image_metadata(id,run_id,inventory_item_id,relative_path,absolute_path,filename,extension,format,file_size,width,height,aspect_ratio,mode,has_alpha,animated,frame_count,modified_at,readable,valid_image,validation_status,validation_message,reference_count,reference_status) values(1,1,'inventory-key',?,?,?,?,?,10,100,200,.5,'RGB',0,0,1,'2026-01-01T00:00:00Z',?,1,'valid','ok',1,'referenced')",(relative,str(path),path.name,extension,fmt,int(exists)))
  c.commit()
 return repo

def test_media_key_and_mimes_are_deterministic():
 assert len(media_key('Imagens/Camisa.jpg'))==64
 assert media_key('Imagens\\Camisa.jpg')==media_key('imagens/camisa.jpg')
 assert media_key('a.jpg')!=media_key('b.jpg')
 assert MIME_BY_FORMAT['JPEG']=='image/jpeg' and MIME_BY_FORMAT['PNG']=='image/png' and MIME_BY_FORMAT['GIF']=='image/gif' and MIME_BY_FORMAT['WEBP']=='image/webp'

def test_build_resolve_metadata_headers_and_safety(tmp_path,monkeypatch):
 repo=seed(tmp_path/'media.db',tmp_path/'workspace');service=MediaService(repo);result=service.build();assert result['schema_version']==MEDIA_SCHEMA_VERSION and result['unique_assets']==1 and result['available_assets']==1
 asset=repo.page(24,0)['items'][0];assert asset['mediaUrl'] and 'relativePath' not in asset
 resolved,path=MediaResolver(repo).resolve(asset['mediaKey']);assert path.is_file() and resolved['mime_type']=='image/jpeg'
 import app.api.routes.media as module
 monkeypatch.setattr(module,'service',service);monkeypatch.setattr(module,'resolver',MediaResolver(repo));client=TestClient(app)
 meta=client.get(f"/api/media/assets/{asset['mediaKey']}/metadata");assert meta.status_code==200
 response=client.get(asset['mediaUrl']);assert response.status_code==200 and response.headers['content-type']=='image/jpeg' and response.headers['cache-control']=='public, max-age=3600' and 'etag' in response.headers and 'last-modified' in response.headers
 assert client.get(asset['mediaUrl'],headers={'If-None-Match':response.headers['etag']}).status_code==304
 payload=json.dumps(meta.json());assert 'absolutePath' not in payload and 'workspacePath' not in payload and str(tmp_path) not in payload
 assert client.get('/api/media/assets/../secret').status_code==404 and client.get('/api/media/assets/%2e%2e%2fsecret').status_code==404 and client.get('/api/media/assets/C:%5Csecret').status_code==404

def test_missing_svg_and_containment(tmp_path,monkeypatch):
 missing=seed(tmp_path/'missing.db',tmp_path/'missing-workspace',exists=False);MediaService(missing).build();asset=missing.page(24,0)['items'][0];assert not asset['available']
 with pytest.raises(MediaResolutionError):MediaResolver(missing).resolve(asset['mediaKey'])
 svg=seed(tmp_path/'svg.db',tmp_path/'svg-workspace','.svg','SVG');service=MediaService(svg);service.build();a=svg.page(24,0)['items'][0];assert a['available'] and a['mediaUrl'] is None
 import app.api.routes.media as module
 monkeypatch.setattr(module,'service',service);monkeypatch.setattr(module,'resolver',MediaResolver(svg));assert TestClient(app).get(f"/api/media/assets/{a['mediaKey']}").status_code==415
 with svg.database.connect() as c:c.execute("update media_assets set relative_path='../outside.jpg'");c.commit()
 with pytest.raises(MediaResolutionError):MediaResolver(svg).resolve(a['mediaKey'])

def test_requires_view_and_preserves_previous_on_rollback(tmp_path,monkeypatch):
 service=MediaService(MediaRepository(tmp_path/'empty.db'))
 with pytest.raises(ValueError,match='View Model'):service.build()
 repo=seed(tmp_path/'rollback.db',tmp_path/'workspace');service=MediaService(repo);service.build();before=repo.latest_run_row()['id'];original=repo.persist
 def fail(run,assets,relations):assets[0]['bad']='x';return original(run,assets,relations)
 monkeypatch.setattr(repo,'persist',fail)
 with pytest.raises(sqlite3.OperationalError):service.build()
 assert repo.latest_run_row()['id']==before
