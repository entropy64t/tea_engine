"""TeaEngine package"""

# terminal_engine/__init__.py

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .engine import Engine
    from .renderer import Renderer
    from .types import Vector2, Bounds2
    from .ai import AIBase, SimpleAI
    from .clock import Clock
    from .graphic_things import Colour, AnimationData, FgPresets
    from .entity import Entity, EntityTag

__all__ = (
    "Engine",
    "Renderer",
    "Vector2",
    "Bounds2",
    "AIBase",
    "Clock",
    "Colour",
    "AnimationData",
    "FgPresets",
    "Entity",
    "EntityTag",
    "SimpleAI"
)

_import_cache = {}

def __getattr__(name: str):
    if name in _import_cache:
        return _import_cache[name]
    
    if name == 'Engine':
        from .engine import Engine
        _import_cache[name] = Engine
    if name == 'Renderer':
        from .renderer import Renderer
        _import_cache[name] = Renderer
    if name == 'AIBase':
        from .ai import AIBase
        _import_cache[name] = AIBase
    if name == 'SimpleAI':
        from .ai import SimpleAI
        _import_cache[name] = SimpleAI
    if name == 'Vector2':
        from .cy.vector import Vector2
        _import_cache[name] = Vector2
    if name == 'Bounds2':
        from .cy.vector import Bounds2
        _import_cache[name] = Bounds2
    if name == 'Clock':
        from .clock import Clock
        _import_cache[name] = Clock
    if name == 'Colour':
        from .graphic_things import Colour
        _import_cache[name] = Colour
    if name == 'AnimationData':
        from .graphic_things import AnimationData
        _import_cache[name] = AnimationData
    if name == 'FgPresets':
        from .graphic_things import FgPresets
        _import_cache[name] = FgPresets
    if name == 'Entity':
        from .entity import Entity
        _import_cache[name] = Entity
    if name == 'EntityTag':
        from .entity import EntityTag
        _import_cache[name] = EntityTag
        
    return _import_cache[name]