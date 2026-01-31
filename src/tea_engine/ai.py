from abc import ABC, abstractmethod

from typing import Optional, TYPE_CHECKING

from tea_engine.entity import Entity
from tea_engine.engine import Engine

class AIBase(ABC):
    @abstractmethod
    def update(self, entity_tied: Entity, engine: Optional[Engine]):
        "do nothing"
        
class SimpleAI(AIBase):
    def update(self, entity_tied: Entity, engine: Optional[Engine]):
        if engine is None:
            raise ValueError("SimpleAI needs access to Engine")
                                        
        entity_tied.direction.randomize(entity_tied.position, entity_tied.map_bounds)