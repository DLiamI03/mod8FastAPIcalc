"""
Calculator operations module.
Contains all arithmetic operations for the calculator.
"""

import logging
from typing import Union

# Configure logging
logger = logging.getLogger(__name__)


def add(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    Add two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        Sum of a and b
    """
    logger.info(f"Adding {a} + {b}")
    result = a + b
    logger.info(f"Addition result: {result}")
    return result


def subtract(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    Subtract second number from first number.

    Args:
        a: First number
        b: Second number

    Returns:
        Difference of a and b
    """
    logger.info(f"Subtracting {b} from {a}")
    result = a - b
    logger.info(f"Subtraction result: {result}")
    return result


def multiply(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    Multiply two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        Product of a and b
    """
    logger.info(f"Multiplying {a} * {b}")
    result = a * b
    logger.info(f"Multiplication result: {result}")
    return result


def divide(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    Divide first number by second number.

    Args:
        a: First number (dividend)
        b: Second number (divisor)

    Returns:
        Quotient of a and b

    Raises:
        ValueError: If b is zero (division by zero)
    """
    logger.info(f"Dividing {a} by {b}")

    if b == 0:
        logger.error("Division by zero attempted")
        raise ValueError("Cannot divide by zero")

    result = a / b
    logger.info(f"Division result: {result}")
    return result


def power(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    Raise first number to the power of second number.

    Args:
        a: Base number
        b: Exponent

    Returns:
        a raised to the power of b
    """
    logger.info(f"Calculating {a} ^ {b}")
    result = a**b
    logger.info(f"Power result: {result}")
    return result


def square_root(a: Union[int, float]) -> Union[int, float]:
    """
    Calculate square root of a number.

    Args:
        a: Number to find square root of

    Returns:
        Square root of a

    Raises:
        ValueError: If a is negative
    """
    logger.info(f"Calculating square root of {a}")

    if a < 0:
        logger.error("Square root of negative number attempted")
        raise ValueError("Cannot calculate square root of negative number")

    result = a**0.5
    logger.info(f"Square root result: {result}")
    return result


def percentage(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    Calculate percentage of a number.

    Args:
        a: Base number
        b: Percentage value

    Returns:
        b percent of a
    """
    logger.info(f"Calculating {b}% of {a}")
    result = (a * b) / 100
    logger.info(f"Percentage result: {result}")
    return result
