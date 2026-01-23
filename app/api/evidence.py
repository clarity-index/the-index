"""
Evidence API endpoints.

This module provides REST API endpoints for managing evidence and links.
"""

from typing import List

from fastapi import APIRouter, HTTPException, Path, Query

from app.core.models import EpistemicStatus, Evidence, EvidenceCreate, Link, LinkCreate
from app.evidence.service import evidence_service

router = APIRouter(prefix="/evidence", tags=["evidence"])


@router.post("/", response_model=Evidence, status_code=201)
def submit_evidence(evidence: EvidenceCreate):
    """
    Submit new evidence to the system.

    Args:
        evidence: Evidence data including type, source identifier, and metadata

    Returns:
        The created evidence with assigned ID and quality score
    """
    return evidence_service.submit_evidence(evidence)


@router.get("/{evidence_id}", response_model=Evidence)
def get_evidence(evidence_id: str = Path(..., description="Unique evidence identifier")):
    """
    Retrieve specific evidence by ID.

    Args:
        evidence_id: Unique evidence identifier

    Returns:
        The evidence if found

    Raises:
        HTTPException: 404 if evidence not found
    """
    evidence = evidence_service.get_evidence(evidence_id)
    if not evidence:
        raise HTTPException(status_code=404, detail="Evidence not found")
    return evidence


@router.get("/", response_model=List[Evidence])
def list_evidence(
    limit: int = Query(100, ge=1, le=1000, description="Maximum results"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
):
    """
    List all evidence with pagination.

    Args:
        limit: Maximum number of results (1-1000)
        offset: Pagination offset

    Returns:
        List of evidence items
    """
    return evidence_service.list_evidence(limit=limit, offset=offset)


@router.post("/links", response_model=Link, status_code=201)
def create_link(link: LinkCreate):
    """
    Create a link between a claim and evidence (or another claim).

    This endpoint allows linking evidence to claims with a specific relation type
    (supports, contradicts, etc.) and strength.

    Args:
        link: Link data including claim_id, evidence_id/claim_id_2, relation type, and strength

    Returns:
        The created link with assigned ID
    """
    return evidence_service.create_link(link)


@router.get("/links/claim/{claim_id}", response_model=List[Link])
def get_links_for_claim(claim_id: str = Path(..., description="Unique claim identifier")):
    """
    Get all links associated with a claim.

    Args:
        claim_id: Unique claim identifier

    Returns:
        List of links for the claim
    """
    return evidence_service.get_links_for_claim(claim_id)


@router.get("/links/evidence/{evidence_id}", response_model=List[Link])
def get_links_for_evidence(evidence_id: str = Path(..., description="Unique evidence identifier")):
    """
    Get all links associated with evidence.

    Args:
        evidence_id: Unique evidence identifier

    Returns:
        List of links for the evidence
    """
    return evidence_service.get_links_for_evidence(evidence_id)


@router.get("/epistemic-status/{claim_id}", response_model=EpistemicStatus)
def get_epistemic_status(claim_id: str = Path(..., description="Unique claim identifier")):
    """
    Compute and retrieve the epistemic status for a claim.

    This endpoint calculates the claim's status based on:
    - Supporting and contradicting evidence weights
    - Independence score (diversity of evidence sources)
    - Robustness score (replication and quality)

    Args:
        claim_id: Unique claim identifier

    Returns:
        Computed epistemic status for the claim
    """
    return evidence_service.compute_epistemic_status(claim_id)
