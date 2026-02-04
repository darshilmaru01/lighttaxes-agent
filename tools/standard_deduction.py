def standard_deduction(filing_status: str) -> int:
    filing_status = filing_status.lower()
    table = {
        "single": 14600,
        "mfj": 29200,
        "hoh": 21900
    }
    return table[filing_status]