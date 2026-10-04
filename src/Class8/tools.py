import re
from typing import Any


def _valid_value(shipment_value: float) -> float:
    value = float(shipment_value)
    if value < 0:
        raise ValueError("shipment_value must be non-negative")
    return value


def calculate_delay_compensation(
    shipment_value: float, report: str
) -> dict[str, Any]:
    """Pay 5% of shipment value per delayed day, capped at 20% or $250."""
    value = _valid_value(shipment_value)
    day_match = re.search(r"\b(\d+(?:\.\d+)?)\s*days?\b", report, re.IGNORECASE)
    hour_match = re.search(r"\b(\d+(?:\.\d+)?)\s*hours?\b", report, re.IGNORECASE)
    if day_match:
        delay_days = float(day_match.group(1))
    elif hour_match:
        delay_days = max(float(hour_match.group(1)) / 24, 1)
    else:
        delay_days = 1

    amount = min(value * 0.05 * delay_days, value * 0.20, 250.0)
    return {
        "category": "delayed",
        "compensation_amount": round(amount, 2),
        "currency": "USD",
        "reason": f"5% of shipment value per delayed day ({delay_days:g} day(s)), capped at 20% and $250.",
    }


def calculate_damage_compensation(
    shipment_value: float, report: str
) -> dict[str, Any]:
    """Compensate the reported damage percentage or a severity-based estimate."""
    value = _valid_value(shipment_value)
    percentage_match = re.search(r"\b(\d{1,3}(?:\.\d+)?)\s*%", report)
    if percentage_match:
        damage_percentage = min(float(percentage_match.group(1)), 100.0)
        reason = f"Compensation is based on the reported {damage_percentage:g}% damage severity."
    elif re.search(r"\b(severe|destroyed|unusable)\b", report, re.IGNORECASE):
        damage_percentage = 75.0
        reason = "Severe damage is compensated at 75% of shipment value."
    elif re.search(r"\b(moderate|significant)\b", report, re.IGNORECASE):
        damage_percentage = 35.0
        reason = "Moderate damage is compensated at 35% of shipment value."
    else:
        damage_percentage = 10.0
        reason = "Minor or unspecified damage is compensated at 10% of shipment value."

    return {
        "category": "damaged",
        "compensation_amount": round(value * damage_percentage / 100, 2),
        "currency": "USD",
        "reason": reason,
    }


def calculate_lost_compensation(shipment_value: float) -> dict[str, Any]:
    """Refund the full declared shipment value when a shipment is lost."""
    value = _valid_value(shipment_value)
    return {
        "category": "lost",
        "compensation_amount": round(value, 2),
        "currency": "USD",
        "reason": "Lost shipments are compensated for the full declared shipment value.",
    }