# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'DataStreams'
copyright = '2022, 0xEvan'
author = '0xEvan'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.todo', 
    'sphinx.ext.viewcode', 
    'sphinx.ext.duration', 
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc', 
    'sphinx_rtd_theme', 
    'sphinx.ext.autosummary', 
    'sphinx_autodoc_defaultargs']

autodoc_modules = ['mypackage.*']
autodoc_class_members = ['Streamer', 'DataStream']
autodoc_member_order = 'bysource'
autodoc_typehints = 'description'


templates_path = ['_templates']

napoleon_include_init_with_doc = False


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
