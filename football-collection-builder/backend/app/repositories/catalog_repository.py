from __future__ import annotations
import sqlite3,hashlib
from pathlib import Path
from app.database.database import DEFAULT_DATABASE_PATH, Database
from app.database.schema import SCHEMA_SQL

CATALOG_DATA_TABLES = ('catalog_item_images','catalog_inferences','catalog_issues','catalog_items','catalog_collections','catalog_teams','catalog_countries')

class CatalogRepository:
    def __init__(self, database_path: str | Path = DEFAULT_DATABASE_PATH): self.database=Database(database_path)
    def create_schema(self):
        with self.database.connect() as c:
            c.executescript(SCHEMA_SQL);self._backfill_stable_keys(c)
    @staticmethod
    def stable_key(entity_type, *parts):
        canonical='|'.join(str(x or '').replace('\\','/').strip('/').casefold() for x in parts)
        return f'{entity_type}:'+hashlib.sha256(canonical.encode('utf-8')).hexdigest()
    def _backfill_stable_keys(self,c):
        builds=c.execute('SELECT id FROM catalog_build_runs').fetchall()
        for b in builds:
            rid=b['id']
            for r in c.execute('SELECT id,relative_path FROM catalog_countries WHERE build_run_id=?',(rid,)).fetchall():c.execute("INSERT OR IGNORE INTO catalog_stable_keys(build_run_id,entity_type,entity_id,stable_key) VALUES(?,?,?,?)",(rid,'country',r['id'],self.stable_key('country',r['relative_path'])))
            for r in c.execute('SELECT t.id,t.relative_path,c.relative_path country_path FROM catalog_teams t LEFT JOIN catalog_countries c ON c.id=t.country_id WHERE t.build_run_id=?',(rid,)).fetchall():c.execute("INSERT OR IGNORE INTO catalog_stable_keys(build_run_id,entity_type,entity_id,stable_key) VALUES(?,?,?,?)",(rid,'team',r['id'],self.stable_key('team',self.stable_key('country',r['country_path']) if r['country_path'] else '',r['relative_path'])))
            for r in c.execute("SELECT x.id,x.relative_path,s.stable_key parent_key FROM catalog_collections x JOIN catalog_stable_keys s ON s.build_run_id=x.build_run_id AND s.entity_type='team' AND s.entity_id=x.team_id WHERE x.build_run_id=?",(rid,)).fetchall():c.execute("INSERT OR IGNORE INTO catalog_stable_keys(build_run_id,entity_type,entity_id,stable_key) VALUES(?,?,?,?)",(rid,'collection',r['id'],self.stable_key('collection',r['parent_key'],r['relative_path'])))
            for r in c.execute("SELECT i.id,i.relative_path,coalesce(cs.stable_key,ts.stable_key) parent_key FROM catalog_items i LEFT JOIN catalog_stable_keys cs ON cs.build_run_id=i.build_run_id AND cs.entity_type='collection' AND cs.entity_id=i.collection_id JOIN catalog_stable_keys ts ON ts.build_run_id=i.build_run_id AND ts.entity_type='team' AND ts.entity_id=i.team_id WHERE i.build_run_id=?",(rid,)).fetchall():c.execute("INSERT OR IGNORE INTO catalog_stable_keys(build_run_id,entity_type,entity_id,stable_key) VALUES(?,?,?,?)",(rid,'item',r['id'],self.stable_key('item',r['parent_key'],r['relative_path'])))
            issue_rows=c.execute('SELECT id,issue_type,entity_type,entity_id,relative_path,message FROM catalog_issues WHERE build_run_id=? ORDER BY id',(rid,)).fetchall();occurrences={};new_issue_keys=[]
            for q in issue_rows:
                e=c.execute('SELECT stable_key FROM catalog_stable_keys WHERE build_run_id=? AND entity_type=? AND entity_id=?',(rid,q['entity_type'],q['entity_id'])).fetchone();context=hashlib.sha256(q['message'].encode('utf-8')).hexdigest()[:16]
                base=(q['issue_type'],e['stable_key'] if e else 'none',q['relative_path'],context);occurrences[base]=occurrences.get(base,0)+1;new_issue_keys.append((q['id'],self.stable_key('issue',*base,f'occurrence:{occurrences[base]}')))
            for issue_id,new_key in new_issue_keys:
                old=c.execute("SELECT stable_key FROM catalog_stable_keys WHERE build_run_id=? AND entity_type='issue' AND entity_id=?",(rid,issue_id)).fetchone()
                if old and old['stable_key']!=new_key:c.execute('UPDATE catalog_manual_reviews SET issue_stable_key=? WHERE issue_id=?',(new_key,issue_id))
            c.execute("DELETE FROM catalog_stable_keys WHERE build_run_id=? AND entity_type='issue'",(rid,))
            c.executemany("INSERT INTO catalog_stable_keys(build_run_id,entity_type,entity_id,stable_key) VALUES(?,?,?,?)",[(rid,'issue',i,k) for i,k in new_issue_keys])
    def prerequisites(self):
        self.create_schema()
        with self.database.connect() as c:
            return tuple(c.execute(q).fetchone() is not None for q in (
                'SELECT 1 FROM inventory_metadata LIMIT 1',
                "SELECT 1 FROM html_parse_runs WHERE status IN ('completed','completed_with_errors') LIMIT 1",
                "SELECT 1 FROM image_parse_runs WHERE status IN ('completed','completed_with_errors') LIMIT 1"))
    def source_data(self):
        self.create_schema()
        with self.database.connect() as c:
            folders=[dict(r) for r in c.execute('SELECT relative_path,name,depth FROM inventory_folders ORDER BY depth,relative_path')]
            pages=[dict(r) for r in c.execute("SELECT * FROM html_pages WHERE run_id=(SELECT id FROM html_parse_runs WHERE status IN ('completed','completed_with_errors') ORDER BY id DESC LIMIT 1) AND parse_status='parsed' ORDER BY relative_path")]
            refs=[dict(r) for r in c.execute('SELECT * FROM html_image_references WHERE page_id IN (SELECT id FROM html_pages WHERE run_id=(SELECT id FROM html_parse_runs WHERE status IN (\'completed\',\'completed_with_errors\') ORDER BY id DESC LIMIT 1)) ORDER BY page_id,id')]
            images=[dict(r) for r in c.execute("SELECT id,inventory_item_id,relative_path FROM image_metadata WHERE run_id=(SELECT id FROM image_parse_runs WHERE status IN ('completed','completed_with_errors') ORDER BY id DESC LIMIT 1)")]
        return folders,pages,refs,images
    def save_build(self, run, countries, teams, collections, items, relations, inferences, issues, replace_previous=True):
        self.create_schema(); c=self.database.connect()
        try:
            c.execute('PRAGMA foreign_keys=ON'); c.execute('BEGIN')
            cur=c.execute('INSERT INTO catalog_build_runs(started_at,finished_at,duration_ms,status,countries,teams,collections,items,image_relations,issues,message) VALUES(?,?,?,?,?,?,?,?,?,?,?)',run)
            rid=int(cur.lastrowid)
            country_ids={}
            for key,x in countries.items():
                row=c.execute('INSERT INTO catalog_countries(build_run_id,original_name,normalized_name,slug,relative_path,confidence,source) VALUES(?,?,?,?,?,?,?)',(rid,*x)).lastrowid; country_ids[key]=int(row)
                c.execute('INSERT INTO catalog_stable_keys(build_run_id,entity_type,entity_id,stable_key) VALUES(?,?,?,?)',(rid,'country',row,self.stable_key('country',x[3])))
            team_ids={}
            for key,x in teams.items():
                row=c.execute('INSERT INTO catalog_teams(build_run_id,country_id,original_name,normalized_name,slug,relative_path,confidence,source) VALUES(?,?,?,?,?,?,?,?)',(rid,country_ids.get(x[0]),*x[1:])).lastrowid; team_ids[key]=int(row)
                c.execute('INSERT INTO catalog_stable_keys(build_run_id,entity_type,entity_id,stable_key) VALUES(?,?,?,?)',(rid,'team',row,self.stable_key('team',self.stable_key('country',countries[x[0]][3]) if x[0] in countries else '',x[4])))
            collection_ids={}
            for key,x in collections.items():
                row=c.execute('INSERT INTO catalog_collections(build_run_id,team_id,original_name,normalized_name,relative_path,classification,inclusion_month,inclusion_year,inclusion_batch,confidence,source) VALUES(?,?,?,?,?,?,?,?,?,?,?)',(rid,team_ids[x[0]],*x[1:])).lastrowid; collection_ids[key]=int(row)
                c.execute('INSERT INTO catalog_stable_keys(build_run_id,entity_type,entity_id,stable_key) VALUES(?,?,?,?)',(rid,'collection',row,self.stable_key('collection',self.stable_key('team',self.stable_key('country',countries[teams[x[0]][0]][3]) if teams[x[0]][0] in countries else '',teams[x[0]][4]),x[3])))
            item_ids={}
            for key,x in items.items():
                row=c.execute('INSERT INTO catalog_items(build_run_id,team_id,collection_id,source_page_id,original_title,title,relative_path,slug,item_type,confidence,source) VALUES(?,?,?,?,?,?,?,?,?,?,?)',(rid,team_ids[x[0]],collection_ids.get(x[1]),*x[2:])).lastrowid; item_ids[key]=int(row)
                parent_id=collection_ids.get(x[1]) or team_ids[x[0]];parent_type='collection' if x[1] in collection_ids else 'team';parent=c.execute('SELECT stable_key FROM catalog_stable_keys WHERE build_run_id=? AND entity_type=? AND entity_id=?',(rid,parent_type,parent_id)).fetchone()['stable_key'];c.execute('INSERT INTO catalog_stable_keys(build_run_id,entity_type,entity_id,stable_key) VALUES(?,?,?,?)',(rid,'item',row,self.stable_key('item',parent,x[5])))
            c.executemany('INSERT INTO catalog_item_images(build_run_id,catalog_item_id,image_metadata_id,source_page_id,reference_original,relative_path,display_order,alt_text,is_primary_candidate) VALUES(?,?,?,?,?,?,?,?,?)',[(rid,item_ids[x[0]],*x[1:]) for x in relations])
            c.executemany('INSERT INTO catalog_inferences(build_run_id,entity_type,entity_id,field,value,source,source_reference,confidence,reason) VALUES(?,?,?,?,?,?,?,?,?)',[(rid,x[0],team_ids.get(x[1],country_ids.get(x[1],item_ids.get(x[1],0))),*x[2:]) for x in inferences])
            entity_maps={'country':country_ids,'team':team_ids,'collection':collection_ids,'item':item_ids}
            c.executemany('INSERT INTO catalog_issues(build_run_id,issue_type,severity,entity_type,entity_id,relative_path,message,created_at) VALUES(?,?,?,?,?,?,?,?)',[(rid,x[0],x[1],x[2],entity_maps.get(x[2],{}).get(x[3]) if x[3] else None,*x[4:]) for x in issues])
            issue_rows=c.execute('SELECT id,issue_type,entity_type,entity_id,relative_path,message FROM catalog_issues WHERE build_run_id=?',(rid,)).fetchall()
            occurrences={}
            for q in issue_rows:
                entity_key='none'
                if q['entity_id'] is not None:
                    ek=c.execute('SELECT stable_key FROM catalog_stable_keys WHERE build_run_id=? AND entity_type=? AND entity_id=?',(rid,q['entity_type'],q['entity_id'])).fetchone();entity_key=ek['stable_key'] if ek else 'none'
                context=hashlib.sha256(q['message'].encode('utf-8')).hexdigest()[:16]
                base=(q['issue_type'],entity_key,q['relative_path'],context);occurrences[base]=occurrences.get(base,0)+1;c.execute('INSERT INTO catalog_stable_keys(build_run_id,entity_type,entity_id,stable_key) VALUES(?,?,?,?)',(rid,'issue',q['id'],self.stable_key('issue',*base,f'occurrence:{occurrences[base]}')))
            self._reconcile_reviews(c,rid)
            if replace_previous:
                old=[r['id'] for r in c.execute('SELECT id FROM catalog_build_runs WHERE id<>?',(rid,))]
                for oid in old: c.execute('DELETE FROM catalog_build_runs WHERE id=?',(oid,))
            c.commit(); return rid
        except Exception: c.rollback(); raise
        finally: c.close()
    def _reconcile_reviews(self,c,new_build_id):
        reviews=c.execute("SELECT * FROM catalog_manual_reviews WHERE reverted_at IS NULL").fetchall()
        for r in reviews:
            issue_matches=c.execute("SELECT entity_id FROM catalog_stable_keys WHERE build_run_id=? AND entity_type='issue' AND stable_key=?",(new_build_id,r['issue_stable_key'])).fetchall()
            entity_matches=c.execute('SELECT entity_id FROM catalog_stable_keys WHERE build_run_id=? AND entity_type=? AND stable_key=?',(new_build_id,r['entity_type'],r['entity_stable_key'])).fetchall()
            target_matches=[]
            if r['target_stable_key']:
                target_type={'MR_ASSIGN_COUNTRY':'country','MR_ASSIGN_TEAM':'team','MR_ASSIGN_COLLECTION':'collection'}.get(r['resolution_code'])
                target_matches=c.execute('SELECT entity_id FROM catalog_stable_keys WHERE build_run_id=? AND entity_type=? AND stable_key=?',(new_build_id,target_type,r['target_stable_key'])).fetchall() if target_type else []
            status=self.reconciliation_status(len(issue_matches),len(entity_matches),len(target_matches) if r['target_stable_key'] else 1);now=__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat().replace('+00:00','Z')
            c.execute('UPDATE catalog_manual_reviews SET issue_id=?,current_entity_id=?,current_build_run_id=?,reconciliation_status=?,reconciled_at=?,reconciliation_message=?,updated_at=? WHERE id=?',(issue_matches[0]['entity_id'] if len(issue_matches)==1 else None,entity_matches[0]['entity_id'] if len(entity_matches)==1 else None,new_build_id,status,now,'Correspondência inequívoca por stableKey.' if status=='matched' else 'Revisão não aplicada: correspondência ausente ou ambígua.',now,r['id']))
    @staticmethod
    def reconciliation_status(issue_matches,entity_matches,target_matches=1):
        if issue_matches>1 or entity_matches>1 or target_matches>1:return 'conflict'
        if issue_matches==0 or entity_matches==0 or target_matches==0:return 'orphaned'
        return 'matched'
    def last_build(self):
        self.create_schema()
        with self.database.connect() as c: r=c.execute("SELECT * FROM catalog_build_runs WHERE status='completed' ORDER BY id DESC LIMIT 1").fetchone()
        return None if r is None else self._camel(dict(r))
    @staticmethod
    def _camel(x):
        names={'started_at':'startedAt','finished_at':'finishedAt','duration_ms':'durationMs','image_relations':'imageRelations','build_run_id':'buildRunId','original_name':'originalName','normalized_name':'normalizedName','relative_path':'relativePath','country_id':'countryId','team_id':'teamId','collection_id':'collectionId','source_page_id':'sourcePageId','item_type':'itemType','issue_type':'issueType','created_at':'createdAt','image_count':'imageCount','item_count':'itemCount','collection_count':'collectionCount','country_name':'countryName','collection_name':'collectionName','source_reference':'sourceReference','reference_original':'referenceOriginal','display_order':'order','alt_text':'altText','is_primary_candidate':'isPrimaryCandidate'}
        return {names.get(k,k):v for k,v in x.items()}
    def summary(self):
        run=self.last_build()
        if not run: return None
        with self.database.connect() as c:
            rid=run['id']; uc=c.execute("SELECT count(*) n FROM catalog_countries WHERE build_run_id=? AND confidence='unknown'",(rid,)).fetchone()['n']; ut=c.execute("SELECT count(*) n FROM catalog_teams WHERE build_run_id=? AND confidence='unknown'",(rid,)).fetchone()['n']
        return {**{k:run[k] for k in ('countries','teams','collections','items','imageRelations','issues')},'unknownCountries':uc,'unknownTeams':ut,'duration':run['durationMs'],'builtAt':run['finishedAt']}
    def page(self, kind, limit, offset, search=None, **filters):
        table={'countries':'catalog_countries','teams':'catalog_teams','items':'catalog_items','issues':'catalog_issues'}[kind]; run=self.last_build(); cond=['x.build_run_id=?']; params=[run['id'] if run else -1]
        joins=''; select='x.*'
        if kind=='teams': joins=' LEFT JOIN catalog_countries c ON c.id=x.country_id'; select="x.*,c.original_name country_name,(SELECT count(*) FROM catalog_collections z WHERE z.team_id=x.id) collection_count,(SELECT count(*) FROM catalog_items z WHERE z.team_id=x.id) item_count,(SELECT count(*) FROM catalog_item_images z JOIN catalog_items i ON i.id=z.catalog_item_id WHERE i.team_id=x.id) image_count"
        if kind=='items': joins=' LEFT JOIN catalog_collections c ON c.id=x.collection_id'; select="x.*,c.original_name collection_name,(SELECT count(*) FROM catalog_item_images z WHERE z.catalog_item_id=x.id) image_count"
        if search:
            cols={'countries':'x.original_name','teams':'x.original_name','items':'x.title','issues':'x.message'}; cond.append(f"({cols[kind]} LIKE ? OR x.relative_path LIKE ?)"); params += [f'%{search}%',f'%{search}%']
        mapping={'countryId':'country_id','confidence':'confidence','teamId':'team_id','collectionId':'collection_id','itemType':'item_type','issueType':'issue_type','severity':'severity'}
        for key,val in filters.items():
            if val is not None and val!='': cond.append(f'x.{mapping[key]}=?'); params.append(val)
        where=' AND '.join(cond)
        with self.database.connect() as c:
            total=c.execute(f'SELECT count(*) n FROM {table} x {joins} WHERE {where}',params).fetchone()['n']; rows=c.execute(f'SELECT {select} FROM {table} x {joins} WHERE {where} ORDER BY x.relative_path,x.id LIMIT ? OFFSET ?',[*params,limit,offset]).fetchall()
        return {'items':[self._camel(dict(r)) for r in rows],'total':total,'limit':limit,'offset':offset}
    def team_detail(self, entity_id): return self._detail('teams',entity_id)
    def item_detail(self, entity_id): return self._detail('items',entity_id)
    def _detail(self,kind,entity_id):
        run=self.last_build()
        if not run:return None
        with self.database.connect() as c:
            if kind=='teams':
                row=c.execute('SELECT t.*,c.original_name country_name FROM catalog_teams t LEFT JOIN catalog_countries c ON c.id=t.country_id WHERE t.id=? AND t.build_run_id=?',(entity_id,run['id'])).fetchone()
                if not row:return None
                result={'team':self._camel(dict(row)),'collections':[self._camel(dict(x)) for x in c.execute('SELECT * FROM catalog_collections WHERE team_id=? ORDER BY relative_path',(entity_id,))],'items':self.page('items',100,0,teamId=entity_id)['items']}
                image_count=c.execute('SELECT count(*) n FROM catalog_item_images r JOIN catalog_items i ON i.id=r.catalog_item_id WHERE i.team_id=?',(entity_id,)).fetchone()['n']
            else:
                row=c.execute('SELECT i.*,t.original_name team_name,c.original_name country_name,k.original_name collection_name,p.title page_title FROM catalog_items i JOIN catalog_teams t ON t.id=i.team_id LEFT JOIN catalog_countries c ON c.id=t.country_id LEFT JOIN catalog_collections k ON k.id=i.collection_id LEFT JOIN html_pages p ON p.id=i.source_page_id WHERE i.id=? AND i.build_run_id=?',(entity_id,run['id'])).fetchone()
                if not row:return None
                result={'item':self._camel(dict(row)),'images':[self._camel(dict(x)) for x in c.execute('SELECT r.*,m.filename,m.width,m.height,m.format FROM catalog_item_images r JOIN image_metadata m ON m.id=r.image_metadata_id WHERE r.catalog_item_id=? ORDER BY r.display_order,r.id LIMIT 200',(entity_id,))]}; image_count=len(result['images'])
            result['imageCount']=image_count; result['inferences']=[self._camel(dict(x)) for x in c.execute('SELECT * FROM catalog_inferences WHERE entity_type=? AND entity_id=?',(kind[:-1],entity_id))]; result['issues']=[self._camel(dict(x)) for x in c.execute('SELECT * FROM catalog_issues WHERE entity_type=? AND entity_id=?',(kind[:-1],entity_id))]
        return result
