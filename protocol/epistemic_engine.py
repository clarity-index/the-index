"""
Deterministic Epistemic Engine

This module provides deterministic computation functions for epistemic status
and weighted support calculation. No heuristics or machine learning allowed.

Functions:
- compute_status(claim_id): Compute the epistemic status of a claim
- compute_weighted_support(claim_id): Calculate weighted support score
"""

from typing import Dict, List, Optional, Tuple


def compute_status(claim_id: str, links: Optional[List[Dict]] = None) -> str:
    """
    Compute the epistemic status of a claim based on weighted evidence.
    
    This is a deterministic computation that MUST produce identical results
    given identical inputs. No machine learning or heuristics are allowed.
    
    Args:
        claim_id: The claim identifier
        links: Optional list of links to/from the claim. If None, will be fetched.
        
    Returns:
        Status string: one of 'proposed', 'supported', 'contested', 'refuted', 'deprecated'
        
    Algorithm:
        1. Calculate supporting_weight from all supporting links
        2. Calculate contradicting_weight from all contradicting links
        3. Apply deterministic thresholds to determine status
        
    Thresholds (as defined in protocol spec):
        - proposed: insufficient evidence (default)
        - supported: supporting_weight > 3.0 AND supporting/contradicting ratio > 2.0
        - contested: both weights > 1.0 AND difference < 1.0
        - refuted: contradicting_weight > 3.0 AND contradicting/supporting ratio > 2.0
        - deprecated: only via governance (not computed)
    """
    # If links not provided, this is a stub that returns proposed
    # In a real implementation, this would fetch links from storage
    if links is None:
        # Stub: Return default status
        return "proposed"
    
    # Calculate weighted support and contradiction
    supporting_weight = 0.0
    contradicting_weight = 0.0
    
    for link in links:
        # Only consider links targeting this claim
        if link.get("target_id") != claim_id and link.get("source_id") != claim_id:
            continue
        
        relation_type = link.get("relation_type")
        weight = link.get("weight", 1.0)
        
        # Aggregate supporting evidence
        if relation_type in ["supports", "weakly_supports"]:
            supporting_weight += weight
        
        # Aggregate contradicting evidence
        elif relation_type in ["contradicts", "conflicts_with"]:
            contradicting_weight += weight
    
    # Apply deterministic thresholds
    threshold_support = 3.0
    threshold_refute = 3.0
    threshold_min = 1.0
    threshold_contested = 1.0
    ratio_support = 2.0
    ratio_refute = 2.0
    
    # Check for supported status
    if supporting_weight > threshold_support:
        if contradicting_weight == 0 or (supporting_weight / (contradicting_weight + 1.0)) > ratio_support:
            return "supported"
    
    # Check for refuted status
    if contradicting_weight > threshold_refute:
        if supporting_weight == 0 or (contradicting_weight / (supporting_weight + 1.0)) > ratio_refute:
            return "refuted"
    
    # Check for contested status
    if (supporting_weight > threshold_min and 
        contradicting_weight > threshold_min and
        abs(supporting_weight - contradicting_weight) < threshold_contested):
        return "contested"
    
    # Default to proposed
    return "proposed"


def compute_weighted_support(
    claim_id: str,
    links: Optional[List[Dict]] = None,
    reputation_scores: Optional[Dict[str, float]] = None
) -> Tuple[float, float]:
    """
    Calculate weighted support and contradiction for a claim.
    
    This is a deterministic computation that applies reputation weighting
    to link strengths.
    
    Args:
        claim_id: The claim identifier
        links: Optional list of links to/from the claim
        reputation_scores: Optional dict mapping attestor_id to reputation score
        
    Returns:
        Tuple of (supporting_weight, contradicting_weight)
        
    Algorithm:
        1. For each link, get base weight from link.weight
        2. Multiply by attestor reputation score (if available)
        3. Sum all supporting weights
        4. Sum all contradicting weights
        5. Return both values
    """
    # If links not provided, this is a stub that returns zeros
    if links is None:
        return (0.0, 0.0)
    
    supporting_weight = 0.0
    contradicting_weight = 0.0
    
    for link in links:
        # Only consider links targeting this claim
        if link.get("target_id") != claim_id and link.get("source_id") != claim_id:
            continue
        
        relation_type = link.get("relation_type")
        base_weight = link.get("weight", 1.0)
        attestor_id = link.get("attestor_id")
        
        # Apply reputation weighting if available
        reputation_multiplier = 1.0
        if reputation_scores and attestor_id in reputation_scores:
            # Use square root of reputation for diminishing returns
            # This prevents single high-reputation actors from dominating
            reputation_multiplier = reputation_scores[attestor_id] ** 0.5
        
        adjusted_weight = base_weight * reputation_multiplier
        
        # Aggregate by relation type
        if relation_type in ["supports", "weakly_supports"]:
            supporting_weight += adjusted_weight
        elif relation_type in ["contradicts", "conflicts_with"]:
            contradicting_weight += adjusted_weight
    
    return (supporting_weight, contradicting_weight)


