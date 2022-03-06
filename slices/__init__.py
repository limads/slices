import ctypes
from ctypes import cdll, c_double, c_void_p, pointer, Structure, c_int, c_ulong, cast, POINTER, sizeof

def contiguous_access(i, ptr, len):
    if i >= 0:
        if i < len:
            return ptr[i]
        else:
            raise IndexError(f"Index {i} outside range of slice of size {len}")
    else:
        if abs(i) < len:
            return ptr[len - abs(i)]
        else:
            raise IndexError(f"Reverse index {i} outside range of slice of size {len}")

class SliceIter:

    def __init__(self, slice):
        self.slice = slice
        self.index = -1

    def __next__(self):
        self.index = self.index + 1
        if self.index == self.slice.len:
            raise StopIteration
        return self.slice[self.index]

# Might export that to PyPI as module named "slices". Then at Python, import slices.Slice, and use that
# to work with Rust/Python FFI.
class Slice(Structure):
    _fields_ = [("ptr", POINTER(c_double)), ("len", c_ulong)]

    def __repr__(self):
        s = "Slice(["
        for i in range(self.len - 1):
            s += f"{self[i]}, "
        s += f"{self[self.len-1]}])"
        return s

    def len(self):
        return self.len

    def __init__(self, iterable=[]):
        v = list(iterable)
        
        raw_buf = ctypes.create_string_buffer(sizeof(c_double) * len(v))
        buf = cast(raw_buf, ctypes.POINTER(ctypes.c_double))
        
        for (ix, a) in enumerate(v):
            buf[ix] = a

        self.ptr = buf
        self.len = len(v)

    def __getitem__(self, i):
        return contiguous_access(i, self.ptr, self.len)

    def __iter__(self):
        return SliceIter(self)


