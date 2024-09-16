import os
import sys
sys.path.insert(0, os.path.abspath('../../'))


project = 'sprynger'
copyright = '2024, Nils Herrmann'
author = 'Nils Herrmann'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',  # Optional: for Google and NumPy style docstrings
]

templates_path = ['_templates']
exclude_patterns = []

autoclass_content = "both"  # Document both class-level and __init__ method docstrings


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
