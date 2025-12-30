from typing import Any

from agents.eligibility_shared import EligibilityResult, enforce_confidence


REQUIRED_FIELDS = {"form_type", "jurisdiction", "applicant_name"}


def evaluate_government_form_eligibility(payload: dict[str, Any], confidence_threshold: float = 0.8) -> dict[str, Any]:
    missing = REQUIRED_FIELDS - payload.keys()
    if missing:
        result = EligibilityResult(
            eligible=False,
            confidence=0.32,
            reason=f"Missing required fields: {', '.join(sorted(missing))}.",
            requires_human_review=True
        )
        return result.to_dict()

    form_type = str(payload.get("form_type", "")).lower()
    supported_forms = {"passport", "dmv", "voter_registration", "benefits"}

    if form_type in supported_forms:
        result = EligibilityResult(
            eligible=True,
            confidence=0.88,
            reason=f"Form type '{form_type}' is supported for intake.",
            requires_human_review=False
        )
    else:
        result = EligibilityResult(
            eligible=False,
            confidence=0.65,
            reason=f"Form type '{form_type}' is not in the supported list.",
            requires_human_review=False
        )

    return enforce_confidence(result, confidence_threshold).to_dict()
