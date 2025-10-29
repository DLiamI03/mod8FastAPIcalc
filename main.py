"""
FastAPI Calculator Application.
Provides REST API endpoints for basic arithmetic operations.
"""

import logging
from pathlib import Path
from typing import Union

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, validator

from app.operations import (
    add,
    divide,
    multiply,
    percentage,
    power,
    square_root,
    subtract,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("calculator.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="FastAPI Calculator",
    description="A comprehensive calculator API with web interface",
    version="1.0.0",
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")


# Pydantic models for request/response
class CalculationRequest(BaseModel):
    """Model for calculation requests with two operands."""

    a: Union[int, float]
    b: Union[int, float]


class SingleOperandRequest(BaseModel):
    """Model for calculation requests with single operand."""

    a: Union[int, float]


class CalculationResponse(BaseModel):
    """Model for calculation responses."""

    result: Union[int, float]
    operation: str
    operands: dict


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the calculator web interface."""
    logger.info("Serving calculator web interface")
    return templates.TemplateResponse(request, "calculator.html")


@app.post("/api/add", response_model=CalculationResponse)
async def api_add(calculation: CalculationRequest):
    """
    Add two numbers.

    Args:
        calculation: Request containing two numbers to add

    Returns:
        CalculationResponse with the sum
    """
    try:
        logger.info(f"API addition request: {calculation.a} + {calculation.b}")
        result = add(calculation.a, calculation.b)
        return CalculationResponse(
            result=result,
            operation="addition",
            operands={"a": calculation.a, "b": calculation.b},
        )
    except Exception as e:
        logger.error(f"Addition error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/subtract", response_model=CalculationResponse)
async def api_subtract(calculation: CalculationRequest):
    """
    Subtract second number from first number.

    Args:
        calculation: Request containing two numbers for subtraction

    Returns:
        CalculationResponse with the difference
    """
    try:
        logger.info(f"API subtraction request: {calculation.a} - {calculation.b}")
        result = subtract(calculation.a, calculation.b)
        return CalculationResponse(
            result=result,
            operation="subtraction",
            operands={"a": calculation.a, "b": calculation.b},
        )
    except Exception as e:
        logger.error(f"Subtraction error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/multiply", response_model=CalculationResponse)
async def api_multiply(calculation: CalculationRequest):
    """
    Multiply two numbers.

    Args:
        calculation: Request containing two numbers to multiply

    Returns:
        CalculationResponse with the product
    """
    try:
        logger.info(f"API multiplication request: {calculation.a} * {calculation.b}")
        result = multiply(calculation.a, calculation.b)
        return CalculationResponse(
            result=result,
            operation="multiplication",
            operands={"a": calculation.a, "b": calculation.b},
        )
    except Exception as e:
        logger.error(f"Multiplication error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/divide", response_model=CalculationResponse)
async def api_divide(calculation: CalculationRequest):
    """
    Divide first number by second number.

    Args:
        calculation: Request containing dividend and divisor

    Returns:
        CalculationResponse with the quotient

    Raises:
        HTTPException: If division by zero is attempted
    """
    try:
        logger.info(f"API division request: {calculation.a} / {calculation.b}")
        result = divide(calculation.a, calculation.b)
        return CalculationResponse(
            result=result,
            operation="division",
            operands={"a": calculation.a, "b": calculation.b},
        )
    except ValueError as e:
        logger.error(f"Division error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Division error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/api/power", response_model=CalculationResponse)
async def api_power(calculation: CalculationRequest):
    """
    Raise first number to the power of second number.

    Args:
        calculation: Request containing base and exponent

    Returns:
        CalculationResponse with the result
    """
    try:
        logger.info(f"API power request: {calculation.a} ^ {calculation.b}")
        result = power(calculation.a, calculation.b)
        return CalculationResponse(
            result=result,
            operation="power",
            operands={"a": calculation.a, "b": calculation.b},
        )
    except Exception as e:
        logger.error(f"Power error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/square-root", response_model=CalculationResponse)
async def api_square_root(calculation: SingleOperandRequest):
    """
    Calculate square root of a number.

    Args:
        calculation: Request containing number to find square root of

    Returns:
        CalculationResponse with the square root

    Raises:
        HTTPException: If square root of negative number is attempted
    """
    try:
        logger.info(f"API square root request: √{calculation.a}")
        result = square_root(calculation.a)
        return CalculationResponse(
            result=result, operation="square_root", operands={"a": calculation.a}
        )
    except ValueError as e:
        logger.error(f"Square root error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Square root error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/api/percentage", response_model=CalculationResponse)
async def api_percentage(calculation: CalculationRequest):
    """
    Calculate percentage of a number.

    Args:
        calculation: Request containing base number and percentage

    Returns:
        CalculationResponse with the percentage result
    """
    try:
        logger.info(f"API percentage request: {calculation.b}% of {calculation.a}")
        result = percentage(calculation.a, calculation.b)
        return CalculationResponse(
            result=result,
            operation="percentage",
            operands={"a": calculation.a, "b": calculation.b},
        )
    except Exception as e:
        logger.error(f"Percentage error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    logger.info("Health check requested")
    return {"status": "healthy", "message": "Calculator API is running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
