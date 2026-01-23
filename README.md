# The Index

**A Protocol for Verifiable Scientific Knowledge**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Overview

The Index is a protocol and reference implementation for representing, linking, and evaluating verifiable scientific knowledge. Built on the BitRep identity substrate, The Index provides a structured, reputation-weighted system for scientific claims, evidence, and epistemic relationships in a transparent and decentralized manner.

### Key Features

- **Structured Claims**: Atomic scientific statements with semantic representation (subject-predicate-object)
- **Evidence Linking**: Connect claims to empirical or theoretical support with explicit relation types
- **Epistemic Status**: Computed assessment of claim standing based on weighted evidence
- **BitRep Integration**: Cryptographic identity, attestation, and reputation weighting
- **Governance**: Community-driven protocol evolution through decentralized mechanisms
- **Protocol Invariants**: Enforced requirements ensuring data integrity and verifiability

---

## Repository Structure

```
the-index/
├── app/                      # FastAPI application implementation
│   ├── api/                  # API endpoints (claims, evidence, governance)
│   ├── claims/               # Claims service layer
│   ├── evidence/             # Evidence service layer
│   ├── governance/           # Governance service layer
│   └── core/                 # Core models and configuration
├── schema/                   # JSON schemas for data models
│   └── claim.schema.json     # Canonical claim schema
├── ontology/                 # Ontology definitions (planned)
├── examples/                 # Reference examples (planned)
├── docs/                     # Documentation
│   ├── API_DOCUMENTATION.md  # API reference
│   ├── DEVELOPER_SETUP.md    # Developer guide
│   └── SECURITY.md           # Security considerations
├── tests/                    # Test suite
├── claim_api.py              # Pydantic models aligned with schema
├── claim_layer.py            # Claim layer with protocol invariants
├── INDEX_ARCHITECTURE.md     # Normative protocol specification
├── CONTRIBUTING.md           # Contribution guidelines
└── README.md                 # This file
```

---

## Purpose

The Index aims to create a global, machine-readable, human-verifiable map of scientific knowledge that evolves through:

- **Evidence-based evaluation** rather than authority or consensus
- **Replication and verification** rather than citation counts
- **Community governance** rather than central control
- **Transparent computation** rather than opaque algorithms

---

## Getting Started

### Prerequisites

- Python 3.9 or higher
- pip or uv for package management

### Installation

1. Clone the repository:
```bash
git clone https://github.com/clarity-index/the-index.git
cd the-index
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development
```

### Running the API Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

API documentation is available at `http://localhost:8000/docs`

### Running Tests

```bash
pytest
```

With coverage:
```bash
pytest --cov=app --cov-report=html
```

---

## Core Concepts

### Claims

Claims are atomic scientific statements with:
- **Semantic structure**: Subject-predicate-object representation
- **Attribution**: Linked to BitRep identity
- **Evidence requirement**: Must have either evidence references OR justification
- **Status**: Computed from weighted evidence (proposed, supported, contested, refuted, deprecated)

### Evidence

Evidence represents empirical or theoretical support:
- **Types**: experiment, observation, dataset, simulation, theorem, meta-analysis
- **Metadata**: methodology, sample size, uncertainty, instrumentation, replication
- **Linking**: Must be linked to at least one claim

### Links

Links define relationships between claims and evidence:
- **Relation types**: supports, contradicts, weakly_supports, refines, generalizes, depends_on, conflicts_with
- **Weighting**: Strength and reputation-based weighting
- **Attestation**: All links are BitRep attestations

### Epistemic Status

Computed deterministically from:
- Supporting weight (sum of weighted supporting links)
- Contradicting weight (sum of weighted contradicting links)
- Independence (diversity of sources and contributors)
- Robustness (replication and methodological quality)

---

## Protocol Invariants

The Index enforces key invariants to maintain integrity:

1. **Evidence or Justification**: Claims MUST have either `evidence_refs` OR `justification`
2. **Attribution**: All contributions MUST be attributed to a BitRep identity
3. **Semantic Structure**: Claims MUST have subject, predicate, and object
4. **Link Targets**: Links MUST connect to either evidence OR another claim, never both
5. **Immutability**: Core objects are immutable (except status updates and metadata corrections)

See [INDEX_ARCHITECTURE.md](INDEX_ARCHITECTURE.md) for the complete normative specification.

---

## API Overview

### Claim Endpoints

- `POST /claims` - Create a new claim
- `GET /claims/{id}` - Retrieve a specific claim
- `GET /claims` - List claims (with filtering and pagination)
- `GET /claims/search` - Search claims by text
- `GET /claims/{id}/status` - Get epistemic status

### Evidence Endpoints

- `POST /evidence` - Submit new evidence
- `GET /evidence/{id}` - Retrieve specific evidence
- `GET /evidence` - List evidence

### Link Endpoints

- `POST /links` - Create a new link
- `GET /links` - List links (filterable by claim, relation type)

### Governance Endpoints

- `POST /governance/proposals` - Submit a proposal
- `GET /governance/proposals` - List proposals
- `POST /governance/votes` - Cast a vote

See [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md) for detailed API reference.

---

## Contributing

We welcome contributions to The Index! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for:

- Code of conduct
- Development workflow
- Coding standards
- Pull request process
- Governance participation

### Quick Start for Contributors

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting (`pytest && ruff check .`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to your fork (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Tools

- **Testing**: pytest with coverage
- **Linting**: ruff for code quality
- **Type checking**: mypy for static analysis
- **API testing**: httpx for integration tests

---

## Architecture

The Index is built on a layered architecture:

1. **Claim Layer**: Scientific statements with validation
2. **Evidence Layer**: Supporting artifacts and metadata
3. **Link Layer**: Relationships with attestation
4. **Epistemic Engine**: Status computation (in development)
5. **Governance Layer**: Community-driven evolution
6. **API Layer**: RESTful interfaces for all operations

For the complete normative specification, see [INDEX_ARCHITECTURE.md](INDEX_ARCHITECTURE.md).

---

## Roadmap

### Phase 1: Core Models ✓
- Claims, evidence, links data models
- Basic API endpoints
- Protocol invariant enforcement

### Phase 2: Epistemic Engine (In Progress)
- Status computation algorithms
- Weighting and caching
- Deterministic evaluation

### Phase 3: Governance Integration (Planned)
- Schema evolution mechanism
- Ontology management
- Community voting

### Phase 4: External Integrations (Planned)
- arXiv, CrossRef, PubMed adapters
- Institutional repository connectors
- GitHub dataset integration

### Phase 5: Public Release (Planned)
- Documentation and tutorials
- Community onboarding
- Production deployment

---

## Documentation

- **[INDEX_ARCHITECTURE.md](INDEX_ARCHITECTURE.md)**: Normative protocol specification
- **[docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md)**: API reference
- **[docs/DEVELOPER_SETUP.md](docs/DEVELOPER_SETUP.md)**: Development guide
- **[docs/SECURITY.md](docs/SECURITY.md)**: Security considerations
- **[CONTRIBUTING.md](CONTRIBUTING.md)**: Contribution guidelines
- **[INDEX.md](INDEX.md)**: The canonical index

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

The Index is built on the BitRep identity and reputation substrate. Special thanks to all contributors and the broader scientific community for inspiration and feedback.

---

## Contact

- **GitHub Issues**: [https://github.com/clarity-index/the-index/issues](https://github.com/clarity-index/the-index/issues)
- **Discussions**: [https://github.com/clarity-index/the-index/discussions](https://github.com/clarity-index/the-index/discussions)

---

**Status**: Active Development  
**Version**: 0.1.0  
**Protocol Version**: 1.0.0

