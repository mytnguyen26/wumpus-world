import pytest
from wumpus.world import World

def test_placement():
    world = World()
    assert world.board[3][0] == "agent"
    assert world.board[1][0] == "wumpus"
    
def test_update_agent_pos():
    world = World()
    world.update_agent_pos((2,3))
    assert world.board[2][3] == "agent"