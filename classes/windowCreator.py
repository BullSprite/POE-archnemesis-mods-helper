from tkinter import *
from abc import ABC, abstractmethod
from typing import Union, Any


class windowCreator(ABC):
    _elements : dict[str, dict[str, Any]]
    def __init__(self, master: Tk = None) -> None:
        if master:
            self._window = Toplevel(master)
        else:
            self._window = Tk()
        self._createLayout()
        if not master:
            self._window.mainloop()

    @abstractmethod
    def _createLayout(self) -> None:
        ...

    def __getitem__(self, key: str):
        if key == "element":
            return self._elements
        elif key == "window":
            return self._window
        else:
            raise KeyError(f"'{key}'")
