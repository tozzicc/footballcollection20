from datetime import datetime,timezone
from time import perf_counter
from app.repositories.catalog_quality_repository import CatalogQualityRepository
from app.services.catalog_quality_rules import evaluate,pattern
class CatalogQualityService:
 def __init__(self,repository=None):self.repository=repository or CatalogQualityRepository()
 def status(self):
  build=self.repository.catalog_run();last=self.repository.latest();return {'catalogAvailable':build is not None,'qualityAnalysisAvailable':last is not None,'catalogBuildRunId':None if build is None else build['id'],'lastAnalysis':last,'status':'available' if last else 'not_analyzed'}
 @staticmethod
 def score(entity_total,classified,pending):
  if entity_total<=0:return 0.0
  classification=classified/entity_total; issue_factor=max(0,1-pending/(entity_total+pending))
  return round(max(0,min(100,100*(.75*classification+.25*issue_factor))),1)
 def analyze(self,replace=True):
  build=self.repository.catalog_run()
  if not build:raise ValueError('Catálogo persistido necessário. O Catalog Builder não será executado automaticamente.')
  start=datetime.now(timezone.utc);clock=perf_counter();issues=self.repository.issues_for_analysis(build['id']);assess=[];res=[];now=start.isoformat().replace('+00:00','Z')
  for issue in issues:
   rule=evaluate(issue);pat=pattern(issue)
   if rule and rule.applicable:
    assess.append((issue['id'],'auto_resolved',pat,rule.evidence,rule.reason));res.append((issue['id'],'automatic',rule.code,issue.get('message'),rule.resolved_value,rule.confidence,rule.evidence,rule.reason,now))
   else:
    reason='Os dados persistidos não fornecem evidência inequívoca para alterar a classificação.'
    if issue['issue_type']=='missing_image':reason='A referência permanece ausente nos dados persistidos; nenhum caminho é corrigido automaticamente.'
    assess.append((issue['id'],'review_required',pat,issue.get('relative_path') or '',reason))
  auto=len(res);review=len(issues)-auto
  entity_total=build['countries']+build['teams']+build['collections']+build['items']
  classified=entity_total-sum(1 for x in issues if x['issue_type'] in ('unknown_country','unknown_team','unclassified_folder'))
  score=self.score(entity_total,classified,review);finish=datetime.now(timezone.utc);duration=round((perf_counter()-clock)*1000)
  run=(build['id'],start.isoformat().replace('+00:00','Z'),finish.isoformat().replace('+00:00','Z'),duration,'completed',len(issues),auto,review,score,'Análise concluída somente sobre dados persistidos.')
  rid=self.repository.save(run,assess,res,replace);return {**self.repository.latest(),'id':rid}
 def summary(self):
  data=self.repository.metrics()
  if not data:return None
  run,types,sevs,c,ct,cu=data
  def n(prefix,confidence):return c.get(prefix+'_'+confidence,0)
  return {'totalIssues':run['totalIssues'],'openIssues':0,'autoResolvedIssues':run['autoResolved'],'reviewRequiredIssues':run['reviewRequired'],'issuesByType':types,'issuesBySeverity':sevs,
   'countriesTotal':sum(n('countries',x) for x in ('confirmed','inferred','unknown')),'countriesConfirmed':n('countries','confirmed'),'countriesInferred':n('countries','inferred'),'countriesUnknown':n('countries','unknown'),
   'teamsTotal':sum(n('teams',x) for x in ('confirmed','inferred','unknown')),'teamsConfirmed':n('teams','confirmed'),'teamsInferred':n('teams','inferred'),'teamsUnknown':n('teams','unknown'),
   'itemsTotal':sum(n('items',x) for x in ('confirmed','inferred','unknown')),'itemsConfirmed':n('items','confirmed'),'itemsInferred':n('items','inferred'),'itemsUnknown':n('items','unknown'),
   'collectionsTotal':ct,'collectionsClassified':ct-cu,'collectionsUnknown':cu,'missingImages':types.get('missing_image',0),'qualityScore':run['qualityScore'],'analyzedAt':run['finishedAt'],'durationMs':run['durationMs']}
