from __future__ import annotations
import re,unicodedata
from collections import defaultdict
from datetime import datetime,timezone
from pathlib import PurePosixPath
from app.repositories.team_branding_repository import TeamBrandingRepository

RULES_VERSION='1.0.0';RULE_CODE='TB001_TEAM_LANDING_LOGOS_DIRECTORY'
def now():return datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
def normalized(value):return re.sub(r'[^a-z0-9]+',' ',unicodedata.normalize('NFKD',value).encode('ascii','ignore').decode().casefold()).strip()
def identify_team_branding(team,pages,references):
 directory=team['relative_path'].replace('\\','/').strip('/');folder=PurePosixPath(directory).name
 landing=[p for p in pages if PurePosixPath(p['relative_path']).parent.as_posix().casefold()==directory.casefold() and normalized(PurePosixPath(p['relative_path']).stem)==normalized(folder)]
 page_ids={p['id'] for p in landing};candidates={r['referenced_inventory_item_id']:r for r in references if r['page_id'] in page_ids and r.get('referenced_inventory_item_id')}
 if len(candidates)==1:
  inventory,row=next(iter(candidates.items()));return {'team_stable_key':team['stable_key'],'inventory_reference':inventory,'relative_path':row['resolved_relative_path'].replace('\\','/'),'source_page':' | '.join(sorted(p['relative_path'] for p in landing)),'rule_code':RULE_CODE,'confidence':'high','status':'matched'}
 return {'team_stable_key':team['stable_key'],'inventory_reference':None,'relative_path':None,'source_page':' | '.join(sorted(p['relative_path'] for p in landing)) or None,'rule_code':RULE_CODE if landing else None,'confidence':'none','status':'ambiguous' if len(candidates)>1 else 'unavailable'}
class TeamBrandingService:
 def __init__(self,repository=None):self.repository=repository or TeamBrandingRepository()
 def build(self):
  source=self.repository.source()
  if not source:raise ValueError('Catálogo persistido necessário.')
  build,teams,pages,refs=source;rows=[identify_team_branding(x,pages,refs) for x in teams];counts=defaultdict(int)
  for row in rows:counts[row['status']]+=1
  stamp=now();run={'catalog_build_id':build,'started_at':stamp,'completed_at':stamp,'status':'completed','teams':len(rows),'matched':counts['matched'],'unavailable':counts['unavailable'],'ambiguous':counts['ambiguous'],'rules_version':RULES_VERSION};rid=self.repository.persist(run,rows);return {'brandingRun':rid,**run}
