from datetime import datetime,timezone
from app.repositories.catalog_manual_review_repository import CatalogManualReviewRepository
ALLOWED={'unknown_country':{'MR_ASSIGN_COUNTRY'},'unknown_team':{'MR_ASSIGN_TEAM'},'unclassified_folder':{'MR_CLASSIFY_FOLDER'},'ambiguous_structure':{'MR_ASSIGN_TEAM','MR_ASSIGN_COLLECTION'},'missing_image':{'MR_CONFIRM_MISSING_IMAGE'}}
CLASSIFICATIONS={'inclusion_period','collection','unknown'}
class CatalogManualReviewService:
 def __init__(self,repository=None):self.repository=repository or CatalogManualReviewRepository()
 def prerequisites(self):
  build,quality=self.repository.state()
  if not build:raise ValueError('Catálogo persistido necessário.')
  if not quality or quality['catalog_build_run_id']!=build:raise ValueError('Análise de qualidade atual necessária.')
  return build,quality
 def status(self):
  build,quality=self.repository.state();s=self.repository.summary() if quality else {'pending':0,'resolved':0,'acknowledged':0,'deferred':0,'total':0,'lastReviewAt':None}
  return {'catalogAvailable':build is not None,'qualityAnalysisAvailable':quality is not None,'pending':s['pending'],'resolved':s['resolved'],'acknowledged':s['acknowledged'],'deferred':s['deferred'],'total':s['total'],'lastReviewAt':s['lastReviewAt']}
 def context(self,issue_id):
  self.prerequisites();q=self.repository.issue(issue_id)
  if not q:raise ValueError('Issue não encontrado na análise atual.')
  current=self.repository.current_review(q['issue_stable_key']);history=self.repository.history_for(q['issue_stable_key'])
  actions=sorted(ALLOWED.get(q['issue_type'],set())|{'MR_ACKNOWLEDGE','MR_DEFER'})
  return {'issue':q,'entity':{'type':q['entity_type'],'id':q['entity_id'],'name':q['entity_name'],'stableKey':q['entity_stable_key']},'qualityAssessment':{'status':q['quality_status'],'pattern':q['pattern'],'evidence':q['assessment_evidence'],'reason':q['assessment_reason']},'currentReview':current,'history':history,'allowedActions':actions,'overlay':self.overlay(q,current)}
 def candidates(self,issue_id,search='',limit=20):
  build,_=self.prerequisites();q=self.repository.issue(issue_id)
  if not q:raise ValueError('Issue não encontrado.')
  if q['issue_type']=='unknown_country':kind='country'
  elif q['issue_type'] in ('unknown_team','ambiguous_structure'):kind='team'
  else:return []
  table={'country':'catalog_countries','team':'catalog_teams'}[kind];conditions=['x.build_run_id=?'];params=[build]
  if q['issue_type']=='ambiguous_structure' and q['entity_type']=='item':conditions.append('x.country_id=(select current_team.country_id from catalog_items current_item join catalog_teams current_team on current_team.id=current_item.team_id where current_item.id=?)');params.append(q['entity_id'])
  if search:conditions.append('(x.original_name like ? or x.relative_path like ?)');params += [f'%{search}%']*2
  with self.repository.database.connect() as c:
   if kind=='team':rows=c.execute(f"select x.*,s.stable_key,c.original_name country_name from {table} x join catalog_stable_keys s on s.build_run_id=x.build_run_id and s.entity_type=? and s.entity_id=x.id left join catalog_countries c on c.id=x.country_id where {' and '.join(conditions)} order by x.original_name limit ?",[kind,*params,limit]).fetchall()
   else:rows=c.execute(f"select x.*,s.stable_key from {table} x join catalog_stable_keys s on s.build_run_id=x.build_run_id and s.entity_type=? and s.entity_id=x.id where {' and '.join(conditions)} order by x.original_name limit ?",[kind,*params,limit]).fetchall()
  return [dict(x) for x in rows]
 def validate(self,issue_id,request):
  build,quality=self.prerequisites();q=self.repository.issue(issue_id)
  if not q:raise ValueError('Issue não encontrado.')
  code=request.resolutionCode
  if code not in ALLOWED.get(q['issue_type'],set()):raise ValueError('Código de resolução inválido para este tipo de issue.')
  target=None;field=None;proposed=None;target_key=None
  if code in ('MR_ASSIGN_COUNTRY','MR_ASSIGN_TEAM','MR_ASSIGN_COLLECTION'):
   if request.targetEntityId is None:raise ValueError('Entidade alvo obrigatória.')
   kind={'MR_ASSIGN_COUNTRY':'country','MR_ASSIGN_TEAM':'team','MR_ASSIGN_COLLECTION':'collection'}[code];target=self.repository.target(kind,request.targetEntityId,build)
   if not target:raise ValueError('Entidade alvo não existe no build atual.')
   field={'country':'effectiveCountryId','team':'effectiveTeamId','collection':'effectiveCollectionId'}[kind];proposed=target['original_name'];target_key=target['stable_key']
  elif code=='MR_CLASSIFY_FOLDER':
   if request.classification not in CLASSIFICATIONS:raise ValueError('Classificação inválida.')
   field='effectiveClassification';proposed=request.classification
  elif code=='MR_CONFIRM_MISSING_IMAGE':field='missingImageStatus';proposed='confirmed_missing'
  return q,build,quality,field,proposed,target_key
 def preview(self,issue_id,request):
  q,build,quality,field,proposed,target_key=self.validate(issue_id,request)
  current=q['relative_path'] if q['issue_type']=='missing_image' else (q['entity_name'] or q['message']);return {'valid':True,'currentValue':current,'proposedValue':proposed,'effects':[f'Overlay {field} será registrado.'],'warnings':['O valor original permanecerá inalterado.'],'message':'Decisão válida; nenhuma alteração foi persistida.','targetStableKey':target_key}
 def resolve(self,issue_id,request):
  q,build,quality,field,proposed,target_key=self.validate(issue_id,request);return self._save(q,build,quality,request.resolutionCode,'resolved',field,q['entity_name'] or q['message'],proposed,target_key,request.reason,request.notes)
 def acknowledge(self,issue_id,reason):
  build,quality=self.prerequisites();q=self.repository.issue(issue_id)
  if not q:raise ValueError('Issue não encontrado.')
  return self._save(q,build,quality,'MR_ACKNOWLEDGE','acknowledged',None,q['message'],q['message'],None,reason,None)
 def defer(self,issue_id,reason):
  build,quality=self.prerequisites();q=self.repository.issue(issue_id)
  if not q:raise ValueError('Issue não encontrado.')
  return self._save(q,build,quality,'MR_DEFER','deferred',None,q['message'],None,None,reason,None)
 def _save(self,q,build,quality,code,status,field,previous,resolved,target_key,reason,notes):
  now=datetime.now(timezone.utc).isoformat().replace('+00:00','Z');data={'issue_stable_key':q['issue_stable_key'],'issue_id':q['id'],'quality_run_id':quality['id'],'original_build_run_id':build,'current_build_run_id':build,'review_type':q['issue_type'],'status':status,'entity_type':q['entity_type'],'original_entity_id':q['entity_id'],'current_entity_id':q['entity_id'],'entity_stable_key':q['entity_stable_key'] or 'none','field_name':field,'previous_value':previous,'resolved_value':resolved,'target_stable_key':target_key,'resolution_code':code,'reason':reason,'notes':notes,'source':'manual','author':'local_user','reviewed_at':now,'created_at':now,'updated_at':now,'reconciliation_status':'matched','reconciled_at':now,'reconciliation_message':'Revisão criada no build atual.'};rid=self.repository.save(data);return {'id':rid,**data}
 def revert(self,issue_id):
  self.prerequisites();q=self.repository.issue(issue_id)
  if not q:raise ValueError('Issue não encontrado.')
  current=self.repository.current_review(q['issue_stable_key'])
  if not current:raise ValueError('Nenhuma decisão ativa para reverter.')
  self.repository.revert(current['id']);return {'issueId':issue_id,'status':'pending','revertedReviewId':current['id']}
 @staticmethod
 def overlay(q,review):
  result={'hasManualReview':bool(review),'effectiveCountryId':None,'effectiveTeamId':None,'effectiveCollectionId':None,'effectiveClassification':None}
  if not review or review['reconciliation_status']!='matched' or review['status']!='resolved':return result
  field=review['field_name'];result[field]=review['resolved_value'];return result
