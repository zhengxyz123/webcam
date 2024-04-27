import ctypes
from ctypes import c_int32 as _s32
from ctypes import c_int64 as _s64
from ctypes import c_uint8 as _u8
from ctypes import c_uint16 as _u16
from ctypes import c_uint32 as _u32
from ctypes import c_void_p
from enum import IntEnum

from webcam.ioctl import _IOR, _IOW, _IOWR
from webcam.v4l2.controls import *
from webcam.v4l2.fourcc import *

# /usr/include/linux/videodev2.h:71
VIDEO_MAX_FRAME = 32
VIDEO_MAX_PLANES = 8


# /usr/include/linux/videodev2.h:86
class v4l2_field(IntEnum):
    V4L2_FIELD_ANY = 0
    V4L2_FIELD_NONE = 1
    V4L2_FIELD_TOP = 2
    V4L2_FIELD_BOTTOM = 3
    V4L2_FIELD_INTERLACED = 4
    V4L2_FIELD_SEQ_TB = 5
    V4L2_FIELD_SEQ_BT = 6
    V4L2_FIELD_ALTERNATE = 7
    V4L2_FIELD_INTERLACED_TB = 8
    V4L2_FIELD_INTERLACED_BT = 9


# /usr/include/linux/videodev2.h:139
class v4l2_buf_type(IntEnum):
    V4L2_BUF_TYPE_VIDEO_CAPTURE = 1
    V4L2_BUF_TYPE_VIDEO_OUTPUT = 2
    V4L2_BUF_TYPE_VIDEO_OVERLAY = 3
    V4L2_BUF_TYPE_VBI_CAPTURE = 4
    V4L2_BUF_TYPE_VBI_OUTPUT = 5
    V4L2_BUF_TYPE_SLICED_VBI_CAPTURE = 6
    V4L2_BUF_TYPE_SLICED_VBI_OUTPUT = 7
    V4L2_BUF_TYPE_VIDEO_OUTPUT_OVERLAY = 8
    V4L2_BUF_TYPE_VIDEO_CAPTURE_MPLANE = 9
    V4L2_BUF_TYPE_VIDEO_OUTPUT_MPLANE = 10
    V4L2_BUF_TYPE_SDR_CAPTURE = 11
    V4L2_BUF_TYPE_SDR_OUTPUT = 12
    V4L2_BUF_TYPE_META_CAPTURE = 13
    V4L2_BUF_TYPE_META_OUTPUT = 14
    V4L2_BUF_TYPE_PRIVATE = 0x80  # deprecated


# /usr/include/linux/videodev2.h:185
class v4l2_memory(IntEnum):
    V4L2_MEMORY_MMAP = 1
    V4L2_MEMORY_USERPTR = 2
    V4L2_MEMORY_OVERLAY = 3
    V4L2_MEMORY_DMABUF = 4


# /usr/include/linux/videodev2.h:193
class v4l2_colorspace(IntEnum):
    V4L2_COLORSPACE_DEFAULT = 0
    V4L2_COLORSPACE_SMPTE170M = 1
    V4L2_COLORSPACE_SMPTE240M = 2
    V4L2_COLORSPACE_REC709 = 3
    V4L2_COLORSPACE_BT878 = 4  # deprecated
    V4L2_COLORSPACE_470_SYSTEM_M = 5
    V4L2_COLORSPACE_470_SYSTEM_BG = 6
    V4L2_COLORSPACE_JPEG = 7
    V4L2_COLORSPACE_SRGB = 8
    V4L2_COLORSPACE_OPRGB = 9
    V4L2_COLORSPACE_BT2020 = 10
    V4L2_COLORSPACE_RAW = 11
    V4L2_COLORSPACE_DCI_P3 = 12


# /usr/include/linux/videodev2.h:258
class v4l2_xfer_func(IntEnum):
    V4L2_XFER_FUNC_DEFAULT = 0
    V4L2_XFER_FUNC_709 = 1
    V4L2_XFER_FUNC_SRGB = 2
    V4L2_XFER_FUNC_OPRGB = 3
    V4L2_XFER_FUNC_SMPTE240M = 4
    V4L2_XFER_FUNC_NONE = 5
    V4L2_XFER_FUNC_DCI_P3 = 6
    V4L2_XFER_FUNC_SMPTE2084 = 7


