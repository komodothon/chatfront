"""/test/test_eg_1.py"""

import pytest
from eg_1 import divide 

def test_divide_valid():
    assert divide(10, 2) == 5.0

def test_divide_zero():
    with pytest.raises(ValueError) as exc_info:
        divide(10, 0)
    assert str(exc_info.value) == "Cannot divide by zero" 


