import tea_engine as tea
import random

def main():
    clock = tea.Clock(0.2)
    bounds = tea.Bounds2(tea.Vector2(0, 0), tea.Vector2(10, 10))
    engine = tea.Engine(bounds)
    renderer = tea.Renderer(engine)
    
    clock += renderer.clear
    clock += engine.update
    clock += renderer.render
    
    entity = tea.Entity("demo entity", [], engine)
    entity.sprite = "@"
    entity.sprite_len = 1
    entity.assign_ai(tea.SimpleAI())
    entity.map_bounds = bounds.shrink(1, 0)
    lst = list(tea.FgPresets)
    lst.remove(tea.FgPresets.BLACK)
    
    for _ in range(5):
        e = engine.spawn(entity, tea.Vector2(_, _))
        e.colour = [random.choice(lst).value]
        #print(e.map_bounds.tl, e.map_bounds.br)
        #input()
    #e = engine.spawn(entity, tea.Vector2(6, 7))
    
    try:
        while True:
            clock.tick()
            #print(e.position, e.direction, e.ai)
            #input()
    except KeyboardInterrupt:
        return 