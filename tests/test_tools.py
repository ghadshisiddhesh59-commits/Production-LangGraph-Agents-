from backend.agent.tools import calculator, current_time


def test_calculator():

    result = calculator.invoke(
        "25 * 48"
    )

    assert result == "1200"


def test_current_time():

    result = current_time.invoke({})

    assert isinstance(
        result,
        str
    )

    assert len(result) > 0