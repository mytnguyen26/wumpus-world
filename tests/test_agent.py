import pytest
from wumpus.agent import Agent
from wumpus.engine import Engine
from wumpus.world import World

def test_tell_knowledgebase():
    world = World(mode=0)
    engine = Engine(world.start_agent_pos, world.board_size)
    agent = Agent(engine, world)
    
    agent.agent_pos = (0, 2)
    world.sensor(agent.agent_pos)
    engine.tell(move = agent.agent_pos, percept = agent.agent_percept)

    assert len(engine.knowledge) > 0

def test_move():
    world2 = World(mode=0)
    engine2 = Engine(world2.start_agent_pos, 4)
    agent2 = Agent(engine2, world2)

    percept = world2.sensor(agent2.agent_pos)
    agent2.update_percept(percept)
    
    assert agent2.move() in [(2,0), (3,1)]
    