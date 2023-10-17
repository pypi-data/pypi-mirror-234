from .jsonconfig import JSONWrapConfig
from .core import WrapConfig, FileWrapConfig
from .inmemory import InMemoryConfig

__all__ = [
    "JSONWrapConfig",
    "WrapConfig",
    "InMemoryConfig",
    "FileWrapConfig",
]

# YAML support is optional
try:
    from .yamlconf import YAMLWrapConfig

    __all__.append("YAMLWrapConfig")
except (ImportError, ModuleNotFoundError):
    pass

__version__ = "0.1.8"
