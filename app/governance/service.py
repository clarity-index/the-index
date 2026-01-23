"""
Governance service layer.

This module provides business logic for governance proposals, voting,
and finalization with reputation-weighted quadratic scaling.
"""

import math
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from app.core.config import settings
from app.governance.models import (
    Proposal,
    ProposalCreate,
    ProposalFinalize,
    ProposalStatus,
    Vote,
    VoteChoice,
    VoteCreate,
)


class GovernanceService:
    """
    Service for managing governance proposals and voting.

    This service implements reputation-weighted voting with quadratic scaling
    for decentralized governance of The Index.
    """

    def __init__(self):
        """Initialize the governance service with in-memory storage."""
        # In-memory storage (replace with database in production)
        self._proposals: Dict[str, Proposal] = {}
        self._votes: Dict[str, Vote] = {}
        # Track votes by proposal and voter to prevent double voting
        self._voter_proposals: Dict[str, set] = {}

    def create_proposal(self, proposal_data: ProposalCreate) -> Proposal:
        """
        Create a new governance proposal.

        Args:
            proposal_data: Proposal data

        Returns:
            The created proposal
        """
        proposal_id = f"proposal_{uuid.uuid4().hex[:12]}"

        proposal = Proposal(
            id=proposal_id,
            title=proposal_data.title,
            description=proposal_data.description,
            proposal_type=proposal_data.proposal_type,
            proposed_changes=proposal_data.proposed_changes,
            proposer=proposal_data.proposer,
            status=ProposalStatus.DRAFT,
            created_at=datetime.utcnow(),
        )

        self._proposals[proposal_id] = proposal
        return proposal

    def activate_proposal(
        self, proposal_id: str, voting_duration_days: int = 7
    ) -> Optional[Proposal]:
        """
        Activate a proposal for voting.

        Args:
            proposal_id: The proposal identifier
            voting_duration_days: Duration of voting period in days

        Returns:
            The activated proposal if found and eligible, None otherwise
        """
        proposal = self._proposals.get(proposal_id)
        if not proposal or proposal.status != ProposalStatus.DRAFT:
            return None

        now = datetime.utcnow()
        proposal.status = ProposalStatus.ACTIVE
        proposal.voting_starts_at = now
        proposal.voting_ends_at = now + timedelta(days=voting_duration_days)

        return proposal

    def get_proposal(self, proposal_id: str) -> Optional[Proposal]:
        """
        Retrieve a proposal by ID.

        Args:
            proposal_id: The proposal identifier

        Returns:
            The proposal if found, None otherwise
        """
        return self._proposals.get(proposal_id)

    def list_proposals(
        self, status: Optional[ProposalStatus] = None, limit: int = 100, offset: int = 0
    ) -> List[Proposal]:
        """
        List proposals with optional filtering.

        Args:
            status: Filter by proposal status
            limit: Maximum number of proposals to return
            offset: Offset for pagination

        Returns:
            List of proposals
        """
        proposals = list(self._proposals.values())

        if status:
            proposals = [p for p in proposals if p.status == status]

        # Sort by creation date, newest first
        proposals.sort(key=lambda p: p.created_at, reverse=True)

        return proposals[offset : offset + limit]

    def cast_vote(self, vote_data: VoteCreate) -> Optional[Vote]:
        """
        Cast a vote on a proposal with reputation-weighted quadratic scaling.

        Args:
            vote_data: Vote data including proposal_id, voter, choice, and reputation

        Returns:
            The created vote if successful, None if voting not allowed
        """
        proposal = self._proposals.get(vote_data.proposal_id)
        if not proposal:
            return None

        # Check if proposal is active and voting is open
        if proposal.status != ProposalStatus.ACTIVE:
            return None

        now = datetime.utcnow()
        if proposal.voting_starts_at and now < proposal.voting_starts_at:
            return None
        if proposal.voting_ends_at and now > proposal.voting_ends_at:
            return None

        # Check if voter has already voted on this proposal
        voter_key = f"{vote_data.voter}_{vote_data.proposal_id}"
        if voter_key in self._voter_proposals:
            return None  # Already voted

        # Calculate weighted vote with quadratic scaling
        weighted_vote = self._calculate_weighted_vote(
            vote_data.reputation, settings.governance_quadratic_scaling
        )

        vote_id = f"vote_{uuid.uuid4().hex[:12]}"
        vote = Vote(
            id=vote_id,
            proposal_id=vote_data.proposal_id,
            voter=vote_data.voter,
            choice=vote_data.choice,
            reputation=vote_data.reputation,
            weighted_vote=weighted_vote,
            timestamp=datetime.utcnow(),
        )

        self._votes[vote_id] = vote
        self._voter_proposals[voter_key] = True  # Mark as voted

        # Update proposal vote tallies
        if vote_data.choice == VoteChoice.YES:
            proposal.yes_votes += weighted_vote
        elif vote_data.choice == VoteChoice.NO:
            proposal.no_votes += weighted_vote
        elif vote_data.choice == VoteChoice.ABSTAIN:
            proposal.abstain_votes += weighted_vote

        return vote

    def finalize_proposal(self, finalize_data: ProposalFinalize) -> Optional[Proposal]:
        """
        Finalize a proposal after voting ends.

        Args:
            finalize_data: Finalization data

        Returns:
            The finalized proposal if successful, None otherwise
        """
        proposal = self._proposals.get(finalize_data.proposal_id)
        if not proposal:
            return None

        # Check if proposal can be finalized
        if proposal.status != ProposalStatus.ACTIVE:
            return None

        now = datetime.utcnow()
        if proposal.voting_ends_at and now < proposal.voting_ends_at:
            return None

        # Calculate if proposal passes
        total_votes = proposal.yes_votes + proposal.no_votes + proposal.abstain_votes

        # Require minimum participation (quorum)
        if total_votes == 0:
            proposal.status = ProposalStatus.REJECTED
        else:
            yes_ratio = (
                proposal.yes_votes / (proposal.yes_votes + proposal.no_votes)
                if (proposal.yes_votes + proposal.no_votes) > 0
                else 0
            )

            # Pass if yes votes exceed threshold
            if yes_ratio >= settings.governance_quorum_threshold:
                proposal.status = ProposalStatus.PASSED
            else:
                proposal.status = ProposalStatus.REJECTED

        proposal.executed_at = now

        return proposal

    def get_votes_for_proposal(self, proposal_id: str) -> List[Vote]:
        """
        Get all votes for a proposal.

        Args:
            proposal_id: The proposal identifier

        Returns:
            List of votes for the proposal
        """
        return [vote for vote in self._votes.values() if vote.proposal_id == proposal_id]

    def _calculate_weighted_vote(self, reputation: float, use_quadratic: bool) -> float:
        """
        Calculate weighted vote from reputation score.

        Args:
            reputation: Raw reputation score
            use_quadratic: Whether to apply quadratic scaling

        Returns:
            Weighted vote value
        """
        if use_quadratic:
            # Quadratic scaling: sqrt of reputation
            # This reduces the influence of high-reputation voters
            return math.sqrt(reputation)
        else:
            # Linear scaling
            return reputation


# Global service instance
governance_service = GovernanceService()
