# cython: boundscheck=False, wraparound=False, cdivision=True

from libc.stdlib cimport malloc, free
from cpython.set cimport PySet_Add, PySet_Discard
from cpython.dict cimport PyDict_GetItem, PyDict_SetItem

cdef class SpaceGrid:
    cdef dict grid
    cdef int width

    def __init__(self, int width):
        self.grid = {}
        self.width = width

    cdef inline void _add(self, int idx, object nameid):
        cdef object s = self.grid.get(idx)
        if s is None:
            s = set()
            self.grid[idx] = s
        PySet_Add(s, nameid)

    cdef inline void _rem(self, int idx, object nameid):
        cdef object s = self.grid.get(idx)
        if s is None:
            return
        PySet_Discard(s, nameid)
        if not s:
            del self.grid[idx]

    # batch add
    def add_range(self, int start, int count, int step, object nameid):
        cdef int i
        for i in range(count):
            self._add(start + i * step, nameid)

    # batch remove
    def rem_range(self, int start, int count, int step, object nameid):
        cdef int i
        for i in range(count):
            self._rem(start + i * step, nameid)

    def get(self, int where, object default = None):
        return self.grid.get(where, default)
