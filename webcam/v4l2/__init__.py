import os
from collections import namedtuple
from ctypes import string_at
from io import BytesIO
from mmap import mmap

from pyglet.image import AbstractImage, ImageData
from pyglet.image import load as load_image

from webcam import BaseWebCam, BaseWebCamControlsManager, WebCamException
from webcam.v4l2.controls import *
from webcam.v4l2.fourcc import *
from webcam.v4l2.videodev2 import *

v4l2ControlInfo = namedtuple(
    "v4l2ControlInfo",
    "name cid minimum maximum default type available",
    defaults=["", 0, 0, 0, 0, int, False],
)
_str2cid = {
    "brightness": V4L2_CID_BRIGHTNESS,
    "contrast": V4L2_CID_CONTRAST,
    "auto_white_balance": V4L2_CID_AUTO_WHITE_BALANCE,
    "gamma": V4L2_CID_GAMMA,
    "red_balance": V4L2_CID_RED_BALANCE,
    "blue_balance": V4L2_CID_BLUE_BALANCE,
    "hflip": V4L2_CID_HFLIP,
    "vflip": V4L2_CID_VFLIP,
    "white_balance_temperature": V4L2_CID_WHITE_BALANCE_TEMPERATURE,
    "sharpness": V4L2_CID_SHARPNESS,
    "rotate": V4L2_CID_ROTATE,
}


class v4l2WebCamControlsManager(BaseWebCamControlsManager):
    def __init__(self, fd: int) -> None:
        super().__init__(fd)
        self._fd = fd
        self._ctrl_info = {}

    def __getitem__(self, name: str) -> int | bool:
        if name not in self._ctrl_info:
            self.get_info(name)
        if not self._ctrl_info[name].available:
            raise WebCamException(f"control {name!r} is not supported")
        info = self._ctrl_info[name]
        ctrl = v4l2_control(id=_str2cid[name])
        VIDIOC_G_CTRL(self._fd, ctrl)
        return info.type(ctrl.value)

    def __setitem__(self, name: str, value: int | bool) -> None:
        if name not in self._ctrl_info:
            self.get_info(name)
        if not self._ctrl_info[name].available:
            raise WebCamException(f"control {name!r} is not supported")
        info = self._ctrl_info[name]
        value = max(info.minimum, min(info.maximum, int(value)))
        ctrl = v4l2_control(id=_str2cid[name], value=value)
        VIDIOC_S_CTRL(self._fd, ctrl)

    def get_info(self, name: str) -> v4l2ControlInfo:
        if name not in _str2cid:
            raise WebCamException(f"control {name!r} is not supported")
        if name in self._ctrl_info:
            return self._ctrl_info[name]
        ctrl = v4l2_queryctrl(id=_str2cid[name])
        try:
            VIDIOC_QUERYCTRL(self._fd, ctrl)
        except:
            self._ctrl_info[name] = v4l2ControlInfo(cid=ctrl.id)
            return self._ctrl_info[name]
        if ctrl.type == v4l2_ctrl_type.V4L2_CTRL_TYPE_BOOLEAN:
            ctrl_type = bool
        else:
            ctrl_type = int
        self._ctrl_info[name] = v4l2ControlInfo(
            name=string_at(ctrl.name).decode(),
            cid=ctrl.id,
            minimum=ctrl.minimum,
            maximum=ctrl.maximum,
            default=ctrl.default_value,
            type=ctrl_type,
            available=True,
        )
        return self._ctrl_info[name]


