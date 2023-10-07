import datetime
import os
import sys

from dap import __maintainer__, __version__
from sphinx_doc.autodoc import process_docstring, skip_member
from sphinx.application import Sphinx

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath(".."))

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Data Access Platform Client Library"
copyright = f"{datetime.datetime.now().year}, Instructure, Inc."
author = __maintainer__

version = __version__
release = __version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",  # Documentation from doc-strings
    "sphinx.ext.todo",  # to-do syntax highlighting
    "sphinx.ext.ifconfig",  # Content based configuration
    "sphinx_rtd_theme",
    "myst_parser",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", ".mypy_cache", ".pytest_cache"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "navigation_depth": 3,
    "collapse_navigation": True,
    "sticky_navigation": True,
}
html_static_path = ["_static"]
html_show_sourcelink = False
html_show_sphinx = False
html_show_copyright = True

# -- Options including documentation from Python doc-strings -----------------

autoclass_content = "class"
autodoc_class_signature = "separated"
autodoc_default_options = {
    "exclude-members": "__init__",
    "member-order": "bysource",
    "show-inheritance": True,
}
autodoc_typehints = "signature"


def setup(app: Sphinx) -> None:
    app.connect("autodoc-process-docstring", process_docstring)
    app.connect("autodoc-skip-member", skip_member)
