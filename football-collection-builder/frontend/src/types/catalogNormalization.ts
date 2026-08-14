export type NormalizationStatus='normalized'|'unchanged'|'review_required'|'overridden'
export type NormalizationRun={id:number;completedAt:string;durationMs:number;rulesVersion:string;countriesProcessed:number;teamsProcessed:number;collectionsProcessed:number;itemsProcessed:number;normalizedCount:number;unchangedCount:number;reviewRequiredCount:number;overriddenCount:number}
export type NormalizationStatusResponse={catalogAvailable:boolean;reviewAvailable:boolean;normalizationAvailable:boolean;lastRun:NormalizationRun|null;rulesVersion:string}
export type NormalizationSummary={countries:number;teams:number;collections:number;items:number;normalized:number;unchanged:number;reviewRequired:number;overridden:number;events:number;durationMs:number;rulesVersion:string;lastRunAt:string}
export type NormalizedEntity=Record<string,unknown>&{id:number;stableKey:string;sourceEntityId:number;originalPath:string;slug:string;normalizationStatus:NormalizationStatus;normalizationSource:string;confidence:string;ruleCodes:string[]}
export type NormalizationPage={items:NormalizedEntity[];total:number;limit:number;offset:number}
