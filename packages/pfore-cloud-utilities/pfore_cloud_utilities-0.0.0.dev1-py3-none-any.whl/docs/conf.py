from datetime import date
import os
import shutil

import toml

import audeer


config = toml.load('../pyproject.toml')


# Project -----------------------------------------------------------------
project = config['project']['name']
copyright = f'2023-{date.today().year} lidl e-commerce'
author = ', '.join(author['name'] for author in config['project']['authors'])
version = os.environ.get('ARTIFACT_LABEL', audeer.git_repo_version())
title = 'Documentation'


# General -----------------------------------------------------------------
master_doc = 'index'
source_suffix = '.rst'
exclude_patterns = [
    'api-src',
    'build',
    'tests',
    'Thumbs.db',
    '.DS_Store',
]
templates_path = ['_templates']
pygments_style = None
extensions = [
    'sphinx.ext.graphviz',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',  # support for Google-style docstrings
    'sphinx.ext.autosummary',
    'sphinx_autodoc_typehints',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx_copybutton',
]

napoleon_use_ivar = True  # List of class attributes
# autodoc_inherit_docstrings = False  # disable docstring inheritance
intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
}
linkcheck_ignore = []
# Ignore package dependencies during building the docs
# This fixes URL link issues with pandas and sphinx_autodoc_typehints
autodoc_mock_imports = []
graphviz_output_format = 'svg'

# Disable auto-generation of TOC entries in the API
# https://github.com/sphinx-doc/sphinx/issues/6316
toc_object_entries = False

# HTML --------------------------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_context = {}
html_title = title

# Copy API (sub-)module RST files to docs/api/ folder ---------------------
audeer.rmdir('api')
audeer.mkdir('api')
api_src_files = audeer.list_file_names('api-src')
api_dst_files = [
    audeer.path('api', os.path.basename(src_file))
    for src_file in api_src_files
]
for src_file, dst_file in zip(api_src_files, api_dst_files):
    shutil.copyfile(src_file, dst_file)
