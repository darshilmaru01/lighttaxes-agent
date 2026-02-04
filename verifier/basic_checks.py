def verify_consistency(inputs: dict, outputs: dict):
    errors = []

    wages = sum(w.get("amount", 0.0) for w in inputs.get("w2", []))
    interest = inputs.get("schedule_b_interest", 0.0)

    expected_total_income = wages + interest

    if abs(outputs["total_income"] - expected_total_income) > 1:
        errors.append(
            f"Total income mismatch: expected {expected_total_income}, got {outputs['total_income']}"
        )

    if outputs["taxable_income"] < 0:
        errors.append("Taxable income cannot be negative.")

    if outputs["total_tax"] < 0:
        errors.append("Total tax cannot be negative.")

    return errors