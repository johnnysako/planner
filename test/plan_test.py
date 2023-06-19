from src.plan import Plan


def test_can_initialize_plan():
    config = {
        "average_growth": 6
    }

    plan = Plan(config)
    assert plan.get_growth() == 6
