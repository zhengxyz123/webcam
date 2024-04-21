import os

from webcam import v4l2


def a2s(l):
    return "".join([chr(c) for c in l if c])


class WebCam:
    def __init__(self, devnum: int):
        self._device = f"/dev/video{devnum}"
        self._fd = os.open(self._device, os.O_RDWR)
        self._cap_readwrite = False
        self._cap_streaming = False

        self._check_capability()
        self._check_fmt()
        self._set_fmt()

    def __del__(self):
        os.close(self._fd)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(device={self._device!r})"

    def _check_capability(self):
        cap = v4l2.VIDIOC_QUERYCAP(self._fd)
        if not cap.capabilities & v4l2.V4L2_CAP_VIDEO_CAPTURE:
            raise OSError(f"{self._device} can not capture video")
        if cap.capabilities & v4l2.V4L2_CAP_READWRITE:
            self._cap_readwrite = True
        if cap.capabilities & v4l2.V4L2_CAP_STREAMING:
            self._cap_streaming = True
        # print("driver:", a2s(cap.driver))
        # print("card:", a2s(cap.card))
        # print("bus_info:", a2s(cap.bus_info))
        # print("version:", hex(cap.version))
        # print("capabilities:", hex(cap.capabilities))
        # print("device_caps:", hex(cap.device_caps))
        # print("reserved:", a2s(cap.reserved))

    def _check_fmt(self):
        vfmt = v4l2.v4l2_fmtdesc()
        vfmt.type = v4l2.v4l2_buf_type.V4L2_BUF_TYPE_VIDEO_CAPTURE
        index = 0
        while True:
            vfmt.index = index
            index += 1
            try:
                v4l2.VIDIOC_ENUM_FMT(self._fd, vfmt)
            except OSError:
                break
            # print("index:", vfmt.index)
            # print("type:", vfmt.type)
            # print("flags:", vfmt.flags)
            # print("description:", a2s(vfmt.description))
            # print("pixelformat:", hex(vfmt.pixelformat))
            # print("mbus_code:", vfmt.mbus_code)
            # print("reserved:", a2s(vfmt.reserved))

    def _set_fmt(self):
        vfmt = v4l2.v4l2_format()
        vfmt.type = v4l2.v4l2_buf_type.V4L2_BUF_TYPE_VIDEO_CAPTURE
        vfmt.fmt.pix.width = 640
        vfmt.fmt.pix.height = 480
        vfmt.fmt.pix.pixelformat = v4l2.V4L2_PIX_FMT_RGB32
        try:
            v4l2.VIDIOC_S_FMT(self._fd, vfmt)
        except OSError:
            raise OSError("can not set webcam")
