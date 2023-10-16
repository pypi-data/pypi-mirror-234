import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))

project = "quivr-ext-integration-test"

version = "1.0.0"
release = "1.0.0"

extensions = ["sphinx.ext.autodoc", "sphinx.ext.intersphinx", "quivr_sphinx_autodoc"]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "pyarrow": ("https://arrow.apache.org/docs/", None),
    "pandas": ("https://pandas.pydata.org/docs/", None),
}
