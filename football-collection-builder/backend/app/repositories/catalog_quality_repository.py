from pathlib import Path
from app.database.database import DEFAULT_DATABASE_PATH,Database
from app.database.schema import SCHEMA_SQL
class CatalogQualityRepository:
 def __init__(self,database_path:str|Path=DEFAULT_DATABASE_PATH):self.database=Database(database_path)
 def create_schema(self):
  with self.database.connect() as c:c.executescript(SCHEMA_SQL)
 def catalog_run(self):
  self.create_schema()
  with self.database.connect() as c:r=c.execute("select * from catalog_build_runs where status='completed' order by id desc limit 1").fetchone()
  return None if r is None else dict(r)
 def issues_for_analysis(self,build_id):
  with self.database.connect() as c:
   rows=c.execute("""select q.*,co.original_name collection_original_name,co.classification collection_classification,
    case q.entity_type when 'country' then cn.original_name when 'team' then t.original_name when 'item' then i.title else co.original_name end entity_name,
    case q.entity_type when 'country' then cn.confidence when 'team' then t.confidence when 'item' then i.confidence else co.confidence end entity_confidence,
    tc.original_name country_name,tc.relative_path country_path,tc.confidence country_confidence,
    hr.resolved_relative_path,hr.exists_in_inventory,hr.status reference_status
    from catalog_issues q left join catalog_countries cn on q.entity_type='country' and cn.id=q.entity_id
    left join catalog_teams t on q.entity_type='team' and t.id=q.entity_id
    left join catalog_collections co on q.entity_type='collection' and co.id=q.entity_id
    left join catalog_items i on q.entity_type='item' and i.id=q.entity_id
    left join catalog_teams et on et.id=co.team_id left join catalog_teams it on it.id=i.team_id
    left join catalog_countries tc on tc.id=coalesce(t.country_id,et.country_id,it.country_id)
    left join html_image_references hr on q.issue_type='missing_image' and hr.page_id=i.source_page_id and q.message like '%'||hr.src_original||'%'
    where q.build_run_id=? group by q.id order by q.id""",(build_id,)).fetchall()
  return [dict(r) for r in rows]
 def save(self,run,assessments,resolutions,replace=True):
  self.create_schema();c=self.database.connect()
  try:
   c.execute('PRAGMA foreign_keys=ON');c.execute('BEGIN')
   if replace:
    for table in ('catalog_resolutions','catalog_issue_assessments','catalog_quality_runs'):c.execute(f'delete from {table}')
   cur=c.execute('insert into catalog_quality_runs(catalog_build_run_id,started_at,finished_at,duration_ms,status,total_issues,auto_resolved,review_required,quality_score,message) values(?,?,?,?,?,?,?,?,?,?)',run);rid=int(cur.lastrowid)
   c.executemany('insert into catalog_issue_assessments(quality_run_id,issue_id,resolution_status,pattern,evidence,reason) values(?,?,?,?,?,?)',[(rid,*x) for x in assessments])
   c.executemany('insert into catalog_resolutions(quality_run_id,issue_id,resolution_type,rule_code,previous_value,resolved_value,confidence,evidence,reason,created_at) values(?,?,?,?,?,?,?,?,?,?)',[(rid,*x) for x in resolutions]);c.commit();return rid
  except Exception:c.rollback();raise
  finally:c.close()
 @staticmethod
 def camel(d):
  m={'catalog_build_run_id':'catalogBuildRunId','started_at':'startedAt','finished_at':'finishedAt','duration_ms':'durationMs','total_issues':'totalIssues','auto_resolved':'autoResolved','review_required':'reviewRequired','quality_score':'qualityScore','issue_type':'issueType','entity_type':'entityType','entity_id':'entityId','relative_path':'relativePath','created_at':'createdAt','resolution_status':'resolutionStatus','rule_code':'ruleCode','resolution_type':'resolutionType','previous_value':'previousValue','resolved_value':'resolvedValue','quality_run_id':'qualityRunId','issue_id':'issueId'}
  return {m.get(k,k):v for k,v in d.items()}
 def latest(self):
  self.create_schema()
  with self.database.connect() as c:r=c.execute("select * from catalog_quality_runs where status='completed' order by id desc limit 1").fetchone()
  return None if r is None else self.camel(dict(r))
 def metrics(self):
  run=self.latest()
  if not run:return None
  rid=run['id'];bid=run['catalogBuildRunId']
  with self.database.connect() as c:
   types={r['issue_type']:r['n'] for r in c.execute('select q.issue_type,count(*) n from catalog_issue_assessments a join catalog_issues q on q.id=a.issue_id where a.quality_run_id=? group by q.issue_type',(rid,))};sevs={r['severity']:r['n'] for r in c.execute('select q.severity,count(*) n from catalog_issue_assessments a join catalog_issues q on q.id=a.issue_id where a.quality_run_id=? group by q.severity',(rid,))}
   counts={}
   for table,key in [('catalog_countries','countries'),('catalog_teams','teams'),('catalog_items','items')]:
    for r in c.execute(f'select confidence,count(*) n from {table} where build_run_id=? group by confidence',(bid,)):counts[f'{key}_{r[0]}']=r[1]
   col_total=c.execute('select count(*) from catalog_collections where build_run_id=?',(bid,)).fetchone()[0];col_unknown=c.execute("select count(*) from catalog_collections where build_run_id=? and classification='unknown'",(bid,)).fetchone()[0]
  return run,types,sevs,counts,col_total,col_unknown
 def page(self,kind,limit,offset,**f):
  run=self.latest();rid=run['id'] if run else -1;params=[rid]
  if kind=='issues':
   joins='join catalog_issues q on q.id=a.issue_id left join catalog_resolutions r on r.quality_run_id=a.quality_run_id and r.issue_id=a.issue_id left join catalog_items i on q.entity_type=\'item\' and i.id=q.entity_id left join catalog_teams t on (q.entity_type=\'team\' and t.id=q.entity_id) or t.id=i.team_id left join catalog_countries c on (q.entity_type=\'country\' and c.id=q.entity_id) or c.id=t.country_id';select='q.*,a.resolution_status,a.pattern,a.evidence,a.reason,r.rule_code,r.confidence';cond=['a.quality_run_id=?'];mapping={'issueType':'q.issue_type','severity':'q.severity','resolutionStatus':'a.resolution_status','teamId':'t.id','countryId':'c.id'}
   if f.get('search'):cond.append('(q.message like ? or q.relative_path like ?)');params += [f"%{f['search']}%"]*2
  else:
   joins='join catalog_issues q on q.id=r.issue_id';select='r.*,q.issue_type,q.relative_path';cond=['r.quality_run_id=?'];mapping={'ruleCode':'r.rule_code','resolutionType':'r.resolution_type','confidence':'r.confidence'}
  for k,col in mapping.items():
   if f.get(k) not in (None,''):cond.append(col+'=?');params.append(f[k])
  table='catalog_issue_assessments a' if kind=='issues' else 'catalog_resolutions r';where=' and '.join(cond)
  with self.database.connect() as c:
   total=c.execute(f'select count(*) from {table} {joins} where {where}',params).fetchone()[0];rows=c.execute(f'select {select} from {table} {joins} where {where} order by {table.split()[-1]}.id limit ? offset ?',[*params,limit,offset]).fetchall()
  return {'items':[self.camel(dict(x)) for x in rows],'total':total,'limit':limit,'offset':offset}
 def detail(self,issue_id):
  page=self.page('issues',1,0,search=None)
  run=self.latest()
  with self.database.connect() as c:r=c.execute('select q.*,a.resolution_status,a.pattern,a.evidence,a.reason,r.rule_code,r.previous_value,r.resolved_value,r.confidence from catalog_issues q join catalog_issue_assessments a on a.issue_id=q.id left join catalog_resolutions r on r.issue_id=q.id and r.quality_run_id=a.quality_run_id where q.id=? and a.quality_run_id=?',(issue_id,run['id'] if run else -1)).fetchone(); inf=c.execute('select * from catalog_inferences where entity_type=(select entity_type from catalog_issues where id=?) and entity_id=(select entity_id from catalog_issues where id=?)',(issue_id,issue_id)).fetchall()
  return None if r is None else {'issue':self.camel(dict(r)),'inferences':[self.camel(dict(x)) for x in inf]}
 def groups(self):
  run=self.latest()
  with self.database.connect() as c:rows=c.execute("select q.issue_type,a.pattern,q.issue_type||':'||a.pattern key,count(*) count,sum(a.resolution_status='auto_resolved') auto_resolvable_count,sum(a.resolution_status='review_required') review_required_count from catalog_issue_assessments a join catalog_issues q on q.id=a.issue_id where a.quality_run_id=? group by q.issue_type,a.pattern order by count desc",(run['id'] if run else -1,)).fetchall()
  return [self.camel(dict(x)) for x in rows]
