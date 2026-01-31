# cython: boundscheck=False, wraparound=False, cdivision=True
from libc.stdlib cimport rand, RAND_MAX

cdef int DIRS[8][2]
DIRS[:] = [
    (-1, -1), (-1, 0), (-1, 1),
    ( 0, -1),          ( 0, 1),
    ( 1, -1), ( 1, 0), ( 1, 1),
]

cdef class Vector2:
    cdef public int x
    cdef public int y

    def __init__(self, int x=0, int y=0):
        self.x = x
        self.y = y

    cpdef Vector2 copy(self):
        return Vector2(self.x, self.y)

    cpdef void set(self, int x, int y):
        self.x = x
        self.y = y

    def __add__(self, Vector2 other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, Vector2 other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __repr__(self):
        return f"Vector2({self.x}, {self.y})"

    cpdef void randomize(self, Vector2 pos, Bounds2 bounds):
        cdef int vx = self.x
        cdef int vy = self.y
        cdef int px = pos.x
        cdef int py = pos.y

        cdef int minx = bounds._tl.x
        cdef int miny = bounds._tl.y
        cdef int maxx = bounds._br.x
        cdef int maxy = bounds._br.y

        cdef int dx, dy, nx, ny
        cdef int ddx, ddy

        # fallback direction
        cdef int fb_dx = 0
        cdef int fb_dy = 0
        cdef bint has_fb = False

        # valid candidates (stack-allocated)
        cdef int cand_dx[8]
        cdef int cand_dy[8]
        cdef int n = 0
        cdef int i

        for i in range(8):
            dx = DIRS[i][0]
            dy = DIRS[i][1]

            nx = px + dx
            ny = py + dy

            # bounds check
            if nx < minx or nx > maxx or ny < miny or ny > maxy:
                continue

            # first in-bounds = fallback
            if not has_fb:
                fb_dx = dx
                fb_dy = dy
                has_fb = True

            # (new - old).length² == 1
            ddx = dx - vx
            ddy = dy - vy
            if ddx*ddx + ddy*ddy == 1:
                cand_dx[n] = dx
                cand_dy[n] = dy
                n += 1

        if n > 0:
            i = rand() % n
            self.x = cand_dx[i]
            self.y = cand_dy[i]
        elif has_fb:
            self.x = fb_dx
            self.y = fb_dy
        else:
            self.x = 0
            self.y = 0



cdef class Bounds2:
    cdef public Vector2 _tl
    cdef public Vector2 _br

    def __init__(self, Vector2 top_left, Vector2 bottom_right):
        self._tl = top_left
        self._br = bottom_right

    cpdef bint contains_xy(self, int x, int y):
        return (
            self._tl.x <= x <= self._br.x and
            self._tl.y <= y <= self._br.y
        )

    def __contains__(self, Vector2 p):
        return self.contains_xy(p.x, p.y)

    def __add__(self, Vector2 v):
        return Bounds2(
            Vector2(self._tl.x + v.x, self._tl.y + v.y),
            Vector2(self._br.x + v.x, self._br.y + v.y),
        )

    cpdef Bounds2 shrink(self, int x, int y):
        return Bounds2(
            self._tl,
            Vector2(self._br.x - x, self._br.y - y)
        )

    @property
    def tl(self):
        return self._tl

    @property
    def br(self):
        return self._br
