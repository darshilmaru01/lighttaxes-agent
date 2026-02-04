from lxml import etree

def extract_1040_values(xml_path):
    tree = etree.parse(xml_path)
    root = tree.getroot()

    def get(tag):
        el = root.find(f".//{tag}")
        return float(el.text) if el is not None else None

    return {
        "total_income": get("TotalIncome"),
        "adjusted_gross_income": get("AdjustedGrossIncome"),
        "taxable_income": get("TaxableIncome"),
        "total_tax": get("Tax")
    }