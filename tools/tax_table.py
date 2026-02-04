# tools/tax_table.py
def compute_tax(taxable_income: float, filing_status: str) -> float:
    """
    Simplified tax calculation.
    Good enough for early test cases like single-w2.
    """
    if taxable_income <= 0:
        return 0.0

    # VERY simplified brackets (demo only)
    if filing_status == "single":
        if taxable_income <= 11000:
            return taxable_income * 0.10
        elif taxable_income <= 44725:
            return 11000 * 0.10 + (taxable_income - 11000) * 0.12
        else:
            return 5147 + (taxable_income - 44725) * 0.22

    # fallback
    return taxable_income * 0.10