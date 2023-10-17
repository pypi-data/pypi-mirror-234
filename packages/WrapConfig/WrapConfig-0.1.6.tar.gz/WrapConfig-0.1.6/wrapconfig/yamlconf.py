from typing import Optional, Type
import os
from .core import FileWrapConfig
import yaml


class YAMLWrapConfig(FileWrapConfig):
    def save(self):
        if not os.path.exists(self.path):
            os.makedirs(os.path.dirname(self.path), exist_ok=True)

        dump = yaml.dump(self._data)
        with open(self.path, "w") as f:
            f.write(dump)

    def load(self):
        with open(self.path, "r") as f:
            self._data = yaml.safe_load(f)
