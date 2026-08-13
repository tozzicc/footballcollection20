from pathlib import Path
from datetime import datetime,timezone
from app.database.database import DEFAULT_DATABASE_PATH,Database
from app.database.schema import SCHEMA_SQL
class CatalogManualReviewRepository:
 def __init__(self,database_path:str|Path=DEFAULT_DATABASE_PATH):self.database=Database(database_path)
 def create_schema(self):
  from app.repositories.catalog_repository import CatalogRepository
  CatalogRepository(self.database.path).create_schema()
 def state(self):
  self.create_schema()
  with self.database.connect() as c:
   build=c.execute("select id from catalog_build_runs where status='completed' order by id desc limit 1").fetchone();quality=c.execute("select id,catalog_build_run_id,quality_score from catalog_quality_runs where status='completed' order by id desc limit 1").fetchone()
  return (None if build is None else build['id'],None if quality is None else dict(quality))
 def issue(self,issue_id):
  build,quality=self.state()
  if not quality:return None
  with self.database.connect() as c:r=c.execute("""select q.*,a.resolution_status quality_status,a.pattern,a.evidence assessment_evidence,a.reason assessment_reason,
   sk.stable_key issue_stable_key,esk.stable_key entity_stable_key,
   case q.entity_type when 'country' then cn.original_name when 'team' then t.original_name when 'collection' then co.original_name when 'item' then i.title end entity_name
   from catalog_issues q join catalog_issue_assessments a on a.issue_id=q.id and a.quality_run_id=?
   join catalog_stable_keys sk on sk.build_run_id=q.build_run_id and sk.entity_type='issue' and sk.entity_id=q.id
   left join catalog_stable_keys esk on esk.build_run_id=q.build_run_id and esk.entity_type=q.entity_type and esk.entity_id=q.entity_id
   left join catalog_countries cn on q.entity_type='country' and cn.id=q.entity_id left join catalog_teams t on q.entity_type='team' and t.id=q.entity_id
   left join catalog_collections co on q.entity_type='collection' and co.id=q.entity_id left join catalog_items i on q.entity_type='item' and i.id=q.entity_id where q.id=?""",(quality['id'],issue_id)).fetchone()
  return None if r is None else dict(r)
 def target(self,entity_type,entity_id,build_id):
  table={'country':'catalog_countries','team':'catalog_teams','collection':'catalog_collections'}[entity_type]
  with self.database.connect() as c:r=c.execute(f"select x.*,s.stable_key from {table} x join catalog_stable_keys s on s.build_run_id=x.build_run_id and s.entity_type=? and s.entity_id=x.id where x.id=? and x.build_run_id=?",(entity_type,entity_id,build_id)).fetchone()
  return None if r is None else dict(r)
 def current_review(self,issue_key):
  with self.database.connect() as c:r=c.execute('select * from catalog_manual_reviews where issue_stable_key=? and reverted_at is null order by id desc limit 1',(issue_key,)).fetchone()
  return None if r is None else dict(r)
 def history_for(self,issue_key):
  with self.database.connect() as c:rows=c.execute('select * from catalog_manual_reviews where issue_stable_key=? order by id desc',(issue_key,)).fetchall()
  return [dict(x) for x in rows]
 def save(self,data):
  c=self.database.connect()
  try:
   c.execute('BEGIN')
   if c.execute('select 1 from catalog_manual_reviews where issue_stable_key=? and reverted_at is null',(data['issue_stable_key'],)).fetchone():raise ValueError('Este issue já possui decisão ativa.')
   cols=','.join(data);marks=','.join('?' for _ in data);cur=c.execute(f'insert into catalog_manual_reviews({cols}) values({marks})',tuple(data.values()));c.commit();return int(cur.lastrowid)
  except Exception:c.rollback();raise
  finally:c.close()
 def revert(self,review_id):
  now=datetime.now(timezone.utc).isoformat().replace('+00:00','Z');c=self.database.connect()
  try:
   c.execute('BEGIN');r=c.execute('select * from catalog_manual_reviews where id=?',(review_id,)).fetchone()
   if not r:raise ValueError('Revisão não encontrada.')
   if r['reverted_at']:raise ValueError('A decisão já foi revertida.')
   c.execute("update catalog_manual_reviews set reverted_at=?,updated_at=?,reconciliation_status='pending_reconciliation',reconciliation_message='Decisão revertida pelo usuário.' where id=?",(now,now,review_id));c.commit()
  except Exception:c.rollback();raise
  finally:c.close()
 def queue(self,limit,offset,filters):
  build,quality=self.state();params=[quality['id'] if quality else -1];cond=['a.quality_run_id=?'];m={'issueType':'q.issue_type','severity':'q.severity'}
  for k,col in m.items():
   if filters.get(k):cond.append(col+'=?');params.append(filters[k])
  status=filters.get('status');effective="coalesce((select r.status from catalog_manual_reviews r where r.issue_stable_key=sk.stable_key and r.reverted_at is null order by r.id desc limit 1),'pending')"
  if status:cond.append(effective+'=?');params.append(status)
  if filters.get('search'):cond.append('(q.message like ? or q.relative_path like ?)');params += [f"%{filters['search']}%"]*2
  where=' and '.join(cond);base=f"from catalog_issue_assessments a join catalog_issues q on q.id=a.issue_id join catalog_stable_keys sk on sk.build_run_id=q.build_run_id and sk.entity_type='issue' and sk.entity_id=q.id where {where}"
  with self.database.connect() as c:total=c.execute('select count(*) '+base,params).fetchone()[0];rows=c.execute(f"select q.*,a.resolution_status quality_status,a.pattern,{effective} review_status "+base+" order by case q.severity when 'error' then 0 when 'warning' then 1 else 2 end,q.id limit ? offset ?",[*params,limit,offset]).fetchall()
  return {'items':[dict(x) for x in rows],'total':total,'limit':limit,'offset':offset}
 def summary(self):
  page=self.queue(1,0,{});total=page['total'];build,quality=self.state()
  with self.database.connect() as c:
   counts={r['status']:r['n'] for r in c.execute("select status,count(*) n from catalog_manual_reviews where reverted_at is null and reconciliation_status='matched' group by status")};bytype={r['issue_type']:r['n'] for r in c.execute("select q.issue_type,count(*) n from catalog_issue_assessments a join catalog_issues q on q.id=a.issue_id where a.quality_run_id=? group by q.issue_type",(quality['id'] if quality else -1,))};bycode={r['resolution_code']:r['n'] for r in c.execute('select resolution_code,count(*) n from catalog_manual_reviews where reverted_at is null group by resolution_code')};last=c.execute('select max(reviewed_at) from catalog_manual_reviews').fetchone()[0]
  done=counts.get('resolved',0)+counts.get('acknowledged',0);return {'total':total,'pending':total-sum(counts.values()),'resolved':counts.get('resolved',0),'acknowledged':counts.get('acknowledged',0),'deferred':counts.get('deferred',0),'progressPercentage':round(100*done/total,1) if total else 0,'byIssueType':bytype,'byResolutionCode':bycode,'lastReviewAt':last,'qualityScore':quality['quality_score'] if quality else None}
 def history(self,limit,offset,filters):
  cond=['1=1'];params=[]
  if filters.get('status'):cond.append('r.status=?');params.append(filters['status'])
  if filters.get('resolutionCode'):cond.append('r.resolution_code=?');params.append(filters['resolutionCode'])
  if filters.get('issueType'):cond.append('q.issue_type=?');params.append(filters['issueType'])
  if filters.get('search'):cond.append('(r.reason like ? or q.relative_path like ?)');params += [f"%{filters['search']}%"]*2
  where=' and '.join(cond)
  with self.database.connect() as c:total=c.execute(f'select count(*) from catalog_manual_reviews r left join catalog_issues q on q.id=r.issue_id where {where}',params).fetchone()[0];rows=c.execute(f'select r.*,q.issue_type,q.relative_path from catalog_manual_reviews r left join catalog_issues q on q.id=r.issue_id where {where} order by r.id desc limit ? offset ?',[*params,limit,offset]).fetchall()
  return {'items':[dict(x) for x in rows],'total':total,'limit':limit,'offset':offset}
