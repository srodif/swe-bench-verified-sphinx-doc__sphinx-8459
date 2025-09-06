#!/usr/bin/env python3
"""
Simple test to verify the fix for autodoc_type_aliases works with autodoc_typehints='description'
"""
from __future__ import annotations

import sys
sys.path.insert(0, 'tests/roots/test-ext-autodoc/target')

import tempfile
from pathlib import Path

# Test without running the full test suite to avoid Jinja2 compatibility issues
def test_type_aliases_fix():
    """Test the fix by directly calling the record_typehints function"""
    from sphinx.ext.autodoc.typehints import record_typehints
    from sphinx.application import Sphinx
    from sphinx.config import Config
    from sphinx.environment import BuildEnvironment
    from collections import OrderedDict
    from typing import Dict, Any
    
    # Import the existing annotations module to test with it
    from annotations import sum as sum_func
    
    print(f"Function annotations: {sum_func.__annotations__}")
    
    # Mock app with config that has type aliases
    class MockApp:
        def __init__(self):
            self.config = type('Config', (), {})()
            # Use the same mapping as in the test
            self.config.autodoc_type_aliases = {'myint': 'myint'}
            self.env = type('Env', (), {})()
            self.env.temp_data = {}
    
    app = MockApp()
    
    print(f"Type aliases config: {app.config.autodoc_type_aliases}")
    
    # Let's also test the inspect.signature function directly
    from sphinx.util import inspect
    from sphinx.util.typing import stringify
    try:
        sig = inspect.signature(sum_func, type_aliases=app.config.autodoc_type_aliases)
        print(f"Signature parameters from inspect.signature:")
        for param in sig.parameters.values():
            print(f"  {param.name}: {param.annotation} (type: {type(param.annotation)})")
            print(f"    stringified: {stringify(param.annotation)}")
        print(f"Return annotation: {sig.return_annotation} (type: {type(sig.return_annotation)})")
        print(f"  stringified: {stringify(sig.return_annotation)}")
    except Exception as e:
        print(f"Error with inspect.signature: {e}")
        import traceback
        traceback.print_exc()
    
    # Call the record_typehints function
    try:
        record_typehints(app, 'function', 'sum_func', sum_func, {}, '', '')
        
        # Check if annotations were recorded with aliases
        annotations = app.env.temp_data.get('annotations', {})
        func_annotations = annotations.get('sum_func', {})
        
        print("Recorded annotations:", func_annotations)
        
        # Check if the alias was applied
        x_annotation = func_annotations.get('x', '')
        y_annotation = func_annotations.get('y', '')
        return_annotation = func_annotations.get('return', '')
        
        print(f"x parameter annotation: {x_annotation}")
        print(f"y parameter annotation: {y_annotation}")
        print(f"return annotation: {return_annotation}")
        
        # Test if the aliases are applied - should stay as 'myint', not resolve to 'int'
        if x_annotation == 'myint' and y_annotation == 'myint' and return_annotation == 'myint':
            print("✓ SUCCESS: Type aliases are being applied correctly!")
            return True
        elif x_annotation == 'int' or y_annotation == 'int' or return_annotation == 'int':
            print("✗ FAILURE: Type aliases are not being applied, found resolved type instead")
            return False
        else:
            print(f"? UNKNOWN: Unexpected annotation format")
            return False
            
    except Exception as e:
        print(f"Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_type_aliases_fix()
    sys.exit(0 if success else 1)