# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

sys.path.insert(0, os.path.abspath("../../pydantic-modelgen/src/pydanticmodelgen"))
import pydanticmodelgen  # noqa


project = "pydantic-modelgen"
copyright = "2024, Niklas von Moers"
author = "Niklas von Moers"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",  # For generating API docs
    "sphinx.ext.napoleon",  # For Google-style docstrings
]

templates_path = ["_templates"]
exclude_patterns = []
autodoc_mock_imports = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
html_static_path = ["_static"]
