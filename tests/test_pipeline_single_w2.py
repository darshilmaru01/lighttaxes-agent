from orchestrator.runner import run_pipeline

def test_single_w2_pipeline_end_to_end():
    input_data = {
        "filing_status": "single",
        "w2": [{"amount": 60000}],
        "1099_int": [{"amount": 200}]
    }

    output = run_pipeline(input_data)

    assert output["total_income"] == 60200
    assert output["agi"] == 60200
    assert output["deduction"] == 14600
    assert output["taxable_income"] == 45600
    assert output["total_tax"] > 0
