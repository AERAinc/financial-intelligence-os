from pydantic import BaseModel, Field
from typing import List, Optional

class CompanyNodeCreate(BaseModel):
    name: str = Field(..., description="Name of the company or entity")
    industry: Optional[str] = Field(None, description="Industry sector")
    jurisdiction: Optional[str] = Field(None, description="Country or state of incorporation")

class RelationshipCreate(BaseModel):
    source_company: str = Field(..., description="Source company name")
    target_company: str = Field(..., description="Target company name")
    rel_type: str = Field(..., description="Relationship type: OWNS, BUYS_FROM, SELLS_TO, HAS_LOAN")
    value: Optional[float] = Field(None, description="Transaction value or ownership percentage")

class GraphQueryResponse(BaseModel):
    message: str
    nodes_affected: int