# /usr/include/linux/videodev2.h:299
class v4l2_ycbcr_encoding(IntEnum):
    V4L2_YCBCR_ENC_DEFAULT = 0
    V4L2_YCBCR_ENC_601 = 1
    V4L2_YCBCR_ENC_709 = 2
    V4L2_YCBCR_ENC_XV601 = 3
    V4L2_YCBCR_ENC_XV709 = 4
    V4L2_YCBCR_ENC_SYCC = 5
    V4L2_YCBCR_ENC_BT2020 = 6
    V4L2_YCBCR_ENC_BT2020_CONST_LUM = 7
    V4L2_YCBCR_ENC_SMPTE240M = 8


# /usr/include/linux/videodev2.h:349
class v4l2_hsv_encoding(IntEnum):
    V4L2_HSV_ENC_180 = 128
    V4L2_HSV_ENC_256 = 129


# /usr/include/linux/videodev2.h:369
class v4l2_quantization(IntEnum):
    V4L2_QUANTIZATION_DEFAULT = 0
    V4L2_QUANTIZATION_FULL_RANGE = 1
    V4L2_QUANTIZATION_LIM_RANGE = 2


# /usr/include/linux/videodev2.h:407
class v4l2_rect(ctypes.Structure):
    _fields_ = [
        ("left", _s32),
        ("top", _s32),
        ("width", _u32),
        ("height", _u32),
    ]


# /usr/include/linux/videodev2.h:435
class v4l2_capability(ctypes.Structure):
    _fields_ = [
        ("driver", _u8 * 16),
        ("card", _u8 * 32),
        ("bus_info", _u8 * 32),
        ("version", _u32),
        ("capabilities", _u32),
        ("device_caps", _u32),
        ("reserved", _u32 * 3),
    ]


# /usr/include/linux/videodev2.h:446
V4L2_CAP_VIDEO_CAPTURE = 0x00000001

# /usr/include/linux/videodev2.h:477
V4L2_CAP_READWRITE = 0x01000000
V4L2_CAP_STREAMING = 0x04000000
V4L2_CAP_META_OUTPUT = 0x08000000


# /usr/include/linux/videodev2.h:490
class v4l2_pix_format(ctypes.Structure):
    _fields_ = [
        ("width", _u32),
        ("height", _u32),
        ("pixelformat", _u32),
        ("field", _u32),
        ("bytesperline", _u32),
        ("sizeimage", _u32),
        ("colorspace", _u32),
        ("priv", _u32),
        ("flags", _u32),
        ("encoding", _u32),
        ("quantization", _u32),
        ("xfer_func", _u32),
    ]


# /usr/include/linux/videodev2.h:789
V4L2_PIX_FMT_FLAG_PREMUL_ALPHA = 0x00000001
V4L2_PIX_FMT_FLAG_SET_CSC = 0x00000002


# /usr/include/linux/videodev2.h:795
class v4l2_fmtdesc(ctypes.Structure):
    _fields_ = [
        ("index", _u32),
        ("type", _u32),
        ("flags", _u32),
        ("description", _u8 * 32),
        ("pixelformat", _u32),
        ("mbus_code", _u32),
        ("reserved", _u32 * 3),
    ]


# /usr/include/linux/videodev2.h:886
class v4l2_timecode(ctypes.Structure):
    _fields_ = [
        ("type", _u32),  # V4L2_TC_TYPE_*
        ("flags", _u32),  # V4L2_TC_FLAG_*
        ("frames", _u8),
        ("seconds", _u8),
        ("minutes", _u8),
        ("hours", _u8),
        ("userbits", _u8 * 4),  # V4L2_TC_USERBITS_*
    ]


# /usr/include/linux/videodev2.h:897
V4L2_TC_TYPE_24FPS = 1
V4L2_TC_TYPE_25FPS = 2
V4L2_TC_TYPE_30FPS = 3
V4L2_TC_TYPE_50FPS = 4
V4L2_TC_TYPE_60FPS = 5

# /usr/include/linux/videodev2.h:904
V4L2_TC_FLAG_DROPFRAME = 0x0001
V4L2_TC_FLAG_COLORFRAME = 0x0002
V4L2_TC_USERBITS_field = 0x000C
V4L2_TC_USERBITS_USERDEFINED = 0x0000
V4L2_TC_USERBITS_8BITCHARS = 0x0008


