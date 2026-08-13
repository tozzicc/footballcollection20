export type QualityRun={id:number;catalogBuildRunId:number;finishedAt:string|null;durationMs:number;status:string;totalIssues:number;autoResolved:number;reviewRequired:number;qualityScore:number}
export type QualityStatus={catalogAvailable:boolean;qualityAnalysisAvailable:boolean;catalogBuildRunId:number|null;lastAnalysis:QualityRun|null;status:string}
export type QualitySummary={totalIssues:number;openIssues:number;autoResolvedIssues:number;reviewRequiredIssues:number;issuesByType:Record<string,number>;issuesBySeverity:Record<string,number>;countriesUnknown:number;teamsUnknown:number;collectionsUnknown:number;missingImages:number;qualityScore:number;analyzedAt:string;durationMs:number}
export type QualityIssue={id:number;issueType:string;severity:string;entityType:string;relativePath:string;message:string;resolutionStatus:string;pattern:string;evidence:string;reason:string;ruleCode:string|null;confidence:string|null}
export type Resolution={id:number;issueId:number;ruleCode:string;previousValue:string|null;resolvedValue:string|null;confidence:string;reason:string}
export type QualityGroup={key:string;issueType:string;pattern:string;count:number;auto_resolvable_count:number;review_required_count:number}
export type Page<T>={items:T[];total:number;limit:number;offset:number}
