# BlobKeeper
BlobKeeper is a lightweight Python library for managing binary data blobs efficiently and persistently using SQLite and a contiguous binary data file. It's designed for scenarios where you need to store and retrieve binary data associated with keys.



## Features
- Efficient storage and retrieval of binary data blobs.
- Using SQLite for locking & metadata.
- Support for integer or text keys.
- Optional data file read-only mode.
- Data integrity checks using CRC32 checksums.
- Written in pure-Python with zero dependencies.



## Installation
You can install BlobKeeper using pip:
```bash
pip3 install blobkeeper
```



## Quick Start
Here's how to get started with BlobKeeper:
```python
from blobkeeper import connect
# Create a connection with default settings (integer keys, read-only mode).
connection = connect('my_blobs')
# Storing binary data
connection['my_key'] = b'Hello, BlobKeeper!'
# Retrieving binary data
data = connection['my_key']
# Checking the number of items stored
count = connection.count()
# Closing the connection
connection.close()
```



## Documentation
### `connect(path: str, keytype: Keytype = str, ro: bool = False) -> Connection`
- `path`: The base file name for the BlobKeeper storage (without extension).
- `keytype`: The type of keys used (int for integer keys or str for text keys).
- `ro`: Read-only mode. If set to `True`, the Connection won't allow file modifications.
### `Connection` Class
#### `get(key: Key) -> Optional[bytes]`
Retrieve binary data associated with a key or None.
#### `__getitem__(key: Key) -> bytes`
Retrieve binary data associated with a key. KeyError is not exists.
#### `__setitem__(key: Key, value: bytes) -> None`
Store binary data associated with a key.
#### `__delitem__(key: Key) -> None`
Delete key rendering data inaccessible.
#### `count() -> int`
Return number of items stored.
#### `size() -> int`
Return the size of the data file in bytes.
#### `commit() -> None`
Commit changes to disk.
#### `close() -> None`
Commit changes & close connection.



## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.



## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
