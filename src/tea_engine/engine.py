from __future__ import annotations
from typing import TYPE_CHECKING

from tea_engine import Bounds2, Vector2
if TYPE_CHECKING:
    from tea_engine import Entity
from tea_engine.cy.spacegrid import SpaceGrid

class Engine:
    def __init__(self, bounds: Bounds2, logging: bool = False) -> None:
        self.entities: dict[int, Entity] = {} # fish nameid -> fish
        # self.fish: set[Fish] = set()
        self.bounds = bounds
        self.curr_id = 0
        # self.log = Log(logging)
        self.removes: list[Entity] = []
        self.width = self.bounds.br.x - self.bounds.tl.x
        
        # self.space: dict[int, set[str]] = {} # posy * bounds.y + posx -> fish nameids on that tile
        self.space = SpaceGrid(self.width)
    
    def spawn(self, data: Entity, position: Vector2):
        entity = data.copy(position, self, self.curr_id)
        # self.fish.add(fish)
        self.entities[entity.nameid()] = entity
        start = entity.position.x + entity.position.y * self.width
        count = entity.sprite_len
        self.space.add_range(start, count, 1, entity.nameid())
        self.curr_id += 1
        return entity
    
    def remove(self, entity: Entity):
        self.removes.append(entity)
        
    def update(self):
        self._animate_ents()
        
        self._move_ents()
                    
        self._collide_ents()
        
        self._remove_ents()
        
    def _collide_ents(self):
        for nameid, entity in self.entities.items():
            # collision checks
            for i in range(entity.sprite_len):
                sp = self.space.get(entity.position.x + i + entity.position.y * self.width)
                if len(sp) > 1:
                    # collide! 
                    for other_nameid in sp:
                        if other_nameid == nameid:
                            continue
                        self.entities[nameid].on_collision(self.entities[other_nameid])
                        
    def _remove_ents(self):
        for entity in self.removes:
            if entity not in self.entities:
                continue
            n = entity.nameid()
            self.entities.pop(n)
            start = entity.position.x + entity.position.y * self.width
            count = entity.sprite_len
            self.space.rem_range(start, count, 1, n)
            print(f"removed {entity}")
            input()
                
        self.removes.clear()
        
    def _move_ents(self):
        for nameid, entity in self.entities.items():
            if entity.ai == None: 
                continue
            
            entity.ai.update(entity, self)
            
            self.spacemov(entity)
            
    def _animate_ents(self):
        for entity in self.entities.values():
            if entity.has_animation:
                entity.update_sprite()
            # self.log.print(f"{fish.nameid()} updates sprite!")
                
    def _spacemov(self, entity: Entity):
        # Precompute commonly used values
        x = entity.position.x
        y = entity.position.y
        w = self.width
        dir = entity.direction
        nameid = entity.nameid()
        sprite_len = entity.sprite_len

        # Move in x
        x += dir.x
        if dir.x == -1:
            self.space.add_range(x + y*w, 1, 1, nameid)
            self.space.rem_range(x + y*w + sprite_len, 1, 1, nameid)
        elif dir.x == 1:
            self.space.add_range(x + y*w + sprite_len - 1, 1, 1, nameid)
            self.space.rem_range(x + y*w - 1, 1, 1, nameid)
        
        # Move in y
        y += dir.y
        if dir.y == -1:
            base = x + y*w
            self.space.add_range(base, sprite_len, 1, nameid)
            self.space.rem_range(base + w, sprite_len, 1, nameid)
        elif dir.y == 1:
            base = x + y*w
            self.space.add_range(base, sprite_len, 1, nameid)
            self.space.rem_range(base - w, sprite_len, 1, nameid)

        # Update entity position
        entity.position.x = x
        entity.position.y = y