#!/usr/bin/env python3
"""
Test to understand the difference between myint and JSONObject cases
"""
from __future__ import annotations

import sys
sys.path.insert(0, 'tests/roots/test-ext-autodoc/target')

from typing import Dict, Any
from sphinx.util import inspect
from sphinx.util.typing import stringify

# Import the annotations module
from annotations import sum as sum_func, myint

# Create our test case
JSONObject = Dict[str, Any]

def test_func(data: JSONObject) -> JSONObject:
    """Test function with type aliases."""
    return {}

print("=== MYINT CASE (working) ===")
print(f"myint in module globals: {myint}")
print(f"sum_func annotations: {sum_func.__annotations__}")

print("\n=== JSONOBJECT CASE (not working) ===")
print(f"JSONObject in local scope: {JSONObject}")
print(f"test_func annotations: {test_func.__annotations__}")

print("\n=== Testing signature processing ===")

# Test case 1: myint with type aliases
print("\nCase 1: myint with type aliases {'myint': 'myint'}")
try:
    sig1 = inspect.signature(sum_func, type_aliases={'myint': 'myint'})
    for param in sig1.parameters.values():
        print(f"  {param.name}: {param.annotation} -> {stringify(param.annotation)}")
    print(f"  return: {sig1.return_annotation} -> {stringify(sig1.return_annotation)}")
except Exception as e:
    print(f"Error: {e}")

# Test case 2: myint without type aliases 
print("\nCase 2: myint without type aliases")
try:
    sig2 = inspect.signature(sum_func, type_aliases={})
    for param in sig2.parameters.values():
        print(f"  {param.name}: {param.annotation} -> {stringify(param.annotation)}")
    print(f"  return: {sig2.return_annotation} -> {stringify(sig2.return_annotation)}")
except Exception as e:
    print(f"Error: {e}")

# Test case 3: JSONObject with type aliases
print("\nCase 3: JSONObject with type aliases {'JSONObject': 'types.JSONObject'}")
try:
    sig3 = inspect.signature(test_func, type_aliases={'JSONObject': 'types.JSONObject'})
    for param in sig3.parameters.values():
        print(f"  {param.name}: {param.annotation} -> {stringify(param.annotation)}")
    print(f"  return: {sig3.return_annotation} -> {stringify(sig3.return_annotation)}")
except Exception as e:
    print(f"Error: {e}")

# Test case 4: JSONObject without type aliases
print("\nCase 4: JSONObject without type aliases")
try:
    sig4 = inspect.signature(test_func, type_aliases={})
    for param in sig4.parameters.values():
        print(f"  {param.name}: {param.annotation} -> {stringify(param.annotation)}")
    print(f"  return: {sig4.return_annotation} -> {stringify(sig4.return_annotation)}")
except Exception as e:
    print(f"Error: {e}")

print("\n=== Module globals comparison ===")
import annotations
print(f"annotations module globals contains 'myint': {'myint' in dir(annotations)}")
print(f"current module globals contains 'JSONObject': {'JSONObject' in globals()}")