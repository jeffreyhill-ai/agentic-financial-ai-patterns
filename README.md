# Agentic Financial AI Patterns

Design notes and example patterns for building financial AI systems that are useful beyond demos.

The focus is not prompt tricks. The focus is behavior architecture: schemas, tool contracts, review queues, approval gates, source grounding, evals, and audit trails.

These are the product and platform patterns that make financial AI systems trustworthy enough to operate.

## Patterns

### Source-linked facts

Financial AI systems should not turn evidence into anonymous prose. Extracted facts need provenance.

```json
{
  "fact_type": "liability.balance",
  "label": "Mortgage balance",
  "value": 428500,
  "currency": "USD",
  "as_of_date": "2026-06-30",
  "confidence": 0.82,
  "source": {
    "document_id": "statement-2026-06",
    "page": 2,
    "excerpt": "Principal balance: $428,500"
  },
  "review_status": "needs_advisor_review"
}
```

### Review before persistence

AI-generated facts, assumptions, and narratives should stay provisional until a human approves them.

```text
proposed_fact
  -> review_task
  -> approve | correct | reject
  -> saved_client_artifact
```

### Tool contracts before free-form automation

Trusted financial systems should expose narrow, auditable tools instead of arbitrary shell or browser control.

Prefer:

- `import_files`
- `extract_document_text`
- `extract_pdf_tables`
- `normalize_financial_facts`
- `detect_fact_conflicts`
- `create_review_tasks`
- `draft_snapshot`
- `save_approved_snapshot`

Avoid:

- open-ended shell execution
- unrestricted filesystem reads
- autonomous credentialed login
- unattended financial portal automation

### Uncertainty as product surface

Uncertainty should not be hidden inside a paragraph. It should become a task.

Examples:

- Confirm whether a recurring deposit is payroll or transfer.
- Resolve contradiction between tax return income and paystub income.
- Ask client for missing insurance premium.
- Review low-confidence mortgage balance.

### Precise privacy claims

If an AI API is used, do not claim that no data ever leaves the computer.

Say:

> Persistent records stay local or firm-controlled. AI payloads are minimized, transient, and reviewable.

## Why These Patterns Matter

Financial AI lives inside regulated, high-trust workflows. The important question is not whether a model can generate a plausible answer.

The important question is whether the system can show:

- where the answer came from
- how confident it is
- what changed
- who approved it
- what should happen next

These are the questions that separate a convincing AI demo from a product architecture a financial institution can actually trust.