class v4l2WebCam(BaseWebCam):
    def __init__(self, index: int, width: int = 640, height: int = 480) -> None:
        super().__init__(index, width, height)
        self._device = f"/dev/video{index}"
        self._fd = os.open(self._device, os.O_RDWR)
        self._data_fmt = ""
        self._controls = v4l2WebCamControlsManager(self._fd)
        self._available_pixfmt = []
        self._mmaps = []

        self._check()
        self._init()

    def __del__(self) -> None:
        if self._is_open:
            self.close()
        for m in self._mmaps:
            m.close()
        os.close(self._fd)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(device={self._device!r})"

    def _check(self) -> None:
        self._capability = VIDIOC_QUERYCAP(self._fd)
        if not self._capability.capabilities & V4L2_CAP_VIDEO_CAPTURE:
            raise WebCamException(f"{self._device} can not capture video")
        if not self._capability.capabilities & V4L2_CAP_STREAMING:
            raise WebCamException(f"{self._device} does not support streaming")

        vfmt = v4l2_fmtdesc(index=0, type=v4l2_buf_type.V4L2_BUF_TYPE_VIDEO_CAPTURE)
        while True:
            try:
                VIDIOC_ENUM_FMT(self._fd, vfmt)
            except OSError:
                break
            vfmt.index += 1
            self._available_pixfmt.append(vfmt.pixelformat)

    def _init(self) -> None:
        vfmt = v4l2_format(type=v4l2_buf_type.V4L2_BUF_TYPE_VIDEO_CAPTURE)
        vfmt.fmt.pix.width = self._size[0]
        vfmt.fmt.pix.height = self._size[1]
        if V4L2_PIX_FMT_MJPEG in self._available_pixfmt:
            self._data_fmt = "MJPEG"
            vfmt.fmt.pix.pixelformat = V4L2_PIX_FMT_MJPEG
        elif any(l := [fmt in self._available_pixfmt for fmt in pixfmt_rgba]):
            self._data_fmt = "RGBA"
            vfmt.fmt.pix.pixelformat = pixfmt_rgba[l.index(True)]
        elif any(l := [fmt in self._available_pixfmt for fmt in pixfmt_rgb]):
            self._data_fmt = "RGB"
            vfmt.fmt.pix.pixelformat = pixfmt_rgb[l.index(True)]
        else:
            raise WebCamException(
                f"{self._device} does not support RGB, RGBA or MJPEG format"
            )
        VIDIOC_S_FMT(self._fd, vfmt)
        self._size = (vfmt.fmt.pix.width, vfmt.fmt.pix.height)

        reqbuf = v4l2_requestbuffers(
            count=4,
            type=v4l2_buf_type.V4L2_BUF_TYPE_VIDEO_CAPTURE,
            memory=v4l2_memory.V4L2_MEMORY_MMAP,
        )
        try:
            VIDIOC_REQBUFS(self._fd, reqbuf)
        except OSError:
            raise WebCamException(f"{self._device} does not support mmap-streaming")

        for i in range(reqbuf.count):
            buffer = v4l2_buffer(
                index=i, type=reqbuf.type, memory=v4l2_memory.V4L2_MEMORY_MMAP
            )
            VIDIOC_QUERYBUF(self._fd, buffer)
            VIDIOC_QBUF(self._fd, buffer)
            self._mmaps.append(
                mmap(self._fd, length=buffer.length, offset=buffer.m.offset)
            )

    def open(self) -> None:
        if self._is_open:
            return
        VIDIOC_STREAMON(self._fd, v4l2_buf_type.V4L2_BUF_TYPE_VIDEO_CAPTURE)
        self._is_open = True

    def close(self) -> None:
        if not self._is_open:
            return
        VIDIOC_STREAMOFF(self._fd, v4l2_buf_type.V4L2_BUF_TYPE_VIDEO_CAPTURE)
        self._is_open = False

    def capture(self) -> AbstractImage:
        if not self._is_open:
            self.open()
        buffer = v4l2_buffer(
            type=v4l2_buf_type.V4L2_BUF_TYPE_VIDEO_CAPTURE,
            memory=v4l2_memory.V4L2_MEMORY_MMAP,
        )
        VIDIOC_DQBUF(self._fd, buffer)
        result = self._mmaps[buffer.index].read(buffer.length)
        self._mmaps[buffer.index].seek(0)
        VIDIOC_QBUF(self._fd, buffer)
        if self._data_fmt == "MJPEG":
            image = load_image("image.jpg", BytesIO(result))
        else:
            image = ImageData(*self._size, self._data_fmt, result)
        return image

    @property
    def controls(self) -> v4l2WebCamControlsManager:
        return self._controls


__all__ = ("v4l2WebCamControlsManager", "v4l2WebCam")
