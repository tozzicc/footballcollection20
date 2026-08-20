import pytest
from app.services.catalog_builder_service import CatalogBuilderService, normalize, resolve_record_collection, slug
from app.services.catalog_editorial_records import EditorialRecord

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
        contexts=[{'html_page_id':7,'image_reference_id':1,'dom_order':0,'container_type':'adjacent_table','context_text':'CAMISA 2014','extraction_rule':'HX001','status':'matched'}]
        return folders,pages,refs,images,contexts
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

def reference(value,identifier=1):return {'id':identifier,'resolved_relative_path':value}
def record(*paths):return EditorialRecord('record','matched','HX001','description',tuple(reference(value,index) for index,value in enumerate(paths,1)))
def collection(team,value):return (team,value.split('/')[-1],'normalized',value,'inclusion_period',1,2024,None,'inferred','folder')

def test_record_with_one_collection_resolves_that_collection():
    collections={'brasil/team/01 24':collection('brasil/team','camisas/brasil/team/01_24')}
    assert resolve_record_collection(record('camisas/brasil/team/01_24/a.jpg'),collections,'brasil/team')==('brasil/team/01 24','matched')

def test_two_records_on_same_page_resolve_independently():
    collections={key:collection('brasil/team',f'camisas/brasil/team/{folder}') for key,folder in [('brasil/team/01 24','01_24'),('brasil/team/02 24','02_24')]}
    assert resolve_record_collection(record('camisas/brasil/team/01_24/a.jpg'),collections,'brasil/team')[0]=='brasil/team/01 24'
    assert resolve_record_collection(record('camisas/brasil/team/02_24/b.jpg'),collections,'brasil/team')[0]=='brasil/team/02 24'

def test_many_records_can_resolve_different_collections():
    collections={f'brasil/team/0{i} 24':collection('brasil/team',f'camisas/brasil/team/0{i}_24') for i in range(1,4)}
    assert [resolve_record_collection(record(f'camisas/brasil/team/0{i}_24/{i}.jpg'),collections,'brasil/team')[0] for i in range(1,4)]==list(collections)

def test_exclusive_record_uses_all_its_references():
    collections={'brasil/team/01 24':collection('brasil/team','camisas/brasil/team/01_24')}
    assert resolve_record_collection(record('camisas/brasil/team/01_24/a.jpg','camisas/brasil/team/01_24/b.jpg'),collections,'brasil/team')[1]=='matched'

def test_ambiguous_record_is_not_assigned_to_first_collection():
    collections={key:collection('brasil/team',f'camisas/brasil/team/{folder}') for key,folder in [('brasil/team/01 24','01_24'),('brasil/team/02 24','02_24')]}
    assert resolve_record_collection(record('camisas/brasil/team/01_24/a.jpg','camisas/brasil/team/02_24/b.jpg'),collections,'brasil/team')==(None,'ambiguous')

def test_record_without_collection_evidence_is_preserved_unassigned():
    assert resolve_record_collection(record('camisas/brasil/team/root.jpg'),{},'brasil/team')==(None,'unavailable')

def test_cross_team_candidate_is_not_assigned():
    collections={'italia/torino/fot gio':collection('italia/torino','camisas/italia/torino/fot_gio')}
    assert resolve_record_collection(record('camisas/italia/torino/fot_gio/a.jpg'),collections,'italia/roma')==(None,'cross_team')

def test_resolution_does_not_duplicate_records_or_references():
    current=record('camisas/brasil/team/01_24/a.jpg','camisas/brasil/team/01_24/b.jpg');collections={'brasil/team/01 24':collection('brasil/team','camisas/brasil/team/01_24')};before=current.references
    resolve_record_collection(current,collections,'brasil/team');assert current.references==before and len(current.references)==2

def test_resolution_is_deterministic():
    collections={'brasil/team/01 24':collection('brasil/team','camisas/brasil/team/01_24')};current=record('camisas/brasil/team/01_24/a.jpg')
    assert {resolve_record_collection(current,collections,'brasil/team') for _ in range(10)}=={('brasil/team/01 24','matched')}

class MultiCollectionRepository(FakeRepository):
    def source_data(self):
        folders=[{'relative_path':'paises/brasil','name':'brasil','depth':2},{'relative_path':'paises/brasil/team','name':'team','depth':3},{'relative_path':'camisas/brasil/team/01_24','name':'01_24','depth':4},{'relative_path':'camisas/brasil/team/02_24','name':'02_24','depth':4}]
        pages=[{'id':1,'relative_path':'paises/brasil/team/2024.htm','title':'2024'}]
        refs=[{'id':1,'page_id':1,'referenced_inventory_item_id':'a','resolved_relative_path':'camisas/brasil/team/01_24/a.jpg','src_original':'a.jpg','alt_text':'A','is_external':0},{'id':2,'page_id':1,'referenced_inventory_item_id':'b','resolved_relative_path':'camisas/brasil/team/02_24/b.jpg','src_original':'b.jpg','alt_text':'B','is_external':0}]
        images=[{'id':1,'inventory_item_id':'a','relative_path':'camisas/brasil/team/01_24/a.jpg'},{'id':2,'inventory_item_id':'b','relative_path':'camisas/brasil/team/02_24/b.jpg'}]
        contexts=[{'html_page_id':1,'image_reference_id':1,'dom_order':0,'container_type':'adjacent_table','context_text':'A','extraction_rule':'HX001','status':'matched','structural_group_key':'group-a'},{'html_page_id':1,'image_reference_id':2,'dom_order':1,'container_type':'adjacent_table','context_text':'B','extraction_rule':'HX001','status':'matched','structural_group_key':'group-b'}]
        return folders,pages,refs,images,contexts

def test_build_assigns_each_editorial_record_to_its_own_collection():
    repo=MultiCollectionRepository();CatalogBuilderService(repo).build();items=repo.saved[4]
    assert len(items)==2
    assert {value[1] for value in items.values()}=={'brasil/team/01 24','brasil/team/02 24'}
    assert len({value[5] for value in items.values()})==2
