from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Iterable, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from tea_engine import Engine, AIBase
from .cy.vector import Vector2, Bounds2
from .graphic_things import Colour

class EntityTag:
    def __init__(self, tag_name: str) -> None:
        self.tag_name = tag_name.upper().strip()
        self._tv = hash(self.tag_name)
         
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, EntityTag): 
            return False
        
        return self._tv == value._tv
    
    def __repr__(self) -> str:
        return self.tag_name
    
class Entity:
    sprite: str = "<nosprite>"
    sprite_len: int = 0
    colour: list[Colour] = []
    map_bounds: Bounds2 
    collider: Bounds2
    has_animation: bool = False
    
    def __init__(self, name: str, tags: list[EntityTag], engine: Optional[Engine] = None) -> None:
        self.name = name
        self.tags = tags
        self.engine = engine
        self.position = Vector2()
        self.direction = Vector2()
        self.ai = None
        self.id = 0
        
    def add_tag(self, tag: EntityTag):
        self.tags.append(tag)
        
    def has_tag(self, tag: EntityTag | str):
        if isinstance(tag, EntityTag):
            return tag in self.tags
        else:
            return EntityTag(tag) in self.tags
        
    def copy(self, pos: Vector2, engine: Optional[Engine] = None, id: int = 0):
        eng = engine if engine else self.engine
        cpy = Entity(
            self.name,
            self.tags,
            eng
        )
        cpy.position = pos
        cpy.id = id
        cpy.colour = self.colour
        cpy.sprite = self.sprite
        cpy.map_bounds = self.map_bounds
        cpy.sprite_len = self.sprite_len
        cpy.has_animation = self.has_animation
        cpy.ai = cpy.ai or self.ai
        return cpy
        
    def has_any_tag(self, tags: Iterable[EntityTag | str]):
        return any(self.has_tag(t) for t in tags)
        
    def assign_ai(self, ai: AIBase):
        self.ai = ai
        
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Entity): 
            return super().__eq__(value)
        return value.name == self.name and value.id == self.id
    
    def __hash__(self) -> int:
        return self.nameid().__hash__()
    
    def nameid(self):
        return self.id#f"{self.name}_{self.id}"
        
    def on_collision(self, other: Entity):
        "Abstract method for managing collisions" 
        pass
    
    def collides(self, other: Entity):
        pymatch = self.position.y == other.position.y
        if not pymatch:
            return False
        
        xstart = self.position.x
        xend = xstart + self.sprite_len
        
        c1 = xstart <= other.position.x <= xend
        
        xstart = other.position.x
        xend = xstart + other.sprite_len
        
        c2 = xstart <= self.position.x <= xend
        
        return c1 or c2