from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class CompanyNodeCreate(BaseModel):
    name: str = Field(..., description="Name of the company node")
    ticker: Optional[str] = Field(None, description="Stock ticker symbol")
    sector: Optional[str] = Field(None, description="Industry sector")
    properties: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional custom metadata properties")

class RelationshipCreate(BaseModel):
    source_company: str = Field(..., description="Name or identifier of the source company")
    target_company: str = Field(..., description="Name or identifier of the target company")
    rel_type: str = Field("OWNS", description="Neo4j relationship type (e.g., OWNS, SUPPLIES, INVESTS)")
    properties: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Relationship metadata properties")

class GraphQueryResponse(BaseModel):
    message: str = Field(..., description="Execution status message")
    nodes_affected: int = Field(1, description="Number of nodes or edges affected")