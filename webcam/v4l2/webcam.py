import os
from collections import namedtuple
from ctypes import string_at
from mmap import mmap

from webcam import BaseWebCam, BaseWebCamControlsManager, WebCamException, v4l2

v4l2ControlInfo = namedtuple(
    "v4l2ControlInfo",
    "name cid minimum maximum default type available",
    defaults=["", 0, 0, 0, 0, int, False],
)
_str2cid = {
    "brightness": v4l2.V4L2_CID_BRIGHTNESS,
    "contrast": v4l2.V4L2_CID_CONTRAST,
    "auto_white_balance": v4l2.V4L2_CID_AUTO_WHITE_BALANCE,
    "gamma": v4l2.V4L2_CID_GAMMA,
    "red_balance": v4l2.V4L2_CID_RED_BALANCE,
    "blue_balance": v4l2.V4L2_CID_BLUE_BALANCE,
    "hflip": v4l2.V4L2_CID_HFLIP,
    "vflip": v4l2.V4L2_CID_VFLIP,
    "white_balance_temperature": v4l2.V4L2_CID_WHITE_BALANCE_TEMPERATURE,
    "sharpness": v4l2.V4L2_CID_SHARPNESS,
    "rotate": v4l2.V4L2_CID_ROTATE,
}


class v4l2WebCamControlsManager(BaseWebCamControlsManager):
    def __init__(self, fd: int):
        super().__init__(fd)
        self._fd = fd
        self._ctrl_info = {}

    def __getitem__(self, name: str) -> int | bool:
        if name not in self._ctrl_info:
            self.get_info(name)
        if not self._ctrl_info[name].available:
            raise WebCamException(f"control {name!r} is not supported")
        info = self._ctrl_info[name]
        ctrl = v4l2.v4l2_control(id=_str2cid[name])
        v4l2.VIDIOC_G_CTRL(self._fd, ctrl)
        return info.type(ctrl.value)

    def __setitem__(self, name: str, value: int | bool):
        if name not in self._ctrl_info:
            self.get_info(name)
        if not self._ctrl_info[name].available:
            raise WebCamException(f"control {name!r} is not supported")
        info = self._ctrl_info[name]
        value = max(info.minimum, min(info.maximum, int(value)))
        ctrl = v4l2.v4l2_control(id=_str2cid[name], value=value)
        v4l2.VIDIOC_S_CTRL(self._fd, ctrl)

    def get_info(self, name: str) -> v4l2ControlInfo:
        if name not in _str2cid:
            raise WebCamException(f"control {name!r} is not supported")
        if name in self._ctrl_info:
            return self._ctrl_info[name]
        ctrl = v4l2.v4l2_queryctrl(id=_str2cid[name])
        try:
            v4l2.VIDIOC_QUERYCTRL(self._fd, ctrl)
        except:
            self._ctrl_info[name] = v4l2ControlInfo(cid=ctrl.id)
            return self._ctrl_info[name]
        if ctrl.type == v4l2.v4l2_ctrl_type.V4L2_CTRL_TYPE_BOOLEAN:
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
    def __init__(self, index: int):
        super().__init__(index)
        self._device = f"/dev/video{index}"
        self._fd = os.open(self._device, os.O_RDWR)
        self._controls = v4l2WebCamControlsManager(self._fd)
        self._available_pixfmt = []
        self._mmaps = []

        self._check()
        self._init()

    def __del__(self):
        if self._is_opening:
            self.close()
        for m in self._mmaps:
            m.close()
        os.close(self._fd)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(device={self._device!r})"

    def _check(self):
        self._capability = v4l2.VIDIOC_QUERYCAP(self._fd)
        if not self._capability.capabilities & v4l2.V4L2_CAP_VIDEO_CAPTURE:
            raise WebCamException(f"{self._device} can not capture video")
        if not self._capability.capabilities & v4l2.V4L2_CAP_STREAMING:
            raise WebCamException(f"{self._device} does not support streaming")

        vfmt = v4l2.v4l2_fmtdesc(type=v4l2.v4l2_buf_type.V4L2_BUF_TYPE_VIDEO_CAPTURE)
        index = 0
        while True:
            vfmt.index = index
            index += 1
            try:
                v4l2.VIDIOC_ENUM_FMT(self._fd, vfmt)
            except OSError:
                break
            self._available_pixfmt.append(vfmt.pixelformat)

        if v4l2.V4L2_PIX_FMT_MJPEG not in self._available_pixfmt:
            raise WebCamException(f"{self._device} does not support mjpeg format")

    def _init(self):
        vfmt = v4l2.v4l2_format(type=v4l2.v4l2_buf_type.V4L2_BUF_TYPE_VIDEO_CAPTURE)
        vfmt.fmt.pix.width = 640
        vfmt.fmt.pix.height = 480
        vfmt.fmt.pix.pixelformat = v4l2.V4L2_PIX_FMT_MJPEG
        v4l2.VIDIOC_S_FMT(self._fd, vfmt)

        reqbuf = v4l2.v4l2_requestbuffers(
            count=4,
            type=v4l2.v4l2_buf_type.V4L2_BUF_TYPE_VIDEO_CAPTURE,
            memory=v4l2.v4l2_memory.V4L2_MEMORY_MMAP,
        )
        try:
            v4l2.VIDIOC_REQBUFS(self._fd, reqbuf)
        except OSError:
            raise WebCamException(f"{self._device} does not support mmap-streaming")

        for i in range(reqbuf.count):
            buffer = v4l2.v4l2_buffer(
                index=i, type=reqbuf.type, memory=v4l2.v4l2_memory.V4L2_MEMORY_MMAP
            )
            v4l2.VIDIOC_QUERYBUF(self._fd, buffer)
            v4l2.VIDIOC_QBUF(self._fd, buffer)
            self._mmaps.append(
                mmap(self._fd, length=buffer.length, offset=buffer.m.offset)
            )

    def open(self):
        if self._is_opening:
            return
        v4l2.VIDIOC_STREAMON(self._fd, v4l2.v4l2_buf_type.V4L2_BUF_TYPE_VIDEO_CAPTURE)
        self._is_opening = True

    def close(self):
        if not self._is_opening:
            return
        v4l2.VIDIOC_STREAMOFF(self._fd, v4l2.v4l2_buf_type.V4L2_BUF_TYPE_VIDEO_CAPTURE)
        self._is_opening = False

    def capture(self) -> bytes:
        if not self._is_opening:
            self.open()
        buffer = v4l2.v4l2_buffer(
            type=v4l2.v4l2_buf_type.V4L2_BUF_TYPE_VIDEO_CAPTURE,
            memory=v4l2.v4l2_memory.V4L2_MEMORY_MMAP,
        )
        v4l2.VIDIOC_DQBUF(self._fd, buffer)
        result = self._mmaps[buffer.index].read(buffer.length)
        self._mmaps[buffer.index].seek(0)
        v4l2.VIDIOC_QBUF(self._fd, buffer)
        return result

    @property
    def controls(self) -> v4l2WebCamControlsManager:
        return self._controls
