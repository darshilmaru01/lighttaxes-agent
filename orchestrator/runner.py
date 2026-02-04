from agents.schedule_b import ScheduleBAgent
from agents.schedule_1 import Schedule1Agent
from agents.form_1040 import Form1040Agent
from verifier.basic_checks import verify_consistency

def run_pipeline(input_data: dict):
    sched_b = ScheduleBAgent()
    b_out = sched_b.run(input_data)

    sched_1 = Schedule1Agent()
    s1_out = sched_1.run({**input_data, **b_out})

    form_1040 = Form1040Agent()
    final_out = form_1040.run({**input_data, **b_out, **s1_out})

    verifier_errors = verify_consistency(
        {**input_data, **b_out},
        final_out
    )

    if verifier_errors:
        final_out["verifier_errors"] = verifier_errors

    return final_out
