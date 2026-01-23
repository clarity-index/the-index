"""
Claim API implementation aligned with the canonical claim JSON schema.

This module provides Pydantic models and API endpoints for claim submission
and retrieval, with centralized schema validation.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, model_validator


class Provenance(BaseModel):
    """Provenance and attestation information for a claim."""

    signature: Optional[str] = Field(None, description="Cryptographic signature of the claim")
    attestation_id: Optional[str] = Field(None, description="BitRep attestation identifier")


class Claim(BaseModel):
    """
    Canonical Claim model aligned with /schema/claim.schema.json.
    
    A structured scientific claim with explicit validation of protocol invariants:
    - MUST have either evidence_refs OR justification
    - MUST include subject, predicate, object for semantic structure
    - MUST be attributed to a BitRep identity (contributor_id)
    """

    id: str = Field(..., description="Unique identifier for the claim", pattern=r"^claim_[a-zA-Z0-9_-]+$")
    subject: str = Field(..., min_length=1, description="The subject of the claim")
    predicate: str = Field(..., min_length=1, description="The predicate of the claim")
    object: str = Field(..., min_length=1, description="The object of the claim")
    contributor_id: str = Field(..., min_length=1, description="BitRep identity of the contributor")
    timestamp: datetime = Field(..., description="ISO 8601 timestamp of claim creation")
    
    # Evidence or justification requirement (protocol invariant)
    evidence_refs: Optional[List[str]] = Field(default=None, description="Evidence identifiers")
    justification: Optional[str] = Field(default=None, min_length=1, description="Textual justification")
    
    # Additional fields
    canonical_text: Optional[str] = Field(None, min_length=1, description="Human-readable claim text")
    semantic_representation: Optional[Dict[str, Any]] = Field(
        None, description="Machine-readable semantic structure"
    )
    domains: Optional[List[str]] = Field(default=None, description="Domain tags")
    status: Optional[str] = Field(
        default="proposed",
        description="Current epistemic status",
        pattern=r"^(proposed|supported|contested|refuted|deprecated)$"
    )
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    provenance: Optional[Provenance] = Field(None, description="Provenance information")

    @model_validator(mode="after")
    def validate_evidence_or_justification(self):
        """Enforce protocol invariant: MUST have either evidence_refs OR justification."""
        has_evidence = self.evidence_refs is not None and len(self.evidence_refs) > 0
        has_justification = self.justification is not None and len(self.justification.strip()) > 0
        
        if not has_evidence and not has_justification:
            raise ValueError(
                "Protocol invariant violation: Claim MUST have either evidence_refs or justification"
            )
        
        return self

    class Config:
        json_schema_extra = {
            "example": {
                "id": "claim_001",
                "subject": "quantum_entanglement",
                "predicate": "persists_over",
                "object": "macroscopic_distances",
                "contributor_id": "bitrep_id_123",
                "timestamp": "2024-01-01T00:00:00Z",
                "evidence_refs": ["evidence_001", "evidence_002"],
                "canonical_text": "Quantum entanglement persists over macroscopic distances",
                "semantic_representation": {
                    "subject": "quantum_entanglement",
                    "predicate": "persists_over",
                    "object": "macroscopic_distances"
                },
                "domains": ["quantum_physics", "experimental_physics"],
                "status": "proposed"
            }
        }


class ClaimCreate(BaseModel):
    """Model for creating a new claim via API."""

    subject: str = Field(..., min_length=1)
    predicate: str = Field(..., min_length=1)
    object: str = Field(..., min_length=1)
    contributor_id: str = Field(..., min_length=1)
    evidence_refs: Optional[List[str]] = None
    justification: Optional[str] = Field(default=None, min_length=1)
    canonical_text: Optional[str] = Field(None, min_length=1)
    semantic_representation: Optional[Dict[str, Any]] = None
    domains: Optional[List[str]] = None

    @model_validator(mode="after")
    def validate_evidence_or_justification(self):
        """Enforce protocol invariant: MUST have either evidence_refs OR justification."""
        has_evidence = self.evidence_refs is not None and len(self.evidence_refs) > 0
        has_justification = self.justification is not None and len(self.justification.strip()) > 0
        
        if not has_evidence and not has_justification:
            raise ValueError(
                "Protocol invariant violation: Claim MUST have either evidence_refs or justification"
            )
        
        return self


class ClaimResponse(BaseModel):
    """Response model for claim retrieval."""

    claim: Claim
    links_count: Optional[int] = Field(None, description="Number of links to this claim")
    epistemic_status: Optional[Dict[str, Any]] = Field(
        None, description="Computed epistemic status"
    )
