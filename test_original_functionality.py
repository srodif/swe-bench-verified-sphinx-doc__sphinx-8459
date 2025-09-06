#!/usr/bin/env python3
"""
Test the original annotations functionality still works
"""
from __future__ import annotations

import sys
sys.path.insert(0, 'tests/roots/test-ext-autodoc/target')

# Test without running the full test suite to avoid Jinja2 compatibility issues
def test_original_case():
    """Test that the original use case still works"""
    from sphinx.ext.autodoc.typehints import record_typehints
    from collections import OrderedDict
    
    # Import the existing annotations module to test with it
    from annotations import sum as sum_func
    
    print(f"Function annotations: {sum_func.__annotations__}")
    
    # Test case 1: No type aliases (should resolve to int)
    class MockApp1:
        def __init__(self):
            self.config = type('Config', (), {})()
            self.config.autodoc_type_aliases = {}
            self.env = type('Env', (), {})()
            self.env.temp_data = {}
    
    app1 = MockApp1()
    record_typehints(app1, 'function', 'sum_func', sum_func, {}, '', '')
    
    annotations1 = app1.env.temp_data.get('annotations', {})
    func_annotations1 = annotations1.get('sum_func', {})
    print(f"Without type aliases: {func_annotations1}")
    
    # Test case 2: With type aliases (should keep as myint)
    class MockApp2:
        def __init__(self):
            self.config = type('Config', (), {})()
            self.config.autodoc_type_aliases = {'myint': 'myint'}
            self.env = type('Env', (), {})()
            self.env.temp_data = {}
    
    app2 = MockApp2()
    record_typehints(app2, 'function', 'sum_func', sum_func, {}, '', '')
    
    annotations2 = app2.env.temp_data.get('annotations', {})
    func_annotations2 = annotations2.get('sum_func', {})
    print(f"With type aliases: {func_annotations2}")
    
    # Check the results
    success = True
    
    # Without aliases, should resolve to int
    if func_annotations1.get('x') != 'int':
        print(f"✗ FAILURE: Without aliases, expected 'int', got '{func_annotations1.get('x')}'")
        success = False
    
    # With aliases, should stay as myint
    if func_annotations2.get('x') != 'myint':
        print(f"✗ FAILURE: With aliases, expected 'myint', got '{func_annotations2.get('x')}'")
        success = False
        
    if success:
        print("✓ SUCCESS: Both cases work correctly!")
    
    return success

if __name__ == "__main__":
    success = test_original_case()
    sys.exit(0 if success else 1)