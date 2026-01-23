# Ontology Registry

This directory contains the ontology definitions for The Index protocol. The ontology provides structured vocabularies for domains, predicates, relation types, and evidence types used throughout the system.

## Purpose

The ontology serves to:

1. **Standardize terminology** across implementations
2. **Enable semantic interoperability** between different scientific domains
3. **Facilitate automated reasoning** over claims and evidence
4. **Support evolution** through versioned, governed changes

## Core Ontology

The core ontology (`core.json`) defines fundamental types and relationships that are built into the protocol:

- **Relation Types**: supports, contradicts, weakly_supports, refines, generalizes, depends_on, conflicts_with
- **Evidence Types**: experiment, observation, dataset, simulation, theorem, meta_analysis
- **Status Categories**: proposed, supported, contested, refuted, deprecated

These core types are part of the protocol specification and MUST be supported by all implementations.

## Extended Ontologies

Extended ontologies MAY be added for:

- Discipline-specific domains (e.g., `physics.json`, `biology.json`, `mathematics.json`)
- Specialized predicates (e.g., `chemical_reactions.json`, `genetic_relationships.json`)
- Custom relation types for specific use cases

Extended ontologies MUST be registered through the governance process before use.

## Ontology Structure

Each ontology file follows this JSON structure:

```json
{
  "id": "unique-ontology-id",
  "version": "1.0.0",
  "name": "Ontology Name",
  "description": "Description of the ontology",
  "namespace": "https://clarity-index.github.io/ontologies/name",
  "created": "2024-01-23T00:00:00Z",
  "updated": "2024-01-23T00:00:00Z",
  "contributors": ["bitrep_id_1", "bitrep_id_2"],
  "terms": [
    {
      "id": "term_id",
      "label": "Human-readable label",
      "definition": "Precise definition of the term",
      "type": "relation|evidence_type|domain|predicate",
      "parent": "parent_term_id",
      "aliases": ["alternative_name_1", "alternative_name_2"],
      "examples": ["Example usage 1", "Example usage 2"]
    }
  ]
}
```

## Governance

Ontology changes follow the governance process defined in INDEX_ARCHITECTURE.md:

1. **Proposal**: Submit a proposal for new terms or changes
2. **Review**: Community review period (7-14 days recommended)
3. **Vote**: Reputation-weighted voting
4. **Integration**: Approved changes are integrated and versioned

Breaking changes to the core ontology require a protocol version increment.

## Usage

Implementations should:

1. Load the core ontology at startup
2. Validate claim predicates and relation types against the ontology
3. Support ontology-based search and filtering
4. Respect ontology hierarchies in epistemic computation

## Contributing

To propose ontology additions or changes:

1. Review existing terms to avoid duplication
2. Follow the structured format above
3. Provide clear definitions and examples
4. Submit through the governance process
5. Engage with community feedback

## File Index

- **core.json**: Core protocol ontology (REQUIRED)
- **domains.json**: Scientific domain taxonomy (PLANNED)
- **predicates.json**: Common predicates library (PLANNED)
- **evidence_methods.json**: Evidence methodology taxonomy (PLANNED)

---

**Version**: 1.0.0  
**Last Updated**: 2024-01-23
=======
# Ontology

This directory will contain ontology definitions for The Index.