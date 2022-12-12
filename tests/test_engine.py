from wumpus.engine import Engine
from wumpus.agent import Agent

def test_ask():
    agent_pos = (3,1)
    engine = Engine()
    engine.knowledge = {
        (3,0): {
            "visited": 1,
            "stench": 0, "breeze": 0, "glitter": 0, "bump": 0, "scream": 0,
            "wumpus": 0, "pit": 0, "ok": 1, "bad": 0
        },
        (3,1): {
            "visited": 1,
            "stench": 0, "breeze": 1, "glitter": 0, "bump": 0, "scream": 0,
            "wumpus": 0, "pit": 0, "ok": 1, "bad": 0
        },
        (2,1): {
            "visited": 0,
            "stench": 0, "breeze": 0, "glitter": 0, "bump": 0, "scream": 0,
            "wumpus": 0, "pit": 1, "ok": 0, "bad": 0
        },
        (3,2): {
            "visited": 0,
            "stench": 0, "breeze": 0, "glitter": 0, "bump": 0, "scream": 0,
            "wumpus": 0, "pit": 1, "ok": 0, "bad": 0
        }
    }
    

    assert engine.ask(agent_pos) == (3,0)