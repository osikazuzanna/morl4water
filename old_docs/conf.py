# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Adding path -------------------------------------------------------------
import os
import sys

# # Add the path to the directory containing your Python modules for morl4water there are 2 paths needed
sys.path.insert(0, os.path.abspath('../../core/models'))
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('../..')) 
# sys.path.insert(0, os.path.abspath('../morl4water'))
# Debugging: Print sys.path to confirm it’s correct
print("Python sys.path used by autodoc:")
for path in sys.path:
    print(path)

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'morl4water'
copyright = '2024, HIPPO LAB'
author = 'HIPPO LAB'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

#OLD
extensions = [
    'sphinx.ext.autodoc',  # Enables autodoc
    'sphinx.ext.napoleon',  # Optional: Enables Google/NumPy-style docstrings
    'sphinx.ext.autosummary', # To generate summary tables with links to the modules
    'myst_parser', #for using index.md instead of index.rst
]



# # Set autosummary to generate .rst files
autosummary_generate = True
autosummary_imported_members = True

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

#NEW

# extensions = [
#     "sphinx.ext.napoleon",
#     "sphinx.ext.doctest",
#     "sphinx.ext.autodoc",
#     "sphinx.ext.githubpages",
#     "myst_parser",
# ]

templates_path = ["_templates"]
exclude_patterns = []

# Napoleon settings
napoleon_use_ivar = True
napoleon_use_admonition_for_references = True
# See https://github.com/sphinx-doc/sphinx/issues/9119
napoleon_custom_sections = [("Returns", "params_style")]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
#ADDED:
html_theme_options = {
    "source_repository": "https://github.com/osikazuzanna/morl4water/",
    "source_branch": "main",
    "source_directory": "docs/",
}

html_static_path = ['_static']

#ADDED
# Include both the class and __init__ docstrings when describing the class
autoclass_content = "both"
