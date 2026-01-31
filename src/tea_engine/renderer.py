from __future__ import annotations
from typing import TYPE_CHECKING
import sys

if TYPE_CHECKING:
    from tea_engine import Engine, Bounds2
from tea_engine.cy.renderer_concat import concat_bytearr
from tea_engine import FgPresets, Colour

ansi_rgb = {}

class Renderer:
    def __init__(self, engine: Engine) -> None:
        self.engine = engine
        
        self.w = self.engine.bounds.br.x - self.engine.bounds.tl.x + 2
        self.h = self.engine.bounds.br.y - self.engine.bounds.tl.y + 3
        self.buffer = [[" "] * self.w for j in range(self.h)]
        self.clr_buffer = [[(0, 0, 0)] * self.w for j in range(self.h)]
        bord_w = ["#"] * self.w
        cbord_w = [(100, 200, 255)] * self.w
        
        self.buffer[0][:] = bord_w
        self.buffer[-1][:] = bord_w
        self.clr_buffer[0][:] = cbord_w
        self.clr_buffer[-1][:] = cbord_w
        for i in range(self.h):
            self.buffer[i][0] = "#"
            self.clr_buffer[i][0] = (100, 200, 255)
            self.buffer[i][-1] = "#"
            self.clr_buffer[i][-1] = (100, 200, 255)
            
        self.out: list[str] = []
        self.bytes = bytearray()
        
        for colour in FgPresets:
            ansi_rgb[colour.value.tpl] = bytes(colour.value.str, 'ascii')
            
        ansi_rgb[(100, 200, 255)] = bytes(Colour(100, 200, 255).str, 'ascii')
    
    def render(self):
        self.clear()
        self.generate()
        self.fast_concat()
        self.write_bytearr()

    def generate(self):
        for nameid, entity in self.engine.entities.items():
            x = entity.position.x
            y = entity.position.y

            if not (0 <= y < self.h - 2):
                continue

            spr = entity.sprite   # MUST be cached!
            clr = entity.colour
            row = self.buffer[y + 1]
            clrow = self.clr_buffer[y + 1]

            for i, ch in enumerate(spr):
                xi = x + i + 1
                if 0 <= xi < self.w:
                    row[xi] = ch
                    clrow[xi] = clr[i].tpl        
                    
    def fast_concat(self):
        self.bytes = concat_bytearr(
            self.buffer,
            self.clr_buffer,
            ansi_rgb,
            self.h,
            self.w
        )

    def concat_v2(self):
        out = self.out
        app = out.append
        ext = out.extend
        ansi = ansi_rgb
        bfr = self.buffer
        cbfr = self.clr_buffer
        
        out.clear()
        out.append("\x1b[H")

        for y in range(self.h):
            row = bfr[y]
            crow = cbfr[y]

            x = 0
            while x < self.w:
                begin = x
                c = crow[x]
                while x < self.w and crow[x] == c:
                    x += 1
                if c not in ansi:
                    ansi[c] = f"\x1b[38;2;{c[0]};{c[1]};{c[2]}m"
                app(ansi[c])
                ext(row[begin:x])
                
            app("\x1b[0m\n")
            
    def concat(self):
        self.out.clear() 
        self.out.append("\x1b[H") 
        
        current_color = (-1, -1, -1) 
        
        for y in range(self.h): 
            row = self.buffer[y] 
            crow = self.clr_buffer[y] 
            
            for x in range(self.w): 
                c = crow[x] 
                if c != current_color: 
                    if c not in ansi_rgb: 
                        ansi_rgb[c] = f"\x1b[38;2;{c[0]};{c[1]};{c[2]}m" 
                    self.out.append(ansi_rgb[c]) 
                    current_color = c 
                self.out.append(row[x]) 
                    
            self.out.append("\x1b[0m\n") 
            current_color = (-1, -1, -1)
    
    def concat_bytearr(self):
        out = bytearray()
        ansi = ansi_rgb  # dict mapping (r,g,b) -> ANSI bytes
        bfr = self.buffer
        cbfr = self.clr_buffer

        out.extend(b"\x1b[H")  # move cursor to top-left

        for y in range(self.h):
            row = bfr[y]
            crow = cbfr[y]

            x = 0
            current_color = None

            while x < self.w:
                begin = x
                c = crow[x]

                # advance x while color stays the same
                while x < self.w and crow[x] == c:
                    x += 1

                # add ANSI code if color changed
                if c != current_color:
                    if c not in ansi:
                        ansi[c] = f"\x1b[38;2;{c[0]};{c[1]};{c[2]}m".encode('ascii')
                    out.extend(ansi[c])
                    current_color = c

                # append the whole run at once
                out.extend(''.join(row[begin:x]).encode('ascii'))

            # reset color at end of line
            out.extend(b"\x1b[0m\n")
            current_color = None
        self.bytes = out
            
    def write(self):
        sys.stdout.write("".join(self.out))
        sys.stdout.flush()
        
    def write_bytearr(self):
        sys.stdout.buffer.write(self.bytes)
        
    def clear(self):
        blank = [" "] * (self.w - 2)
        bclr = [(0, 0, 0)] * (self.w - 2)
        for y in range(1, self.h - 1):
            self.buffer[y][1:-1] = blank
            self.clr_buffer[y][1:-1] = bclr