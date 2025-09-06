#!/usr/bin/env python3
"""
Test how typing.get_type_hints works with type aliases and localns
"""
from __future__ import annotations

import typing
import sys
sys.path.insert(0, 'tests/roots/test-ext-autodoc/target')

from typing import Dict, Any
from annotations import sum as sum_func, myint

# Create our test case
JSONObject = Dict[str, Any]

def test_func(data: JSONObject) -> JSONObject:
    """Test function with type aliases."""
    return {}

print("=== Testing typing.get_type_hints with different localns ===")

print("\nCase 1: sum_func (myint case)")
print(f"Raw annotations: {sum_func.__annotations__}")

# Without localns
hints1 = typing.get_type_hints(sum_func)
print(f"Without localns: {hints1}")

# With localns containing myint mapped to myint
hints2 = typing.get_type_hints(sum_func, localns={'myint': 'myint'})
print(f"With localns {{'myint': 'myint'}}: {hints2}")

# With localns containing myint mapped to the actual type
hints3 = typing.get_type_hints(sum_func, localns={'myint': myint})
print(f"With localns {{'myint': myint}}: {hints3}")

print("\nCase 2: test_func (JSONObject case)")
print(f"Raw annotations: {test_func.__annotations__}")

# Without localns - this should fail because JSONObject is not in globals of test_func's module
try:
    hints4 = typing.get_type_hints(test_func)
    print(f"Without localns: {hints4}")
except Exception as e:
    print(f"Without localns: ERROR - {e}")

# With localns containing JSONObject
try:
    hints5 = typing.get_type_hints(test_func, localns={'JSONObject': JSONObject})
    print(f"With localns {{'JSONObject': JSONObject}}: {hints5}")
except Exception as e:
    print(f"With localns {{'JSONObject': JSONObject}}: ERROR - {e}")

# With localns containing JSONObject mapped to string
try:
    hints6 = typing.get_type_hints(test_func, localns={'JSONObject': 'types.JSONObject'})
    print(f"With localns {{'JSONObject': 'types.JSONObject'}}: {hints6}")
except Exception as e:
    print(f"With localns {{'JSONObject': 'types.JSONObject'}}: ERROR - {e}")