def compute_independence_score(claim_id: str, links: Optional[List[Dict]] = None) -> float:
    """
    Compute independence score based on diversity of evidence sources.
    
    This measures how many different contributors and evidence sources
    support or contradict a claim. Higher diversity = higher independence.
    
    Args:
        claim_id: The claim identifier
        links: Optional list of links
        
    Returns:
        Independence score between 0.0 and 1.0
        
    Algorithm:
        1. Count unique attestors
        2. Count unique evidence sources
        3. Calculate diversity metric
        4. Normalize to 0.0-1.0 range
    """
    if links is None:
        return 0.0
    
    # Count unique attestors
    attestors = set()
    evidence_sources = set()
    
    for link in links:
        if link.get("target_id") != claim_id and link.get("source_id") != claim_id:
            continue
        
        attestor_id = link.get("attestor_id")
        if attestor_id:
            attestors.add(attestor_id)
        
        # Track evidence diversity
        target_id = link.get("target_id")
        if target_id and target_id.startswith("evidence_"):
            evidence_sources.add(target_id)
    
    # Calculate independence score
    # More unique sources = higher score
    # Use logarithmic scaling for diminishing returns
    import math
    unique_attestors = len(attestors)
    unique_sources = len(evidence_sources)
    
    # Combine attestor and source diversity
    diversity_score = math.log1p(unique_attestors) + math.log1p(unique_sources)
    
    # Normalize to 0-1 range (assuming max ~10 unique contributors is "high")
    max_expected_diversity = math.log1p(10) * 2
    normalized_score = min(1.0, diversity_score / max_expected_diversity)
    
    return normalized_score


def compute_robustness_score(claim_id: str, evidence: Optional[List[Dict]] = None) -> float:
    """
    Compute robustness score based on evidence quality and replication.
    
    This measures the quality of evidence supporting the claim including
    replication studies and methodological rigor.
    
    Args:
        claim_id: The claim identifier
        evidence: Optional list of evidence objects
        
    Returns:
        Robustness score between 0.0 and 1.0
        
    Algorithm:
        1. Aggregate quality scores from evidence
        2. Check for replication studies
        3. Assess methodological diversity
        4. Calculate composite robustness score
    """
    if evidence is None or len(evidence) == 0:
        return 0.0
    
    total_quality = 0.0
    has_replication = False
    evidence_types = set()
    
    for ev in evidence:
        # Aggregate quality scores
        quality_score = ev.get("quality_score", 0.5)
        total_quality += quality_score
        
        # Check for replication
        metadata = ev.get("metadata", {})
        replication_history = metadata.get("replication_history", [])
        if len(replication_history) > 0:
            has_replication = True
        
        # Track evidence type diversity
        ev_type = ev.get("type")
        if ev_type:
            evidence_types.add(ev_type)
    
    # Calculate average quality
    avg_quality = total_quality / len(evidence)
    
    # Bonus for replication
    replication_bonus = 0.2 if has_replication else 0.0
    
    # Bonus for diverse evidence types
    diversity_bonus = min(0.2, len(evidence_types) * 0.05)
    
    # Combine scores (max 1.0)
    robustness = min(1.0, avg_quality + replication_bonus + diversity_bonus)
    
    return robustness


# Stub implementations for testing and future development

def validate_status_computation(claim_id: str) -> bool:
    """
    Validate that status computation is deterministic and reproducible.
    
    This is a testing/validation function to ensure the epistemic engine
    produces consistent results.
    
    Args:
        claim_id: The claim identifier
        
    Returns:
        True if computation is valid and deterministic
    """
    # Stub: Always returns True
    # In production, this would run the computation multiple times
    # and verify identical results
    return True


def get_status_thresholds() -> Dict[str, float]:
    """
    Get the current status computation thresholds.
    
    Returns:
        Dictionary of threshold values used in status computation
    """
    return {
        "threshold_support": 3.0,
        "threshold_refute": 3.0,
        "threshold_min": 1.0,
        "threshold_contested": 1.0,
        "ratio_support": 2.0,
        "ratio_refute": 2.0,
    }
