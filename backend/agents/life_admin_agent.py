class LifeAdminAgent:
    def __init__(self, name: str) -> None:
        self.name = name

    def plan(self, summary: str) -> list[str]:
        return [
            f"Clarify requester goals for: {summary}",
            "Identify dependencies",
            "Draft execution checklist"
        ]
