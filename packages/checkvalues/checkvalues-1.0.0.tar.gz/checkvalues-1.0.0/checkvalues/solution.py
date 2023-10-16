import hashlib

import pandas as pd


class Solution(object):
    def __init__(self):
        self._df = pd.DataFrame(columns=["label", "type", "name", "args", "kwargs", "encrypted", "expected", "points"])

    def add(self, label, type, name, expected, args=None, kwargs=None, encrypted=True, points=1):
        if encrypted: expected = hashlib.md5(str(expected).encode()).hexdigest()
        self._df.loc[len(self._df), self._df.columns] =\
            [label, type, name, args, kwargs, encrypted, expected, points]

    def save(self, path):
        self._df.to_csv(path, index=False)