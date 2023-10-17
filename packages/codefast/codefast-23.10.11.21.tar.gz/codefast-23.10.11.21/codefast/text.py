#!/usr/bin/env python3
from typing import List, Any

class MarkDownHelper(object):

    @staticmethod
    def to_table(headers:List[Any], data:List[List[Any]]) -> str:
        """ Convert data to markdown table.
        Args:
            headers: list of str
            data: list of list of str
        """
        for d in data:
            assert len(headers) == len(
                d), f'{headers} vs {d} not match on length'
        table = []
        headers = [''] + headers + ['']
        table.append('|'.join(headers))
        splits = [''] + ['-'] * (len(headers) - 2) + ['']
        table.append('|'.join(splits))
        for row in data:
            row = [''] + list(map(str, row)) + ['']
            table.append('|'.join(row))
        return '\n'.join(table)
