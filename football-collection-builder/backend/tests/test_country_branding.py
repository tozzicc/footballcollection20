from app.repositories.catalog_repository import CatalogRepository
from app.services.country_branding_service import RULE_CODE,WORLD_RULE_CODE,identify_country_branding

def country(stable='country:stable',path='paises/brasil'):return {'stable_key':stable,'relative_path':path,'original_name':'Brasil'}
def page(identifier,path='paises/brasil/brazil.htm'):return {'id':identifier,'relative_path':path}
def image(page_id,inventory,path,width=None,height=None):return {'page_id':page_id,'referenced_inventory_item_id':inventory,'resolved_relative_path':path,'width_declared':width,'height_declared':height}

def test_header_logo_before_thumbnail_grid_is_country_branding():
 refs=[image(10,'country:logo','logos/selection.gif'),image(10,'team:logo','logos/team.gif','60','60')]
 first=identify_country_branding(country(),[page(10)],refs);second=identify_country_branding(country(),[page(10)],refs)
 assert first==second and first['status']=='matched' and first['rule_code']==RULE_CODE
 assert first['inventory_reference']=='country:logo' and 'id' not in first

def test_grid_without_header_identity_is_unavailable():
 refs=[image(10,'ajax','logos/ajax.gif','60','60'),image(10,'argentina','logos/argentina.gif')]
 result=identify_country_branding(country(path='paises/outros'),[page(10,'paises/outros/others.htm')],refs)
 assert result['status']=='unavailable' and result['inventory_reference'] is None

def test_historical_others_navigation_globe_is_country_branding():
 pages=[page(1,'paises.htm'),page(2,'paises_ita.htm'),page(3,'paises/outros/others.htm')]
 refs=[image(1,'planet','camisas/bandeiras/planeta03.gif','50','50'),image(2,'planet','camisas/bandeiras/planeta03.gif','50','50')]
 result=identify_country_branding(country(path='paises/outros'),pages,refs)
 assert result['status']=='matched' and result['inventory_reference']=='planet'
 assert result['source_page']=='paises_ita.htm' or result['source_page']=='paises.htm'
 assert result['rule_code']==WORLD_RULE_CODE

def test_unrelated_nested_page_and_filename_are_not_evidence():
 refs=[image(10,'country:logo','logos/brasil.gif'),image(10,'team:logo','logos/team.gif','60','60')]
 result=identify_country_branding(country(),[page(10,'paises/brasil/team/team.htm')],refs)
 assert result['status']=='unavailable'

def test_multiple_structural_headers_are_ambiguous_and_stable_key_survives_ids():
 key=CatalogRepository.stable_key('country',None,'paises/brasil')
 pages=[page(1),page(2,'paises/brasil/index.htm')]
 refs=[image(1,'a','logos/a.gif'),image(1,'t1','logos/t1.gif','60','60'),image(2,'b','logos/b.gif'),image(2,'t2','logos/t2.gif','60','60')]
 assert identify_country_branding(country(key),pages,refs)['status']=='ambiguous'
 a=identify_country_branding(country(key),[page(1)],refs[:2]);b=identify_country_branding(country(key),[page(999)],[{**x,'page_id':999} for x in refs[:2]])
 assert a['country_stable_key']==b['country_stable_key']==key and a['inventory_reference']==b['inventory_reference']=='a'
