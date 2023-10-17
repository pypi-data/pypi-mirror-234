import os
from .types import Offset, Length


class Data:
    def __init__(self, filepath:str, end:Offset, ro:bool=True):
        open(filepath, 'ab').close()
        mode = 'rb' if ro else 'rb+'
        self.f = open(filepath, mode)
        self.end = end

    def __len__(self):
        return self.end

    def read(self, offset:Offset, length:Length) -> bytes:
        self.f.seek(offset)
        return self.f.read(length)

    def write(self, offset:Offset, b:bytes) -> Length:
        self.f.seek(offset)
        return self.f.write(b)

    def append(self, b:bytes) -> tuple[Offset, Length]:
        length = self.write(self.end, b)
        self.end += length
        return self.end - length, length

    def commit(self):
        self.f.flush()
        os.fsync(self.f.fileno())

    def close(self):
        self.f.close()
