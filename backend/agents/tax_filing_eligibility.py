from typing import Any

from agents.eligibility_shared import EligibilityResult, enforce_confidence


REQUIRED_FIELDS = {"tax_year", "filing_status", "resident_state"}


def evaluate_tax_filing_eligibility(payload: dict[str, Any], confidence_threshold: float = 0.8) -> dict[str, Any]:
    missing = REQUIRED_FIELDS - payload.keys()
    if missing:
        result = EligibilityResult(
            eligible=False,
            confidence=0.28,
            reason=f"Missing required fields: {', '.join(sorted(missing))}.",
            requires_human_review=True
        )
        return result.to_dict()

    filing_status = str(payload.get("filing_status", "")).lower()
    supported_statuses = {"single", "married", "head_of_household"}
    has_dependents = bool(payload.get("dependents"))

    if filing_status not in supported_statuses:
        result = EligibilityResult(
            eligible=False,
            confidence=0.6,
            reason=f"Filing status '{filing_status}' is not supported for simple filings.",
            requires_human_review=False
        )
        return enforce_confidence(result, confidence_threshold).to_dict()

    if has_dependents:
        result = EligibilityResult(
            eligible=False,
            confidence=0.7,
            reason="Dependents present; not eligible for simple filing flow.",
            requires_human_review=False
        )
    else:
        result = EligibilityResult(
            eligible=True,
            confidence=0.86,
            reason="Filing status supported and no dependents indicated.",
            requires_human_review=False
        )

    return enforce_confidence(result, confidence_threshold).to_dict()
