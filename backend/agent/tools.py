from datetime import datetime

from simpleeval import simple_eval
from langchain_core.tools import tool

from backend.logger import logger


@tool
def calculator(expression: str) -> str:
    """Safely calculate a mathematical expression."""

    logger.info(
        "Calculator called: %s",
        expression
    )

    try:
        result = simple_eval(expression)

        logger.info(
            "Calculator result: %s",
            result
        )

        return str(result)

    except Exception:

        logger.exception(
            "Calculator failed"
        )

        return "Could not calculate the expression."


@tool
def current_time() -> str:
    """Return the current local date and time."""

    logger.info(
        "Current time tool called"
    )

    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


TOOLS = [
    calculator,
    current_time
]