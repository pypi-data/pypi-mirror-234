import importlib.metadata

from clyjin_templates.plugin import TemplatesPlugin

__version__ = importlib.metadata.version("clyjin_templates")
MainPlugin = TemplatesPlugin
