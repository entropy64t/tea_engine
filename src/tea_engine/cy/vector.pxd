cdef class Vector2:
    cdef public int x
    cdef public int y

    cpdef Vector2 copy(self)
    cpdef void set(self, int x, int y)
    cpdef void randomize(self, Vector2 pos, Bounds2 bounds)

cdef class Bounds2:
    cdef public Vector2 _tl
    cdef public Vector2 _br

    cpdef bint contains_xy(self, int x, int y)
    cpdef Bounds2 shrink(self, int x, int y)