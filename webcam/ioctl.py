from ctypes import sizeof
from fcntl import ioctl

_IOC_NRBITS = 8
_IOC_TYPEBITS = 8
_IOC_SIZEBITS = 14
_IOC_DIRBITS = 2

_IOC_NRSHIFT = 0
_IOC_TYPESHIFT = _IOC_NRSHIFT + _IOC_NRBITS
_IOC_SIZESHIFT = _IOC_TYPESHIFT + _IOC_TYPEBITS
_IOC_DIRSHIFT = _IOC_SIZESHIFT + _IOC_SIZEBITS

_IOC_NONE = 0
_IOC_WRITE = 1
_IOC_READ = 2


def _IOC(dir, type, nr, size):
    return (
        (dir << _IOC_DIRSHIFT)
        | (type << _IOC_TYPESHIFT)
        | (nr << _IOC_NRSHIFT)
        | (size << _IOC_SIZESHIFT)
    )


def _IOR(type, nr, struct):
    request = _IOC(_IOC_READ, ord(type), nr, sizeof(struct))

    def f(fileno):
        buffer = struct()
        ioctl(fileno, request, buffer)
        return buffer

    return f


def _IOW(type, nr, struct):
    request = _IOC(_IOC_WRITE, ord(type), nr, sizeof(struct))

    def f(fileno, buffer):
        ioctl(fileno, request, buffer)

    return f


def _IOWR(type, nr, struct):
    request = _IOC(_IOC_READ | _IOC_WRITE, ord(type), nr, sizeof(struct))

    def f(fileno, buffer):
        ioctl(fileno, request, buffer)
        return buffer

    return f
