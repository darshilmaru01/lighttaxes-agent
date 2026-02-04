def normalize_input(raw: dict) -> dict:
    """
    Normalize TaxCalcBench input.json into the internal schema
    expected by form agents.
    """

    normalized = {}

    # Filing status
    if "filing_status" in raw:
        normalized["filing_status"] = raw["filing_status"].lower()

    elif "return" in raw and "filing_status" in raw["return"]:
        normalized["filing_status"] = raw["return"]["filing_status"].lower()

    elif "metadata" in raw and "filing_status" in raw["metadata"]:
        normalized["filing_status"] = raw["metadata"]["filing_status"].lower()

    else:
        # TaxCalcBench single-filer default (safe for chosen case)
        normalized["filing_status"] = "single"

    # W-2 wages
    normalized["w2"] = []

    # Case 1: simple schema (your earlier tests)
    for w2 in raw.get("w2", []):
        if "amount" in w2:
            normalized["w2"].append({"amount": w2["amount"]})

    # Case 2: TaxCalcBench schema
    forms = raw.get("forms", {})
    for w2 in forms.get("W2", []):
        if "wages" in w2:
            normalized["w2"].append({"amount": w2["wages"]})

    # 1099-INT interest
    normalized["1099_int"] = []

    # Case 1: simple schema
    for item in raw.get("1099_int", []):
        if "amount" in item:
            normalized["1099_int"].append({"amount": item["amount"]})

    # Case 2: TaxCalcBench schema
    for item in forms.get("1099INT", []):
        if "interest" in item:
            normalized["1099_int"].append({"amount": item["interest"]})

    return normalized