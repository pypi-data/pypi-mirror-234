from Calculator_martynara.calculator_martynara import Calculator
import pytest

# Create a fixture for the Calculator instance
@pytest.fixture
def calculator():
    return Calculator()

# Test cases for the Calculator class
def test_insert(calculator):
    assert calculator.insert(5) == 5  # Inserting a value should update memory to 5

def test_reset(calculator):
    assert calculator.reset() == 0  # Reset should set memory to 0

def test_add(calculator):
    calculator.insert(5)
    assert calculator.add(3) == 8  # Adding 3 to 5 should give 8

def test_add_neg(calculator):
    calculator.insert(5)
    assert calculator.add(-3) == 2  # Adding -3 to 5 should give 2

def test_subtract(calculator):
    calculator.insert(10)
    assert calculator.subtract(3) == 7  # Subtracting 3 from 10 should give 7

def test_multiply(calculator):
    calculator.insert(4)
    assert calculator.multiply(2) == 8  # Multiplying 4 by 2 should give 8

def test_divide(calculator):
    calculator.insert(12)
    assert calculator.divide(3) == 4  # Dividing 12 by 3 should give 4

def test_root(calculator):
    calculator.insert(16)
    assert calculator.root(2) == 4  # Taking the square root of 16 should give 4

def test_divide_by_zero(calculator):
    calculator.insert(10)
    with pytest.raises(ZeroDivisionError):
        calculator.divide(0)  # Dividing by zero should raise a ZeroDivisionError

def test_root_with_power_zero(calculator):
    calculator.insert(10)
    assert calculator.root(0) == 10  # Taking the 0th root should give the original value

# Mixed method tests
def test_insert_and_multiply(calculator):
    assert calculator.insert(4) == 4
    assert calculator.multiply(2) == 8
    assert calculator.multiply(0.5) == 4  # Multiplying by a decimal

def test_insert_and_root(calculator):
    assert calculator.insert(16) == 16
    assert calculator.root(2) == 4
    assert calculator.root(3) == 1.5874  # Calculating a non-integer root

def test_insert_and_reset_and_root(calculator):
    calculator.insert(27)
    calculator.reset()
    assert calculator.root(3) == 0.0  # Root of 0 after reset
    
if __name__ == "__main":
    pytest.main()
