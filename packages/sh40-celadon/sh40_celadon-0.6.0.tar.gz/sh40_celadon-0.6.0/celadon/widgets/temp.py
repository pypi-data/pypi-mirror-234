from ..enums import MouseAction
from .container import Tower


class Temp(Tower):
    def __init__(self, **widget_args) -> None:
        super().__init__(**widget_args)

        self._offset = None

    def on_click(self, _: MouseAction, position: tuple[int, int]) -> bool:
        self._offset = tuple(position[i] - self.position[i] for i in range(2))

        return True

    def on_release(self, *_) -> bool:
        self._offset = None

        return True

    def on_drag(self, _, position: tuple[int, int]) -> bool:
        if self._offset is None:
            return False

        self.position = tuple(position[i] - self._offset[i] for i in range(2))
        return True
