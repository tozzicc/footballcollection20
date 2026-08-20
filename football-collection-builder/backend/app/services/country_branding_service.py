from collections import defaultdict
from datetime import datetime,timezone
from pathlib import PurePosixPath
from app.repositories.country_branding_repository import CountryBrandingRepository

RULES_VERSION='1.1.0';RULE_CODE='CB001_COUNTRY_LANDING_HEADER_LOGO';WORLD_RULE_CODE='CB002_HISTORICAL_OTHERS_NAVIGATION_GLOBE'
def now():return datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
def identify_country_branding(country,pages,references):
 directory=country['relative_path'].replace('\\','/').strip('/')
 if directory.casefold()=='paises/outros':
  navigation={p['id']:p for p in pages if PurePosixPath(p['relative_path'].replace('\\','/')).name.casefold() in {'paises.htm','paises_ita.htm','paises_ing.htm'}}
  globe=[(navigation[r['page_id']],r) for r in references if r['page_id'] in navigation and r.get('resolved_relative_path','').replace('\\','/').casefold()=='camisas/bandeiras/planeta03.gif' and r.get('referenced_inventory_item_id')]
  inventory={r['referenced_inventory_item_id']:(p,r) for p,r in globe}
  if len(inventory)==1:
   asset,(page,row)=next(iter(inventory.items()));return {'country_stable_key':country['stable_key'],'inventory_reference':asset,'relative_path':row['resolved_relative_path'].replace('\\','/'),'source_page':page['relative_path'],'rule_code':WORLD_RULE_CODE,'confidence':'high','status':'matched'}
 landing=[p for p in pages if PurePosixPath(p['relative_path'].replace('\\','/')).parent.as_posix().casefold()==directory.casefold()]
 candidates=[]
 for page in landing:
  page_refs=[r for r in references if r['page_id']==page['id'] and r.get('referenced_inventory_item_id')]
  # Nas landings históricas, o emblema editorial do país/seleção vem antes da grade
  # e não recebe dimensões de thumbnail. Uma grade iniciada em 60x60 não tem identidade própria.
  if len(page_refs)>1 and not page_refs[0].get('width_declared') and not page_refs[0].get('height_declared') and any(r.get('width_declared') or r.get('height_declared') for r in page_refs[1:]):
   candidates.append((page,page_refs[0]))
 unique={r['referenced_inventory_item_id']:(p,r) for p,r in candidates}
 if len(unique)==1:
  inventory,(page,row)=next(iter(unique.items()));return {'country_stable_key':country['stable_key'],'inventory_reference':inventory,'relative_path':row['resolved_relative_path'].replace('\\','/'),'source_page':page['relative_path'],'rule_code':RULE_CODE,'confidence':'high','status':'matched'}
 return {'country_stable_key':country['stable_key'],'inventory_reference':None,'relative_path':None,'source_page':' | '.join(sorted(p['relative_path'] for p in landing)) or None,'rule_code':RULE_CODE if landing else None,'confidence':'none','status':'ambiguous' if len(unique)>1 else 'unavailable'}

class CountryBrandingService:
 def __init__(self,repository=None):self.repository=repository or CountryBrandingRepository()
 def build(self):
  source=self.repository.source()
  if not source:raise ValueError('Catálogo persistido necessário.')
  build,countries,pages,refs=source;rows=[identify_country_branding(x,pages,refs) for x in countries];counts=defaultdict(int)
  for row in rows:counts[row['status']]+=1
  stamp=now();run={'catalog_build_id':build,'started_at':stamp,'completed_at':stamp,'status':'completed','countries':len(rows),'matched':counts['matched'],'unavailable':counts['unavailable'],'ambiguous':counts['ambiguous'],'rules_version':RULES_VERSION};rid=self.repository.persist(run,rows);return {'brandingRun':rid,**run}
