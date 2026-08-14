from __future__ import annotations
import re
from pathlib import Path,PurePosixPath

ALLOWED_EXTENSIONS={'.jpg','.jpeg','.png','.gif','.bmp','.webp','.tif','.tiff','.svg'}
class MediaResolutionError(Exception):pass
class MediaResolver:
 def __init__(self,repository):self.repository=repository
 def resolve(self,media_key):
  if not re.fullmatch(r'[0-9a-f]{64}',media_key):raise MediaResolutionError('Asset não encontrado.')
  asset=self.repository.asset(media_key)
  if not asset:raise MediaResolutionError('Asset não encontrado.')
  relative=asset['relative_path'].replace('\\','/');pure=PurePosixPath(relative)
  if pure.is_absolute() or '..' in pure.parts or ':' in relative or relative.startswith('//'):raise MediaResolutionError('Asset não encontrado.')
  workspace=self.repository.workspace()
  if not workspace:raise MediaResolutionError('Asset não encontrado.')
  root=Path(workspace).resolve();candidate=(root/Path(*pure.parts)).resolve()
  try:candidate.relative_to(root)
  except ValueError:raise MediaResolutionError('Asset não encontrado.')
  if asset['extension'].lower() not in ALLOWED_EXTENSIONS or not candidate.is_file():raise MediaResolutionError('Asset não encontrado.')
  return asset,candidate
