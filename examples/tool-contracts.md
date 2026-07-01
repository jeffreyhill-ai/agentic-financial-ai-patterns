# Governed Financial AI Tool Contracts

Trusted financial AI systems should expose narrow, auditable tools with explicit inputs, outputs, permissions, and review boundaries.

## Example Tool Surface

| Tool | Purpose | Boundary |
| --- | --- | --- |
| `import_evidence` | Add documents, statements, notes, screenshots, or provider payload references to a workspace | No facts are persisted without extraction and review |
| `extract_source_linked_facts` | Propose structured facts with source references, confidence, and lineage | Output remains provisional |
| `detect_fact_conflicts` | Identify contradictions, missing fields, stale values, or low-confidence evidence | Creates review tasks, not final judgments |
| `create_review_tasks` | Turn uncertainty into advisor-visible work | Requires human review before downstream persistence |
| `draft_client_snapshot` | Generate a narrative or dashboard input from approved facts | Must use approved facts only |
| `save_approved_artifact` | Persist reviewed snapshots, briefs, or checklist items | Requires explicit approval and audit metadata |

## Design Principle

Agentic financial AI should not be given broad authority and then asked to behave. It should be given constrained tools, typed contracts, observable state, and clear approval boundaries.
