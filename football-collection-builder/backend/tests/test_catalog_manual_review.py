from datetime import datetime,timezone
import sqlite3,pytest
from app.repositories.catalog_repository import CatalogRepository
from app.repositories.catalog_manual_review_repository import CatalogManualReviewRepository
from app.services.catalog_manual_review_service import CatalogManualReviewService
from app.models.catalog_review import ReviewResolveRequest
def now():return datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
def build(repo,name='brasil',path='paises/brasil',replace=False):
 countries={name:(name,name,name,path,'inferred','folder')};issues=[('unknown_country','info','country',name,path,'País requer revisão.',now())]
 run=(now(),now(),1,'completed',1,0,0,0,0,1,'ok');return repo.save_build(run,countries,{}, {},{},[],[],issues,replace)
def quality(db,bid):
 c=sqlite3.connect(db);issue=c.execute('select id from catalog_issues where build_run_id=?',(bid,)).fetchone()[0];cur=c.execute("insert into catalog_quality_runs(catalog_build_run_id,started_at,finished_at,duration_ms,status,total_issues,auto_resolved,review_required,quality_score,message) values(?,?,?,?,?,?,?,?,?,?)",(bid,now(),now(),1,'completed',1,0,1,50,'ok'));qid=cur.lastrowid;c.execute("insert into catalog_issue_assessments(quality_run_id,issue_id,resolution_status,pattern,evidence,reason) values(?,?,?,?,?,?)",(qid,issue,'review_required','test','persisted','manual'));c.commit();c.close();return issue
def test_stable_keys_equal_when_autoincrement_ids_change(tmp_path):
 db=tmp_path/'x.db';r=CatalogRepository(db);a=build(r);c=sqlite3.connect(db);first=c.execute("select entity_id,stable_key from catalog_stable_keys where entity_type='country'").fetchone();b=build(r,replace=True);second=c.execute("select entity_id,stable_key from catalog_stable_keys where entity_type='country'").fetchone();assert first[0]!=second[0] and first[1]==second[1]
def test_real_path_change_changes_stable_key(tmp_path):
 db=tmp_path/'x.db';r=CatalogRepository(db);build(r);build(r,'brasil','paises/brasil-novo');c=sqlite3.connect(db);keys=[x[0] for x in c.execute("select stable_key from catalog_stable_keys where entity_type='country' order by id")];assert keys[0]!=keys[1]
def test_preview_resolve_overlay_duplicate_revert_and_history(tmp_path):
 db=tmp_path/'x.db';cr=CatalogRepository(db);bid=build(cr);issue=quality(db,bid);repo=CatalogManualReviewRepository(db);s=CatalogManualReviewService(repo);request=ReviewResolveRequest(resolutionCode='MR_ASSIGN_COUNTRY',targetEntityId=1,reason='Estrutura confirmada.')
 before=repo.history(50,0,{})['total'];p=s.preview(issue,request);assert p['valid'] and repo.history(50,0,{})['total']==before
 saved=s.resolve(issue,request);assert saved['previous_value']=='brasil' and saved['resolved_value']=='brasil' and s.context(issue)['overlay']['hasManualReview']
 with pytest.raises(ValueError,match='decisão ativa'):s.resolve(issue,request)
 assert repo.summary()['resolved']==1;s.revert(issue);assert repo.summary()['pending']==1 and repo.history(50,0,{})['items'][0]['reverted_at']
 with pytest.raises(ValueError,match='Nenhuma decisão ativa'):s.revert(issue)
def test_acknowledge_defer_reason_and_invalid_target(tmp_path):
 db=tmp_path/'x.db';cr=CatalogRepository(db);bid=build(cr);issue=quality(db,bid);s=CatalogManualReviewService(CatalogManualReviewRepository(db))
 with pytest.raises(ValueError):ReviewResolveRequest(resolutionCode='MR_ASSIGN_COUNTRY',targetEntityId=1,reason=' ')
 with pytest.raises(ValueError,match='não existe'):s.preview(issue,ReviewResolveRequest(resolutionCode='MR_ASSIGN_COUNTRY',targetEntityId=999,reason='teste'))
 s.acknowledge(issue,'Conhecido.');assert s.repository.summary()['acknowledged']==1;s.revert(issue);s.defer(issue,'Depois.');assert s.repository.summary()['deferred']==1
def test_reconciliation_matched_orphaned_conflict_and_original_preserved(tmp_path):
 db=tmp_path/'x.db';cr=CatalogRepository(db);a=build(cr);issue=quality(db,a);s=CatalogManualReviewService(CatalogManualReviewRepository(db));s.acknowledge(issue,'confirmado');b=build(cr,replace=True)
 c=sqlite3.connect(db);c.row_factory=sqlite3.Row;review=c.execute('select * from catalog_manual_reviews').fetchone();assert review['reconciliation_status']=='matched' and review['original_entity_id']!=review['current_entity_id'];assert c.execute('select original_name from catalog_countries where build_run_id=?',(b,)).fetchone()[0]=='brasil'
 build(cr,'italia','paises/italia');assert c.execute('select reconciliation_status from catalog_manual_reviews').fetchone()[0]=='orphaned'
 assert cr.reconciliation_status(2,1,1)=='conflict' and cr.reconciliation_status(1,1,1)=='matched' and cr.reconciliation_status(0,1,1)=='orphaned'
def test_rollback_keeps_reviews(tmp_path,monkeypatch):
 db=tmp_path/'x.db';cr=CatalogRepository(db);bid=build(cr);issue=quality(db,bid);repo=CatalogManualReviewRepository(db);s=CatalogManualReviewService(repo);s.acknowledge(issue,'ok')
 with pytest.raises(sqlite3.IntegrityError):
  run=(now(),now(),1,'completed',2,0,0,0,0,0,'bad');cr.save_build(run,{'a':('A','a','a','same','inferred','folder'),'b':('B','b','b','same','inferred','folder')},{},{},{},[],[],[],False)
 assert repo.history(50,0,{})['total']==1
def test_queue_filters_search_pagination_and_no_workspace_access(tmp_path):
 db=tmp_path/'x.db';cr=CatalogRepository(db);bid=build(cr);quality(db,bid);repo=CatalogManualReviewRepository(db);p=repo.queue(1,0,{'issueType':'unknown_country','search':'País'});assert p['total']==1 and len(p['items'])==1
