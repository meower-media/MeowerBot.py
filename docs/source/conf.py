# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import sys
import os

sys.path.insert(0, os.path.abspath('../../'))

from MeowerBot._version import __version__

project = 'MeowerBot.py'
copyright = "2023, ShowierData9978"
author = "ShowierData9978"
release = __version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration



sys.setrecursionlimit(1500)

extensions = ['sphinx_rtd_theme',]
templates_path = ['_templates']
exclude_patterns = []


extensions.append('sphinx.ext.todo')
extensions.append('sphinx.ext.autodoc')
extensions.append('sphinx.ext.autosummary')
extensions.append('sphinx.ext.intersphinx')
extensions.append('sphinx.ext.mathjax')
extensions.append('sphinx.ext.viewcode')
extensions.append('sphinx.ext.graphviz')
extensions.append('sphinx.ext.intersphinx')

autosummary_generate = True


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

html_show_sphinx = False

html_baseurl = ''

if os.getenv('GITHUB_ACTIONS'):
	html_baseurl = "meowerbot.showierdata.xyz"
	extensions.append("sphinx.ext.githubpages")
