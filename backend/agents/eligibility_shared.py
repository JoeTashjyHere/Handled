from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class EligibilityResult:
    eligible: bool
    confidence: float
    reason: str
    requires_human_review: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "eligible": self.eligible,
            "confidence": self.confidence,
            "reason": self.reason,
            "requires_human_review": self.requires_human_review
        }


def enforce_confidence(result: EligibilityResult, threshold: float) -> EligibilityResult:
    requires_review = result.confidence < threshold
    if requires_review:
        return EligibilityResult(
            eligible=result.eligible,
            confidence=result.confidence,
            reason=result.reason,
            requires_human_review=True
        )
    return result
