from abc import ABC, abstractmethod
from typing import Any, Union, Optional, Dict
from copy import deepcopy
import os

ConfigTypes = Union[str, float, int, bool]


ConfigData = Dict[str, Union[ConfigTypes, "ConfigData"]]


class WrapConfig(ABC):
    def __init__(self, default_save: bool = True) -> None:
        super().__init__()
        self._data: ConfigData = {}
        self._default_save = default_save

    @property
    def data(self) -> ConfigData:
        return deepcopy(self._data)

    @abstractmethod
    def load(self):
        """load config from resource"""
        ...

    @abstractmethod
    def save(self):
        """save config to resource"""
        ...

    def set(
        self,
        key: str,
        *subkeys: str,
        value: ConfigTypes,
        save: Optional[bool] = None,
    ):
        """set config"""
        if key not in self._data:
            self._data[key] = {}

        _datadict = self._data
        _key = key
        if not isinstance(_datadict, dict):
            raise TypeError(
                f"Expected dict, got {type(_datadict)}, this might be the result of a key or subkey conflict, which is already a value."
            )
        for subkey in subkeys:
            if subkey not in _datadict[_key]:
                _datadict[_key][subkey] = {}
            _datadict = _datadict[_key]
            _key = subkey
            if not isinstance(_datadict, dict):
                raise TypeError(
                    f"Expected dict, got {type(_datadict)}, this might be the result of a key or subkey conflict, which is already a value."
                )

        _datadict[_key] = value
        if save is None:
            save = self._default_save

        if save:
            self.save()

    def get(self, *keys: str, default: ConfigTypes = None) -> Any:
        """get config value recursively with default value"""
        if not keys:
            return self.data

        _datadict = self._data
        if len(keys) > 1:
            for key in keys[:-1]:
                if key not in _datadict:
                    _datadict[key] = {}
                _datadict = _datadict[key]
                if not isinstance(_datadict, dict):
                    raise TypeError(
                        f"Expected dict, got {type(_datadict)}, this might be the result of a key or subkey conflict, which is already a value."
                    )

        return _datadict.get(keys[-1], default)

    def update(self, data: ConfigData):
        """Deeply update the configuration with the provided data.
        If a key is not present in the configuration, it will be added.
        If a key is present in the configuration, it will be updated.
        """

        def deep_update(target: ConfigData, source: ConfigData) -> None:
            """Helper function to recursively update a dictionary."""
            for key, value in source.items():
                if isinstance(value, dict):
                    target[key] = deep_update(target.get(key, {}), value)
                else:
                    target[key] = value
            return target

        self._data = deep_update(self._data, data)

    def fill(self, data: ConfigData, save: Optional[bool] = None):
        """Deeply update the configuration with the provided data.
        If a key is not present in the configuration, it will be added.
        If a key is present in the configuration, it will not be updated.
        """

        def deep_update(target: ConfigData, source: ConfigData) -> None:
            """Helper function to recursively update a dictionary."""
            for key, value in source.items():
                print(key, value)
                if isinstance(value, dict):
                    if key not in target:
                        target[key] = {}
                    elif not isinstance(target[key], dict):
                        raise TypeError(
                            f"Expected dict, got {type(target[key])}, this might be the result of a key or subkey conflict, which is already a value."
                        )
                    target[key] = deep_update(target[key], value)
                else:
                    if key not in target:
                        target[key] = value
            return target

        self._data = deep_update(self._data, data)

        if save is None:
            save = self._default_save

        if save:
            self.save()


class FileWrapConfig(WrapConfig):
    """WrapConfig that saves and loads from a file"""

    def __init__(self, path, default_save: bool = True) -> None:
        self._path = path
        super().__init__(default_save)
        if os.path.exists(self.path):
            self.load()
        if self._data is None:
            self._data = {}

    @property
    def path(self):
        return self._path
