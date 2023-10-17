import zlib
from typing import Optional
from .data import Data
from .index import Index
from .types import Key, Keytype


class Connection:
    def __init__(self, path:str, keytype:Keytype=str, ro:bool=False):
        self.index = Index(f'{path}.index', keytype)
        self.data = Data(f'{path}.data', self.index.get_end(), ro)
        self.ro = ro

    def get(self, key:Key) -> Optional[bytes]:
        '''Retrieve binary data associated with a key or None.
        '''
        if (record := self.index.get(key)) is not None:
            return self.data.read(*record)

    def __getitem__(self, key:Key) -> bytes:
        '''Retrieve binary data associated with a key. KeyError is not exists.
        '''
        if (out := self.get(key)) is None:
            raise KeyError
        return out

    def __setitem__(self, key:str, value:bytes):
        '''Store binary data associated with a key.
        '''
        assert not self.ro, 'Opened in readonly mode.'
        offset, length = self.data.append(value)
        self.index.put(key, offset, length, zlib.crc32(value))

    def __delitem__(self, key:str):
        '''Delete key rendering data inaccessible.
        '''
        assert not self.ro, 'Opened in readonly mode.'
        del self.index[key]

    def count(self) -> int:
        '''Return number of items stored.
        '''
        return len(self.index)

    def size(self) -> int:
        '''Return the size of the data file in bytes.
        '''
        return len(self.data)

    def commit(self):
        '''Commit changes.
        '''
        self.data.commit()
        self.index.commit()

    def close(self):
        '''Commit changes & close connection.
        '''
        self.commit()
        self.data.close()
        self.index.close()


def connect(*args, **kwargs) -> Connection:
    return Connection(*args, **kwargs)
