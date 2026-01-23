# The Index - Example Claims

This directory contains canonical example claims that demonstrate the use of The Index protocol. All examples are aligned with the JSON schema defined in `/schema/claim.schema.json` and follow protocol invariants.

## Purpose

These examples serve to:

1. **Illustrate protocol usage** with realistic scientific claims
2. **Demonstrate schema compliance** for implementation testing
3. **Provide templates** for contributors creating new claims
4. **Validate implementations** through reference data

## Example Files

- **claim_with_evidence.json**: Claim supported by multiple evidence references
- **claim_with_justification.json**: Claim with textual justification (no evidence refs)
- **quantum_entanglement_claim.json**: Physics domain example
- **biodiversity_claim.json**: Ecology domain example
- **mathematical_theorem_claim.json**: Mathematics domain example

## Schema Compliance

All example claims MUST:

- Include required fields: `id`, `subject`, `predicate`, `object`, `contributor_id`, `timestamp`
- Have either `evidence_refs` (with at least 1 element) OR `justification` (non-empty)
- Use valid status values: `proposed`, `supported`, `contested`, `refuted`, `deprecated`
- Follow ID patterns (e.g., `claim_[a-zA-Z0-9_-]+`)

**Note:** Provenance signatures and attestation IDs in examples use simplified placeholder values for demonstration purposes. In production, these would be actual cryptographic signatures and BitRep attestation identifiers.

## Using These Examples

### For Testing

```python
import json
from claim_api import Claim

# Load and validate example
with open('examples/claim_with_evidence.json') as f:
    claim_data = json.load(f)
    claim = Claim(**claim_data)
    print(f"Valid claim: {claim.id}")
```

### For API Requests

```bash
# Submit example claim via API
curl -X POST http://localhost:8000/claims \
  -H "Content-Type: application/json" \
  -d @examples/claim_with_evidence.json
```

### For Learning

Study the examples to understand:
- How to structure semantic representations (subject-predicate-object)
- When to use evidence_refs vs. justification
- How to specify domains and metadata
- Provenance and attestation structure

## Contributing Examples

To add new examples:

1. Create a JSON file following the schema
2. Validate against `/schema/claim.schema.json`
3. Ensure the example illustrates a specific pattern or use case
4. Add a description to this README
5. Submit via pull request

---

**Last Updated**: 2024-01-23
