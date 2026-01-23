"""
Integration tests for the Governance API.
"""


def test_create_proposal_endpoint(client, sample_proposal_data):
    """Test POST /api/v1/governance/proposal endpoint."""
    response = client.post("/api/v1/governance/proposal", json=sample_proposal_data)

    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["title"] == sample_proposal_data["title"]
    assert data["status"] == "draft"


def test_activate_proposal_endpoint(client, sample_proposal_data):
    """Test POST /api/v1/governance/proposal/{proposal_id}/activate endpoint."""
    # Create a proposal
    create_response = client.post("/api/v1/governance/proposal", json=sample_proposal_data)
    proposal_id = create_response.json()["id"]

    # Activate the proposal
    response = client.post(
        f"/api/v1/governance/proposal/{proposal_id}/activate", params={"voting_duration_days": 7}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "active"
    assert data["voting_starts_at"] is not None
    assert data["voting_ends_at"] is not None


def test_get_proposal_endpoint(client, sample_proposal_data):
    """Test GET /api/v1/governance/proposal/{proposal_id} endpoint."""
    # Create a proposal
    create_response = client.post("/api/v1/governance/proposal", json=sample_proposal_data)
    proposal_id = create_response.json()["id"]

    # Retrieve the proposal
    response = client.get(f"/api/v1/governance/proposal/{proposal_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == proposal_id


def test_list_proposals_endpoint(client, sample_proposal_data):
    """Test GET /api/v1/governance/proposal endpoint."""
    # Create multiple proposals
    for i in range(3):
        data = sample_proposal_data.copy()
        data["title"] = f"Test proposal {i}"
        client.post("/api/v1/governance/proposal", json=data)

    response = client.get("/api/v1/governance/proposal")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


def test_cast_vote_endpoint(client, sample_proposal_data):
    """Test POST /api/v1/governance/vote endpoint."""
    # Create and activate a proposal
    create_response = client.post("/api/v1/governance/proposal", json=sample_proposal_data)
    proposal_id = create_response.json()["id"]

    client.post(
        f"/api/v1/governance/proposal/{proposal_id}/activate", params={"voting_duration_days": 7}
    )

    # Cast a vote
    vote_data = {
        "proposal_id": proposal_id,
        "voter": "test_voter_1",
        "choice": "yes",
        "reputation": 100.0,
    }
    response = client.post("/api/v1/governance/vote", json=vote_data)

    assert response.status_code == 201
    data = response.json()
    assert data["proposal_id"] == proposal_id
    assert data["choice"] == "yes"
    assert data["weighted_vote"] == 10.0  # sqrt(100)


def test_cast_vote_on_inactive_proposal(client, sample_proposal_data):
    """Test voting on inactive proposal returns error."""
    # Create a proposal but don't activate it
    create_response = client.post("/api/v1/governance/proposal", json=sample_proposal_data)
    proposal_id = create_response.json()["id"]

    # Try to vote
    vote_data = {
        "proposal_id": proposal_id,
        "voter": "test_voter_1",
        "choice": "yes",
        "reputation": 100.0,
    }
    response = client.post("/api/v1/governance/vote", json=vote_data)

    assert response.status_code == 400


def test_finalize_proposal_endpoint(client, sample_proposal_data):
    """Test POST /api/v1/governance/finalize endpoint."""
    # Create and activate a proposal
    create_response = client.post("/api/v1/governance/proposal", json=sample_proposal_data)
    proposal_id = create_response.json()["id"]

    activate_response = client.post(
        f"/api/v1/governance/proposal/{proposal_id}/activate", params={"voting_duration_days": 1}
    )
    assert activate_response.status_code == 200

    # Cast votes
    for i in range(3):
        vote_data = {
            "proposal_id": proposal_id,
            "voter": f"test_voter_{i}",
            "choice": "yes",
            "reputation": 100.0,
        }
        client.post("/api/v1/governance/vote", json=vote_data)

    # We need to manually adjust the voting end time for testing
    # In a real scenario, we'd wait or use time mocking
    # For now, we'll test that finalization before end time fails
    finalize_data = {"proposal_id": proposal_id, "finalizer": "test_finalizer"}
    response = client.post("/api/v1/governance/finalize", json=finalize_data)

    # Should fail because voting hasn't ended
    assert response.status_code == 400


def test_get_proposal_votes_endpoint(client, sample_proposal_data):
    """Test GET /api/v1/governance/proposal/{proposal_id}/votes endpoint."""
    # Create and activate a proposal
    create_response = client.post("/api/v1/governance/proposal", json=sample_proposal_data)
    proposal_id = create_response.json()["id"]

    client.post(
        f"/api/v1/governance/proposal/{proposal_id}/activate", params={"voting_duration_days": 7}
    )

    # Cast multiple votes
    for i in range(3):
        vote_data = {
            "proposal_id": proposal_id,
            "voter": f"test_voter_{i}",
            "choice": "yes",
            "reputation": 100.0,
        }
        client.post("/api/v1/governance/vote", json=vote_data)

    # Get votes
    response = client.get(f"/api/v1/governance/proposal/{proposal_id}/votes")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


def test_health_check_endpoint(client):
    """Test GET /health endpoint."""
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_root_endpoint(client):
    """Test GET / endpoint."""
    response = client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
