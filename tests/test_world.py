import pytest
from wumpus.world import World

def test_kill_wumpus_successful():
    world = World(mode=0)
    
    request_kill_pos = (1,0)
    assert world.kill_wumpus(request_kill_pos)
    
def test_sensor():
    world = World(mode=0)
    percept = world.sensor((2,0))
    assert percept["stench"] == 1
    
