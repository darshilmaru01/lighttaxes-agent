# agents/schedule_b.py
from agents.base import FormAgent

class ScheduleBAgent(FormAgent):
    name = "Schedule B"

    def run(self, inputs: dict):
        interest = sum(i.get("amount", 0.0) for i in inputs.get("1099_int", []))
        dividends = sum(i.get("amount", 0.0) for i in inputs.get("1099_div", []))

        return {
            "schedule_b_interest": interest,
            "schedule_b_dividends": dividends
        }