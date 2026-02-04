# agents/form_1040.py
from agents.base import FormAgent
from tools.standard_deduction import standard_deduction
from tools.tax_table import compute_tax
from tools.pdf_navigator import PDFNavigator
from llm.client import ask_llm

class Form1040Agent(FormAgent):
    name = "Form 1040"

    def run(self, inputs: dict):
        filing_status = inputs["filing_status"]

        wages = sum(w.get("amount", 0.0) for w in inputs.get("w2", []))
        additional_income = inputs.get("schedule1_additional_income", 0.0)
        adjustments = inputs.get("schedule1_adjustments", 0.0)

        total_income = wages + additional_income
        agi = total_income - adjustments

        # --- PDF grounding step
        pdf = PDFNavigator("data/irs_pdfs/i1040gi--2024.pdf")
        deduction_context = pdf.search("standard deduction", max_pages=5)

        llm_prompt = f"""
You are computing Form 1040 deductions.

IRS instruction excerpts:
{deduction_context}

Taxpayer filing status: {filing_status}

Question:
Should this taxpayer take the standard deduction, and what is the rule?
Answer briefly and cite the instruction.
"""

        deduction_reasoning = ask_llm(llm_prompt)

        # Deterministic deduction
        deduction = standard_deduction(filing_status)

        taxable_income = max(0.0, agi - deduction)
        tax = compute_tax(taxable_income, filing_status)

        return {
            "total_income": total_income,
            "agi": agi,
            "deduction": deduction,
            "taxable_income": taxable_income,
            "total_tax": tax,
            "deduction_reasoning": deduction_reasoning
        }
