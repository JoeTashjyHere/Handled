from typing import Any

from agents.eligibility_shared import EligibilityResult, enforce_confidence


REQUIRED_FIELDS = {"expense_category", "provider_name", "amount", "date_of_service"}


def evaluate_hsa_fsa_eligibility(payload: dict[str, Any], confidence_threshold: float = 0.8) -> dict[str, Any]:
    missing = REQUIRED_FIELDS - payload.keys()
    if missing:
        result = EligibilityResult(
            eligible=False,
            confidence=0.3,
            reason=f"Missing required fields: {', '.join(sorted(missing))}.",
            requires_human_review=True
        )
        return result.to_dict()

    category = str(payload.get("expense_category", "")).lower()
    eligible_categories = {
        "medical",
        "dental",
        "vision",
        "prescription",
        "therapy",
        "diagnostic"
    }

    if category in eligible_categories:
        result = EligibilityResult(
            eligible=True,
            confidence=0.92,
            reason=f"Expense category '{category}' is typically HSA/FSA eligible.",
            requires_human_review=False
        )
    else:
        result = EligibilityResult(
            eligible=False,
            confidence=0.7,
            reason=f"Expense category '{category}' is not in the known eligible list.",
            requires_human_review=False
        )

    return enforce_confidence(result, confidence_threshold).to_dict()
