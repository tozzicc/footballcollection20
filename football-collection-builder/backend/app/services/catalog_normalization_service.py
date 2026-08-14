from __future__ import annotations
import json,time
from datetime import datetime,timezone
from app.repositories.catalog_normalization_repository import CatalogNormalizationRepository
from app.services.catalog_normalization_rules import RULES_VERSION,inclusion_period,is_unknown,normalize_value,slugify,unique_slug

def now():return datetime.now(timezone.utc).isoformat().replace('+00:00','Z')

class CatalogNormalizationService:
    def __init__(self,repository=None):self.repository=repository or CatalogNormalizationRepository()
    def status(self):
        catalog=self.repository.latest_catalog();run=self.repository.latest_run()
        review=False
        if catalog:
            with self.repository.database.connect() as c:review=bool(c.execute('select 1 from catalog_manual_reviews where current_build_run_id=? limit 1',(catalog['id'],)).fetchone())
        return {'catalogAvailable':catalog is not None,'reviewAvailable':review,'normalizationAvailable':run is not None,'lastRun':run,'rulesVersion':RULES_VERSION}
    def run(self):
        catalog=self.repository.latest_catalog()
        if not catalog:raise ValueError('Catálogo persistido necessário.')
        started=now();clock=time.perf_counter();source=self.repository.load_source(catalog['id']);review_map={x['entity_stable_key']:x for x in source['reviews']};targets=source['targets']
        output={x:[] for x in ('countries','teams','collections','items')};events=[];counts={'normalized':0,'unchanged':0,'review_required':0,'overridden':0};used={}
        specs=(('countries','country','original_name','CN001'),('teams','team','original_name','TM001'),('collections','collection','original_name','CL001'),('items','item','original_title','IT001'))
        timestamp=now()
        for plural,entity_type,value_field,rule_code in specs:
            for row in source[plural]:
                original=row[value_field];normalized,changes=normalize_value(original);display=normalized;review=review_map.get(row['stable_key']);source_name='original';status='unchanged';rules=[]
                collection_type=row.get('classification')
                if review:
                    target=targets.get(review.get('target_stable_key') or '')
                    if target and target.get('value'):normalized=display=normalize_value(target['value'])[0]
                    if review.get('field_name')=='effectiveClassification' and review.get('resolved_value'):collection_type=review['resolved_value']
                    source_name='manual_review';status='overridden';rules=['MR001']
                elif is_unknown(original,row.get('confidence','')):
                    status='review_required'
                elif changes:
                    source_name='deterministic_rule';status='normalized';rules=[rule_code]
                scope='countries' if plural=='countries' else (row.get('country_stable_key') if plural=='teams' else row.get('team_stable_key') if plural=='collections' else row.get('collection_stable_key') or row.get('team_stable_key'))
                slug,collision=unique_slug(slugify(display),row['stable_key'],used.setdefault(scope,set()));rules.append('SL002' if collision else 'SL001')
                common={'stable_key':row['stable_key'],'source_entity_id':row['id'],'original_path':row['relative_path'],'slug':slug,'normalization_status':status,'normalization_source':source_name,'confidence':row.get('confidence','unknown'),'rule_codes':json.dumps(rules),'created_at':timestamp,'updated_at':timestamp}
                if plural=='countries':data={**common,'original_name':original,'normalized_name':normalized,'display_name':display}
                elif plural=='teams':data={**common,'country_stable_key':row.get('country_stable_key'),'original_name':original,'normalized_name':normalized,'display_name':display}
                elif plural=='collections':data={**common,'team_stable_key':row['team_stable_key'],'country_stable_key':row.get('country_stable_key'),'original_name':original,'normalized_name':normalized,'display_name':inclusion_period(row.get('inclusion_month'),row.get('inclusion_year'),row.get('inclusion_batch')) or display,'collection_type':collection_type or 'unknown','inclusion_period':inclusion_period(row.get('inclusion_month'),row.get('inclusion_year'),row.get('inclusion_batch')),'inclusion_month':row.get('inclusion_month'),'inclusion_year':row.get('inclusion_year'),'inclusion_batch':row.get('inclusion_batch')}
                else:data={**common,'team_stable_key':row['team_stable_key'],'country_stable_key':row.get('country_stable_key'),'collection_stable_key':row.get('collection_stable_key'),'original_title':original,'normalized_title':normalized,'display_title':display,'source_page':row['source_page']}
                output[plural].append(data);counts[status]+=1
                if status!='unchanged' or collision:
                    event_rule='MR001' if status=='overridden' else ('SL002' if collision and not changes else rule_code)
                    message={'normalized':'Transformação determinística aplicada.','review_required':'Entidade preservada por falta de evidência segura.','overridden':'Revisão manual reconciliada aplicada.','unchanged':'Colisão de slug resolvida deterministicamente.'}[status]
                    events.append({'entity_type':entity_type,'entity_stable_key':row['stable_key'],'rule_code':event_rule,'previous_value':original,'resulting_value':display,'status':status,'source':source_name,'confidence':row.get('confidence','unknown'),'message':message,'created_at':timestamp})
        duration=int((time.perf_counter()-clock)*1000);quality=self.repository.latest_quality(catalog['id'])
        run={'catalog_build_id':catalog['id'],'quality_run_id':None if quality is None else quality['id'],'started_at':started,'completed_at':now(),'status':'completed','rules_version':RULES_VERSION,'countries_processed':len(output['countries']),'teams_processed':len(output['teams']),'collections_processed':len(output['collections']),'items_processed':len(output['items']),'normalized_count':counts['normalized'],'unchanged_count':counts['unchanged'],'review_required_count':counts['review_required'],'overridden_count':counts['overridden'],'duration_ms':duration,'error_message':None}
        rid=self.repository.persist(run,output,events);return {'id':rid,**run}
