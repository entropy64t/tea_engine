# cython: boundscheck=False, wraparound=False

def concat_bytearr(list buffer, list clr_buffer, dict ansi, int h, int w):
    cdef bytearray out = bytearray()
    cdef int y, x, begin
    cdef tuple c, current
    cdef list row, crow

    out.extend(b"\x1b[H")

    for y in range(h):
        row = buffer[y]
        crow = clr_buffer[y]
        x = 0
        current = None

        while x < w:
            begin = x
            c = crow[x]
            while x < w and crow[x] == c:
                x += 1

            if c != current:
                out.extend(ansi[c])
                current = c

            # join in Python, but loop is in C
            out.extend("".join(row[begin:x]).encode("ascii"))

        out.extend(b"\x1b[0m\n")

    return out
