# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
from pathlib import Path
sys.path.insert(0, os.path.abspath(os.path.join('..', '..')))

# -- Auto-generate API docs on every build -----------------------------------
from sphinx.ext.apidoc import main as apidoc_main

def run_apidoc(_):
    source_dir = str(Path(__file__).parent)
    package_dir = str(Path(__file__).parent.parent.parent / 'mb')
    apidoc_main([
        '--force',            # overwrite existing files
        '--module-first',     # put module docstring before submodule list
        '--separate',         # one page per module
        '-o', source_dir,     # output into docs/source/
        package_dir,          # the package to document
    ])

def setup(app):
    app.connect('builder-inited', run_apidoc)

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'mb_utils'
copyright = '2026, Malav'
author = 'Malav'
release = '2.0.27'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

autodoc_member_order = 'bysource'
autosummary_generate = True

autodoc_mock_imports = [
    'colorama',
    'boto3',
    'tqdm',
    'pandas',
    'PIL',
    'yaml',
    'line_profiler',
    'snakeviz',
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
# html_static_path = ['_static']
