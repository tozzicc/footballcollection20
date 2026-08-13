export type ReviewSummary={total:number;pending:number;resolved:number;acknowledged:number;deferred:number;progressPercentage:number;byIssueType:Record<string,number>;byResolutionCode:Record<string,number>;lastReviewAt:string|null;qualityScore:number|null}
export type ReviewIssue={id:number;issue_type:string;severity:string;entity_type:string;relative_path:string;message:string;review_status:string;quality_status:string;pattern:string}
export type ReviewPage={items:ReviewIssue[];total:number;limit:number;offset:number}
export type ReviewCandidate={id:number;original_name:string;relative_path:string;country_name?:string;stable_key:string}
export type ReviewDetail={issue:ReviewIssue&Record<string,unknown>;entity:{type:string;id:number;name:string;stableKey:string};qualityAssessment:{status:string;pattern:string;evidence:string;reason:string};currentReview:Record<string,unknown>|null;history:Array<Record<string,unknown>>;allowedActions:string[];overlay:Record<string,unknown>}
export type ReviewProposal={resolutionCode:string;targetEntityId?:number;classification?:string;reason:string;notes?:string}
export type ReviewPreview={valid:boolean;currentValue:string;proposedValue:string;effects:string[];warnings:string[];message:string}
