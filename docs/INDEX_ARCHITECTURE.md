# INDEX_ARCHITECTURE.md
## The Index — A Normative Protocol Specification for Verifiable Scientific Knowledge

**Version:** 1.0  
**Status:** Draft Specification  
**Date:** 2024-01-23

---

## Table of Contents

1. [Scope and Introduction](#1-scope-and-introduction)
2. [Terminology and Definitions](#2-terminology-and-definitions)
3. [Core Principles](#3-core-principles)
4. [Core Data Model](#4-core-data-model)
5. [Claim Lifecycle](#5-claim-lifecycle)
6. [API Surfaces](#6-api-surfaces)
7. [Ontology Integration](#7-ontology-integration)
8. [Provenance and Attestation](#8-provenance-and-attestation)
9. [Governance Hooks](#9-governance-hooks)
10. [Security and Integrity Considerations](#10-security-and-integrity-considerations)
11. [Versioning and Evolution](#11-versioning-and-evolution)

---

## 1. Scope and Introduction

### 1.1 Purpose

The Index is a normative protocol specification for representing, linking, and evaluating verifiable scientific knowledge. This document defines the requirements and architecture for implementations of The Index protocol.

### 1.2 Scope

This specification defines:

- Core data models for claims, evidence, and relationships
- Protocol invariants that implementations MUST enforce
- API surfaces for interacting with The Index
- Integration requirements with BitRep identity substrate
- Governance mechanisms for protocol evolution

This specification does NOT define:

- Specific storage backends or database schemas
- User interface requirements
- Authentication mechanisms (delegated to BitRep)
- Specific cryptographic algorithms (delegated to BitRep)

### 1.3 Relationship to BitRep

The Index MUST be built on top of BitRep, which provides:

- Cryptographic identities for all contributors
- Attestation mechanisms for provenance
- Reputation scoring for weighted evidence
- Governance infrastructure for protocol evolution
- Privacy and selective disclosure capabilities

Implementations of The Index MUST NOT implement their own identity, attestation, or reputation systems.

### 1.4 Conformance Keywords

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119.

---

## 2. Terminology and Definitions

### 2.1 Core Terms

**Claim**: An atomic scientific statement with structured semantic representation (subject-predicate-object) and attribution to a BitRep identity.

**Evidence**: An empirical or theoretical artifact that supports, contradicts, or refines claims. Evidence MUST be linked to at least one claim.

**Link**: An attested relationship between a claim and evidence, or between two claims. Links MUST specify a relation type and MAY include strength weighting.

**Epistemic Status**: A computed assessment of a claim's standing based on weighted evidence and link relationships.

**Contributor**: A participant in The Index identified by a BitRep identity. All actions MUST be attributed to a contributor.

**Protocol Invariant**: A requirement that implementations MUST enforce at all times to maintain protocol integrity.

### 2.2 Epistemic Terms

**Supporting Weight**: The sum of weighted supporting links for a claim, adjusted by contributor reputation.

**Contradicting Weight**: The sum of weighted contradicting links for a claim, adjusted by contributor reputation.

**Independence**: A measure of diversity in evidence sources and contributor identities for a claim.

**Robustness**: A measure of replication, methodological quality, and cross-domain consistency for a claim.

---

## 3. Core Principles

### 3.1 Verifiability

All claims, evidence, and links MUST be:
- Attributed to a BitRep identity
- Cryptographically signed via BitRep attestations
- Independently verifiable by any observer

Implementations MUST reject unsigned or unattributed contributions.

### 3.2 Modularity

The protocol MUST maintain clear separation between:
- The claim layer (scientific statements)
- The evidence layer (supporting artifacts)
- The link layer (relationships)
- The governance layer (protocol evolution)

These layers MUST interoperate through well-defined interfaces.

### 3.3 Epistemic Transparency

The epistemic status of any claim MUST be:
- Computable from public data
- Derived using deterministic algorithms
- Reproducible by independent implementations

Implementations MUST NOT use subjective judgment or hidden signals in status computation.

### 3.4 Decentralization

The protocol MUST NOT require:
- Central authority for truth determination
- Privileged administrators with special powers
- Single points of failure

Protocol evolution MUST occur through decentralized governance.

### 3.5 Reputation Weighting

Evidence and links MUST be weighted by the BitRep reputation of contributors. Implementations MUST apply reputation weighting consistently in epistemic status computation.

### 3.6 Deterministic Computation

Epistemic status computation MUST be deterministic. Given identical input data and algorithm parameters, all implementations MUST produce identical results.

---

## 4. Core Data Model

### 4.1 Claim Object

A Claim MUST contain the following required fields:

- `id` (string): Unique identifier matching pattern `claim_[a-zA-Z0-9_-]+`
- `subject` (string): The subject of the claim (non-empty)
- `predicate` (string): The relationship or property being asserted (non-empty)
- `object` (string): What is being asserted about the subject (non-empty)
- `contributor_id` (string): BitRep identity of the creator (non-empty)
- `timestamp` (ISO 8601 datetime): When the claim was created

A Claim MUST contain at least one of:
- `evidence_refs` (array of strings): References to evidence (minimum 1 element if present)
- `justification` (string): Textual justification (non-empty if present)

**Protocol Invariant**: Claims MUST have either evidence_refs OR justification.

A Claim MAY contain:
- `canonical_text` (string): Human-readable claim text
- `semantic_representation` (object): Machine-readable semantic structure
- `domains` (array of strings): Domain tags
- `status` (enum): One of: proposed, supported, contested, refuted, deprecated
- `created_at` (ISO 8601 datetime): Creation timestamp
- `updated_at` (ISO 8601 datetime): Last update timestamp
- `provenance` (object): Attestation and signature information

Implementations MUST validate that all claims conform to these requirements.

### 4.2 Evidence Object

An Evidence object MUST contain:

- `id` (string): Unique identifier matching pattern `evidence_[a-zA-Z0-9_-]+`
- `type` (enum): One of: experiment, observation, dataset, simulation, theorem, meta_analysis
- `source_identifier` (string): External identifier (DOI, arXiv ID, etc.)
- `submitted_by` (string): BitRep identity of submitter
- `created_at` (ISO 8601 datetime): Submission timestamp

An Evidence object MAY contain:

- `metadata` (object): Domain-specific metadata including:
  - `methodology` (string)
  - `sample_size` (integer)
  - `uncertainty` (float)
  - `instrumentation` (string)
  - `replication_history` (array of strings)
- `quality_score` (float, 0.0-1.0): Computed quality assessment

Evidence MUST be linked to at least one claim to be included in the epistemic graph.

### 4.3 Link Object

A Link MUST contain:

- `id` (string): Unique identifier
- `claim_id` (string): ID of the claim being linked
- `relation_type` (enum): One of: supports, contradicts, weakly_supports, refines, generalizes, depends_on, conflicts_with
- `attested_by` (string): BitRep identity creating the link
- `timestamp` (ISO 8601 datetime): Link creation time

A Link MUST contain exactly one of:
- `evidence_id` (string): ID of linked evidence (for claim-evidence links)
- `claim_id_2` (string): ID of second claim (for claim-claim links)

A Link MAY contain:
- `strength` (float, 0.0-1.0): Relationship strength (default 1.0)

**Protocol Invariant**: Links MUST connect to either evidence OR another claim, never both.

### 4.4 Epistemic Cache

Implementations SHOULD maintain an epistemic cache for performance. A cache entry MUST contain:

- `claim_id` (string): ID of the claim
- `status` (enum): Computed status category
- `supporting_weight` (float): Total weighted support
- `contradicting_weight` (float): Total weighted contradiction
- `independence_score` (float, 0.0-1.0): Evidence diversity measure
- `robustness_score` (float, 0.0-1.0): Quality and replication measure
- `last_computed_at` (ISO 8601 datetime): Cache timestamp

Implementations MUST invalidate cache entries when underlying data changes.

### 4.5 Immutability

Claims, evidence, and links MUST be immutable after creation, except for:
- Claim status updates (via epistemic computation)
- Cache recomputation
- Metadata corrections (via governance)

Implementations MUST preserve creation timestamps and original content.

---

## 5. Claim Lifecycle

### 5.1 Creation Phase

When a claim is created, implementations MUST:

1. Validate all required fields are present
2. Verify contributor_id corresponds to valid BitRep identity
3. Enforce evidence_refs OR justification requirement
4. Assign unique claim ID
5. Set status to "proposed"
6. Record creation timestamp
7. Store claim persistently

### 5.2 Linking Phase

After creation, contributors MAY:

- Submit evidence and create claim-evidence links
- Create claim-claim links to establish relationships
- Update link strength values

All links MUST be attested by a BitRep identity.

### 5.3 Evaluation Phase

Implementations MUST periodically or on-demand:

1. Compute supporting_weight from supporting links
2. Compute contradicting_weight from contradicting links
3. Calculate independence_score from source diversity
4. Calculate robustness_score from quality metrics
5. Determine status category based on weights
6. Update epistemic cache

### 5.4 Status Categories

Implementations MUST assign status based on these criteria:

- **proposed**: Default status, insufficient evidence
- **supported**: supporting_weight significantly exceeds contradicting_weight
- **contested**: supporting_weight and contradicting_weight are comparable
- **refuted**: contradicting_weight significantly exceeds supporting_weight
- **deprecated**: Claim superseded or retracted via governance

Implementations SHOULD define specific thresholds for status transitions.

### 5.5 Deprecation

Claims MAY be deprecated through:
- Governance proposal and vote
- Contributor retraction (for their own claims)
- Community consensus mechanisms

Deprecated claims MUST remain in the graph but SHOULD be marked clearly.

---

## 6. API Surfaces

### 6.1 Required Endpoints

Implementations MUST provide the following HTTP REST API endpoints:

#### 6.1.1 Claim Endpoints

- `POST /claims` - Create a new claim
  - MUST validate protocol invariants
  - MUST return 400 for invalid claims
  - MUST return 201 with claim object on success

- `GET /claims/{id}` - Retrieve a specific claim
  - MUST return 404 if not found
  - MUST return 200 with claim object if found

- `GET /claims` - List claims with filtering
  - MUST support pagination (limit, offset)
  - SHOULD support filtering by status, domain, contributor
  - MUST return 200 with array of claims

- `GET /claims/search` - Search claims by text
  - MUST support full-text search on canonical_text
  - MUST return 200 with array of matching claims

#### 6.1.2 Evidence Endpoints

- `POST /evidence` - Submit new evidence
  - MUST validate required fields
  - MUST return 201 with evidence object on success

- `GET /evidence/{id}` - Retrieve specific evidence
  - MUST return 404 if not found
  - MUST return 200 with evidence object if found

- `GET /evidence` - List evidence with filtering
  - MUST support pagination
  - SHOULD support filtering by type, source

#### 6.1.3 Link Endpoints

- `POST /links` - Create a new link
  - MUST validate claim and evidence/claim_2 exist
  - MUST enforce protocol invariants
  - MUST return 201 with link object on success

- `GET /links` - List links
  - MUST support filtering by claim_id
  - MUST support filtering by relation_type
  - MUST return 200 with array of links

#### 6.1.4 Epistemic Status Endpoints

- `GET /claims/{id}/status` - Get computed epistemic status
  - MUST return current cached status if available
  - SHOULD trigger recomputation if cache is stale
  - MUST return 200 with status object

- `POST /claims/{id}/status/compute` - Force status recomputation
  - MUST recompute from current graph state
  - MUST update cache
  - MUST return 200 with updated status

### 6.2 Optional Endpoints

Implementations MAY provide:

- `GET /graph` - Query subgraphs
- `GET /claims/{id}/dependencies` - Dependency analysis
- `GET /claims/{id}/evidence` - Evidence network for claim
- Graph traversal and visualization endpoints

### 6.3 Error Handling

Implementations MUST return appropriate HTTP status codes:

- 400: Bad Request (invalid input, protocol violations)
- 404: Not Found (resource does not exist)
- 409: Conflict (duplicate IDs, constraint violations)
- 500: Internal Server Error (implementation errors)

Error responses SHOULD include descriptive messages.

---

## 7. Ontology Integration

### 7.1 Ontology Requirements

Implementations SHOULD support a hierarchical ontology for:

- Domain classification
- Predicate vocabularies
- Relation type taxonomies
- Evidence type categorization

### 7.2 Core Ontology

The protocol MUST define a core ontology including:

- Fundamental relation types (supports, contradicts, etc.)
- Basic evidence types (experiment, observation, etc.)
- Standard epistemic status categories

### 7.3 Extended Ontologies

Implementations MAY support extended ontologies for:

- Discipline-specific domains
- Specialized evidence types
- Custom relation types

Extended ontologies MUST be registered through governance.

### 7.4 Ontology Evolution

Ontology changes MUST follow governance procedures:

1. Proposal submission with rationale
2. Community review period
3. Reputation-weighted voting
4. Implementation migration path

Breaking ontology changes MUST be versioned.

---

## 8. Provenance and Attestation

### 8.1 Identity Requirements

All contributions MUST be attributed to a BitRep identity. Implementations MUST:

- Verify BitRep identity signatures
- Reject contributions without valid attribution
- Store contributor_id with all objects

### 8.2 Attestation Anchoring

Claims, evidence, and links SHOULD be anchored as BitRep attestations. Implementations SHOULD:

- Generate attestation for each contribution
- Store attestation ID in provenance metadata
- Support attestation verification

### 8.3 Reputation Integration

Implementations MUST integrate BitRep reputation for:

- Link strength weighting in epistemic computation
- Governance vote weighting
- Quality score calculation

Implementations MUST fetch current reputation scores from BitRep.

### 8.4 Provenance Tracking

Implementations MUST maintain complete provenance chains:

- Original contributor and timestamp
- Modification history (if applicable)
- Attestation signatures
- Reputation scores at time of contribution

---

## 9. Governance Hooks

### 9.1 Governance Scope

Governance MUST cover:

- Schema evolution (adding/modifying fields)
- Ontology updates (new domains, relations, types)
- Protocol parameter changes (status thresholds, weights)
- Conflict resolution (disputed claims, spam)

### 9.2 Proposal Mechanism

Implementations MUST support:

- Proposal submission by any contributor
- Structured proposal format with rationale
- Community review period (RECOMMENDED: 7-14 days)
- Outcome recording in governance log

### 9.3 Voting Mechanism

Implementations MUST implement:

- Reputation-weighted voting via BitRep
- Quadratic scaling (vote_weight = sqrt(reputation))
- Transparent vote tallying
- Quorum requirements

### 9.4 Execution

Approved proposals MUST trigger:

- Automatic schema/ontology updates (if applicable)
- Migration scripts for breaking changes
- Notification to all implementations
- Version increment

---

## 10. Security and Integrity Considerations

### 10.1 Cryptographic Security

Implementations MUST:

- Use BitRep cryptographic signatures for all attestations
- Verify signatures before accepting contributions
- Support signature verification by third parties

Implementations MUST NOT:

- Accept unsigned contributions
- Implement custom cryptographic schemes
- Store private keys

### 10.2 Input Validation

Implementations MUST validate all inputs:

- Field type and format validation
- Length limits on text fields
- Numeric range validation
- Pattern matching for IDs

Implementations MUST reject invalid inputs with descriptive errors.

### 10.3 Sybil Resistance

Implementations MUST leverage BitRep reputation for Sybil resistance:

- Weight contributions by reputation
- Apply diminishing returns for multiple contributions from same identity
- Support community flagging of suspicious behavior

### 10.4 Privacy Considerations

Implementations SHOULD support:

- Selective disclosure via BitRep
- Pseudonymous contribution (real identity hidden)
- Confidential evidence submission with delayed reveal

Implementations MUST NOT:

- Expose private BitRep identity information
- Link pseudonymous identities without consent
- Share data with unauthorized parties

### 10.5 Integrity Guarantees

Implementations MUST ensure:

- Immutability of core objects (claims, evidence, links)
- Deterministic epistemic computation
- Auditability of all actions
- Provenance chain integrity

---

## 11. Versioning and Evolution

### 11.1 Versioning Scheme

The Index protocol uses semantic versioning: MAJOR.MINOR.PATCH

- **MAJOR**: Breaking changes to core data models or protocol invariants
- **MINOR**: Backward-compatible feature additions
- **PATCH**: Bug fixes and clarifications

Current version: 1.0.0

### 11.2 Breaking Changes

Breaking changes MUST:

- Increment MAJOR version
- Provide migration documentation
- Include deprecation period (RECOMMENDED: 6 months minimum)
- Be approved through governance vote

Examples of breaking changes:
- Modifying required fields in core data models
- Changing protocol invariants
- Removing API endpoints
- Incompatible ontology restructuring

### 11.3 Backward Compatibility

Implementations SHOULD maintain backward compatibility for:

- Reading older data formats
- Supporting deprecated API endpoints during transition
- Honoring legacy attestations

### 11.4 Evolution Principles

Protocol evolution MUST follow these principles:

1. **Minimal Disruption**: Prefer additive changes over breaking changes
2. **Community Consensus**: Major changes require governance approval
3. **Migration Support**: Provide tools for transitioning implementations
4. **Documentation**: Update specification and migration guides
5. **Transparency**: Announce changes with rationale and timeline

### 11.5 Implementation Compliance

Implementations MUST declare their protocol version and MUST comply with all MUST/REQUIRED directives for that version.

Implementations SHOULD implement RECOMMENDED features but MAY omit them with justification.

Implementations MAY extend the protocol with additional features but MUST NOT violate protocol invariants.

---

## 12. Conclusion

This specification defines The Index as a protocol for verifiable scientific knowledge built on the BitRep identity substrate. Compliant implementations MUST enforce all protocol invariants, provide required API surfaces, and participate in decentralized governance.

The protocol is designed to evolve through community governance while maintaining integrity, transparency, and decentralization. All implementations share responsibility for upholding these principles.

---

**Document History:**
- Version 1.0 (2024-01-23): Initial normative specification
