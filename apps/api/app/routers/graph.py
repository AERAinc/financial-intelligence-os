from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

# Gracefully handle engine imports with descriptive errors if modules are missing
try:
    from engines.graph.neo4j.schemas import (
        CompanyNodeCreate,
        RelationshipCreate,
        GraphQueryResponse,
    )
    from engines.graph.neo4j.analytics import kg_service
except ImportError as err:
    raise ImportError(
        f"Critical Dependency Error: Failed to load graph engine modules. "
        f"Ensure 'engines.graph' is accessible via PYTHONPATH. Details: {err}"
    ) from err

logger = logging.getLogger("financial_intelligence_os.routers.graph")

router = APIRouter(
    prefix="/api/v1/graph",
    tags=["Knowledge Graph Intelligence Engine"],
)


class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Human-readable error description")
    error_code: Optional[str] = Field(None, description="Internal error classification code")


@router.post(
    "/company",
    response_model=GraphQueryResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid payload parameters"},
        500: {"model": ErrorResponse, "description": "Database or internal engine error"},
    },
)
def add_company_node(data: CompanyNodeCreate) -> GraphQueryResponse:
    """Create or update a corporate entity node within the knowledge graph."""
    try:
        logger.debug(f"Processing company node creation request for: {getattr(data, 'name', 'Unknown')}")
        record: Dict[str, Any] = kg_service.create_company(data)
        
        company_name = record.get("name", "Unknown Entity")
        return GraphQueryResponse(
            message=f"Successfully created/updated company node: {company_name}",
            nodes_affected=1,
        )
    except ValueError as val_err:
        logger.warning(f"Validation error while creating company node: {val_err}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(val_err),
        ) from val_err
    except Exception as exc:
        logger.exception("Unexpected error occurred while communicating with the Neo4j graph engine.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An internal error occurred while processing the graph operation: {exc}",
        ) from exc


@router.post(
    "/relationship",
    response_model=GraphQueryResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid relationship parameters or missing nodes"},
        500: {"model": ErrorResponse, "description": "Database or internal engine error"},
    },
)
def add_relationship(data: RelationshipCreate) -> GraphQueryResponse:
    """Establish a directed relationship edge between two corporate entity nodes."""
    try:
        logger.debug(
            f"Establishing relationship between "
            f"{getattr(data, 'source_company', 'Source')} and "
            f"{getattr(data, 'target_company', 'Target')}"
        )
        record: Dict[str, Any] = kg_service.create_relationship(data)
        
        rel_type = record.get("rel_type", "CONNECTED")
        source = getattr(data, "source_company", "Source")
        target = getattr(data, "target_company", "Target")

        return GraphQueryResponse(
            message=f"Successfully created relationship [{rel_type}] between {source} and {target}",
            nodes_affected=1,
        )
    except ValueError as val_err:
        logger.warning(f"Validation error while creating relationship: {val_err}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(val_err),
        ) from val_err
    except Exception as exc:
        logger.exception("Unexpected error occurred during relationship creation in the graph engine.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An internal error occurred while processing the relationship: {exc}",
        ) from exc