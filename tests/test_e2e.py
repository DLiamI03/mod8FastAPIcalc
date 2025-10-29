"""
End-to-End tests for FastAPI Calculator using Playwright.
Tests user interactions with the web interface.
"""

import asyncio
import time

import pytest
from playwright.async_api import Browser, BrowserContext, Page, async_playwright


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def browser():
    """Create a browser instance for the test session."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-dev-shm-usage']  # For CI environments
        )
        yield browser
        await browser.close()


@pytest.fixture
async def page(browser: Browser):
    """Create a new page for each test."""
    context = await browser.new_context()
    page = await context.new_page()
    yield page
    await context.close()


@pytest.fixture
async def calculator_page(page: Page):
    """Navigate to the calculator page."""
    # Assuming the FastAPI server is running on localhost:8000
    # In CI, this will be handled by the GitHub Actions setup
    await page.goto("http://localhost:8000")

    # Wait for the page to load completely
    await page.wait_for_selector("#display")

    # Verify the calculator interface is loaded
    assert await page.title() == "FastAPI Calculator"

    yield page


class TestCalculatorInterface:
    """Test cases for calculator user interface."""

    async def test_page_loads_correctly(self, calculator_page: Page):
        """Test that the calculator page loads with all elements."""
        # Check that the display is present and shows 0
        display = calculator_page.locator("#display")
        await expect(display).to_have_value("0")

        # Check that all number buttons are present
        for i in range(10):
            button = calculator_page.locator(f"text='{i}'")
            await expect(button).to_be_visible()

        # Check that operation buttons are present
        operations = ["+", "-", "×", "÷", "=", "C", "CE", "√", "x^y", "%"]
        for op in operations:
            button = calculator_page.locator(f"text='{op}'")
            await expect(button).to_be_visible()

    async def test_number_input(self, calculator_page: Page):
        """Test that number buttons update the display."""
        display = calculator_page.locator("#display")

        # Click number 1
        await calculator_page.click("text='1'")
        await expect(display).to_have_value("1")

        # Click number 2
        await calculator_page.click("text='2'")
        await expect(display).to_have_value("12")

        # Click number 3
        await calculator_page.click("text='3'")
        await expect(display).to_have_value("123")

    async def test_decimal_point(self, calculator_page: Page):
        """Test decimal point input."""
        display = calculator_page.locator("#display")

        # Click 1, then decimal, then 5
        await calculator_page.click("text='1'")
        await calculator_page.click("text='.'")
        await calculator_page.click("text='5'")

        await expect(display).to_have_value("1.5")

    async def test_clear_functions(self, calculator_page: Page):
        """Test clear and clear entry functions."""
        display = calculator_page.locator("#display")

        # Enter some numbers
        await calculator_page.click("text='1'")
        await calculator_page.click("text='2'")
        await calculator_page.click("text='3'")
        await expect(display).to_have_value("123")

        # Test clear entry (CE)
        await calculator_page.click("text='CE'")
        await expect(display).to_have_value("0")

        # Enter numbers again
        await calculator_page.click("text='4'")
        await calculator_page.click("text='5'")
        await expect(display).to_have_value("45")

        # Test clear (C)
        await calculator_page.click("text='C'")
        await expect(display).to_have_value("0")


class TestBasicCalculations:
    """Test cases for basic arithmetic operations."""

    async def test_addition(self, calculator_page: Page):
        """Test addition operation."""
        display = calculator_page.locator("#display")
        result_element = calculator_page.locator("#result")

        # Calculate 5 + 3
        await calculator_page.click("text='5'")
        await calculator_page.click("text='+'")
        await calculator_page.click("text='3'")
        await calculator_page.click("text='='")

        # Wait for result and verify
        await expect(result_element).to_be_visible()
        result_value = calculator_page.locator("#resultValue")
        await expect(result_value).to_have_text("8")

    async def test_subtraction(self, calculator_page: Page):
        """Test subtraction operation."""
        display = calculator_page.locator("#display")
        result_element = calculator_page.locator("#result")

        # Calculate 10 - 4
        await calculator_page.click("text='1'")
        await calculator_page.click("text='0'")
        await calculator_page.click("text='-'")
        await calculator_page.click("text='4'")
        await calculator_page.click("text='='")

        # Wait for result and verify
        await expect(result_element).to_be_visible()
        result_value = calculator_page.locator("#resultValue")
        await expect(result_value).to_have_text("6")

    async def test_multiplication(self, calculator_page: Page):
        """Test multiplication operation."""
        result_element = calculator_page.locator("#result")

        # Calculate 6 × 7
        await calculator_page.click("text='6'")
        await calculator_page.click("text='×'")
        await calculator_page.click("text='7'")
        await calculator_page.click("text='='")

        # Wait for result and verify
        await expect(result_element).to_be_visible()
        result_value = calculator_page.locator("#resultValue")
        await expect(result_value).to_have_text("42")

    async def test_division(self, calculator_page: Page):
        """Test division operation."""
        result_element = calculator_page.locator("#result")

        # Calculate 15 ÷ 3
        await calculator_page.click("text='1'")
        await calculator_page.click("text='5'")
        await calculator_page.click("text='÷'")
        await calculator_page.click("text='3'")
        await calculator_page.click("text='='")

        # Wait for result and verify
        await expect(result_element).to_be_visible()
        result_value = calculator_page.locator("#resultValue")
        await expect(result_value).to_have_text("5")

    async def test_division_by_zero(self, calculator_page: Page):
        """Test division by zero shows error."""
        error_element = calculator_page.locator("#error")

        # Calculate 5 ÷ 0
        await calculator_page.click("text='5'")
        await calculator_page.click("text='÷'")
        await calculator_page.click("text='0'")
        await calculator_page.click("text='='")

        # Wait for error message and verify
        await expect(error_element).to_be_visible()
        error_message = calculator_page.locator("#errorMessage")
        await expect(error_message).to_contain_text("Cannot divide by zero")


class TestAdvancedOperations:
    """Test cases for advanced mathematical operations."""

    async def test_square_root(self, calculator_page: Page):
        """Test square root operation."""
        result_element = calculator_page.locator("#result")

        # Calculate √16
        await calculator_page.click("text='1'")
        await calculator_page.click("text='6'")
        await calculator_page.click("text='√'")

        # Wait for result and verify
        await expect(result_element).to_be_visible()
        result_value = calculator_page.locator("#resultValue")
        await expect(result_value).to_have_text("4")

    async def test_square_root_negative(self, calculator_page: Page):
        """Test square root of negative number shows error."""
        error_element = calculator_page.locator("#error")

        # Try to calculate √(-4) - this requires entering -4 first
        # Since we don't have a +/- button, we'll test with 0-4 first, then square root
        await calculator_page.click("text='0'")
        await calculator_page.click("text='-'")
        await calculator_page.click("text='4'")
        await calculator_page.click("text='='")

        # Now try square root of the negative result
        await calculator_page.click("text='√'")

        # Wait for error message and verify
        await expect(error_element).to_be_visible()
        error_message = calculator_page.locator("#errorMessage")
        await expect(error_message).to_contain_text(
            "Cannot calculate square root of negative number"
        )

    async def test_power_operation(self, calculator_page: Page):
        """Test power operation."""
        result_element = calculator_page.locator("#result")

        # Calculate 2^3
        await calculator_page.click("text='2'")
        await calculator_page.click("text='x^y'")
        await calculator_page.click("text='3'")
        await calculator_page.click("text='='")

        # Wait for result and verify
        await expect(result_element).to_be_visible()
        result_value = calculator_page.locator("#resultValue")
        await expect(result_value).to_have_text("8")

    async def test_percentage_operation(self, calculator_page: Page):
        """Test percentage operation."""
        result_element = calculator_page.locator("#result")

        # Calculate 50% of 100 (100 % 50)
        await calculator_page.click("text='1'")
        await calculator_page.click("text='0'")
        await calculator_page.click("text='0'")
        await calculator_page.click("text='%'")
        await calculator_page.click("text='5'")
        await calculator_page.click("text='0'")
        await calculator_page.click("text='='")

        # Wait for result and verify
        await expect(result_element).to_be_visible()
        result_value = calculator_page.locator("#resultValue")
        await expect(result_value).to_have_text("50")


class TestKeyboardInput:
    """Test cases for keyboard input support."""

    async def test_number_keys(self, calculator_page: Page):
        """Test keyboard number input."""
        display = calculator_page.locator("#display")

        # Focus on the page and type numbers
        await calculator_page.keyboard.press("1")
        await calculator_page.keyboard.press("2")
        await calculator_page.keyboard.press("3")

        await expect(display).to_have_value("123")

    async def test_operation_keys(self, calculator_page: Page):
        """Test keyboard operation input."""
        result_element = calculator_page.locator("#result")

        # Calculate 5 + 3 using keyboard
        await calculator_page.keyboard.press("5")
        await calculator_page.keyboard.press("+")
        await calculator_page.keyboard.press("3")
        await calculator_page.keyboard.press("Enter")

        # Wait for result and verify
        await expect(result_element).to_be_visible()
        result_value = calculator_page.locator("#resultValue")
        await expect(result_value).to_have_text("8")

    async def test_clear_key(self, calculator_page: Page):
        """Test keyboard clear functionality."""
        display = calculator_page.locator("#display")

        # Type some numbers
        await calculator_page.keyboard.press("1")
        await calculator_page.keyboard.press("2")
        await calculator_page.keyboard.press("3")
        await expect(display).to_have_value("123")

        # Clear with Escape key
        await calculator_page.keyboard.press("Escape")
        await expect(display).to_have_value("0")


class TestChainedCalculations:
    """Test cases for multiple consecutive calculations."""

    async def test_multiple_operations(self, calculator_page: Page):
        """Test performing multiple calculations in sequence."""
        result_element = calculator_page.locator("#result")

        # Calculate 2 + 3
        await calculator_page.click("text='2'")
        await calculator_page.click("text='+'")
        await calculator_page.click("text='3'")
        await calculator_page.click("text='='")

        # Verify first result
        await expect(result_element).to_be_visible()
        result_value = calculator_page.locator("#resultValue")
        await expect(result_value).to_have_text("5")

        # Continue with × 4
        await calculator_page.click("text='×'")
        await calculator_page.click("text='4'")
        await calculator_page.click("text='='")

        # Verify second result
        await expect(result_value).to_have_text("20")

    async def test_complex_calculation(self, calculator_page: Page):
        """Test a complex multi-step calculation."""
        result_element = calculator_page.locator("#result")

        # Calculate (10 + 5) × 2 = 30
        await calculator_page.click("text='1'")
        await calculator_page.click("text='0'")
        await calculator_page.click("text='+'")
        await calculator_page.click("text='5'")
        await calculator_page.click("text='='")

        # Should show 15
        await expect(result_element).to_be_visible()
        result_value = calculator_page.locator("#resultValue")
        await expect(result_value).to_have_text("15")

        # Continue with × 2
        await calculator_page.click("text='×'")
        await calculator_page.click("text='2'")
        await calculator_page.click("text='='")

        # Should show 30
        await expect(result_value).to_have_text("30")


# Import the expect function for Playwright assertions
from playwright.async_api import expect
