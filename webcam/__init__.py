from sys import platform
from typing import Any

from pyglet.image import AbstractImage


class WebCamException(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class BaseWebCamControlsManager:
    def __init__(self, *args, **kwargs) -> None:
        pass

    def __getitem__(self, name: str) -> Any:
        raise NotImplementedError("this method is not implemented yet")

    def __setitem__(self, name: str, value: Any) -> None:
        raise NotImplementedError("this method is not implemented yet")


class BaseWebCam:
    def __init__(self, index: int, width: int, height: int) -> None:
        self._is_open = False
        self._size = (width, height)

    def open(self) -> None:
        raise NotImplementedError("this method is not implemented yet")

    def close(self) -> None:
        raise NotImplementedError("this method is not implemented yet")

    def capture(self) -> AbstractImage:
        raise NotImplementedError("this method is not implemented yet")

    @property
    def is_open(self) -> bool:
        return self._is_open

    @property
    def size(self) -> tuple[int, int]:
        return self._size

    @property
    def controls(self) -> BaseWebCamControlsManager:
        raise NotImplementedError("this method is not implemented yet")


if platform.startswith("linux") or platform.startswith("freebsd"):
    from webcam.v4l2 import v4l2WebCam as WebCam
    from webcam.v4l2 import v4l2WebCamControlsManager as WebCamControlsManager
