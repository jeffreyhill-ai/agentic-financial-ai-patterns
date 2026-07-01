# Agentic Financial AI Patterns

Design notes and example patterns for building financial AI systems that are useful beyond demos.

The focus is not prompt tricks. The focus is behavior architecture: schemas, tool contracts, review queues, approval gates, source grounding, evals, and audit trails.

These are the product and platform patterns that make financial AI systems trustworthy enough to operate.

The hard part is rarely "calling an API." The hard part is making financial data from many providers behave like a coherent product surface: identifiers do not line up, taxonomies disagree, entitlements vary by client and region, point-in-time values change, research and news carry attribution obligations, and source lineage matters when the system starts to reason or act.

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

### Provider-aware data contracts

Financial data products should not hide provider differences too early. A clean product model still needs to preserve enough source context to explain and debug the result.

Useful contracts often include:

- provider and dataset
- original identifier and normalized identifier
- taxonomy or classification source
- entitlement scope
- as-of date and effective date
- point-in-time behavior
- attribution requirement
- lineage back to source payload or document
- transformation/version metadata

When AI is layered on top, these details stop being back-office concerns. They become part of the trust model.

## Why These Patterns Matter

Financial AI lives inside regulated, high-trust workflows. The important question is not whether a model can generate a plausible answer.

The important question is whether the system can show:

- where the answer came from
- how confident it is
- what changed
- who approved it
- what should happen next

These are the questions that separate a convincing AI demo from a product architecture a financial institution can actually trust.

## Roadmap

Planned examples:

- source-linked fact schema examples
- advisor review queue patterns
- provider-aware data contract examples
- evaluation patterns for financial fact extraction

## Use / Reuse

Content is shared for discussion, portfolio, and professional context. No license is granted for commercial reuse, redistribution, or derivative use without permission.
