#!/usr/bin/env python3
"""
Test how typing.get_type_hints works with localns parameter
"""

import typing
from typing import Dict, Any

# Define a type alias
JSONObject = Dict[str, Any]

def test_func(data: JSONObject) -> JSONObject:
    """Test function with type aliases."""
    return {}

# Test 1: Without localns
print("Test 1: Without localns")
hints1 = typing.get_type_hints(test_func)
print(f"Hints: {hints1}")

# Test 2: With localns containing the type alias
print("\nTest 2: With localns containing type alias")
localns = {'JSONObject': JSONObject}
hints2 = typing.get_type_hints(test_func, localns=localns)
print(f"Hints: {hints2}")

# Test 3: With localns containing string replacement (this should not work)
print("\nTest 3: With localns containing string replacement")
localns_str = {'JSONObject': 'test.JSONObject'}
try:
    hints3 = typing.get_type_hints(test_func, localns=localns_str)
    print(f"Hints: {hints3}")
except Exception as e:
    print(f"Error: {e}")

# Test 4: What happens in the current module namespace
print("\nTest 4: Current module namespace")
print(f"JSONObject in globals: {'JSONObject' in globals()}")
print(f"JSONObject type: {type(JSONObject)}")