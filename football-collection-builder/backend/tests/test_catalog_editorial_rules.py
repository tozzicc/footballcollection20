from app.services.catalog_editorial_rules import season_from

def test_real_season_title_and_filename_patterns():
 assert season_from('1968-1969','x.htm')['label']=='1968–1969'
 assert season_from('1973','x.htm')['label']=='1973'
 assert season_from('sem titulo','paises/time/196869.htm')['label']=='1968–1969'
def test_inclusion_periods_and_invalid_values_are_rejected():
 assert season_from('01_26','x.htm') is None
 assert season_from('01_26_2','x.htm') is None
 assert season_from('qualquer','x.htm') is None
