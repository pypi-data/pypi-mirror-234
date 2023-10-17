#!/usr/bin/env python
import hashlib
import os
from typing import Any, Dict, Iterator, List, Optional, Set, Tuple, Union

from codefast.io.file import FileIO as fio
import pickle 

class fdb(object):
    """ simple key-value database implementation using expiringdict
    """

    def __init__(self, dbpath: str = '/tmp/osdb'):
        '''
        Args:
            ...
        '''
        self.dbpath = dbpath
        fio.rm(dbpath)  # in case file with same name exists

        if not fio.exists(dbpath):
            fio.mkdir(self.dbpath)

    def get_path(self, key: str) -> str:
        return os.path.join(self.dbpath,
                            hashlib.md5(str(key).encode()).hexdigest())

    def set(self, key: str, value: str):
        with open(self.get_path(key), 'w') as f:
            f.write(str(value))

    def get(self, key: str) -> Union[str, None]:
        return fio.reads(self.get_path(key))

    def exists(self, key: str) -> bool:
        return fio.exists(self.get_path(key))

    def keys(self) -> Iterator[str]:
        raise Exception(
            'there is no keys() method for this db, use osdb instead'
        )
    
    def values(self) -> Iterator[str]:
        for k in fio.walk(self.dbpath):
            yield fio.reads(k)

    def __getitem__(self, key: str) -> Union[str, None]:
        return self.get(key)

    def __setitem__(self, key: str, value: str) -> None:
        self.set(key, value)

    def delete(self, key: str) -> None:
        return self.pop(key)

    def __len__(self) -> int:
        return len([k for k in self.values()])

    def __repr__(self) -> str:
        return 'fdb(%s)' % self.dbpath

    
