from __future__ import annotations
from enum import Enum

class AnimationData:
    def __init__(self, frame_count: int, frames_l: list[str], frames_r: list[str], frame_time: float) -> None:
        self.frame_count = frame_count
        self._frames_l = frames_l
        self._frames_r = frames_r
        self.frame_time = frame_time
        self.active_frames = self._frames_l
        self._frame = 0
        if self.frame_count != len(self._frames_l):
            raise ValueError("Frame count does not match the amount of frames facing left")
        if self.frame_count != len(self._frames_r):
            raise ValueError("Frame count does not match the amount of frames facing rignt")
        
    def animate(self):
        self._frame += 1
        if self._frame >= self.frame_count:
            self._frame = 0
            
        return self.active_frames[self._frame]

    @staticmethod
    def copy(anim_data: AnimationData, variation: bool = False):
        new = AnimationData(
            frame_count=anim_data.frame_count,
            frames_l=anim_data._frames_l,
            frames_r=anim_data._frames_r,
            frame_time=anim_data.frame_time
        )
        if variation:
            import random
            new._frame = random.randint(0, new.frame_count)
        return new
        
class Colour:
    def __init__(self, r: int, g: int, b: int, is_bg: bool = False) -> None:
        self.r = r
        self.g = g
        self.b = b
        self.is_bg = is_bg
        self._switch = 38 if not is_bg else 48
        self.str = f"\x1b[{self._switch};2;{self.r};{self.g};{self.b}m"
        self.tpl = (self.r, self.g, self.b)
    
    @staticmethod
    def reset():
        return f"\x1b[0m"
    
    @staticmethod
    def from_str(string: str):
        return FgPresets[string.upper()].value
        
class FgPresets(Enum):
    WHITE = Colour(255, 255, 255)
    BLACK = Colour(0, 0, 0)
    GREEN = Colour(25, 222, 50)
    BLUE = Colour(25, 50, 225)
    RED = Colour(155, 30, 0)
    ORANGE = Colour(235, 107, 52)
    YELLOW = Colour(224, 188, 56)