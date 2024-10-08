from ctypes import c_uint32 as _u32


# /usr/include/linux/videodev2.h:79
def v4l2_fourcc(a: str, b: str, c: str, d: str) -> int:
    ai, bi, ci, di = ord(a), ord(b), ord(c), ord(d)
    return (
        _u32(ai).value
        | (_u32(bi).value << 8)
        | (_u32(ci).value << 16)
        | (_u32(di).value << 24)
    )


# /usr/include/linux/videodev2.h:81
def v4l2_fourcc_be(a: str, b: str, c: str, d: str) -> int:
    return v4l2_fourcc(a, b, c, d) | (1 << 31)


# /usr/include/linux/videodev2.h:513
V4L2_PIX_FMT_RGB332 = v4l2_fourcc("R", "G", "B", "1")
V4L2_PIX_FMT_RGB444 = v4l2_fourcc("R", "4", "4", "4")
V4L2_PIX_FMT_ARGB444 = v4l2_fourcc("A", "R", "1", "2")
V4L2_PIX_FMT_XRGB444 = v4l2_fourcc("X", "R", "1", "2")
V4L2_PIX_FMT_RGBA444 = v4l2_fourcc("R", "A", "1", "2")
V4L2_PIX_FMT_RGBX444 = v4l2_fourcc("R", "X", "1", "2")
V4L2_PIX_FMT_ABGR444 = v4l2_fourcc("A", "B", "1", "2")
V4L2_PIX_FMT_XBGR444 = v4l2_fourcc("X", "B", "1", "2")
V4L2_PIX_FMT_BGRA444 = v4l2_fourcc("G", "A", "1", "2")
V4L2_PIX_FMT_BGRX444 = v4l2_fourcc("B", "X", "1", "2")
V4L2_PIX_FMT_RGB555 = v4l2_fourcc("R", "G", "B", "O")
V4L2_PIX_FMT_ARGB555 = v4l2_fourcc("A", "R", "1", "5")
V4L2_PIX_FMT_XRGB555 = v4l2_fourcc("X", "R", "1", "5")
V4L2_PIX_FMT_RGBA555 = v4l2_fourcc("R", "A", "1", "5")
V4L2_PIX_FMT_RGBX555 = v4l2_fourcc("R", "X", "1", "5")
V4L2_PIX_FMT_ABGR555 = v4l2_fourcc("A", "B", "1", "5")
V4L2_PIX_FMT_XBGR555 = v4l2_fourcc("X", "B", "1", "5")
V4L2_PIX_FMT_BGRA555 = v4l2_fourcc("B", "A", "1", "5")
V4L2_PIX_FMT_BGRX555 = v4l2_fourcc("B", "X", "1", "5")
V4L2_PIX_FMT_RGB565 = v4l2_fourcc("R", "G", "B", "P")
V4L2_PIX_FMT_RGB555X = v4l2_fourcc("R", "G", "B", "Q")
V4L2_PIX_FMT_ARGB555X = v4l2_fourcc_be("A", "R", "1", "5")
V4L2_PIX_FMT_XRGB555X = v4l2_fourcc_be("X", "R", "1", "5")
V4L2_PIX_FMT_RGB565X = v4l2_fourcc("R", "G", "B", "R")
V4L2_PIX_FMT_BGR666 = v4l2_fourcc("B", "G", "R", "H")
V4L2_PIX_FMT_BGR24 = v4l2_fourcc("B", "G", "R", "3")
V4L2_PIX_FMT_RGB24 = v4l2_fourcc("R", "G", "B", "3")
V4L2_PIX_FMT_BGR32 = v4l2_fourcc("B", "G", "R", "4")
V4L2_PIX_FMT_ABGR32 = v4l2_fourcc("A", "R", "2", "4")
V4L2_PIX_FMT_XBGR32 = v4l2_fourcc("X", "R", "2", "4")
V4L2_PIX_FMT_BGRA32 = v4l2_fourcc("R", "A", "2", "4")
V4L2_PIX_FMT_BGRX32 = v4l2_fourcc("R", "X", "2", "4")
V4L2_PIX_FMT_RGB32 = v4l2_fourcc("R", "G", "B", "4")
V4L2_PIX_FMT_RGBA32 = v4l2_fourcc("A", "B", "2", "4")
V4L2_PIX_FMT_RGBX32 = v4l2_fourcc("X", "B", "2", "4")
V4L2_PIX_FMT_ARGB32 = v4l2_fourcc("B", "A", "2", "4")
V4L2_PIX_FMT_XRGB32 = v4l2_fourcc("B", "X", "2", "4")
V4L2_PIX_FMT_GREY = v4l2_fourcc("G", "R", "E", "Y")
V4L2_PIX_FMT_Y4 = v4l2_fourcc("Y", "0", "4", " ")
V4L2_PIX_FMT_Y6 = v4l2_fourcc("Y", "0", "6", " ")
V4L2_PIX_FMT_Y10 = v4l2_fourcc("Y", "1", "0", " ")
V4L2_PIX_FMT_Y12 = v4l2_fourcc("Y", "1", "2", " ")
V4L2_PIX_FMT_Y14 = v4l2_fourcc("Y", "1", "4", " ")
V4L2_PIX_FMT_Y16 = v4l2_fourcc("Y", "1", "6", " ")
V4L2_PIX_FMT_Y16_BE = v4l2_fourcc_be("Y", "1", "6", " ")
V4L2_PIX_FMT_Y10BPACK = v4l2_fourcc("Y", "1", "0", "B")
V4L2_PIX_FMT_Y10P = v4l2_fourcc("Y", "1", "0", "P")
V4L2_PIX_FMT_IPU3_Y10 = v4l2_fourcc("i", "p", "3", "y")
V4L2_PIX_FMT_PAL8 = v4l2_fourcc("P", "A", "L", "8")
V4L2_PIX_FMT_UV8 = v4l2_fourcc("U", "V", "8", " ")
V4L2_PIX_FMT_YUYV = v4l2_fourcc("Y", "U", "Y", "V")
V4L2_PIX_FMT_YYUV = v4l2_fourcc("Y", "Y", "U", "V")
V4L2_PIX_FMT_YVYU = v4l2_fourcc("Y", "V", "Y", "U")
V4L2_PIX_FMT_UYVY = v4l2_fourcc("U", "Y", "V", "Y")
V4L2_PIX_FMT_VYUY = v4l2_fourcc("V", "Y", "U", "Y")
V4L2_PIX_FMT_Y41P = v4l2_fourcc("Y", "4", "1", "P")
V4L2_PIX_FMT_YUV444 = v4l2_fourcc("Y", "4", "4", "4")
V4L2_PIX_FMT_YUV555 = v4l2_fourcc("Y", "U", "V", "O")
V4L2_PIX_FMT_YUV565 = v4l2_fourcc("Y", "U", "V", "P")
V4L2_PIX_FMT_YUV24 = v4l2_fourcc("Y", "U", "V", "3")
V4L2_PIX_FMT_YUV32 = v4l2_fourcc("Y", "U", "V", "4")
V4L2_PIX_FMT_AYUV32 = v4l2_fourcc("A", "Y", "U", "V")
V4L2_PIX_FMT_XYUV32 = v4l2_fourcc("X", "Y", "U", "V")
V4L2_PIX_FMT_VUYA32 = v4l2_fourcc("V", "U", "Y", "A")
V4L2_PIX_FMT_VUYX32 = v4l2_fourcc("V", "U", "Y", "X")
V4L2_PIX_FMT_YUVA32 = v4l2_fourcc("Y", "U", "V", "A")
V4L2_PIX_FMT_YUVX32 = v4l2_fourcc("Y", "U", "V", "X")
V4L2_PIX_FMT_M420 = v4l2_fourcc("M", "4", "2", "0")
V4L2_PIX_FMT_NV12 = v4l2_fourcc("N", "V", "1", "2")
V4L2_PIX_FMT_NV21 = v4l2_fourcc("N", "V", "2", "1")
V4L2_PIX_FMT_NV16 = v4l2_fourcc("N", "V", "1", "6")
V4L2_PIX_FMT_NV61 = v4l2_fourcc("N", "V", "6", "1")
V4L2_PIX_FMT_NV24 = v4l2_fourcc("N", "V", "2", "4")
V4L2_PIX_FMT_NV42 = v4l2_fourcc("N", "V", "4", "2")
V4L2_PIX_FMT_P010 = v4l2_fourcc("P", "0", "1", "0")
V4L2_PIX_FMT_NV12M = v4l2_fourcc("N", "M", "1", "2")
V4L2_PIX_FMT_NV21M = v4l2_fourcc("N", "M", "2", "1")
V4L2_PIX_FMT_NV16M = v4l2_fourcc("N", "M", "1", "6")
V4L2_PIX_FMT_NV61M = v4l2_fourcc("N", "M", "6", "1")
V4L2_PIX_FMT_YUV410 = v4l2_fourcc("Y", "U", "V", "9")
V4L2_PIX_FMT_YVU410 = v4l2_fourcc("Y", "V", "U", "9")
V4L2_PIX_FMT_YUV411P = v4l2_fourcc("4", "1", "1", "P")
V4L2_PIX_FMT_YUV420 = v4l2_fourcc("Y", "U", "1", "2")
V4L2_PIX_FMT_YVU420 = v4l2_fourcc("Y", "V", "1", "2")
V4L2_PIX_FMT_YUV422P = v4l2_fourcc("4", "2", "2", "P")
V4L2_PIX_FMT_YUV420M = v4l2_fourcc("Y", "M", "1", "2")
V4L2_PIX_FMT_YVU420M = v4l2_fourcc("Y", "M", "2", "1")
V4L2_PIX_FMT_YUV422M = v4l2_fourcc("Y", "M", "1", "6")
V4L2_PIX_FMT_YVU422M = v4l2_fourcc("Y", "M", "6", "1")
V4L2_PIX_FMT_YUV444M = v4l2_fourcc("Y", "M", "2", "4")
V4L2_PIX_FMT_YVU444M = v4l2_fourcc("Y", "M", "4", "2")
V4L2_PIX_FMT_NV12_4L4 = v4l2_fourcc("V", "T", "1", "2")
V4L2_PIX_FMT_NV12_16L16 = v4l2_fourcc("H", "M", "1", "2")
V4L2_PIX_FMT_NV12_32L32 = v4l2_fourcc("S", "T", "1", "2")
V4L2_PIX_FMT_P010_4L4 = v4l2_fourcc("T", "0", "1", "0")
V4L2_PIX_FMT_NV12MT = v4l2_fourcc("T", "M", "1", "2")
V4L2_PIX_FMT_NV12MT_16X16 = v4l2_fourcc("V", "M", "1", "2")
V4L2_PIX_FMT_NV12M_8L128 = v4l2_fourcc("N", "A", "1", "2")
V4L2_PIX_FMT_NV12M_10BE_8L128 = v4l2_fourcc_be("N", "T", "1", "2")
V4L2_PIX_FMT_SBGGR8 = v4l2_fourcc("B", "A", "8", "1")
V4L2_PIX_FMT_SGBRG8 = v4l2_fourcc("G", "B", "R", "G")
V4L2_PIX_FMT_SGRBG8 = v4l2_fourcc("G", "R", "B", "G")
V4L2_PIX_FMT_SRGGB8 = v4l2_fourcc("R", "G", "G", "B")
V4L2_PIX_FMT_SBGGR10 = v4l2_fourcc("B", "G", "1", "0")
V4L2_PIX_FMT_SGBRG10 = v4l2_fourcc("G", "B", "1", "0")
V4L2_PIX_FMT_SGRBG10 = v4l2_fourcc("B", "A", "1", "0")
V4L2_PIX_FMT_SRGGB10 = v4l2_fourcc("R", "G", "1", "0")
V4L2_PIX_FMT_SBGGR10P = v4l2_fourcc("p", "B", "A", "A")
V4L2_PIX_FMT_SGBRG10P = v4l2_fourcc("p", "G", "A", "A")
V4L2_PIX_FMT_SGRBG10P = v4l2_fourcc("p", "g", "A", "A")
V4L2_PIX_FMT_SRGGB10P = v4l2_fourcc("p", "R", "A", "A")
V4L2_PIX_FMT_SBGGR10ALAW8 = v4l2_fourcc("a", "B", "A", "8")
V4L2_PIX_FMT_SGBRG10ALAW8 = v4l2_fourcc("a", "G", "A", "8")
V4L2_PIX_FMT_SGRBG10ALAW8 = v4l2_fourcc("a", "g", "A", "8")
V4L2_PIX_FMT_SRGGB10ALAW8 = v4l2_fourcc("a", "R", "A", "8")
V4L2_PIX_FMT_SBGGR10DPCM8 = v4l2_fourcc("b", "B", "A", "8")
V4L2_PIX_FMT_SGBRG10DPCM8 = v4l2_fourcc("b", "G", "A", "8")
V4L2_PIX_FMT_SGRBG10DPCM8 = v4l2_fourcc("B", "D", "1", "0")
V4L2_PIX_FMT_SRGGB10DPCM8 = v4l2_fourcc("b", "R", "A", "8")
V4L2_PIX_FMT_SBGGR12 = v4l2_fourcc("B", "G", "1", "2")
V4L2_PIX_FMT_SGBRG12 = v4l2_fourcc("G", "B", "1", "2")
V4L2_PIX_FMT_SGRBG12 = v4l2_fourcc("B", "A", "1", "2")
V4L2_PIX_FMT_SRGGB12 = v4l2_fourcc("R", "G", "1", "2")
V4L2_PIX_FMT_SBGGR12P = v4l2_fourcc("p", "B", "C", "C")
V4L2_PIX_FMT_SGBRG12P = v4l2_fourcc("p", "G", "C", "C")
V4L2_PIX_FMT_SGRBG12P = v4l2_fourcc("p", "g", "C", "C")
V4L2_PIX_FMT_SRGGB12P = v4l2_fourcc("p", "R", "C", "C")
V4L2_PIX_FMT_SBGGR14 = v4l2_fourcc("B", "G", "1", "4")
V4L2_PIX_FMT_SGBRG14 = v4l2_fourcc("G", "B", "1", "4")
V4L2_PIX_FMT_SGRBG14 = v4l2_fourcc("G", "R", "1", "4")
V4L2_PIX_FMT_SRGGB14 = v4l2_fourcc("R", "G", "1", "4")
V4L2_PIX_FMT_SBGGR14P = v4l2_fourcc("p", "B", "E", "E")
V4L2_PIX_FMT_SGBRG14P = v4l2_fourcc("p", "G", "E", "E")
V4L2_PIX_FMT_SGRBG14P = v4l2_fourcc("p", "g", "E", "E")
V4L2_PIX_FMT_SRGGB14P = v4l2_fourcc("p", "R", "E", "E")
V4L2_PIX_FMT_SBGGR16 = v4l2_fourcc("B", "Y", "R", "2")
V4L2_PIX_FMT_SGBRG16 = v4l2_fourcc("G", "B", "1", "6")
V4L2_PIX_FMT_SGRBG16 = v4l2_fourcc("G", "R", "1", "6")
V4L2_PIX_FMT_SRGGB16 = v4l2_fourcc("R", "G", "1", "6")
V4L2_PIX_FMT_HSV24 = v4l2_fourcc("H", "S", "V", "3")
V4L2_PIX_FMT_HSV32 = v4l2_fourcc("H", "S", "V", "4")
V4L2_PIX_FMT_MJPEG = v4l2_fourcc("M", "J", "P", "G")
V4L2_PIX_FMT_JPEG = v4l2_fourcc("J", "P", "E", "G")
V4L2_PIX_FMT_DV = v4l2_fourcc("d", "v", "s", "d")
V4L2_PIX_FMT_MPEG = v4l2_fourcc("M", "P", "E", "G")
V4L2_PIX_FMT_H264 = v4l2_fourcc("H", "2", "6", "4")
V4L2_PIX_FMT_H264_NO_SC = v4l2_fourcc("A", "V", "C", "1")
V4L2_PIX_FMT_H264_MVC = v4l2_fourcc("M", "2", "6", "4")
V4L2_PIX_FMT_H263 = v4l2_fourcc("H", "2", "6", "3")
V4L2_PIX_FMT_MPEG1 = v4l2_fourcc("M", "P", "G", "1")
V4L2_PIX_FMT_MPEG2 = v4l2_fourcc("M", "P", "G", "2")
V4L2_PIX_FMT_MPEG2_SLICE = v4l2_fourcc("M", "G", "2", "S")
V4L2_PIX_FMT_MPEG4 = v4l2_fourcc("M", "P", "G", "4")
V4L2_PIX_FMT_XVID = v4l2_fourcc("X", "V", "I", "D")
V4L2_PIX_FMT_VC1_ANNEX_G = v4l2_fourcc("V", "C", "1", "G")
V4L2_PIX_FMT_VC1_ANNEX_L = v4l2_fourcc("V", "C", "1", "L")
V4L2_PIX_FMT_VP8 = v4l2_fourcc("V", "P", "8", "0")
V4L2_PIX_FMT_VP8_FRAME = v4l2_fourcc("V", "P", "8", "F")
V4L2_PIX_FMT_VP9 = v4l2_fourcc("V", "P", "9", "0")
V4L2_PIX_FMT_VP9_FRAME = v4l2_fourcc("V", "P", "9", "F")
V4L2_PIX_FMT_HEVC = v4l2_fourcc("H", "E", "V", "C")
V4L2_PIX_FMT_FWHT = v4l2_fourcc("F", "W", "H", "T")
V4L2_PIX_FMT_FWHT_STATELESS = v4l2_fourcc("S", "F", "W", "H")
V4L2_PIX_FMT_H264_SLICE = v4l2_fourcc("S", "2", "6", "4")
V4L2_PIX_FMT_HEVC_SLICE = v4l2_fourcc("S", "2", "6", "5")
V4L2_PIX_FMT_CPIA1 = v4l2_fourcc("C", "P", "I", "A")
V4L2_PIX_FMT_WNVA = v4l2_fourcc("W", "N", "V", "A")
V4L2_PIX_FMT_SN9C10X = v4l2_fourcc("S", "9", "1", "0")
V4L2_PIX_FMT_SN9C20X_I420 = v4l2_fourcc("S", "9", "2", "0")
V4L2_PIX_FMT_PWC1 = v4l2_fourcc("P", "W", "C", "1")
V4L2_PIX_FMT_PWC2 = v4l2_fourcc("P", "W", "C", "2")
V4L2_PIX_FMT_ET61X251 = v4l2_fourcc("E", "6", "2", "5")
V4L2_PIX_FMT_SPCA501 = v4l2_fourcc("S", "5", "0", "1")
V4L2_PIX_FMT_SPCA505 = v4l2_fourcc("S", "5", "0", "5")
V4L2_PIX_FMT_SPCA508 = v4l2_fourcc("S", "5", "0", "8")
V4L2_PIX_FMT_SPCA561 = v4l2_fourcc("S", "5", "6", "1")
V4L2_PIX_FMT_PAC207 = v4l2_fourcc("P", "2", "0", "7")
V4L2_PIX_FMT_MR97310A = v4l2_fourcc("M", "3", "1", "0")
V4L2_PIX_FMT_JL2005BCD = v4l2_fourcc("J", "L", "2", "0")
V4L2_PIX_FMT_SN9C2028 = v4l2_fourcc("S", "O", "N", "X")
V4L2_PIX_FMT_SQ905C = v4l2_fourcc("9", "0", "5", "C")
V4L2_PIX_FMT_PJPG = v4l2_fourcc("P", "J", "P", "G")
V4L2_PIX_FMT_OV511 = v4l2_fourcc("O", "5", "1", "1")
V4L2_PIX_FMT_OV518 = v4l2_fourcc("O", "5", "1", "8")
V4L2_PIX_FMT_STV0680 = v4l2_fourcc("S", "6", "8", "0")
V4L2_PIX_FMT_TM6000 = v4l2_fourcc("T", "M", "6", "0")
V4L2_PIX_FMT_CIT_YYVYUY = v4l2_fourcc("C", "I", "T", "V")
V4L2_PIX_FMT_KONICA420 = v4l2_fourcc("K", "O", "N", "I")
V4L2_PIX_FMT_JPGL = v4l2_fourcc("J", "P", "G", "L")
V4L2_PIX_FMT_SE401 = v4l2_fourcc("S", "4", "0", "1")
V4L2_PIX_FMT_S5C_UYVY_JPG = v4l2_fourcc("S", "5", "C", "I")
V4L2_PIX_FMT_Y8I = v4l2_fourcc("Y", "8", "I", " ")
V4L2_PIX_FMT_Y12I = v4l2_fourcc("Y", "1", "2", "I")
V4L2_PIX_FMT_Z16 = v4l2_fourcc("Z", "1", "6", " ")
V4L2_PIX_FMT_MT21C = v4l2_fourcc("M", "T", "2", "1")
V4L2_PIX_FMT_MM21 = v4l2_fourcc("M", "M", "2", "1")
V4L2_PIX_FMT_INZI = v4l2_fourcc("I", "N", "Z", "I")
V4L2_PIX_FMT_CNF4 = v4l2_fourcc("C", "N", "F", "4")
V4L2_PIX_FMT_HI240 = v4l2_fourcc("H", "I", "2", "4")
V4L2_PIX_FMT_QC08C = v4l2_fourcc("Q", "0", "8", "C")
V4L2_PIX_FMT_QC10C = v4l2_fourcc("Q", "1", "0", "C")
V4L2_PIX_FMT_IPU3_SBGGR10 = v4l2_fourcc("i", "p", "3", "b")
V4L2_PIX_FMT_IPU3_SGBRG10 = v4l2_fourcc("i", "p", "3", "g")
V4L2_PIX_FMT_IPU3_SGRBG10 = v4l2_fourcc("i", "p", "3", "G")
V4L2_PIX_FMT_IPU3_SRGGB10 = v4l2_fourcc("i", "p", "3", "r")


pixfmt_rgb = [
    V4L2_PIX_FMT_RGB332,
    V4L2_PIX_FMT_RGB444,
    V4L2_PIX_FMT_RGB555,
    V4L2_PIX_FMT_RGB555X,
    V4L2_PIX_FMT_RGB565,
    V4L2_PIX_FMT_RGB565X,
    V4L2_PIX_FMT_RGB24,
    V4L2_PIX_FMT_RGB32,
]

pixfmt_rgba = [
    V4L2_PIX_FMT_RGBA444,
    V4L2_PIX_FMT_RGBA555,
    V4L2_PIX_FMT_RGBA32,
]
