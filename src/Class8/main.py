from pipeline import process_exception


def main() -> None:
    report = input("Shipment exception report: ").strip()
    value_text = input("Shipment value (USD): ").strip()
    tier = input("Customer tier (standard/premium): ").strip() or "standard"
    result = process_exception(report, float(value_text), tier)
    print(f"\nOutcome: {result['status']} ({result['category']})")
    print(f"Compensation: ${result['compensation_amount']:.2f}")
    for step in result["steps"]:
        print(f"- {step}")
    message = result["manager_note"] or result["customer_message"]
    print(f"\n{message}")


if __name__ == "__main__":
    main()