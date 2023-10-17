import sqlite3
from typing import Optional
from .types import Key, Keytype, Offset, Length, Checksum


class Index:
    def __init__(self, filepath:str, keytype:Keytype):
        self.conn = sqlite3.connect(filepath)
        self.conn.execute('PRAGMA journal_mode = WAL')
        self.conn.execute(f'''
            CREATE TABLE IF NOT EXISTS main (
                key {'INTEGER' if keytype == 'int' else 'TEXT'} PRIMARY KEY,
                offset INTEGER NOT NULL,
                length INTEGER NOT NULL,
                crc32 INTEGER NOT NULL
            )
        ''')
        self.conn.commit()

    def get_end(self) -> int:
        return self.conn.execute('''
            SELECT COALESCE(MAX(offset + length), 0)
            FROM main
        ''').fetchone()[0]

    def get(self, key:Key) -> Optional[tuple[int, int]]:
        return self.conn.execute('''
            SELECT offset, length
            FROM main WHERE key = ?
        ''', [key]).fetchone()

    def put(self, key:Key, offset:Offset, length:Length, crc32:Checksum):
        self.conn.execute('''
            INSERT OR REPLACE INTO main (key, offset, length, crc32)
            VALUES (?, ?, ?, ?)
        ''', [key, offset, length, crc32])

    def __delitem__(self, key:Key):
        self.conn.execute('DELETE FROM main WHERE key = ?', [key])

    def __len__(self):
        return self.conn.execute('''
            SELECT COUNT(key) FROM main
        ''').fetchone()[0]

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()
