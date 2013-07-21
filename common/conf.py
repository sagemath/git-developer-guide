import os, sys

extensions = ['sphinx.ext.inheritance_diagram', 'sphinx.ext.todo',
              'sphinx.ext.extlinks', 'sphinx.ext.mathjax']
templates_path = [os.path.join(os.getcwd(), '..', 'common', 'themes'), 'templates']
# The suffix of source filenames.
source_suffix = '.rst'
# The master toctree document.
master_doc = 'index'
# General information about the project.
project = u""
copyright = u'2013, The Sage Development Team'
release = '1.0'
default_role = 'math'
pygments_style = 'sphinx'
todo_include_todos = True

pythonversion = sys.version.split(' ')[0]
# Python and Sage trac ticket shortcuts. For example, :trac:`7549` .

# Sage trac ticket shortcuts. For example, :trac:`7549` .
extlinks = {
    'python': ('http://docs.python.org/release/'+pythonversion+'/%s', ''),
    'trac': ('http://trac.sagemath.org/%s', 'trac ticket #'),
    'wikipedia': ('http://en.wikipedia.org/wiki/%s', 'Wikipedia article '),
    'arxiv': ('http://arxiv.org/abs/%s', 'Arxiv '),
    'oeis': ('http://oeis.org/%s', 'OEIS sequence '),
    'doi': ('http://dx.doi.org/%s', 'doi:'),
    'mathscinet': ('http://www.ams.org/mathscinet-getitem?mr=%s', 'MathSciNet ')
    }
html_theme = 'sage'

# Theme options are theme-specific and customize the look and feel of
# a theme further.  For a list of options available for each theme,
# see the documentation.
html_theme_options = {}
html_favicon = 'favicon.ico'

# Add any paths that contain custom themes here, relative to this directory.
html_theme_path = [os.path.join(os.getcwd(), '..', 'common', 'themes')]

