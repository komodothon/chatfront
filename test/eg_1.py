"""/test/eg_1.py"""

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
