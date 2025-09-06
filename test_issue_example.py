#!/usr/bin/env python3
"""
Test the exact use case from the issue description
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

# Test without running the full test suite to avoid Jinja2 compatibility issues
def test_issue_example():
    """Test the exact example from the issue"""
    from sphinx.ext.autodoc.typehints import record_typehints
    from collections import OrderedDict
    from typing import Dict, Any
    from sphinx.util import inspect
    from sphinx.util.typing import stringify
    
    # Create the exact function from the issue
    JSONObject = Dict[str, Any]
    
    def sphinx_doc(data: JSONObject) -> JSONObject:
        """Does it work.

        Args:
            data: Does it args.

        Returns:
            Does it work in return.
        """
        return {}
    
    print(f"Function annotations: {sphinx_doc.__annotations__}")
    print(f"JSONObject defined in globals: {'JSONObject' in globals()}")
    print(f"JSONObject type: {JSONObject}")
    
    # Test with the type aliases from the issue - but use a valid alias
    class MockApp:
        def __init__(self):
            self.config = type('Config', (), {})()
            self.config.autodoc_type_aliases = {
                'JSONObject': 'MyJSONObject',  # Use a simpler alias
            }
            self.env = type('Env', (), {})()
            self.env.temp_data = {}
    
    app = MockApp()
    
    # Let's trace what happens during signature processing
    print(f"\nTesting signature processing:")
    try:
        sig = inspect.signature(sphinx_doc, type_aliases=app.config.autodoc_type_aliases)
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
    
    # Also test get_type_hints directly
    import typing
    print(f"\nTesting typing.get_type_hints directly:")
    try:
        hints = typing.get_type_hints(sphinx_doc, localns=app.config.autodoc_type_aliases)
        print(f"Type hints: {hints}")
        for name, hint in hints.items():
            print(f"  {name}: {hint} (type: {type(hint)}) -> {stringify(hint)}")
    except Exception as e:
        print(f"Error with get_type_hints: {e}")
    
    record_typehints(app, 'function', 'sphinx_doc', sphinx_doc, {}, '', '')
    
    annotations = app.env.temp_data.get('annotations', {})
    func_annotations = annotations.get('sphinx_doc', {})
    print(f"\nRecorded annotations: {func_annotations}")
    
    # Check the results
    data_annotation = func_annotations.get('data', '')
    return_annotation = func_annotations.get('return', '')
    
    print(f"data parameter annotation: {data_annotation}")
    print(f"return annotation: {return_annotation}")
    
    # The issue expects MyJSONObject instead of Dict[str, Any]
    if data_annotation == 'MyJSONObject' and return_annotation == 'MyJSONObject':
        print("✓ SUCCESS: Issue is fixed! Type aliases are working correctly.")
        return True
    elif 'Dict[str, Any]' in data_annotation or 'Dict[str, Any]' in return_annotation:
        print("✗ FAILURE: Issue not fixed, still seeing raw Dict[str, Any] type")
        return False
    else:
        print(f"? UNKNOWN: Unexpected result: data='{data_annotation}', return='{return_annotation}'")
        return False

if __name__ == "__main__":
    success = test_issue_example()
    sys.exit(0 if success else 1)