import re
from typing import Any

from chains import classify_chain, draft_email_chain, escalate_chain
from tools import (
    calculate_damage_compensation,
    calculate_delay_compensation,
    calculate_lost_compensation,
)

ESCALATION_THRESHOLDS = {"premium": 250.0, "standard": 500.0}


def _normalize_category(classification: Any) -> str:
    text = str(classification).strip().lower()
    match = re.search(r"\b(delayed|damaged|lost|unknown)\b", text)
    return match.group(1) if match else "unknown"


def process_exception(
    report: str,
    shipment_value: float,
    customer_tier: str = "standard",
    session: Any | None = None,
) -> dict[str, Any]:
    """Classify, compensate, route, and draft a response for one exception."""
    if not report.strip():
        raise ValueError("report must not be empty")
    value = float(shipment_value)
    if value < 0:
        raise ValueError("shipment_value must be non-negative")

    tier = customer_tier.strip().lower()
    if tier not in ESCALATION_THRESHOLDS:
        raise ValueError("customer_tier must be 'standard' or 'premium'")

    steps = ["Classifying the exception report."]
    category = _normalize_category(classify_chain.invoke({"report": report}))

    if category == "delayed":
        compensation = calculate_delay_compensation(value, report)
    elif category == "damaged":
        compensation = calculate_damage_compensation(value, report)
    elif category == "lost":
        compensation = calculate_lost_compensation(value)
    else:
        compensation = {
            "category": "unknown",
            "compensation_amount": 0.0,
            "currency": "USD",
            "reason": "The report could not be confidently classified; no compensation was issued.",
        }

    amount = compensation["compensation_amount"]
    threshold = ESCALATION_THRESHOLDS[tier]
    escalated = category == "unknown" or amount > threshold
    steps.append(f"Classified as {category}; calculated compensation of ${amount:.2f}.")

    chain_input = {
        "report": report,
        "category": category,
        "shipment_value": value,
        "compensation_amount": amount,
        "reason": compensation["reason"],
    }
    if escalated:
        steps.append(
            "Routed to a manager: the category is unknown."
            if category == "unknown"
            else f"Routed to a manager: compensation exceeds the {tier} threshold of ${threshold:.2f}."
        )
        manager_note = escalate_chain.invoke(chain_input)
        customer_message = ""
        status = "escalated"
    else:
        steps.append("Resolved automatically and drafted a customer email.")
        customer_message = draft_email_chain.invoke(chain_input)
        manager_note = ""
        status = "resolved"

    result = {
        "status": status,
        "category": category,
        "customer_tier": tier,
        "shipment_value": round(value, 2),
        "compensation_amount": amount,
        "currency": compensation["currency"],
        "reason": compensation["reason"],
        "escalated": escalated,
        "customer_message": customer_message,
        "manager_note": manager_note,
        "steps": steps,
    }
    if session is not None:
        session.record(result)
    return result