# /usr/include/linux/videodev2.h:945
class v4l2_requestbuffers(ctypes.Structure):
    _fields_ = [
        ("count", _u32),
        ("type", _u32),  # enum v4l2_buf_type
        ("memory", _u32),  # enum v4l2_memory
        ("capabilities", _u32),
        ("flags", _u8),
        ("reserved", _u8),
    ]


# /usr/include/linux/videodev2.h:954
V4L2_MEMORY_FLAG_NON_COHERENT = 1 << 0

# /usr/include/linux/videodev2.h:957
V4L2_BUF_CAP_SUPPORTS_MMAP = 1 << 0
V4L2_BUF_CAP_SUPPORTS_USERPTR = 1 << 1
V4L2_BUF_CAP_SUPPORTS_DMABUF = 1 << 2
V4L2_BUF_CAP_SUPPORTS_REQUESTS = 1 << 3
V4L2_BUF_CAP_SUPPORTS_ORPHANED_BUFS = 1 << 4
V4L2_BUF_CAP_SUPPORTS_M2M_HOLD_CAPTURE_BUF = 1 << 5
V4L2_BUF_CAP_SUPPORTS_MMAP_CACHE_HINTS = 1 << 6


# /usr/include/linux/videodev2.h:987
class v4l2_plane(ctypes.Structure):
    class _v4l2_plane_m(ctypes.Union):
        _fields_ = [
            ("memoffset", _u32),
            ("userptr", ctypes.c_ulong),
            ("fd", _s32),
        ]

    _fields_ = [
        ("bytesused", _u32),
        ("length", _u32),
        ("m", _v4l2_plane_m),
        ("data_offset", _u32),
        ("reserved", _u32 * 11),
    ]


class timeval(ctypes.Structure):
    _fields_ = [
        ("tv_sec", _s64),
        ("tv_usec", _s64),
    ]


# /usr/include/linux/videodev2.h:1034
class v4l2_buffer(ctypes.Structure):
    class _v4l2_buffer_m(ctypes.Union):
        _fields_ = [
            ("offset", _u32),
            ("userptr", ctypes.c_ulong),
            ("planes", ctypes.POINTER(v4l2_plane)),
            ("fd", _s32),
        ]

    class _v4l2_buffer_u0(ctypes.Union):
        _fields_ = [
            ("request_fd", _s32),
            ("reserved", _u32),
        ]

    _fields_ = [
        ("index", _u32),
        ("type", _u32),
        ("bytesused", _u32),
        ("flags", _u32),
        ("field", _u32),
        ("timestamp", timeval),
        ("timecode", v4l2_timecode),
        ("memory", _u32),
        ("m", _v4l2_buffer_m),
        ("length", _u32),
        ("reserved2", _u32),
        ("_u0", _v4l2_buffer_u0),
    ]


# /usr/include/linux/videodev2.h:1074
V4L2_BUF_FLAG_MAPPED = 0x00000001
V4L2_BUF_FLAG_QUEUED = 0x00000002
V4L2_BUF_FLAG_DONE = 0x00000004
V4L2_BUF_FLAG_KEYFRAME = 0x00000008
V4L2_BUF_FLAG_PFRAME = 0x00000010
V4L2_BUF_FLAG_BFRAME = 0x00000020
V4L2_BUF_FLAG_ERROR = 0x00000040
V4L2_BUF_FLAG_IN_REQUEST = 0x00000080
V4L2_BUF_FLAG_TIMECODE = 0x00000100
V4L2_BUF_FLAG_M2M_HOLD_CAPTURE_BUF = 0x00000200
V4L2_BUF_FLAG_PREPARED = 0x00000400
V4L2_BUF_FLAG_NO_CACHE_INVALIDATE = 0x00000800
V4L2_BUF_FLAG_NO_CACHE_CLEAN = 0x00001000
V4L2_BUF_FLAG_TIMESTAMP_MASK = 0x0000E000
V4L2_BUF_FLAG_TIMESTAMP_UNKNOWN = 0x00000000
V4L2_BUF_FLAG_TIMESTAMP_MONOTONIC = 0x00002000
V4L2_BUF_FLAG_TIMESTAMP_COPY = 0x00004000
V4L2_BUF_FLAG_TSTAMP_SRC_MASK = 0x00070000
V4L2_BUF_FLAG_TSTAMP_SRC_EOF = 0x00000000
V4L2_BUF_FLAG_TSTAMP_SRC_SOE = 0x00010000
V4L2_BUF_FLAG_LAST = 0x00100000
V4L2_BUF_FLAG_REQUEST_FD = 0x00800000


