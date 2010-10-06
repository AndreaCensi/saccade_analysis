
import sys, os



extensions = ['sphinx.ext.autodoc', 'sphinx.ext.intersphinx', 'sphinx.ext.coverage', 'sphinx.ext.viewcode', 'sphinxtogithub']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['my_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
#source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'Saccade analysis tools'


# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = '1.0'
# The full version, including alpha/beta/rc tags.
release = '1.0'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = [] 

pygments_style = 'sphinx'
 

html_theme = "haiku"
html_theme_options = { }
 
html_static_path = ['my_static'] 
# Output file base name for HTML help builder.
htmlhelp_basename = 'Saccade analysis tools'
 

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {'http://docs.python.org/': None}
