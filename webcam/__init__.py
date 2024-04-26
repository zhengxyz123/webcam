import os
from ctypes import string_at
from mmap import mmap

from webcam import v4l2

_str2cid = {
    "brightness": (v4l2.V4L2_CID_BRIGHTNESS, int),
    "contrast": (v4l2.V4L2_CID_CONTRAST, int),
    "gamma": (v4l2.V4L2_CID_GAMMA, int),
    "sharpness": (v4l2.V4L2_CID_SHARPNESS, int),
}


class WebCamException(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


class WebCam:
    def __init__(self, devnum: int):
        self._device = f"/dev/video{devnum}"
        self._fd = os.open(self._device, os.O_RDWR)
        self._available_pixfmt = []
        self._mmaps = []
        self._is_opening = False

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

    def __getitem__(self, name: str) -> int | bool:
        if name not in _str2cid:
            raise WebCamException(f"control '{name}' is not found")
        control = v4l2.v4l2_control(id=_str2cid[name][0])
        v4l2.VIDIOC_G_CTRL(self._fd, control)
        return _str2cid[name][1](control.value)

    def __setitem__(self, name: str, value: int | bool):
        if name not in _str2cid:
            raise WebCamException(f"control '{name}' is not found")
        control = v4l2.v4l2_control(id=_str2cid[name][0], value=int(value))
        v4l2.VIDIOC_S_CTRL(self._fd, control)

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

    def capture(self):
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
    def is_opening(self) -> bool:
        return self._is_opening
