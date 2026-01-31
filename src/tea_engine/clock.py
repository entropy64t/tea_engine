from __future__ import annotations
from typing import Callable, Any
import time 

class Clock:
    def __init__(self, tick_rate = 0.1) -> None:
        self.tick_rate = tick_rate
        self._last: float = 0
        self._subscribers: dict[str, Callable[[], Any]] = {}
        self._results: dict[str, Any] = {}
        
    def subscribe(self, fn: Callable[[], Any]):
        self += fn
        
    def register(self, fn: Callable[[], Any], name: str):
        self._subscribers[name] = fn
        
    def get(self, name: str):
        return self._subscribers.get(name, lambda: None)
    
    def result_of(self, name: str):
        return self._results.get(name, None)
        
    def __iadd__(self, fn: Callable[[], Any]):
        self._subscribers[fn.__name__] = fn
        return self
    
    def tick(self):
        now = time.monotonic()
        if now < self._last + self.tick_rate: return
        
        self._last = now
        
        for name in self._subscribers:
            self._subscribers[name]()