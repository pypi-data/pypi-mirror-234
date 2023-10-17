import os
import sys

from upsies import __project_name__

project = __project_name__

sys.path.append(os.path.abspath("./_ext"))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'cli_reference',
    'sphinx_rtd_theme',
]

html_theme = "sphinx_rtd_theme"
html_theme_options = {
    # Make "Developer Reference" more compact
    'titles_only': True,
}

autosummary_generate = True
html_show_sourcelink = False  # Don't show links to rST code

# This is ignored for some reason?
autodoc_member_order = 'bysource'

templates_path = ['_templates']

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "aiobtclientapi": ("https://aiobtclientapi.readthedocs.io/en/stable/", None),
}
