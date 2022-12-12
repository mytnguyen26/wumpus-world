import pytest
from wumpus.agent import Agent
from wumpus.engine import Engine
from wumpus.world import World

def test_tell_knowledgebase():
    world = World()
    engine =  Engine()
    agent = Agent(engine)

    agent.agent_pos = (0, 2)
    world.sensor(agent)
    engine.tell(move = agent.agent_pos, percept = agent.agent_percept)

    assert len(engine.knowledge) > 0