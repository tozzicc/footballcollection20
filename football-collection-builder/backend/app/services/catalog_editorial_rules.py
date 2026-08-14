from __future__ import annotations
import re
from pathlib import PurePosixPath

def _expand(short,start):
 century=(start//100)*100;value=century+short
 return value+100 if value<start else value
def season_from(title,source_page):
 original=(title or '').strip();filename=PurePosixPath((source_page or '').replace('\\','/')).stem
 if re.fullmatch(r'\d{2}_\d{2}(?:_\d+)?',original):return None
 for value,source in ((original,'title'),(filename,'filename')):
  match=re.fullmatch(r'(19\d{2}|20\d{2})\s*[-/]\s*(19\d{2}|20\d{2})',value)
  if match:
   a,b=map(int,match.groups());return {'label':f'{a}–{b}','start':a,'end':b,'source':source,'rule':'SE001'} if b==a+1 else None
  match=re.fullmatch(r'(19\d{2}|20\d{2})',value)
  if match:return {'label':value,'start':int(value),'end':None,'source':source,'rule':'SE002'}
  match=re.fullmatch(r'(\d{2})\s*[-/]\s*(\d{2})',value)
  if match:
   a=int(match.group(1));start=1900+a if a>=30 else 2000+a;end=_expand(int(match.group(2)),start)
   if end==start+1:return {'label':f'{start}–{end}','start':start,'end':end,'source':source,'rule':'SE003'}
  match=re.fullmatch(r'(\d{2})(\d{2})',value)
  if match:
   a=int(match.group(1));start=1900+a if a>=30 else 2000+a;end=_expand(int(match.group(2)),start)
   if end==start+1:return {'label':f'{start}–{end}','start':start,'end':end,'source':source,'rule':'SE004'}
  match=re.fullmatch(r'(19\d{2}|20\d{2})(\d{2})',value)
  if match:
   start=int(match.group(1));end=_expand(int(match.group(2)),start)
   if end==start+1:return {'label':f'{start}–{end}','start':start,'end':end,'source':source,'rule':'SE005'}
 return None
