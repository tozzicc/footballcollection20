from __future__ import annotations
import json
from pathlib import Path
from app.database.database import DEFAULT_DATABASE_PATH, Database
from app.database.schema import SCHEMA_SQL

TABLES={"countries":"catalog_normalized_countries","teams":"catalog_normalized_teams","collections":"catalog_normalized_collections","items":"catalog_normalized_items"}

class CatalogNormalizationRepository:
    def __init__(self,database_path:str|Path=DEFAULT_DATABASE_PATH):self.database=Database(database_path)
    def create_schema(self):
        with self.database.connect() as c:c.executescript(SCHEMA_SQL)
    @staticmethod
    def _camel(row):
        result={}
        for key,value in dict(row).items():
            parts=key.split('_'); result[parts[0]+''.join(x.title() for x in parts[1:])]=value
        if 'ruleCodes' in result:result['ruleCodes']=json.loads(result['ruleCodes'])
        return result
    def latest_catalog(self):
        self.create_schema()
        with self.database.connect() as c:r=c.execute("select * from catalog_build_runs where status='completed' order by id desc limit 1").fetchone()
        return None if r is None else dict(r)
    def latest_quality(self,build_id):
        with self.database.connect() as c:r=c.execute("select * from catalog_quality_runs where status='completed' and catalog_build_run_id=? order by id desc limit 1",(build_id,)).fetchone()
        return None if r is None else dict(r)
    def latest_run(self):
        self.create_schema()
        with self.database.connect() as c:r=c.execute("select * from catalog_normalization_runs where status='completed' order by id desc limit 1").fetchone()
        return None if r is None else self._camel(r)
    def load_source(self,build_id):
        with self.database.connect() as c:
            countries=[dict(x) for x in c.execute("""select x.*,s.stable_key from catalog_countries x join catalog_stable_keys s on s.build_run_id=x.build_run_id and s.entity_type='country' and s.entity_id=x.id where x.build_run_id=? order by x.id""",(build_id,))]
            teams=[dict(x) for x in c.execute("""select x.*,s.stable_key,cs.stable_key country_stable_key from catalog_teams x join catalog_stable_keys s on s.build_run_id=x.build_run_id and s.entity_type='team' and s.entity_id=x.id left join catalog_stable_keys cs on cs.build_run_id=x.build_run_id and cs.entity_type='country' and cs.entity_id=x.country_id where x.build_run_id=? order by x.id""",(build_id,))]
            collections=[dict(x) for x in c.execute("""select x.*,s.stable_key,ts.stable_key team_stable_key,cs.stable_key country_stable_key from catalog_collections x join catalog_stable_keys s on s.build_run_id=x.build_run_id and s.entity_type='collection' and s.entity_id=x.id join catalog_teams t on t.id=x.team_id join catalog_stable_keys ts on ts.build_run_id=x.build_run_id and ts.entity_type='team' and ts.entity_id=x.team_id left join catalog_stable_keys cs on cs.build_run_id=x.build_run_id and cs.entity_type='country' and cs.entity_id=t.country_id where x.build_run_id=? order by x.id""",(build_id,))]
            items=[dict(x) for x in c.execute("""select x.*,s.stable_key,ts.stable_key team_stable_key,cs.stable_key country_stable_key,ks.stable_key collection_stable_key,coalesce(p.relative_path,x.relative_path) source_page from catalog_items x join catalog_stable_keys s on s.build_run_id=x.build_run_id and s.entity_type='item' and s.entity_id=x.id join catalog_teams t on t.id=x.team_id join catalog_stable_keys ts on ts.build_run_id=x.build_run_id and ts.entity_type='team' and ts.entity_id=x.team_id left join catalog_stable_keys cs on cs.build_run_id=x.build_run_id and cs.entity_type='country' and cs.entity_id=t.country_id left join catalog_stable_keys ks on ks.build_run_id=x.build_run_id and ks.entity_type='collection' and ks.entity_id=x.collection_id left join html_pages p on p.id=x.source_page_id where x.build_run_id=? order by x.id""",(build_id,))]
            reviews=[dict(x) for x in c.execute("""select * from catalog_manual_reviews where current_build_run_id=? and status='resolved' and reconciliation_status='matched' and reverted_at is null order by id""",(build_id,))]
            targets={x['stable_key']:dict(x) for x in c.execute("""select s.stable_key,case s.entity_type when 'country' then c.original_name when 'team' then t.original_name when 'collection' then k.original_name when 'item' then i.original_title end value from catalog_stable_keys s left join catalog_countries c on s.entity_type='country' and c.id=s.entity_id left join catalog_teams t on s.entity_type='team' and t.id=s.entity_id left join catalog_collections k on s.entity_type='collection' and k.id=s.entity_id left join catalog_items i on s.entity_type='item' and i.id=s.entity_id where s.build_run_id=?""",(build_id,))}
        return {'countries':countries,'teams':teams,'collections':collections,'items':items,'reviews':reviews,'targets':targets}
    def persist(self,run,entities,events):
        c=self.database.connect()
        try:
            c.execute('BEGIN')
            cols=','.join(run); marks=','.join('?' for _ in run); rid=int(c.execute(f'insert into catalog_normalization_runs({cols}) values({marks})',tuple(run.values())).lastrowid)
            for kind,rows in entities.items():
                table=TABLES[kind]
                for row in rows:
                    data={'normalization_run_id':rid,**row}; columns=','.join(data); placeholders=','.join('?' for _ in data);c.execute(f'insert into {table}({columns}) values({placeholders})',tuple(data.values()))
            for event in events:
                data={'normalization_run_id':rid,**event};columns=','.join(data);placeholders=','.join('?' for _ in data);c.execute(f'insert into catalog_normalization_events({columns}) values({placeholders})',tuple(data.values()))
            c.commit();return rid
        except Exception:c.rollback();raise
        finally:c.close()
    def summary(self):
        run=self.latest_run()
        if not run:return None
        return {'countries':run['countriesProcessed'],'teams':run['teamsProcessed'],'collections':run['collectionsProcessed'],'items':run['itemsProcessed'],'normalized':run['normalizedCount'],'unchanged':run['unchangedCount'],'reviewRequired':run['reviewRequiredCount'],'overridden':run['overriddenCount'],'events':self.events(1,0,{})['total'],'durationMs':run['durationMs'],'rulesVersion':run['rulesVersion'],'lastRunAt':run['completedAt']}
    def page(self,kind,limit,offset,filters):
        run=self.latest_run();table=TABLES[kind];cond=['normalization_run_id=?'];params=[run['id'] if run else -1]
        mapping={'status':'normalization_status','country':'country_stable_key','team':'team_stable_key','collection':'collection_stable_key','type':'collection_type'}
        for key,column in mapping.items():
            if filters.get(key) is not None:cond.append(column+'=?');params.append(filters[key])
        if filters.get('search'):cond.append('(original_name like ? or normalized_name like ? or display_name like ? or original_path like ?)' if kind!='items' else '(original_title like ? or normalized_title like ? or display_title like ? or original_path like ?)');params += [f"%{filters['search']}%"]*4
        where=' and '.join(cond)
        with self.database.connect() as c:total=c.execute(f'select count(*) from {table} where {where}',params).fetchone()[0];rows=c.execute(f'select * from {table} where {where} order by id limit ? offset ?',[*params,limit,offset]).fetchall()
        return {'items':[self._camel(x) for x in rows],'total':total,'limit':limit,'offset':offset}
    def detail(self,kind,stable_key):
        run=self.latest_run();table=TABLES[kind]
        with self.database.connect() as c:
            row=c.execute(f'select * from {table} where normalization_run_id=? and stable_key=?',(run['id'] if run else -1,stable_key)).fetchone()
            if not row:return None
            events=c.execute('select * from catalog_normalization_events where normalization_run_id=? and entity_type=? and entity_stable_key=? order by id',(run['id'],kind[:-1],stable_key)).fetchall()
        result=self._camel(row);result['events']=[self._camel(x) for x in events];return result
    def events(self,limit,offset,filters):
        run=self.latest_run();cond=['normalization_run_id=?'];params=[run['id'] if run else -1]
        for key,column in {'entityType':'entity_type','ruleCode':'rule_code','status':'status','source':'source'}.items():
            if filters.get(key):cond.append(column+'=?');params.append(filters[key])
        if filters.get('search'):cond.append('(previous_value like ? or resulting_value like ? or message like ?)');params += [f"%{filters['search']}%"]*3
        where=' and '.join(cond)
        with self.database.connect() as c:total=c.execute(f'select count(*) from catalog_normalization_events where {where}',params).fetchone()[0];rows=c.execute(f'select * from catalog_normalization_events where {where} order by id limit ? offset ?',[*params,limit,offset]).fetchall()
        return {'items':[self._camel(x) for x in rows],'total':total,'limit':limit,'offset':offset}
