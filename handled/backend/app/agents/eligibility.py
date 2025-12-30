from typing import Any


def reimbursement_eligibility_stub(extracted: dict[str, Any]) -> dict[str, Any]:
    return {
        "eligible": None,
        "reason": "MVP stub: requires human review to confirm eligibility.",
        "confidence": 0.0,
        "human_review_required": True,
    }


def tax_simple_filing_gatekeeper_stub(user_docs_summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "eligible_for_simple_filing": False,
        "reason": "MVP stub: enable simple W-2 flow later with CPA review.",
        "confidence": 0.0,
        "human_review_required": True,
    }
