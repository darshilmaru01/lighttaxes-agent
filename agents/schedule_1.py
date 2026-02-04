# agents/schedule_1.py
from agents.base import FormAgent

class Schedule1Agent(FormAgent):
    name = "Schedule 1"

    def run(self, inputs: dict):
        additional_income = inputs.get("schedule_b_interest", 0.0)
        adjustments = 0.0  # keeping simple for now

        return {
            "schedule1_additional_income": additional_income,
            "schedule1_adjustments": adjustments
        }
