from __future__ import annotations
from typing import Type, Optional
from .core import FileWrapConfig

import json
import os


class JSONWrapConfig(FileWrapConfig):
    def __init__(
        self,
        path: str,
        default_save: bool = True,
        encoder: Optional[Type[json.JSONEncoder]] = None,
        decoder: Optional[Type[json.JSONDecoder]] = None,
    ) -> None:
        self._encoder = encoder
        self._decoder = decoder

        super().__init__(path=path, default_save=default_save)

    def load(self):
        with open(self.path, "r") as f:
            self._data = json.load(f, cls=self._decoder)

    def save(self):
        if not os.path.exists(self.path):
            os.makedirs(os.path.dirname(self.path), exist_ok=True)

        dump = json.dumps(self._data, indent=4, cls=self._encoder)
        with open(self.path, "w") as f:
            f.write(dump)
