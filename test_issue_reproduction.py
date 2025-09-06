#!/usr/bin/env python3
"""Test script to reproduce the autodoc_type_aliases issue."""

import tempfile
import os
from pathlib import Path
from sphinx.application import Sphinx
from sphinx.util.docutils import docutils_namespace

def test_issue_reproduction():
    """Test that reproduces the issue with autodoc_type_aliases not working when autodoc_typehints is 'description'."""
    
    # Create a temporary directory for the test
    with tempfile.TemporaryDirectory() as tmpdir:
        srcdir = Path(tmpdir) / "source"
        outdir = Path(tmpdir) / "build"
        doctreedir = outdir / ".doctrees"
        confdir = srcdir
        
        srcdir.mkdir(parents=True)
        outdir.mkdir(parents=True)
        
        # Create the test Python module
        types_py = srcdir / "types.py"
        types_py.write_text('''
from __future__ import annotations

from typing import Any, Dict

JSONObject = Dict[str, Any]


def sphinx_doc(data: JSONObject) -> JSONObject:
    """Does it work.

    Args:
        data: Does it args.

    Returns:
        Does it work in return.
    """
    return {}
''')
        
        # Create the conf.py file
        conf_py = srcdir / "conf.py"
        conf_py.write_text('''
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon']

autodoc_typehints = 'description'
autodoc_type_aliases = {
    'JSONObject': 'types.JSONObject',
}
''')
        
        # Create the index.rst file
        index_rst = srcdir / "index.rst"
        index_rst.write_text('''
Test Documentation
==================

.. autofunction:: types.sphinx_doc
''')
        
        # Build the documentation
        with docutils_namespace():
            app = Sphinx(
                srcdir=str(srcdir),
                confdir=str(confdir),
                outdir=str(outdir),
                doctreedir=str(doctreedir),
                buildername='html'
            )
            app.build()
        
        # Check the output
        html_file = outdir / "index.html"
        content = html_file.read_text()
        
        print("HTML Content:")
        print(content)
        
        # Check if the type aliases are applied correctly
        if "types.JSONObject" in content:
            print("✓ SUCCESS: Type aliases are working correctly!")
        elif "Dict[str, Any]" in content:
            print("✗ FAILURE: Type aliases are not working, found Dict[str, Any] instead")
        else:
            print("? UNKNOWN: Could not determine if type aliases are working")

if __name__ == "__main__":
    test_issue_reproduction()