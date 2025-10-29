"""
Integration tests for FastAPI Calculator endpoints.
Tests all API endpoints using FastAPI TestClient.
"""

import pytest
from fastapi.testclient import TestClient

from main import app

# Create test client
client = TestClient(app)


class TestHealthEndpoint:
    """Test cases for health check endpoint."""

    def test_health_check(self):
        """Test health check endpoint returns correct response."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "message" in data


class TestRootEndpoint:
    """Test cases for root endpoint."""

    def test_root_endpoint(self):
        """Test root endpoint serves HTML."""
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]


class TestAdditionEndpoint:
    """Test cases for addition API endpoint."""

    def test_add_positive_numbers(self):
        """Test addition with positive numbers."""
        response = client.post("/api/add", json={"a": 2, "b": 3})
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 5
        assert data["operation"] == "addition"
        assert data["operands"]["a"] == 2
        assert data["operands"]["b"] == 3

    def test_add_negative_numbers(self):
        """Test addition with negative numbers."""
        response = client.post("/api/add", json={"a": -5, "b": -3})
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == -8

    def test_add_floats(self):
        """Test addition with floating point numbers."""
        response = client.post("/api/add", json={"a": 2.5, "b": 3.7})
        assert response.status_code == 200
        data = response.json()
        assert abs(data["result"] - 6.2) < 0.0001

    def test_add_with_zero(self):
        """Test addition with zero."""
        response = client.post("/api/add", json={"a": 5, "b": 0})
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 5

    def test_add_invalid_input(self):
        """Test addition with invalid input."""
        response = client.post("/api/add", json={"a": "invalid", "b": 3})
        assert response.status_code == 422  # Validation error

    def test_add_missing_parameters(self):
        """Test addition with missing parameters."""
        response = client.post("/api/add", json={"a": 5})
        assert response.status_code == 422  # Validation error


class TestSubtractionEndpoint:
    """Test cases for subtraction API endpoint."""

    def test_subtract_positive_numbers(self):
        """Test subtraction with positive numbers."""
        response = client.post("/api/subtract", json={"a": 10, "b": 3})
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 7
        assert data["operation"] == "subtraction"

    def test_subtract_negative_result(self):
        """Test subtraction resulting in negative number."""
        response = client.post("/api/subtract", json={"a": 3, "b": 10})
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == -7

    def test_subtract_floats(self):
        """Test subtraction with floating point numbers."""
        response = client.post("/api/subtract", json={"a": 5.5, "b": 2.3})
        assert response.status_code == 200
        data = response.json()
        assert abs(data["result"] - 3.2) < 0.0001


class TestMultiplicationEndpoint:
    """Test cases for multiplication API endpoint."""

    def test_multiply_positive_numbers(self):
        """Test multiplication with positive numbers."""
        response = client.post("/api/multiply", json={"a": 4, "b": 5})
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 20
        assert data["operation"] == "multiplication"

    def test_multiply_by_zero(self):
        """Test multiplication by zero."""
        response = client.post("/api/multiply", json={"a": 5, "b": 0})
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 0

    def test_multiply_negative_numbers(self):
        """Test multiplication with negative numbers."""
        response = client.post("/api/multiply", json={"a": -3, "b": 4})
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == -12

    def test_multiply_floats(self):
        """Test multiplication with floating point numbers."""
        response = client.post("/api/multiply", json={"a": 2.5, "b": 4})
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 10.0


class TestDivisionEndpoint:
    """Test cases for division API endpoint."""

    def test_divide_positive_numbers(self):
        """Test division with positive numbers."""
        response = client.post("/api/divide", json={"a": 10, "b": 2})
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 5
        assert data["operation"] == "division"

    def test_divide_floats(self):
        """Test division with floating point numbers."""
        response = client.post("/api/divide", json={"a": 7.5, "b": 2.5})
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 3.0

    def test_divide_by_zero(self):
        """Test division by zero returns error."""
        response = client.post("/api/divide", json={"a": 5, "b": 0})
        assert response.status_code == 400
        data = response.json()
        assert "Cannot divide by zero" in data["detail"]

    def test_divide_zero_dividend(self):
        """Test dividing zero."""
        response = client.post("/api/divide", json={"a": 0, "b": 5})
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 0


class TestPowerEndpoint:
    """Test cases for power API endpoint."""

    def test_power_positive_integers(self):
        """Test power with positive integers."""
        response = client.post("/api/power", json={"a": 2, "b": 3})
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 8
        assert data["operation"] == "power"

    def test_power_zero_exponent(self):
        """Test power with zero exponent."""
        response = client.post("/api/power", json={"a": 5, "b": 0})
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 1

    def test_power_negative_exponent(self):
        """Test power with negative exponent."""
        response = client.post("/api/power", json={"a": 2, "b": -2})
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 0.25

    def test_power_fractional_exponent(self):
        """Test power with fractional exponent."""
        response = client.post("/api/power", json={"a": 9, "b": 0.5})
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 3.0


class TestSquareRootEndpoint:
    """Test cases for square root API endpoint."""

    def test_square_root_perfect_square(self):
        """Test square root of perfect square."""
        response = client.post("/api/square-root", json={"a": 16})
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 4.0
        assert data["operation"] == "square_root"
        assert "a" in data["operands"]

    def test_square_root_zero(self):
        """Test square root of zero."""
        response = client.post("/api/square-root", json={"a": 0})
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 0.0

    def test_square_root_negative_number(self):
        """Test square root of negative number returns error."""
        response = client.post("/api/square-root", json={"a": -4})
        assert response.status_code == 400
        data = response.json()
        assert "Cannot calculate square root of negative number" in data["detail"]

    def test_square_root_float(self):
        """Test square root with floating point number."""
        response = client.post("/api/square-root", json={"a": 2.25})
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 1.5


class TestPercentageEndpoint:
    """Test cases for percentage API endpoint."""

    def test_percentage_basic(self):
        """Test basic percentage calculation."""
        response = client.post("/api/percentage", json={"a": 100, "b": 50})
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 50.0
        assert data["operation"] == "percentage"

    def test_percentage_zero_base(self):
        """Test percentage of zero."""
        response = client.post("/api/percentage", json={"a": 0, "b": 50})
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 0.0

    def test_percentage_zero_percent(self):
        """Test zero percentage."""
        response = client.post("/api/percentage", json={"a": 100, "b": 0})
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 0.0

    def test_percentage_over_hundred(self):
        """Test percentage over 100%."""
        response = client.post("/api/percentage", json={"a": 100, "b": 150})
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 150.0

    def test_percentage_floats(self):
        """Test percentage with floating point numbers."""
        response = client.post("/api/percentage", json={"a": 200, "b": 25})
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 50.0


class TestAPIValidation:
    """Test cases for API input validation."""

    def test_invalid_json(self):
        """Test endpoints with invalid JSON."""
        response = client.post("/api/add", data="invalid json")
        assert response.status_code == 422

    def test_empty_request(self):
        """Test endpoints with empty request."""
        response = client.post("/api/add", json={})
        assert response.status_code == 422

    def test_extra_fields(self):
        """Test endpoints ignore extra fields."""
        response = client.post("/api/add", json={"a": 2, "b": 3, "extra": "field"})
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 5

    def test_string_numbers(self):
        """Test endpoints with string representations of numbers."""
        response = client.post("/api/add", json={"a": "2", "b": "3"})
        # Pydantic automatically converts string numbers to numbers, so this should succeed
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 5


class TestErrorHandling:
    """Test cases for error handling."""

    def test_nonexistent_endpoint(self):
        """Test request to non-existent endpoint."""
        response = client.post("/api/nonexistent", json={"a": 1, "b": 2})
        assert response.status_code == 404

    def test_wrong_method(self):
        """Test wrong HTTP method."""
        response = client.get("/api/add")
        assert response.status_code == 405  # Method not allowed
