// FastAPI Calculator JavaScript

class Calculator {
    constructor() {
        this.display = document.getElementById('display');
        this.currentInput = '';
        this.firstOperand = null;
        this.operator = null;
        this.waitingForOperand = false;
        this.resultElement = document.getElementById('result');
        this.errorElement = document.getElementById('error');
        this.resultValueElement = document.getElementById('resultValue');
        this.errorMessageElement = document.getElementById('errorMessage');
    }

    updateDisplay(value = this.currentInput) {
        this.display.value = value || '0';
    }

    appendToDisplay(digit) {
        if (this.waitingForOperand) {
            this.currentInput = digit;
            this.waitingForOperand = false;
        } else {
            this.currentInput = this.currentInput === '0' ? digit : this.currentInput + digit;
        }
        this.updateDisplay();
        this.hideMessages();
    }

    setOperation(operation) {
        const inputValue = parseFloat(this.currentInput);

        if (this.firstOperand === null) {
            this.firstOperand = inputValue;
        } else if (this.operator) {
            const result = this.performCalculation();
            if (result !== null) {
                this.currentInput = String(result);
                this.firstOperand = result;
                this.updateDisplay();
            } else {
                return; // Error occurred, don't proceed
            }
        }

        this.waitingForOperand = true;
        this.operator = operation;
        this.hideMessages();
    }

    async calculate() {
        const inputValue = parseFloat(this.currentInput);

        if (this.firstOperand !== null && this.operator && !this.waitingForOperand) {
            const result = await this.performCalculation();
            if (result !== null) {
                this.currentInput = String(result);
                this.firstOperand = null;
                this.operator = null;
                this.waitingForOperand = true;
                this.updateDisplay();
                this.showResult(result);
            }
        }
    }

    async calculateSquareRoot() {
        const inputValue = parseFloat(this.currentInput);
        if (isNaN(inputValue)) {
            this.showError('Invalid input');
            return;
        }

        try {
            const response = await fetch('/api/square-root', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ a: inputValue })
            });

            const data = await response.json();

            if (response.ok) {
                this.currentInput = String(data.result);
                this.updateDisplay();
                this.showResult(data.result);
            } else {
                this.showError(data.detail || 'Calculation error');
            }
        } catch (error) {
            this.showError('Network error: ' + error.message);
        }
    }

    async performCalculation() {
        const firstOperand = this.firstOperand;
        const secondOperand = parseFloat(this.currentInput);

        if (isNaN(firstOperand) || isNaN(secondOperand)) {
            this.showError('Invalid operands');
            return null;
        }

        const endpoints = {
            'add': '/api/add',
            'subtract': '/api/subtract',
            'multiply': '/api/multiply',
            'divide': '/api/divide',
            'power': '/api/power',
            'percentage': '/api/percentage'
        };

        const endpoint = endpoints[this.operator];
        if (!endpoint) {
            this.showError('Invalid operation');
            return null;
        }

        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ a: firstOperand, b: secondOperand })
            });

            const data = await response.json();

            if (response.ok) {
                return data.result;
            } else {
                this.showError(data.detail || 'Calculation error');
                return null;
            }
        } catch (error) {
            this.showError('Network error: ' + error.message);
            return null;
        }
    }

    clearDisplay() {
        this.currentInput = '';
        this.firstOperand = null;
        this.operator = null;
        this.waitingForOperand = false;
        this.updateDisplay('0');
        this.hideMessages();
    }

    clearEntry() {
        this.currentInput = '';
        this.updateDisplay('0');
        this.hideMessages();
    }

    showResult(value) {
        this.resultValueElement.textContent = value;
        this.resultElement.style.display = 'block';
        this.errorElement.style.display = 'none';
    }

    showError(message) {
        this.errorMessageElement.textContent = message;
        this.errorElement.style.display = 'block';
        this.resultElement.style.display = 'none';
    }

    hideMessages() {
        this.resultElement.style.display = 'none';
        this.errorElement.style.display = 'none';
    }
}

// Initialize calculator
const calculator = new Calculator();

// Global functions for HTML onclick handlers
function appendToDisplay(digit) {
    calculator.appendToDisplay(digit);
}

function setOperation(operation) {
    calculator.setOperation(operation);
}

function calculate() {
    calculator.calculate();
}

function calculateSquareRoot() {
    calculator.calculateSquareRoot();
}

function clearDisplay() {
    calculator.clearDisplay();
}

function clearEntry() {
    calculator.clearEntry();
}

// Keyboard support
document.addEventListener('keydown', function(event) {
    const key = event.key;
    
    if (key >= '0' && key <= '9' || key === '.') {
        appendToDisplay(key);
    } else if (key === '+') {
        setOperation('add');
    } else if (key === '-') {
        setOperation('subtract');
    } else if (key === '*') {
        setOperation('multiply');
    } else if (key === '/') {
        event.preventDefault(); // Prevent browser search
        setOperation('divide');
    } else if (key === 'Enter' || key === '=') {
        calculate();
    } else if (key === 'Escape' || key === 'c' || key === 'C') {
        clearDisplay();
    } else if (key === 'Backspace') {
        clearEntry();
    }
});

// Initialize display
calculator.updateDisplay('0');