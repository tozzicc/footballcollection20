from pathlib import Path
from types import SimpleNamespace
from PIL import Image
from app.models.image_parser import ImageReferenceStatus
from app.repositories.image_parser_repository import ImageParserRepository
from app.services.image_parser_service import ImageParserService
import pytest

def item(path: Path):
    return SimpleNamespace(id=path.name,relativePath=path.name,absolutePath=str(path),filename=path.name,extension=path.suffix,size=path.stat().st_size,createdAt=None,modifiedAt=None,readable=True)

def inspect(path: Path):
    return ImageParserService.__new__(ImageParserService)._inspect(item(path),0,ImageReferenceStatus.ORPHAN)

def test_jpeg_dimensions_ratio_mode_and_size(tmp_path):
    path=tmp_path/'photo.JPG'; Image.new('RGB',(40,20),'red').save(path,'JPEG')
    value=inspect(path)
    assert value.validImage and value.format=='JPEG' and value.width==40 and value.height==20
    assert value.aspectRatio==2 and value.mode=='RGB' and value.fileSize==path.stat().st_size

def test_png_alpha(tmp_path):
    path=tmp_path/'alpha.png'; Image.new('RGBA',(3,4),(0,0,0,0)).save(path)
    value=inspect(path)
    assert value.validImage and value.hasAlpha and value.format=='PNG'

def test_animated_gif(tmp_path):
    path=tmp_path/'animated.gif'; frames=[Image.new('RGB',(2,2),'red'),Image.new('RGB',(2,2),'blue')]
    frames[0].save(path,save_all=True,append_images=frames[1:],duration=10,loop=0)
    value=inspect(path)
    assert value.validImage and value.animated and value.frameCount==2

def test_corrupt_and_empty_are_nonfatal(tmp_path):
    corrupt=tmp_path/'bad.png'; corrupt.write_bytes(b'not an image')
    empty=tmp_path/'empty.jpg'; empty.write_bytes(b'')
    assert not inspect(corrupt).validImage
    assert not inspect(empty).validImage

def test_svg_is_not_opened_by_pillow(tmp_path):
    path=tmp_path/'icon.svg'; path.write_text('<svg xmlns="http://www.w3.org/2000/svg"></svg>',encoding='utf-8')
    value=inspect(path)
    assert value.validImage and value.format=='SVG' and value.width is None


def test_replace_is_blocked_before_cascading_catalog_media(tmp_path):
    repo=ImageParserRepository(tmp_path/'guard.db');repo.create_schema()
    with repo.database.connect() as c:
        c.execute("insert into image_parse_runs(id,workspace_path,started_at,duration_ms,status,total_images,valid_images,invalid_images,referenced_images,orphan_images,broken_references,html_audit_available,total_size,message) values(1,'w','a',1,'completed',1,1,0,1,0,0,0,1,'ok')")
        c.execute("insert into image_metadata(id,run_id,inventory_item_id,relative_path,absolute_path,filename,extension,file_size,has_alpha,animated,frame_count,readable,valid_image,validation_status,validation_message,reference_count,reference_status) values(1,1,'inv','a.jpg','a.jpg','a.jpg','.jpg',1,0,0,1,1,1,'valid','ok',1,'referenced')")
        c.execute("insert into catalog_build_runs(id,started_at,duration_ms,status,countries,teams,collections,items,image_relations,issues,message) values(1,'a',1,'completed',0,1,0,1,1,0,'ok')")
        c.execute("insert into catalog_teams(id,build_run_id,original_name,normalized_name,slug,relative_path,confidence,source) values(1,1,'t','t','t','paises/x/t','high','folder')")
        c.execute("insert into catalog_items(id,build_run_id,team_id,original_title,title,relative_path,slug,item_type,confidence,source) values(1,1,1,'i','i','paises/x/t/i.htm','i','shirt','high','html')")
        c.execute("insert into catalog_item_images(build_run_id,catalog_item_id,image_metadata_id,reference_original,relative_path,is_primary_candidate) values(1,1,1,'a.jpg','a.jpg',1)")
        c.commit()
    with pytest.raises(ValueError,match='replacement blocked'):
        repo.save_run(None,[],[],replace_previous=True)
    with repo.database.connect() as c:
        assert c.execute('select count(*) from catalog_item_images').fetchone()[0]==1
        assert c.execute('select count(*) from image_metadata').fetchone()[0]==1
