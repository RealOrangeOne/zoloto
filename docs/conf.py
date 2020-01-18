import zoloto

project = "Zoloto"
copyright = "2020, Jake Howard"  # noqa: A001
author = "Jake Howard"

release = zoloto.__version__

extensions = [
    "sphinx.ext.autodoc",
    "sphinx_autodoc_typehints",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx_rtd_theme",
]

set_type_checking_flag = True

templates_path = []

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}

html_theme = "sphinx_rtd_theme"

html_static_path = []

autodoc_default_options = {
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__",
}
