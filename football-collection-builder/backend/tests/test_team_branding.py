from app.repositories.catalog_repository import CatalogRepository
from app.services.team_branding_service import RULE_CODE,identify_team_branding

def team(stable='team:stable',path='paises/brasil/time'):return {'stable_key':stable,'relative_path':path,'original_name':'Time'}
def page(identifier,path):return {'id':identifier,'relative_path':path}
def image(page_id,inventory,path='logos/time.gif'):return {'page_id':page_id,'referenced_inventory_item_id':inventory,'resolved_relative_path':path}

def test_team_landing_page_logo_is_deterministic_and_independent_of_sql_id():
 pages=[page(10,'paises/brasil/time/time.htm')];refs=[image(10,'inventory:logo')]
 first=identify_team_branding(team(),pages,refs);second=identify_team_branding(team(),pages,refs)
 assert first==second and first['status']=='matched' and first['rule_code']==RULE_CODE
 assert first['team_stable_key']=='team:stable' and first['inventory_reference']=='inventory:logo'
 assert 'id' not in first

def test_absent_and_ambiguous_logo_candidates_are_never_guessed():
 pages=[page(10,'paises/brasil/time/time.htm')]
 absent=identify_team_branding(team(),pages,[])
 ambiguous=identify_team_branding(team(),pages,[image(10,'logo:a'),image(10,'logo:b','logos/other.gif')])
 assert absent['status']=='unavailable' and absent['inventory_reference'] is None
 assert ambiguous['status']=='ambiguous' and ambiguous['inventory_reference'] is None

def test_unrelated_team_media_and_filename_alone_are_not_logo_evidence():
 pages=[page(10,'paises/brasil/time/2025.htm'),page(11,'paises/brasil/time/time.htm')]
 refs=[image(10,'shirt','camisas/brasil/time/time.gif')]
 result=identify_team_branding(team(),pages,refs)
 assert result['status']=='unavailable' and result['inventory_reference'] is None

def test_branding_stable_identity_survives_rebuild_ids():
 key=CatalogRepository.stable_key('team','country:stable','paises/brasil/time')
 a=identify_team_branding(team(key),[page(1,'paises/brasil/time/time.htm')],[image(1,'logo')])
 b=identify_team_branding(team(key),[page(999,'paises/brasil/time/time.htm')],[image(999,'logo')])
 assert a['team_stable_key']==b['team_stable_key']==key and a['inventory_reference']==b['inventory_reference']=='logo'
