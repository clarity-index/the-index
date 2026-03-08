# Index Operations

This directory contains entries for the **Index Operations** database. Each entry documents a named operation in The Index protocol using the canonical schema below.

## Entry Schema

| Field         | Description                                               |
|---------------|-----------------------------------------------------------|
| Title         | Human-readable name of the operation                      |
| Index_Key     | Stable machine-readable identifier (e.g. `IIO-PARITY`)   |
| Type          | Always `Index Operation` for entries in this directory    |
| Layer         | Protocol layer where the operation is enforced            |
| Status        | `Active`, `Draft`, or `Deprecated`                        |
| Canonical     | `true` if this is the authoritative definition            |
| Version       | Semver string for this entry revision                     |
| Parent        | Parent operation group (e.g. `Index Integrity Operations (IIO)`) |
| Dependencies  | Other operations or artefacts this entry depends on       |
| Description   | Prose definition of the operation                         |
| Function      | Numbered list of what the operation does                  |
| Invariants    | Conditions that MUST hold when the operation is active    |
| Failure Modes | Table of known failure modes, triggers, and severities    |
| Enforcement   | How and where the invariants are enforced in code/process |
| Notes         | Additional context, design rationale, and future work     |

## Operation Groups

### Index Integrity Operations (IIO)

| Index_Key   | Title   | Status | Version |
|-------------|---------|--------|---------|
| [IIO-PARITY](IIO-PARITY.md) | Parity | Active | 1.0 |
