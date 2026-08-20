from __future__ import annotations
import re
from app.models.html_parser import HtmlImageContext

RULES={'HX001':'Texto na tabela imediatamente seguinte ao grupo de imagens.','HX002':'Texto na mesma célula de uma única imagem.','HX003':'Texto no mesmo bloco de uma única imagem.','HX004':'Texto compartilhado por múltiplas imagens; associação ambígua.','HX000':'Estrutura sem associação textual suportada.'}
def clean(node):return re.sub(r'\s+',' ',node.get_text(' ',strip=True)).strip() if node else ''
def extract_image_contexts(soup,references):
 contexts=[];nodes=soup.find_all(True);positions={id(node):index for index,node in enumerate(nodes)};group_orders={}
 for order,(tag,ref) in enumerate(zip(soup.find_all('img'),references)):
  table=tag.find_parent('table');cell=tag.find_parent(['td','th']);block=tag.find_parent(['p','div','li','figure']);text='';container=None;rule='HX000';confidence='none';status='unsupported_structure';next_table=table.find_next_sibling('table') if table else None;image_container=None;description_container=None
  if table and next_table and not next_table.find('img') and clean(next_table):text=clean(next_table);container='adjacent_table';rule='HX001';confidence='high';status='matched';image_container=table;description_container=next_table
  elif cell and len(cell.find_all('img'))==1 and clean(cell):text=clean(cell);container=cell.name;rule='HX002';confidence='high';status='matched';image_container=cell;description_container=cell
  elif block and clean(block) and len(block.find_all('img'))==1:text=clean(block);container=block.name;rule='HX003';confidence='medium';status='matched';image_container=block;description_container=block
  elif block and clean(block) and len(block.find_all('img'))>1:text=clean(block);container=block.name;rule='HX004';status='ambiguous';image_container=block;description_container=block
  elif table or cell:container=(table or cell).name;status='no_description';image_container=table or cell
  else:image_container=block or tag
  image_index=positions.get(id(image_container));description_index=positions.get(id(description_container)) if description_container else None;image_type=image_container.name if image_container else None;description_type=description_container.name if description_container else None
  group_key=f"{rule.casefold()}:{image_type or 'unknown'}-{image_index if image_index is not None else 'unknown'}:description-{description_type or 'none'}-{description_index if description_index is not None else 'none'}"
  if group_key not in group_orders:group_orders[group_key]=len(group_orders)
  contexts.append(HtmlImageContext(domOrder=order,referenceOriginal=ref.srcOriginal,resolvedRelativePath=ref.resolvedRelativePath,containerType=container,contextText=text or None,extractionRule=rule,confidence=confidence,status=status,imageContainerDomIndex=image_index,descriptionContainerDomIndex=description_index,structuralGroupKey=group_key,imageContainerType=image_type,descriptionContainerType=description_type,structuralOrder=group_orders[group_key]))
 return contexts
