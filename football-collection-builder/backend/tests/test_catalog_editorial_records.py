from app.repositories.catalog_repository import CatalogRepository
from app.services.catalog_editorial_records import audit_editorial_records, derive_editorial_records

def ref(identifier,page=1):return {'id':identifier,'page_id':page,'src_original':f'{identifier}.jpg'}
def context(identifier,order,text,status='matched',rule='HX001',page=1,group=None):return {'html_page_id':page,'image_reference_id':identifier,'dom_order':order,'container_type':'adjacent_table','context_text':text,'extraction_rule':rule,'status':status,'structural_group_key':group}

def test_single_record_supports_one_or_many_images():
 one=derive_editorial_records([ref(1)],[context(1,0,'CAMISA A')]);many=derive_editorial_records([ref(1),ref(2)],[context(1,0,'CAMISA A'),context(2,1,'CAMISA A')])
 assert len(one)==1 and len(one[0].references)==1 and one[0].anchor=='page'
 assert len(many)==1 and len(many[0].references)==2 and many[0].description=='CAMISA A'

def test_danilo_and_araujo_records_on_same_page_do_not_mix_media():
 refs=[ref(x) for x in range(1,7)];contexts=[context(x,x-1,'DANILO - COPA DO BRASIL - ORIGINAL' if x<4 else 'L. ARAÚJO - COPA DO BRASIL - ORIGINAL') for x in range(1,7)];records=derive_editorial_records(refs,contexts)
 assert len(records)==2 and [len(x.references) for x in records]==[3,3]
 assert {r['id'] for r in records[0].references}=={1,2,3} and {r['id'] for r in records[1].references}=={4,5,6}
 assert records[0].description.startswith('DANILO') and records[1].description.startswith('L. ARAÚJO')

def test_identical_descriptions_in_distinct_dom_groups_never_merge():
 refs=[ref(x) for x in range(1,7)];contexts=[context(x,x-1,'MESMA DESCRICAO',group='hx001:table-a') if x<4 else context(x,x-1,'MESMA DESCRICAO',group='hx001:table-b') for x in range(1,7)]
 first=derive_editorial_records(refs,contexts);second=derive_editorial_records(refs,contexts)
 assert [x.anchor for x in first]==[x.anchor for x in second]==['hx001:table-a','hx001:table-b']
 assert [len(x.references) for x in first]==[3,3]
 assert {r['id'] for r in first[0].references}.isdisjoint({r['id'] for r in first[1].references})

def test_ambiguous_or_unsupported_structure_never_splits():
 ambiguous=derive_editorial_records([ref(1),ref(2)],[context(1,0,'A','ambiguous','HX004'),context(2,1,'B','ambiguous','HX004')]);unsupported=derive_editorial_records([ref(1),ref(2)],[context(1,0,None,'unsupported_structure','HX000'),context(2,1,None,'unsupported_structure','HX000')])
 assert len(ambiguous)==1 and ambiguous[0].status=='ambiguous'
 assert len(unsupported)==1 and unsupported[0].status=='unsupported'

def test_safe_groups_split_around_a_structurally_isolated_unsupported_group():
 refs=[ref(x) for x in range(1,9)]
 contexts=[context(x,x-1,None,'no_description','HX000',group='hx000:table-11') for x in (1,2)]
 contexts += [context(x,x-1,'CHICAO','matched','HX001',group='hx001:table-19') for x in (3,4,5)]
 contexts += [context(x,x-1,'CHICAO','matched','HX001',group='hx001:table-38') for x in (6,7,8)]
 records=derive_editorial_records(refs,contexts)
 assert [x.status for x in records]==['unsupported','matched','matched']
 assert [len(x.references) for x in records]==[2,3,3]
 assert records[1].description==records[2].description=='CHICAO'

def test_editorial_stable_keys_are_distinct_and_deterministic():
 parent='collection:key';page='paises/brasil/flamengo/2025.html';a=CatalogRepository.stable_key('item',parent,f'{page}#editorial:hx001:adjacent_table:dom-0');b=CatalogRepository.stable_key('item',parent,f'{page}#editorial:hx001:adjacent_table:dom-3')
 assert a!=b and a==CatalogRepository.stable_key('item',parent,f'{page}#editorial:hx001:adjacent_table:dom-0')

def test_global_audit_counts_safe_multiple_ambiguous_and_unsupported_pages():
 pages=[{'id':1,'relative_path':'one.htm'},{'id':2,'relative_path':'two.htm'},{'id':3,'relative_path':'three.htm'}];refs=[ref(1,1),ref(2,2),ref(3,2),ref(4,3)];contexts=[context(1,0,'ONE',page=1),context(2,0,'A',page=2),context(3,1,'B',page=2),context(4,0,'X','ambiguous','HX004',3)];stats=audit_editorial_records(pages,refs,contexts)
 assert stats['pages']==3 and stats['multipleRecordPages']==1 and stats['potentiallyGroupedItems']==1
 assert stats['safeRecords']==3 and stats['ambiguousPages']==1 and stats['unsupportedPages']==0
