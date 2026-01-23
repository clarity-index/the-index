"""
Governance API endpoints.

This module provides REST API endpoints for governance proposals and voting
with reputation-weighted quadratic scaling.
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, Path

from app.governance.models import (
    Proposal, ProposalCreate, ProposalStatus,
    Vote, VoteCreate, ProposalFinalize
)
from app.governance.service import governance_service


router = APIRouter(prefix="/governance", tags=["governance"])


@router.post("/proposal", response_model=Proposal, status_code=201)
def create_proposal(proposal: ProposalCreate):
    """
    Create a new governance proposal.
    
    Governance proposals allow the community to propose changes to:
    - Schema evolution
    - Ontology updates
    - Relation type changes
    - Rule modifications
    - Parameter updates
    
    Args:
        proposal: Proposal data including title, description, type, and proposed changes
        
    Returns:
        The created proposal with assigned ID
    """
    return governance_service.create_proposal(proposal)


@router.post("/proposal/{proposal_id}/activate", response_model=Proposal)
def activate_proposal(
    proposal_id: str = Path(..., description="Unique proposal identifier"),
    voting_duration_days: int = Query(7, ge=1, le=30, description="Voting period in days")
):
    """
    Activate a proposal for voting.
    
    This transitions a proposal from DRAFT to ACTIVE status and opens voting
    for the specified duration.
    
    Args:
        proposal_id: Unique proposal identifier
        voting_duration_days: Duration of voting period (1-30 days)
        
    Returns:
        The activated proposal
        
    Raises:
        HTTPException: 404 if proposal not found or not eligible for activation
    """
    proposal = governance_service.activate_proposal(proposal_id, voting_duration_days)
    if not proposal:
        raise HTTPException(
            status_code=404, 
            detail="Proposal not found or not eligible for activation"
        )
    return proposal


@router.get("/proposal/{proposal_id}", response_model=Proposal)
def get_proposal(proposal_id: str = Path(..., description="Unique proposal identifier")):
    """
    Retrieve a specific proposal by ID.
    
    Args:
        proposal_id: Unique proposal identifier
        
    Returns:
        The proposal if found
        
    Raises:
        HTTPException: 404 if proposal not found
    """
    proposal = governance_service.get_proposal(proposal_id)
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    return proposal


@router.get("/proposal", response_model=List[Proposal])
def list_proposals(
    status: Optional[ProposalStatus] = Query(None, description="Filter by status"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum results"),
    offset: int = Query(0, ge=0, description="Pagination offset")
):
    """
    List governance proposals with optional filtering.
    
    Args:
        status: Optional status filter
        limit: Maximum number of results (1-1000)
        offset: Pagination offset
        
    Returns:
        List of proposals matching the filters
    """
    return governance_service.list_proposals(
        status=status,
        limit=limit,
        offset=offset
    )


@router.post("/vote", response_model=Vote, status_code=201)
def cast_vote(vote: VoteCreate):
    """
    Cast a reputation-weighted vote on a proposal.
    
    This endpoint implements quadratic voting where the vote weight is calculated
    as the square root of the voter's reputation score. This reduces the influence
    of high-reputation voters and promotes more democratic decision-making.
    
    Vote weight formula:
    - With quadratic scaling: weight = sqrt(reputation)
    - Without quadratic scaling: weight = reputation
    
    Args:
        vote: Vote data including proposal_id, voter, choice, and reputation
        
    Returns:
        The created vote with calculated weighted value
        
    Raises:
        HTTPException: 400 if voting not allowed (proposal not active, already voted, etc.)
    """
    result = governance_service.cast_vote(vote)
    if not result:
        raise HTTPException(
            status_code=400,
            detail="Voting not allowed. Proposal may not be active, voting period ended, or already voted."
        )
    return result


@router.post("/finalize", response_model=Proposal)
def finalize_proposal(finalize: ProposalFinalize):
    """
    Finalize a proposal after voting ends.
    
    This endpoint calculates the final vote tally and determines whether
    the proposal passes or is rejected based on:
    - Vote ratios (yes vs no)
    - Quorum threshold
    
    A proposal passes if the yes/(yes+no) ratio exceeds the quorum threshold
    (default 50%).
    
    Args:
        finalize: Finalization data including proposal_id and finalizer identity
        
    Returns:
        The finalized proposal with updated status (PASSED or REJECTED)
        
    Raises:
        HTTPException: 400 if finalization not allowed (voting still open, etc.)
    """
    proposal = governance_service.finalize_proposal(finalize)
    if not proposal:
        raise HTTPException(
            status_code=400,
            detail="Finalization not allowed. Proposal may not be active or voting period not ended."
        )
    return proposal


@router.get("/proposal/{proposal_id}/votes", response_model=List[Vote])
def get_proposal_votes(proposal_id: str = Path(..., description="Unique proposal identifier")):
    """
    Get all votes for a specific proposal.
    
    Args:
        proposal_id: Unique proposal identifier
        
    Returns:
        List of votes for the proposal
    """
    return governance_service.get_votes_for_proposal(proposal_id)
