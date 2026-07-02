"""Small reference sketch for a governed advisor-copilot workflow.

This is intentionally standard-library Python so it can run anywhere. In a
production service, these contracts would typically become Pydantic models,
service DTOs, queue payloads, or persisted workflow state.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date
import json
from pathlib import Path
from typing import Literal


ReviewStatus = Literal["approved", "needs_review", "rejected"]
ToolStatus = Literal["succeeded", "failed", "blocked"]


@dataclass(frozen=True)
class SourceReference:
    provider: str
    dataset: str
    source_id: str
    as_of_date: str
    entitlement_scope: str
    excerpt: str | None = None


@dataclass(frozen=True)
class AdvisorCopilotFact:
    fact_id: str
    fact_type: str
    label: str
    value: str | float | int | bool
    confidence: float
    source_refs: list[SourceReference]
    review_status: ReviewStatus

    def validate(self) -> None:
        if not 0 <= self.confidence <= 1:
            raise ValueError(f"{self.fact_id} confidence must be between 0 and 1")
        if not self.source_refs:
            raise ValueError(f"{self.fact_id} must include at least one source")


@dataclass(frozen=True)
class ToolInvocation:
    tool_name: str
    input_contract_version: str
    output_contract_version: str
    purpose: str
    source_fact_ids: list[str]
    status: ToolStatus
    latency_ms: int
    cost_estimate_usd: float


@dataclass(frozen=True)
class ReviewTask:
    task_id: str
    severity: Literal["low", "medium", "high"]
    reason: str
    related_fact_ids: list[str]
    required_reviewer: Literal["advisor", "compliance", "operations"]
    blocks_client_ready_output: bool


def sample_source_refs() -> list[SourceReference]:
    return [
        SourceReference(
            provider="example_custodian",
            dataset="portfolio_positions",
            source_id="position-feed-2026-06-30",
            as_of_date=str(date(2026, 6, 30)),
            entitlement_scope="advisor_household_book",
            excerpt="AAPL market value 1,240,000 USD",
        )
    ]


def build_source_linked_facts() -> list[AdvisorCopilotFact]:
    facts = [
        AdvisorCopilotFact(
            fact_id="fact-position-aapl-001",
            fact_type="portfolio.concentration",
            label="Single-stock concentration",
            value=0.31,
            confidence=0.94,
            source_refs=sample_source_refs(),
            review_status="approved",
        ),
        AdvisorCopilotFact(
            fact_id="fact-client-held-away-001",
            fact_type="held_away.missing_data",
            label="Missing held-away 401k statement",
            value=True,
            confidence=0.88,
            source_refs=[
                SourceReference(
                    provider="advisor_notes",
                    dataset="meeting_notes",
                    source_id="note-2026-06-15",
                    as_of_date=str(date(2026, 6, 15)),
                    entitlement_scope="advisor_household_book",
                    excerpt="Client mentioned current employer 401k but no statement uploaded.",
                )
            ],
            review_status="needs_review",
        ),
    ]
    for fact in facts:
        fact.validate()
    return facts


def run_tools(facts: list[AdvisorCopilotFact]) -> list[ToolInvocation]:
    fact_ids = [fact.fact_id for fact in facts]
    return [
        ToolInvocation(
            tool_name="analyze_concentration_exposure",
            input_contract_version="concentration-input/v1",
            output_contract_version="concentration-output/v1",
            purpose="Calculate issuer-level concentration from approved position facts.",
            source_fact_ids=[fact_id for fact_id in fact_ids if "position" in fact_id],
            status="succeeded",
            latency_ms=842,
            cost_estimate_usd=0.004,
        ),
        ToolInvocation(
            tool_name="detect_missing_held_away_data",
            input_contract_version="missing-data-input/v1",
            output_contract_version="review-task-output/v1",
            purpose="Detect incomplete household context before client-ready output.",
            source_fact_ids=[fact_id for fact_id in fact_ids if "held-away" in fact_id],
            status="succeeded",
            latency_ms=219,
            cost_estimate_usd=0.001,
        ),
    ]


def create_review_tasks(facts: list[AdvisorCopilotFact]) -> list[ReviewTask]:
    tasks: list[ReviewTask] = []
    for fact in facts:
        if fact.review_status == "needs_review":
            tasks.append(
                ReviewTask(
                    task_id=f"review-{fact.fact_id}",
                    severity="medium",
                    reason=f"{fact.label} must be confirmed before client-ready output.",
                    related_fact_ids=[fact.fact_id],
                    required_reviewer="advisor",
                    blocks_client_ready_output=True,
                )
            )
    return tasks


def evaluate_workflow(facts: list[AdvisorCopilotFact], tasks: list[ReviewTask]) -> dict[str, str]:
    all_claims_grounded = all(fact.source_refs for fact in facts)
    unapproved_blocking = any(task.blocks_client_ready_output for task in tasks)
    return {
        "groundedness": "pass" if all_claims_grounded else "fail",
        "financial_correctness": "pass",
        "policy_adherence": "pass",
        "client_ready_without_review": "fail" if unapproved_blocking else "pass",
    }


def run_workflow() -> dict[str, object]:
    facts = build_source_linked_facts()
    tool_invocations = run_tools(facts)
    review_tasks = create_review_tasks(facts)
    eval_results = evaluate_workflow(facts, review_tasks)
    return {
        "run_id": "advisor-copilot-run-001",
        "workflow": "advisor_meeting_brief",
        "risk_level": "medium",
        "status": "advisor_review_required" if review_tasks else "ready_for_advisor_approval",
        "facts": [asdict(fact) for fact in facts],
        "tool_invocations": [asdict(invocation) for invocation in tool_invocations],
        "review_tasks": [asdict(task) for task in review_tasks],
        "eval_results": eval_results,
    }


def load_eval_case_count() -> int:
    path = Path(__file__).with_name("advisor-copilot-eval-cases.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    return len(data["cases"])


def main() -> None:
    result = run_workflow()
    summary = {
        "run_id": result["run_id"],
        "status": result["status"],
        "review_task_count": len(result["review_tasks"]),
        "eval_results": result["eval_results"],
        "eval_case_count": load_eval_case_count(),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
