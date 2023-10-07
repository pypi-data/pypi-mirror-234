# This file is placed in the Public Domain.
# -*- coding: utf-8 -*-
#
# pylint: disable=C,I,R
# ruff: noqa: E402, E501


"Skull, Bones and Number (OTP-CR-117/19)"


NAME = "sbn"
VERSION = "41"


import os
import sys


sys.setrecursionlimit(1500)


curdir = os.getcwd()


sys.path.insert(0, os.path.join(curdir, "..", ".."))
sys.path.insert(0, os.path.join(curdir, ".."))
sys.path.insert(0, os.path.join(curdir))


# -- Options for GENERIC output ---------------------------------------------


project = NAME
master_doc = 'index'
version = '%s' % VERSION
release = '%s' % VERSION
language = 'en'
today = ''
today_fmt = '%B %d, %Y'
needs_sphinx = '1.7'
exclude_patterns = ['_build', '_templates', '_source', 'Thumbs.db', '.DS_Store']
source_suffix = '.rst'
source_encoding = 'utf-8-sig'
modindex_common_prefix = [""]
keep_warnings = False
templates_path = ['_templates']
add_function_parentheses = False
add_module_names = False
show_authors = False
pygments_style = 'colorful'
extensions = [
              'sphinx.ext.autodoc',
              'sphinx.ext.autosummary',
              'sphinx.ext.viewcode',
              'sphinx.ext.todo',
              'sphinx.ext.githubpages'
             ]


# -- Options for HTML output -------------------------------------------------


html_title = "Skull, Bones and Numner (OTP-CR-117/19)"
html_style = 'sbn.css'
html_static_path = ["_static"]
html_css_files = ["sbn.css",]
html_short_title = "%s %s" % (NAME, VERSION)
html_sidebars = {
    '**': [
        'about.html',
        'searchbox.html',
        'navigation.html',
        'relations.html',
    ]
}
html_theme = "alabaster"
html_theme_options = {
    'github_user': 'bthate',
    'github_repo': NAME,
    'github_button': False,
    'github_banner': False,
    'logo': 'skull.jpg',
    'link': '#000',
    'link_hover': '#000',
    'nosidebar': True,
    'show_powered_by': False,
    'show_relbar_top': False,
    'sidebar_width': 10,
}
html_favicon = "skull.jpg"
html_extra_path = []
html_last_updated_fmt = '%Y-%b-%d'
html_additional_pages = {}
html_domain_indices = False
html_use_index = False
html_split_index = False
html_show_sourcelink = False
html_show_sphinx = False
html_show_copyright = False
html_copy_source = False
html_use_opensearch = 'http://%s.rtfd.io/' % NAME
html_file_suffix = '.html'
htmlhelp_basename = 'testdoc'

intersphinx_mapping = {
                       'python': ('https://docs.python.org/3', 'objects.inv'),
                       'sphinx': ('http://sphinx.pocoo.org/', None),
                      }
intersphinx_cache_limit = 1


rst_prolog = '''.. image:: genocide.png
    :width: 100%
    :height: 2.0cm
    :target: index.html

'''

rst_epilog = '''.. raw:: html

     <br>
     <center>
     <b>

:ref:`home <home>` - :ref:`manual <manual>` - :ref:`source <source>` - :ref:`about <about>`

.. raw:: html

    </b>
    </center>
'''

autosummary_generate = True
autodoc_default_flags = ['members', 'undoc-members', 'private-members', "imported-members"]
autodoc_member_order = 'groupwise'
autodoc_docstring_signature = True
autoclass_content = "class"
nitpick_ignore = [
                  ('py:class', 'builtins.BaseException'),
                 ]
