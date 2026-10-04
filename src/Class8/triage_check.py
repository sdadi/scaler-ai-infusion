from pipeline import process_exception

SCENARIOS = [
    {
        "name": "mild delay",
        "report": "The shipment arrived one day late, but the items are fine.",
        "shipment_value": 100.0,
        "customer_tier": "standard",
        "category": "delayed",
        "escalated": False,
    },
    {
        "name": "high-value loss",
        "report": "The high-value shipment is confirmed lost in transit and never delivered.",
        "shipment_value": 2000.0,
        "customer_tier": "standard",
        "category": "lost",
        "escalated": True,
    },
    {
        "name": "minor damage claim",
        "report": "The parcel arrived with minor damage to the outer packaging; contents are usable.",
        "shipment_value": 100.0,
        "customer_tier": "standard",
        "category": "damaged",
        "escalated": False,
    },
    {
        "name": "garbled report",
        "report": "blue window seven quietly unless because parcel maybe yesterday",
        "shipment_value": 10.0,
        "customer_tier": "standard",
        "category": "unknown",
        "escalated": True,
    },
]


def main() -> None:
    failures: list[str] = []
    for scenario in SCENARIOS:
        result = process_exception(
            scenario["report"],
            scenario["shipment_value"],
            scenario["customer_tier"],
        )
        passed = (
            result["category"] == scenario["category"]
            and result["escalated"] is scenario["escalated"]
        )
        print(
            f"{'PASS' if passed else 'FAIL'} {scenario['name']}: "
            f"category={result['category']}, escalated={result['escalated']}"
        )
        if not passed:
            failures.append(scenario["name"])

    if failures:
        raise SystemExit(f"Triage check failed: {', '.join(failures)}")
    print("All four triage scenarios passed.")


if __name__ == "__main__":
    main()