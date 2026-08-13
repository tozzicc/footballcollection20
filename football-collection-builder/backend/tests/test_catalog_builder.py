import pytest
from app.services.catalog_builder_service import CatalogBuilderService, normalize, slug

class FakeRepository:
    def __init__(self, prerequisites=(True,True,True)):
        self.available=prerequisites; self.saved=None
    def prerequisites(self): return self.available
    def last_build(self):
        if not self.saved:return None
        r=self.saved[0]; return {'id':1,'startedAt':r[0],'finishedAt':r[1],'durationMs':r[2],'status':r[3],'countries':r[4],'teams':r[5],'collections':r[6],'items':r[7],'imageRelations':r[8],'issues':r[9],'message':r[10]}
    def source_data(self):
        folders=[
            {'relative_path':'paises/brasil','name':'Brasil','depth':2},
            {'relative_path':'paises/brasil/América_MG','name':'América_MG','depth':3},
            {'relative_path':'paises/outros','name':'outros','depth':2},
            {'relative_path':'paises/outros/sem equipe','name':'sem equipe','depth':3},
            {'relative_path':'camisas/brasil/América_MG/08_23','name':'08_23','depth':4},
            {'relative_path':'camisas/brasil/América_MG/09_24_3','name':'09_24_3','depth':4},
            {'relative_path':'camisas/brasil/América_MG/especial','name':'especial','depth':4},
        ]
        pages=[{'id':7,'relative_path':'paises/brasil/América_MG/2014.htm','title':'Camisa 2014'}]
        refs=[{'id':1,'page_id':7,'referenced_inventory_item_id':'img-1','resolved_relative_path':'camisas/brasil/América_MG/08_23/a.jpg','src_original':'../../../camisas/a.jpg','alt_text':'Frente','is_external':0}]
        images=[{'id':9,'inventory_item_id':'img-1','relative_path':'camisas/brasil/América_MG/08_23/a.jpg'}]
        return folders,pages,refs,images
    def save_build(self,*args): self.saved=args; return 1

@pytest.mark.parametrize('available,name', [((False,True,True),'Inventory'),((True,False,True),'Parser HTML'),((True,True,False),'Parser de Imagens')])
def test_prerequisites_are_not_run_automatically(available,name):
    with pytest.raises(ValueError,match=name): CatalogBuilderService(FakeRepository(available)).build()

def test_normalization_preserves_original_and_creates_slug():
    assert normalize(' América_MG ')=='américa mg'; assert slug(' América_MG ')=='america-mg'

def test_build_infers_structure_periods_items_images_inferences_and_issues():
    repo=FakeRepository(); result=CatalogBuilderService(repo).build(True)
    run,countries,teams,collections,items,relations,inferences,issues,replace=repo.saved
    assert result['status']=='completed' and replace is True
    assert countries['brasil'][0]=='Brasil' and teams['brasil/américa mg'][1]=='América_MG'
    assert collections['brasil/américa mg/08 23'][4:8]==('inclusion_period',8,2023,None)
    assert collections['brasil/américa mg/09 24 3'][4:8]==('inclusion_period',9,2024,3)
    assert collections['brasil/américa mg/especial'][4]=='collection'
    assert items['7'][7]=='shirt_page' and items['7'][1]=='brasil/américa mg/08 23'
    assert relations[0][-1]==1 and relations[0][1]==9
    assert any(x[0]=='item' and x[2]=='itemType' for x in inferences)
    assert {'unknown_country','unknown_team','unclassified_folder'} <= {x[0] for x in issues}
    assert run[4:10]==(2,2,3,1,1,len(issues))

def test_status_reports_each_persisted_prerequisite():
    status=CatalogBuilderService(FakeRepository((True,False,True))).status()
    assert status['inventoryAvailable'] and not status['htmlParserAvailable'] and status['imageParserAvailable']
