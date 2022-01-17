import csv
import heapq
import os
from uuid import uuid4

from tree import Tree


class SSTable:
    def __init__(self):
        self.filename = f"/tmp/sstable-{uuid4()}"

    def write(self, values):
        with open(self.filename, "w") as fp:
            csv.writer(fp).writerows(values)

    def read(self):
        with open(self.filename) as fp:
            yield from csv.reader(fp)


class LSM:
    def __init__(self):
        self.memtable = Tree()
        self.sstables = []

    def get(self, key):
        try:
            return self.memtable.get(key)
        except KeyError:
            return self._get_from_disk(key)

    def set(self, key, val):
        self.memtable.set(key, val)

    def flush(self):
        table = SSTable()
        table.write(self.memtable.walk())
        self.sstables.append(table)
        self.memtable = Tree()

    def compact(self):
        streams = [table.read() for table in self.sstables]
        merged = heapq.merge(*streams, key=lambda x: x[0])
        new_table = SSTable()
        new_table.write(merged)
        compacted_tables = self.sstables
        self.sstables = [new_table]
        for table in compacted_tables:
            os.remove(table.filename)

    def _get_from_disk(self, key):
        for table in reversed(self.sstables):
            for stored_key, val in table.read():
                if stored_key == key:
                    return val
                if stored_key > key:
                    break
        raise KeyError
