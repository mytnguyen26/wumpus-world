import pytest
from wumpus.world import World

def test_placement():
    world = World(mode=0)
    assert world.board[3][0] == "agent"
    assert world.board[1][0] == "wumpus"


    