import pytest
from app.services.catalog_quality_rules import evaluate,pattern
from app.services.catalog_quality_service import CatalogQualityService
def issue(kind,**kw):return {'issue_type':kind,'relative_path':kw.pop('relative_path','paises/outros/x'),**kw}
def test_rules_require_unambiguous_persisted_evidence():
 r=evaluate(issue('unclassified_folder',relative_path='camisas/brasil/x/08_23',collection_original_name='08_23',collection_classification='inclusion_period'));assert r.code=='CQ001' and r.resolved_value=='2023-08'
 assert evaluate(issue('unclassified_folder',collection_original_name='especial',collection_classification='collection')) is None
 assert evaluate(issue('unknown_country',entity_confidence='unknown')) is None
 assert evaluate(issue('unknown_country',entity_confidence='inferred',entity_name='brasil')).code=='CQ002'
 assert evaluate(issue('unknown_team',country_confidence='unknown')) is None
 assert evaluate(issue('unknown_team',country_confidence='inferred',country_name='brasil',country_path='paises/brasil')).code=='CQ003'
def test_period_with_batch_and_missing_patterns():
 r=evaluate(issue('unclassified_folder',collection_original_name='09_24_3',collection_classification='inclusion_period'));assert 'lote 3' in r.resolved_value
 assert pattern(issue('missing_image',resolved_relative_path=None))=='unresolved_path'
 assert pattern(issue('missing_image',resolved_relative_path='x.jpg',exists_in_inventory=0))=='image_not_in_inventory'
 assert pattern(issue('ambiguous_structure'))=='title_folder_mismatch'
@pytest.mark.parametrize('total,classified,pending',[(0,0,0),(100,100,0),(100,50,100)])
def test_quality_score_is_deterministic_and_bounded(total,classified,pending):
 score=CatalogQualityService.score(total,classified,pending);assert 0<=score<=100;assert score==CatalogQualityService.score(total,classified,pending)
class EmptyRepo:
 def catalog_run(self):return None
 def latest(self):return None
def test_catalog_is_required_and_not_built_automatically():
 with pytest.raises(ValueError,match='Catálogo persistido'):CatalogQualityService(EmptyRepo()).analyze()
