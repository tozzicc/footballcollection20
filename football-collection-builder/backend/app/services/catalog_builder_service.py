from __future__ import annotations
import re, unicodedata
from datetime import datetime, timezone
from pathlib import PurePosixPath
from time import perf_counter
from app.repositories.catalog_repository import CatalogRepository

PERIOD=re.compile(r'^(0[1-9]|1[0-2])_(\d{2})(?:_(\d+))?$')
NAV={'index','content','paises','links','menu','principal','main'}

def normalize(value:str)->str: return ' '.join(value.strip().replace('_',' ').replace('-',' ').split()).casefold()
def slug(value:str)->str:
    base=unicodedata.normalize('NFKD',normalize(value)).encode('ascii','ignore').decode(); return re.sub(r'[^a-z0-9]+','-',base).strip('-') or 'unknown'
def path(value:str)->str: return value.replace('\\','/').strip('/')

class CatalogBuilderService:
    def __init__(self, repository=None): self.repository=repository or CatalogRepository()
    def status(self):
        inv,html,img=self.repository.prerequisites(); last=self.repository.last_build()
        return {'inventoryAvailable':inv,'htmlParserAvailable':html,'imageParserAvailable':img,'catalogAvailable':last is not None,'lastBuild':last,'status':'available' if last else 'not_built'}
    def build(self, replace_previous=True):
        inv,html,img=self.repository.prerequisites()
        missing=[n for n,v in [('Inventory',inv),('Parser HTML',html),('Parser de Imagens',img)] if not v]
        if missing: raise ValueError('Pré-requisitos ausentes: '+', '.join(missing)+'. Execute-os separadamente antes do Catalog Builder.')
        started=datetime.now(timezone.utc); clock=perf_counter(); folders,pages,refs,images=self.repository.source_data()
        countries={}; teams={}; collections={}; items={}; relations=[]; inferences=[]; issues=[]
        now=started.isoformat().replace('+00:00','Z')
        # Only the explicit persisted paises branch provides enough evidence for countries and teams.
        for f in folders:
            p=path(f['relative_path']); parts=p.split('/')
            if len(parts)==2 and parts[0].casefold()=='paises':
                key=normalize(parts[1]); confidence='unknown' if key=='outros' else 'inferred'
                countries[key]=(f['name'],normalize(f['name']),slug(f['name']),p,confidence,'folder')
                inferences.append(('country',key,'originalName',f['name'],'folder',p,confidence,'Nome obtido da estrutura persistida de diretórios.'))
                if confidence=='unknown': issues.append(('unknown_country','info','country',key,p,'Agrupamento de país/região sem evidência específica.',now))
            elif len(parts)==3 and parts[0].casefold()=='paises':
                ck=normalize(parts[1]); tk=ck+'/'+normalize(parts[2]); confidence='inferred' if ck in countries and ck!='outros' else 'unknown'
                teams[tk]=(ck if ck in countries else None,f['name'],normalize(f['name']),slug(f['name']),p,confidence,'folder')
                inferences.append(('team',tk,'originalName',f['name'],'folder',p,confidence,'Nome obtido da estrutura persistida de diretórios.'))
                if confidence=='unknown': issues.append(('unknown_team','info','team',tk,p,'Equipe sem país/região confirmado ou inferido.',now))
        # Shirt folders below camisas/country/team are internal collections, including MM_AA batches.
        for f in folders:
            p=path(f['relative_path']); parts=p.split('/')
            if len(parts)<4 or parts[0].casefold()!='camisas': continue
            tk=normalize(parts[1])+'/'+normalize(parts[2])
            if tk not in teams: continue
            name=parts[3]; match=PERIOD.fullmatch(name); classification='inclusion_period' if match else 'collection'
            month=int(match.group(1)) if match else None; year=2000+int(match.group(2)) if match else None; batch=int(match.group(3)) if match and match.group(3) else None
            key=tk+'/'+normalize(name); collections.setdefault(key,(tk,name,normalize(name),'/'.join(parts[:4]),classification,month,year,batch,'inferred','folder'))
            if not match: issues.append(('unclassified_folder','info','collection',key,'/'.join(parts[:4]),'Agrupamento preservado como collection; significado legado não inferido.',now))
        refs_by_page={}
        for r in refs: refs_by_page.setdefault(r['page_id'],[]).append(r)
        image_by_inventory={x['inventory_item_id']:x for x in images}; image_by_path={path(x['relative_path']).casefold():x for x in images}
        for page in pages:
            pp=path(page['relative_path']); parts=pp.split('/'); tk=None
            if len(parts)>=4 and parts[0].casefold()=='paises': tk=normalize(parts[1])+'/'+normalize(parts[2])
            elif len(parts)>=3 and parts[0].casefold()=='paises': tk=normalize(parts[1])+'/'+normalize(PurePosixPath(parts[-1]).stem)
            elif len(parts)>=2 and parts[0].casefold()=='paises':
                stem=normalize(PurePosixPath(parts[-1]).stem)
                candidates=[k for k in teams if k.startswith(normalize(parts[1])+'/') and k.split('/',1)[1]==stem]; tk=candidates[0] if candidates else None
            if tk not in teams: continue
            stem=normalize(PurePosixPath(pp).stem); team_name=tk.split('/',1)[1]
            item_type='index' if stem=='index' else ('navigation' if stem in NAV else ('team_page' if stem==team_name else 'shirt_page'))
            page_refs=refs_by_page.get(page['id'],[]); collection_key=None
            for candidate in page_refs:
                rp=path(candidate['resolved_relative_path'] or '').split('/')
                if len(rp)>=4 and rp[0].casefold()=='camisas':
                    possible=normalize(rp[1])+'/'+normalize(rp[2])+'/'+normalize(rp[3])
                    if possible in collections: collection_key=possible; break
            title=page['title'].strip() or PurePosixPath(pp).stem; key=str(page['id']); items[key]=(tk,collection_key,page['id'],title,title,pp,slug(title),item_type,'inferred','html')
            inferences.append(('item',key,'itemType',item_type,'html',pp,'inferred','Tipo derivado do nome da página e de sua posição na estrutura.'))
            team_tokens={x for x in normalize(teams[tk][1]).split() if len(x)>2}
            title_tokens=set(normalize(title).split())
            if item_type=='team_page' and team_tokens and team_tokens.isdisjoint(title_tokens):
                issues.append(('ambiguous_structure','warning','item',key,pp,'Título da página de equipe diverge do nome preservado da pasta; requer revisão manual.',now))
            for order,r in enumerate(page_refs):
                image=image_by_inventory.get(r['referenced_inventory_item_id']) or image_by_path.get(path(r['resolved_relative_path'] or '').casefold())
                if image:
                    relations.append((key,image['id'],page['id'],r['src_original'],image['relative_path'],order,r['alt_text'],int(order==0)))
                elif not r['is_external']:
                    issues.append(('missing_image','warning','item',key,r['resolved_relative_path'] or pp,f"Imagem referenciada não localizada: {r['src_original']}",now))
        # Detect, but never merge, duplicate normalized team candidates in one country.
        seen={}
        for key,x in teams.items():
            marker=(x[0],x[2]);
            if marker in seen: issues.append(('duplicate_candidate','warning','team',key,x[4],'Nome normalizado repetido no mesmo país/região; nenhum merge foi realizado.',now))
            seen[marker]=key
        finished=datetime.now(timezone.utc); duration=round((perf_counter()-clock)*1000)
        run=(started.isoformat().replace('+00:00','Z'),finished.isoformat().replace('+00:00','Z'),duration,'completed',len(countries),len(teams),len(collections),len(items),len(relations),len(issues),'Catálogo construído exclusivamente a partir dos dados persistidos.')
        rid=self.repository.save_build(run,countries,teams,collections,items,relations,inferences,issues,replace_previous)
        return {**self.repository.last_build(),'id':rid}
