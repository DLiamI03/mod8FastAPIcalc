"""
Unit tests for calculator operations.
Tests all arithmetic functions in the operations module.
"""

import math

import pytest

from app.operations import (
    add,
    divide,
    multiply,
    percentage,
    power,
    square_root,
    subtract,
)


class TestAddition:
    """Test cases for addition operation."""

    def test_add_positive_numbers(self):
        """Test adding two positive numbers."""
        assert add(2, 3) == 5
        assert add(10, 15) == 25
        assert add(0.5, 0.3) == pytest.approx(0.8)

    def test_add_negative_numbers(self):
        """Test adding negative numbers."""
        assert add(-2, -3) == -5
        assert add(-10, 5) == -5
        assert add(10, -5) == 5

    def test_add_zero(self):
        """Test adding zero."""
        assert add(5, 0) == 5
        assert add(0, 5) == 5
        assert add(0, 0) == 0

    def test_add_floats(self):
        """Test adding floating point numbers."""
        assert add(2.5, 3.7) == pytest.approx(6.2)
        assert add(-1.5, 2.5) == pytest.approx(1.0)


class TestSubtraction:
    """Test cases for subtraction operation."""

    def test_subtract_positive_numbers(self):
        """Test subtracting positive numbers."""
        assert subtract(5, 3) == 2
        assert subtract(10, 7) == 3
        assert subtract(3, 5) == -2

    def test_subtract_negative_numbers(self):
        """Test subtracting with negative numbers."""
        assert subtract(-5, -3) == -2
        assert subtract(-5, 3) == -8
        assert subtract(5, -3) == 8

    def test_subtract_zero(self):
        """Test subtracting zero."""
        assert subtract(5, 0) == 5
        assert subtract(0, 5) == -5
        assert subtract(0, 0) == 0

    def test_subtract_floats(self):
        """Test subtracting floating point numbers."""
        assert subtract(5.5, 2.3) == pytest.approx(3.2)
        assert subtract(2.1, 5.7) == pytest.approx(-3.6)


class TestMultiplication:
    """Test cases for multiplication operation."""

    def test_multiply_positive_numbers(self):
        """Test multiplying positive numbers."""
        assert multiply(3, 4) == 12
        assert multiply(7, 6) == 42
        assert multiply(0.5, 4) == 2.0

    def test_multiply_negative_numbers(self):
        """Test multiplying with negative numbers."""
        assert multiply(-3, 4) == -12
        assert multiply(-3, -4) == 12
        assert multiply(3, -4) == -12

    def test_multiply_zero(self):
        """Test multiplying by zero."""
        assert multiply(5, 0) == 0
        assert multiply(0, 5) == 0
        assert multiply(0, 0) == 0

    def test_multiply_one(self):
        """Test multiplying by one."""
        assert multiply(5, 1) == 5
        assert multiply(1, 5) == 5

    def test_multiply_floats(self):
        """Test multiplying floating point numbers."""
        assert multiply(2.5, 4) == 10.0
        assert multiply(1.5, 2.5) == pytest.approx(3.75)


class TestDivision:
    """Test cases for division operation."""

    def test_divide_positive_numbers(self):
        """Test dividing positive numbers."""
        assert divide(10, 2) == 5
        assert divide(15, 3) == 5
        assert divide(7, 2) == 3.5

    def test_divide_negative_numbers(self):
        """Test dividing with negative numbers."""
        assert divide(-10, 2) == -5
        assert divide(10, -2) == -5
        assert divide(-10, -2) == 5

    def test_divide_by_one(self):
        """Test dividing by one."""
        assert divide(5, 1) == 5
        assert divide(-5, 1) == -5

    def test_divide_zero_dividend(self):
        """Test dividing zero."""
        assert divide(0, 5) == 0
        assert divide(0, -5) == 0

    def test_divide_by_zero(self):
        """Test division by zero raises ValueError."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(5, 0)

        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(-5, 0)

    def test_divide_floats(self):
        """Test dividing floating point numbers."""
        assert divide(7.5, 2.5) == 3.0
        assert divide(1, 3) == pytest.approx(0.3333333333)


class TestPower:
    """Test cases for power operation."""

    def test_power_positive_integers(self):
        """Test power with positive integers."""
        assert power(2, 3) == 8
        assert power(5, 2) == 25
        assert power(10, 0) == 1

    def test_power_negative_base(self):
        """Test power with negative base."""
        assert power(-2, 3) == -8
        assert power(-2, 2) == 4
        assert power(-5, 0) == 1

    def test_power_negative_exponent(self):
        """Test power with negative exponent."""
        assert power(2, -2) == 0.25
        assert power(5, -1) == 0.2
        assert power(10, -3) == 0.001

    def test_power_fractional_exponent(self):
        """Test power with fractional exponent."""
        assert power(9, 0.5) == 3.0
        assert power(8, 1 / 3) == pytest.approx(2.0, rel=1e-10)

    def test_power_zero_base(self):
        """Test power with zero base."""
        assert power(0, 5) == 0
        assert power(0, 0) == 1  # 0^0 is defined as 1 in Python


class TestSquareRoot:
    """Test cases for square root operation."""

    def test_square_root_perfect_squares(self):
        """Test square root of perfect squares."""
        assert square_root(4) == 2.0
        assert square_root(9) == 3.0
        assert square_root(16) == 4.0
        assert square_root(25) == 5.0

    def test_square_root_non_perfect_squares(self):
        """Test square root of non-perfect squares."""
        assert square_root(2) == pytest.approx(math.sqrt(2))
        assert square_root(3) == pytest.approx(math.sqrt(3))
        assert square_root(10) == pytest.approx(math.sqrt(10))

    def test_square_root_zero(self):
        """Test square root of zero."""
        assert square_root(0) == 0.0

    def test_square_root_one(self):
        """Test square root of one."""
        assert square_root(1) == 1.0

    def test_square_root_negative_number(self):
        """Test square root of negative number raises ValueError."""
        with pytest.raises(
            ValueError, match="Cannot calculate square root of negative number"
        ):
            square_root(-4)

        with pytest.raises(
            ValueError, match="Cannot calculate square root of negative number"
        ):
            square_root(-1)

    def test_square_root_float(self):
        """Test square root of floating point numbers."""
        assert square_root(2.25) == 1.5
        assert square_root(0.25) == 0.5


class TestPercentage:
    """Test cases for percentage operation."""

    def test_percentage_basic(self):
        """Test basic percentage calculations."""
        assert percentage(100, 50) == 50.0
        assert percentage(200, 25) == 50.0
        assert percentage(80, 75) == 60.0

    def test_percentage_zero_base(self):
        """Test percentage of zero."""
        assert percentage(0, 50) == 0.0
        assert percentage(0, 100) == 0.0

    def test_percentage_zero_percent(self):
        """Test zero percentage."""
        assert percentage(100, 0) == 0.0
        assert percentage(50, 0) == 0.0

    def test_percentage_over_hundred(self):
        """Test percentage over 100%."""
        assert percentage(100, 150) == 150.0
        assert percentage(50, 200) == 100.0

    def test_percentage_negative_base(self):
        """Test percentage of negative number."""
        assert percentage(-100, 50) == -50.0
        assert percentage(-50, 25) == -12.5

    def test_percentage_negative_percent(self):
        """Test negative percentage."""
        assert percentage(100, -50) == -50.0
        assert percentage(50, -25) == -12.5

    def test_percentage_floats(self):
        """Test percentage with floating point numbers."""
        assert percentage(33.33, 30) == pytest.approx(9.999)
        assert percentage(123.45, 12.5) == pytest.approx(15.43125)
