from pathlib import Path
from types import SimpleNamespace
from PIL import Image
from app.models.image_parser import ImageReferenceStatus
from app.services.image_parser_service import ImageParserService

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
