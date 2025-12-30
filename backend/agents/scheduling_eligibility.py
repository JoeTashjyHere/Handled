from typing import Any

from agents.eligibility_shared import EligibilityResult, enforce_confidence


REQUIRED_FIELDS = {"availability_window", "time_zone", "participants"}


def evaluate_scheduling_eligibility(payload: dict[str, Any], confidence_threshold: float = 0.8) -> dict[str, Any]:
    missing = REQUIRED_FIELDS - payload.keys()
    if missing:
        result = EligibilityResult(
            eligible=False,
            confidence=0.35,
            reason=f"Missing required fields: {', '.join(sorted(missing))}.",
            requires_human_review=True
        )
        return result.to_dict()

    participants = payload.get("participants")
    if not isinstance(participants, list) or not participants:
        result = EligibilityResult(
            eligible=False,
            confidence=0.4,
            reason="Participants list is empty or invalid.",
            requires_human_review=True
        )
        return result.to_dict()

    has_constraints = bool(payload.get("hard_constraints"))
    if has_constraints:
        result = EligibilityResult(
            eligible=True,
            confidence=0.85,
            reason="Scheduling has defined constraints and participants.",
            requires_human_review=False
        )
    else:
        result = EligibilityResult(
            eligible=True,
            confidence=0.78,
            reason="Scheduling request is simple but lacks explicit constraints.",
            requires_human_review=False
        )

    return enforce_confidence(result, confidence_threshold).to_dict()
