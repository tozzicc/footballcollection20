from pydantic import BaseModel,field_validator
class ReviewResolveRequest(BaseModel):
 resolutionCode:str;targetEntityId:int|None=None;classification:str|None=None;reason:str;notes:str|None=None
 @field_validator('reason')
 @classmethod
 def reason_required(cls,v):
  if not v.strip():raise ValueError('Motivo obrigatório.')
  return v.strip()
class ReviewReasonRequest(BaseModel):
 reason:str
 @field_validator('reason')
 @classmethod
 def reason_required(cls,v):
  if not v.strip():raise ValueError('Motivo obrigatório.')
  return v.strip()
