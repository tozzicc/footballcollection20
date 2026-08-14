from __future__ import annotations
import re
from app.models.html_parser import HtmlImageContext

RULES={'HX001':'Texto na tabela imediatamente seguinte ao grupo de imagens.','HX002':'Texto na mesma célula de uma única imagem.','HX003':'Texto no mesmo bloco de uma única imagem.','HX004':'Texto compartilhado por múltiplas imagens; associação ambígua.','HX000':'Estrutura sem associação textual suportada.'}
def clean(node):return re.sub(r'\s+',' ',node.get_text(' ',strip=True)).strip() if node else ''
def extract_image_contexts(soup,references):
 contexts=[]
 for order,(tag,ref) in enumerate(zip(soup.find_all('img'),references)):
  table=tag.find_parent('table');cell=tag.find_parent(['td','th']);block=tag.find_parent(['p','div','li','figure']);text='';container=None;rule='HX000';confidence='none';status='unsupported_structure';next_table=table.find_next_sibling('table') if table else None
  if table and next_table and not next_table.find('img') and clean(next_table):text=clean(next_table);container='adjacent_table';rule='HX001';confidence='high';status='matched'
  elif cell and len(cell.find_all('img'))==1 and clean(cell):text=clean(cell);container=cell.name;rule='HX002';confidence='high';status='matched'
  elif block and clean(block) and len(block.find_all('img'))==1:text=clean(block);container=block.name;rule='HX003';confidence='medium';status='matched'
  elif block and clean(block) and len(block.find_all('img'))>1:text=clean(block);container=block.name;rule='HX004';status='ambiguous'
  elif table or cell:container=(table or cell).name;status='no_description'
  contexts.append(HtmlImageContext(domOrder=order,referenceOriginal=ref.srcOriginal,resolvedRelativePath=ref.resolvedRelativePath,containerType=container,contextText=text or None,extractionRule=rule,confidence=confidence,status=status))
 return contexts
