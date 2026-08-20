import sqlite3
import pytest
from app.repositories.catalog_normalization_repository import CatalogNormalizationRepository
from app.services.catalog_normalization_rules import inclusion_period,normalize_value,safe_uppercase_display,slugify,technical_text,unique_slug
from app.services.catalog_normalization_service import CatalogNormalizationService

def seed(path,with_review=False,review_state='matched'):
    repo=CatalogNormalizationRepository(path);repo.create_schema()
    with repo.database.connect() as c:
        c.execute("insert into catalog_build_runs(id,started_at,finished_at,status,message) values(1,'a','b','completed','ok')")
        c.execute("insert into catalog_countries values(1,1,'  BRASIL  ','brasil','brasil','paises/brasil','high','folder')")
        c.execute("insert into catalog_teams values(1,1,1,'SÃO  PAULO FC','sao paulo','sao-paulo','paises/brasil/sp','high','folder')")
        c.execute("insert into catalog_teams values(2,1,1,'unknown team','unknown team','unknown-team','paises/brasil/x','unknown','fallback')")
        c.execute("insert into catalog_collections values(1,1,1,'09_24_2','09_24_2','camisas/brasil/sp/09_24_2','inclusion_period',9,2024,2,'high','folder')")
        c.execute("insert into catalog_items(id,build_run_id,team_id,collection_id,source_page_id,original_title,title,relative_path,slug,item_type,confidence,source) values(1,1,1,1,null,'CAMISA &amp; RARA','CAMISA &amp; RARA','paises/brasil/sp/rara.htm','rara','page','high','html')")
        keys=[('country',1,'country:key'),('team',1,'team:key'),('team',2,'team:unknown'),('collection',1,'collection:key'),('item',1,'item:key')]
        c.executemany('insert into catalog_stable_keys(build_run_id,entity_type,entity_id,stable_key) values(1,?,?,?)',keys)
        if with_review:
            c.execute("insert into catalog_manual_reviews(issue_stable_key,quality_run_id,original_build_run_id,current_build_run_id,review_type,status,entity_type,original_entity_id,current_entity_id,entity_stable_key,field_name,previous_value,resolved_value,target_stable_key,resolution_code,reason,source,author,reviewed_at,created_at,updated_at,reconciliation_status,reconciliation_message) values('issue:key',1,1,1,'unknown_team','resolved','team',2,2,'team:unknown','effectiveTeamId','unknown team','SÃO PAULO FC','team:key','MR_ASSIGN_TEAM','test','manual','tester','a','a','a',?,'test')",(review_state,))
        c.commit()
    return repo

def test_rules_are_conservative_and_deterministic():
    assert technical_text('  São   Paulo &amp; FC ')=='São Paulo & FC'
    assert normalize_value('SÃO PAULO FC')[0]=='São Paulo FC'
    assert safe_uppercase_display('AC MILAN')=='AC Milan'
    assert safe_uppercase_display('PSV')=='PSV'
    assert safe_uppercase_display('AMÉRICA MG')=='América MG'
    assert safe_uppercase_display('São Paulo')=='São Paulo'
    assert slugify(' São Paulo F.C. ')=='sao-paulo-f-c'
    used=set();assert unique_slug('nome','a',used)==('nome',False)
    second=unique_slug('nome','stable:key',used);assert second[0].startswith('nome-') and second==unique_slug('nome','stable:key',{'nome'})
    assert inclusion_period(8,2023,None)=='08/2023'
    assert inclusion_period(9,2024,2)=='09/2024 — lote 2'

def test_requires_catalog(tmp_path):
    service=CatalogNormalizationService(CatalogNormalizationRepository(tmp_path/'empty.db'))
    with pytest.raises(ValueError,match='Catálogo'):service.run()

def test_run_preserves_originals_stable_keys_periods_and_history(tmp_path):
    repo=seed(tmp_path/'catalog.db');service=CatalogNormalizationService(repo);first=service.run();second=service.run()
    assert first['countries_processed']==1 and first['teams_processed']==2 and second['id']!=first['id']
    countries=repo.page('countries',50,0,{})['items'];assert countries[0]['originalName']=='  BRASIL  ' and countries[0]['stableKey']=='country:key' and countries[0]['normalizedName']=='Brasil'
    items=repo.page('items',50,0,{})['items'];assert items[0]['originalTitle']=='CAMISA &amp; RARA' and items[0]['normalizedTitle']=='Camisa & Rara'
    collections=repo.page('collections',50,0,{})['items'];assert collections[0]['inclusionPeriod']=='09/2024 — lote 2' and collections[0]['collectionType']=='inclusion_period'
    unknown=repo.detail('teams','team:unknown');assert unknown['normalizationStatus']=='review_required'
    assert repo.page('teams',1,0,{'search':'SÃO'})['total']==1
    assert repo.page('teams',50,0,{'status':'review_required'})['total']==1
    assert repo.events(50,0,{'status':'review_required'})['total']==1
    with repo.database.connect() as c:assert c.execute("select count(*) from catalog_normalization_runs where status='completed'").fetchone()[0]==2

@pytest.mark.parametrize('state,expected',[('matched','overridden'),('orphaned','review_required'),('conflict','review_required'),('pending_reconciliation','review_required')])
def test_only_matched_manual_review_is_applied(tmp_path,state,expected):
    repo=seed(tmp_path/f'{state}.db',True,state);CatalogNormalizationService(repo).run();row=repo.detail('teams','team:unknown')
    assert row['normalizationStatus']==expected
    if state=='matched':assert row['normalizationSource']=='manual_review' and row['originalName']=='unknown team' and row['displayName']=='São Paulo FC'

def test_transaction_rollback_preserves_previous_run(tmp_path,monkeypatch):
    repo=seed(tmp_path/'rollback.db');service=CatalogNormalizationService(repo);service.run();before=repo.latest_run()['id']
    original=repo.persist
    def fail(run,entities,events):
        entities['countries'][0]['bad_column']='x'
        return original(run,entities,events)
    monkeypatch.setattr(repo,'persist',fail)
    with pytest.raises(sqlite3.OperationalError):service.run()
    assert repo.latest_run()['id']==before
