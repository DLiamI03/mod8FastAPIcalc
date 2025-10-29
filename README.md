# FastAPI Calculator

A comprehensive calculator application built with FastAPI, featuring a web interface, REST API endpoints, comprehensive testing, and continuous integration.

## Features

- **Web Interface**: Modern, responsive calculator UI
- **REST API**: Complete set of API endpoints for arithmetic operations
- **Comprehensive Testing**: Unit, integration, and end-to-end tests
- **Logging**: Detailed logging for operations and error tracking
- **CI/CD**: GitHub Actions workflow for automated testing
- **Code Quality**: Linting, formatting, and type checking

## Supported Operations

- ➕ **Addition**: Add two numbers
- ➖ **Subtraction**: Subtract two numbers
- ✖️ **Multiplication**: Multiply two numbers
- ➗ **Division**: Divide two numbers (with zero-division protection)
- 🔢 **Power**: Raise a number to a power
- √ **Square Root**: Calculate square root (with negative number protection)
- % **Percentage**: Calculate percentage of a number

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd fastapi-calculator
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers (for E2E tests)**
   ```bash
   playwright install
   ```

### Running the Application

1. **Start the FastAPI server**
   ```bash
   uvicorn main:app --reload
   ```

2. **Access the application**
   - Web Interface: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Alternative API Docs: http://localhost:8000/redoc

## API Endpoints

### Base URL: `http://localhost:8000`

| Endpoint | Method | Description | Request Body | Response |
|----------|--------|-------------|--------------|----------|
| `/` | GET | Web interface | - | HTML page |
| `/health` | GET | Health check | - | `{"status": "healthy"}` |
| `/api/add` | POST | Addition | `{"a": number, "b": number}` | `{"result": number, "operation": "addition", "operands": {...}}` |
| `/api/subtract` | POST | Subtraction | `{"a": number, "b": number}` | `{"result": number, "operation": "subtraction", "operands": {...}}` |
| `/api/multiply` | POST | Multiplication | `{"a": number, "b": number}` | `{"result": number, "operation": "multiplication", "operands": {...}}` |
| `/api/divide` | POST | Division | `{"a": number, "b": number}` | `{"result": number, "operation": "division", "operands": {...}}` |
| `/api/power` | POST | Power | `{"a": number, "b": number}` | `{"result": number, "operation": "power", "operands": {...}}` |
| `/api/square-root` | POST | Square Root | `{"a": number}` | `{"result": number, "operation": "square_root", "operands": {...}}` |
| `/api/percentage` | POST | Percentage | `{"a": number, "b": number}` | `{"result": number, "operation": "percentage", "operands": {...}}` |

### Example API Usage

```bash
# Addition
curl -X POST "http://localhost:8000/api/add" \
     -H "Content-Type: application/json" \
     -d '{"a": 5, "b": 3}'

# Response: {"result": 8, "operation": "addition", "operands": {"a": 5, "b": 3}}
```

```bash
# Square Root
curl -X POST "http://localhost:8000/api/square-root" \
     -H "Content-Type: application/json" \
     -d '{"a": 16}'

# Response: {"result": 4.0, "operation": "square_root", "operands": {"a": 16}}
```

## Testing

The application includes comprehensive test coverage:

### Running All Tests

```bash
pytest
```

### Running Specific Test Types

```bash
# Unit tests only
pytest tests/test_operations.py -v

# Integration tests only
pytest tests/test_integration.py -v

# End-to-end tests only
pytest tests/test_e2e.py -v
```

### Test Coverage

```bash
# Generate coverage report
pytest --cov=app --cov-report=html

# View coverage report
open htmlcov/index.html
```

### Test Categories

1. **Unit Tests** (`test_operations.py`)
   - Test all mathematical operations
   - Input validation and error handling
   - Edge cases (division by zero, negative square roots)

2. **Integration Tests** (`test_integration.py`)
   - API endpoint functionality
   - Request/response validation
   - Error handling and status codes

3. **End-to-End Tests** (`test_e2e.py`)
   - Web interface interactions
   - User workflows
   - Keyboard input support

## Project Structure

```
fastapi-calculator/
├── app/
│   └── operations.py          # Mathematical operations
├── static/
│   ├── style.css             # CSS styles
│   └── calculator.js         # Frontend JavaScript
├── templates/
│   └── calculator.html       # HTML template
├── tests/
│   ├── test_operations.py    # Unit tests
│   ├── test_integration.py   # Integration tests
│   └── test_e2e.py          # End-to-end tests
├── .github/workflows/
│   └── ci.yml               # GitHub Actions CI
├── main.py                  # FastAPI application
├── requirements.txt         # Python dependencies
├── pytest.ini             # Pytest configuration
└── README.md              # This file
```

## Development

### Code Quality Tools

The project uses several tools to maintain code quality:

```bash
# Format code with Black
black .

# Sort imports with isort
isort .

# Lint with flake8
flake8 .

# Type checking with mypy
mypy app/
```

### Adding New Operations

1. **Add the mathematical function** to `app/operations.py`
2. **Create API endpoint** in `main.py`
3. **Add unit tests** in `tests/test_operations.py`
4. **Add integration tests** in `tests/test_integration.py`
5. **Update frontend** (if applicable) in `static/calculator.js` and `templates/calculator.html`

### Logging

The application logs all operations and errors to:
- Console output
- `calculator.log` file

Log levels:
- **INFO**: Successful operations
- **ERROR**: Error conditions (division by zero, invalid inputs)

## Continuous Integration

GitHub Actions workflow automatically:

1. **Tests** the application on multiple Python versions (3.9, 3.10, 3.11)
2. **Lints** code with flake8
3. **Checks** code formatting with Black and isort
4. **Performs** type checking with mypy
5. **Runs** all test suites (unit, integration, E2E)
6. **Generates** coverage reports
7. **Performs** security checks with safety and bandit

### Workflow Status

The CI workflow runs on:
- Push to `main` or `develop` branches
- Pull requests to `main` branch

## Deployment

### Local Development Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Server

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker (Optional)

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Browser Support

The web interface supports modern browsers:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### Keyboard Shortcuts

- **Numbers (0-9)**: Enter digits
- **+, -, *, /**: Mathematical operations
- **Enter or =**: Calculate result
- **Escape or C**: Clear all
- **Backspace**: Clear entry

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Kill process on port 8000
   lsof -ti:8000 | xargs kill -9
   ```

2. **Playwright browser not found**
   ```bash
   playwright install chromium
   ```

3. **Module not found errors**
   ```bash
   # Ensure you're in the project directory and virtual environment is activated
   pip install -r requirements.txt
   ```

### Error Handling

The application handles various error conditions:
- **Division by zero**: Returns HTTP 400 with error message
- **Square root of negative**: Returns HTTP 400 with error message
- **Invalid input**: Returns HTTP 422 with validation error
- **Server errors**: Returns HTTP 500 with generic error message

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- FastAPI framework for the excellent web framework
- Playwright for robust end-to-end testing
- pytest for comprehensive testing framework
- GitHub Actions for CI/CD automation