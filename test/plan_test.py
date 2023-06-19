from src.plan import Plan


def test_can_initialize_plan():
    config = {
            "average_growth": 6
        }


    tax = Plan(config)
    assert tax.get_growth() == 6