# /usr/include/linux/videodev2.h:1183
class v4l2_clip(ctypes.Structure):
    pass


v4l2_clip._fields_ = [
    ("c", v4l2_rect),
    ("next", ctypes.POINTER(v4l2_clip)),
]


# /usr/include/linux/videodev2.h:1183
class v4l2_window(ctypes.Structure):
    _fields_ = [
        ("w", v4l2_rect),
        ("field", _u32),
        ("chromakey", _u32),
        ("clips", ctypes.POINTER(v4l2_clip)),
        ("clipcount", _u32),
        ("bitmap", c_void_p),
        ("global_alpha", _u8),
    ]


# /usr/include/linux/videodev2.h:1717
class v4l2_control(ctypes.Structure):
    _fields_ = [
        ("id", _u32),
        ("value", _s32),
    ]


# /usr/include/linux/videodev2.h:1776
class v4l2_ctrl_type(IntEnum):
    V4L2_CTRL_TYPE_INTEGER = 1
    V4L2_CTRL_TYPE_BOOLEAN = 2
    V4L2_CTRL_TYPE_MENU = 3
    V4L2_CTRL_TYPE_BUTTON = 4
    V4L2_CTRL_TYPE_INTEGER64 = 5
    V4L2_CTRL_TYPE_CTRL_CLASS = 6
    V4L2_CTRL_TYPE_STRING = 7
    V4L2_CTRL_TYPE_BITMASK = 8
    V4L2_CTRL_TYPE_INTEGER_MENU = 9
    V4L2_CTRL_COMPOUND_TYPES = 0x0100
    V4L2_CTRL_TYPE_U8 = 0x0100
    V4L2_CTRL_TYPE_U16 = 0x0101
    V4L2_CTRL_TYPE_U32 = 0x0102
    V4L2_CTRL_TYPE_AREA = 0x0106
    V4L2_CTRL_TYPE_HDR10_CLL_INFO = 0x0110
    V4L2_CTRL_TYPE_HDR10_MASTERING_DISPLAY = 0x0111
    V4L2_CTRL_TYPE_H264_SPS = 0x0200
    V4L2_CTRL_TYPE_H264_PPS = 0x0201
    V4L2_CTRL_TYPE_H264_SCALING_MATRIX = 0x0202
    V4L2_CTRL_TYPE_H264_SLICE_PARAMS = 0x0203
    V4L2_CTRL_TYPE_H264_DECODE_PARAMS = 0x0204
    V4L2_CTRL_TYPE_H264_PRED_WEIGHTS = 0x0205
    V4L2_CTRL_TYPE_FWHT_PARAMS = 0x0220
    V4L2_CTRL_TYPE_VP8_FRAME = 0x0240
    V4L2_CTRL_TYPE_MPEG2_QUANTISATION = 0x0250
    V4L2_CTRL_TYPE_MPEG2_SEQUENCE = 0x0251
    V4L2_CTRL_TYPE_MPEG2_PICTURE = 0x0252
    V4L2_CTRL_TYPE_VP9_COMPRESSED_HDR = 0x0260
    V4L2_CTRL_TYPE_VP9_FRAME = 0x0261
    V4L2_CTRL_TYPE_HEVC_SPS = 0x0270
    V4L2_CTRL_TYPE_HEVC_PPS = 0x0271
    V4L2_CTRL_TYPE_HEVC_SLICE_PARAMS = 0x0272
    V4L2_CTRL_TYPE_HEVC_SCALING_MATRIX = 0x0273
    V4L2_CTRL_TYPE_HEVC_DECODE_PARAMS = 0x0274


# /usr/include/linux/videodev2.h:1824
class v4l2_queryctrl(ctypes.Structure):
    _fields_ = [
        ("id", _u32),
        ("type", _u32),
        ("name", _u8 * 32),
        ("minimum", _s32),
        ("maximum", _s32),
        ("step", _s32),
        ("default_value", _s32),
        ("flags", _u32),
        ("reserved", _u32 * 2),
    ]


