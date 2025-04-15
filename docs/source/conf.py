"""Sphinx configuration."""
import os
import sys

try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:
    import tomli as tomllib 

sys.path.insert(0, os.path.abspath('../../'))

with open('../../pyproject.toml', 'rb') as f:
    toml_data = tomllib.load(f)
    release = toml_data['project']['version']
    project = toml_data['project']['name']
    author = toml_data['project']['authors'][0].get('name')

copyright = '2024, Nils A. Herrmann de Alba'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',  # Optional: for Google and NumPy style docstrings
    'sphinx_copybutton'
]
copybutton_prompt_text = ">>> "

templates_path = ['_templates']
exclude_patterns = []

autoclass_content = "both"  # Document both class-level and __init__ method docstrings


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
