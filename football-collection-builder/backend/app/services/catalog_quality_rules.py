from __future__ import annotations
import re
from dataclasses import dataclass
PERIOD=re.compile(r'^(0[1-9]|1[0-2])_(\d{2})(?:_(\d+))?$')
@dataclass
class RuleResult:
    code:str;description:str;applicable:bool;resolved_value:str|None=None;confidence:str='unknown';evidence:str='';reason:str=''
def evaluate(issue:dict)->RuleResult|None:
    if issue['issue_type']=='unclassified_folder':
        name=(issue.get('collection_original_name') or issue['relative_path'].rsplit('/',1)[-1])
        m=PERIOD.fullmatch(name)
        if m and issue.get('collection_classification')=='inclusion_period':
            value=f"{2000+int(m.group(2)):04d}-{int(m.group(1)):02d}"+(f"; lote {m.group(3)}" if m.group(3) else '')
            return RuleResult('CQ001','Reconhece período de inclusão já persistido.',True,value,'confirmed',f"Pasta {name}; classification=inclusion_period",'O padrão MM_AA[_lote] e a classificação persistida são inequívocos.')
    if issue['issue_type']=='unknown_country' and issue.get('entity_confidence') in ('confirmed','inferred'):
        return RuleResult('CQ002','Reconhece país já classificado pela entidade persistida.',True,issue.get('entity_name'),'confirmed',f"confidence={issue['entity_confidence']}",'A entidade relacionada já possui classificação não desconhecida.')
    if issue['issue_type']=='unknown_team' and issue.get('country_confidence') in ('confirmed','inferred'):
        return RuleResult('CQ003','Reconhece equipe com país estrutural inequívoco.',True,issue.get('country_name'),'confirmed',f"country={issue.get('country_path')}; confidence={issue.get('country_confidence')}",'A equipe já está ligada a país estruturalmente classificado.')
    return None
def pattern(issue:dict)->str:
    if issue['issue_type']=='missing_image':
        if not issue.get('resolved_relative_path'): return 'unresolved_path'
        if issue.get('exists_in_inventory')==0:return 'image_not_in_inventory'
        return 'catalog_relation_missing'
    return {'unknown_country':'unknown_country_branch','unknown_team':'unknown_country_branch','unclassified_folder':'unknown_collection_pattern','ambiguous_structure':'title_folder_mismatch'}.get(issue['issue_type'],'unknown_pattern')