# /usr/include/linux/videodev2.h:2131
class v4l2_vbi_format(ctypes.Structure):
    _fields_ = [
        ("sampling_rate", _u32),
        ("offset", _u32),
        ("samples_pre_line", _u32),
        ("sample_format", _u32),
        ("start", _s32 * 2),
        ("count", _u32 * 2),
        ("flags", _u32),
        ("reserved", _u32 * 2),
    ]


# /usr/include/linux/videodev2.h:2143
V4L2_VBI_UNSYNC = 1 << 0
V4L2_VBI_INTERLACED = 1 << 1
V4L2_VBI_ITU_525_F1_START = 1
V4L2_VBI_ITU_525_F2_START = 264
V4L2_VBI_ITU_625_F1_START = 1
V4L2_VBI_ITU_625_F2_START = 314


# /usr/include/linux/videodev2.h:2159
class v4l2_sliced_vbi_format(ctypes.Structure):
    _fields_ = [
        ("service_set", _u16),
        ("service_lines", (_u16 * 2) * 24),
        ("io_size", _u32),
        ("reserved", _u32 * 2),
    ]


# /usr/include/linux/videodev2.h:2261
class v4l2_plane_pix_format(ctypes.Structure):
    _fields_ = [
        ("sizeimage", _u32),
        ("bytesperline", _u32),
        ("reserved", _u16 * 6),
    ]


# /usr/include/linux/videodev2.h:2261
class v42l_pix_format_mplane(ctypes.Structure):
    _fields_ = [
        ("width", _u32),
        ("height", _u32),
        ("pixelformat", _u32),
        ("field", _u32),
        ("colorspace", _u32),
        ("plane_fmt", v4l2_plane_pix_format * VIDEO_MAX_PLANES),
        ("num_planes", _u8),
        ("flags", _u8),
        ("encoding", _u8),
        ("quantization", _u8),
        ("xfer_func", _u8),
        ("reserved", _u8 * 7),
    ]


# /usr/include/linux/videodev2.h:2307
class v4l2_sdr_format(ctypes.Structure):
    _fields_ = [
        ("pixelformat", _u32),
        ("buffersize", _u32),
        ("reserved", _u8 * 24),
    ]


# /usr/include/linux/videodev2.h:2307
class v4l2_meta_format(ctypes.Structure):
    _fields_ = [
        ("dataformat", _u32),
        ("buffersize", _u32),
    ]


# /usr/include/linux/videodev2.h:2336
class v4l2_format(ctypes.Structure):
    class _v4l2_format_fmt(ctypes.Union):
        _fields_ = [
            ("pix", v4l2_pix_format),
            ("pix_mp", v42l_pix_format_mplane),
            ("win", v4l2_window),
            ("vbi", v4l2_vbi_format),
            ("sliced", v4l2_sliced_vbi_format),
            ("sdr", v4l2_sdr_format),
            ("meta", v4l2_meta_format),
            ("raw_data", _u8 * 200),
        ]

    _fields_ = [
        ("type", _u32),
        ("fmt", _v4l2_format_fmt),
    ]


# /usr/include/linux/videodev2.h:2523
VIDIOC_QUERYCAP = _IOR("V", 0, v4l2_capability)
VIDIOC_ENUM_FMT = _IOWR("V", 2, v4l2_fmtdesc)
VIDIOC_G_FMT = _IOWR("V", 4, v4l2_format)
VIDIOC_S_FMT = _IOWR("V", 5, v4l2_format)
VIDIOC_REQBUFS = _IOWR("V", 8, v4l2_requestbuffers)
VIDIOC_QUERYBUF = _IOWR("V", 9, v4l2_buffer)
VIDIOC_QBUF = _IOWR("V", 15, v4l2_buffer)
VIDIOC_DQBUF = _IOWR("V", 17, v4l2_buffer)
VIDIOC_STREAMON = _IOW("V", 18, ctypes.c_int)
VIDIOC_STREAMOFF = _IOW("V", 19, ctypes.c_int)
VIDIOC_G_CTRL = _IOWR("V", 27, v4l2_control)
VIDIOC_S_CTRL = _IOWR("V", 28, v4l2_control)
VIDIOC_QUERYCTRL = _IOWR("V", 36, v4l2_queryctrl)
VIDIOC_TRY_FMT = _IOWR("V", 64, v4l2_format)
