from collections import defaultdict
from typing import Any


class TriageSession:
    def __init__(self) -> None:
        self._entries: list[dict[str, Any]] = []

    def record(self, result: dict[str, Any]) -> None:
        self._entries.append(dict(result))

    def get_daily_log(self) -> list[dict[str, Any]]:
        return [dict(entry) for entry in self._entries]

    def generate_daily_summary(self) -> dict[str, Any]:
        category_totals: dict[str, float] = defaultdict(float)
        compensation_paid = 0.0
        escalated_count = 0

        for entry in self._entries:
            amount = float(entry.get("compensation_amount", 0.0))
            category_totals[str(entry.get("category", "unknown"))] += amount
            if entry.get("escalated", False):
                escalated_count += 1
            else:
                compensation_paid += amount

        costliest_category = (
            max(category_totals, key=category_totals.get) if category_totals else None
        )
        total = len(self._entries)
        return {
            "exceptions_processed": total,
            "total_compensation_paid": round(compensation_paid, 2),
            "escalated_count": escalated_count,
            "escalation_rate": round(escalated_count / total, 4) if total else 0.0,
            "category_compensation_totals": {
                category: round(amount, 2)
                for category, amount in sorted(category_totals.items())
            },
            "costliest_category": costliest_category,
        }


daily_session = TriageSession()