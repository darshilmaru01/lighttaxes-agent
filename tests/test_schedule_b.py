from agents.schedule_b import ScheduleBAgent

def test_schedule_b_interest_only():
    agent = ScheduleBAgent()

    inputs = {
        "1099_int": [
            {"amount": 100},
            {"amount": 250}
        ]
    }

    result = agent.run(inputs)

    assert result["schedule_b_interest"] == 350
    assert result["schedule_b_dividends"] == 0.0