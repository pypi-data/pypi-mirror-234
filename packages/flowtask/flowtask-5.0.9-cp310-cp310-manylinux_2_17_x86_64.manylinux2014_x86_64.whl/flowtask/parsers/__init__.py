"""
DataIntegration parsers.

Navigator can support parsing Tasks from JSON-format, YAML-format and more complex TOML format.
"""
from flowtask.parsers._yaml import YAMLParser
from flowtask.parsers.toml import TOMLParser
from flowtask.parsers.json import JSONParser


__all__ = ("TOMLParser", "YAMLParser", "JSONParser", )
