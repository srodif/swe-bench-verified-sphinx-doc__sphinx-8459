#!/usr/bin/env python3
"""
Test how inspect.signature works with the annotations module
"""

import sys
sys.path.insert(0, 'tests/roots/test-ext-autodoc/target')

from annotations import sum as sum_func, myint
from sphinx.util import inspect
from sphinx.util.typing import stringify

print(f"myint: {myint}")
print(f"type of myint: {type(myint)}")

# Test 1: Regular signature
print("\nTest 1: Regular signature")
sig1 = inspect.signature(sum_func)
print(f"Parameters:")
for param in sig1.parameters.values():
    print(f"  {param.name}: {param.annotation} (type: {type(param.annotation)})")
    print(f"    stringified: {stringify(param.annotation)}")
print(f"Return: {sig1.return_annotation} (type: {type(sig1.return_annotation)})")
print(f"  stringified: {stringify(sig1.return_annotation)}")

# Test 2: With type aliases
print("\nTest 2: With type aliases")
type_aliases = {'myint': 'myint'}
sig2 = inspect.signature(sum_func, type_aliases=type_aliases)
print(f"Parameters:")
for param in sig2.parameters.values():
    print(f"  {param.name}: {param.annotation} (type: {type(param.annotation)})")
    print(f"    stringified: {stringify(param.annotation)}")
print(f"Return: {sig2.return_annotation} (type: {type(sig2.return_annotation)})")
print(f"  stringified: {stringify(sig2.return_annotation)}")

# Test 3: With type aliases mapping to a different object
print("\nTest 3: With type aliases mapping to different object")
type_aliases = {'myint': myint}
sig3 = inspect.signature(sum_func, type_aliases=type_aliases)
print(f"Parameters:")
for param in sig3.parameters.values():
    print(f"  {param.name}: {param.annotation} (type: {type(param.annotation)})")
    print(f"    stringified: {stringify(param.annotation)}")
print(f"Return: {sig3.return_annotation} (type: {type(sig3.return_annotation)})")
print(f"  stringified: {stringify(sig3.return_annotation)}")