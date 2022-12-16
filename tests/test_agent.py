import pytest
from wumpus.agent import Agent
from wumpus.engine import Engine
from wumpus.world import World

def test_tell_knowledgebase():
    world = World(mode=0)
    engine = Engine(world.board_size)
    agent = Agent(engine, world)
    
    agent.agent_pos = (0, 2)
    world.sensor(agent.agent_pos)
    engine.tell(move = agent.agent_pos, percept = agent.agent_percept)

    assert len(engine.knowledge) > 0

def test_move():
    world = World(mode=0)
    engine = Engine(4)
    agent = Agent(engine, world)

    percept = world.sensor(agent.agent_pos)
    agent.update_percept(percept)
    agent_move = agent.move()
    assert isinstance(agent_move, tuple)
    