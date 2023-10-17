from .jsonconfig import JSONConfigManager
from .core import ConfigManager, FileConfigManager
from .inmemory import InMemoryConfig

__all__ = [
    "JSONConfigManager",
    "ConfigManager",
    "InMemoryConfig",
    "FileConfigManager",
]

# YAML support is optional
try:
    from .yamlconf import YAMLConfigManager

    __all__.append("YAMLConfigManager")
except (ImportError, ModuleNotFoundError):
    pass

__version__ = "0.1.1"
