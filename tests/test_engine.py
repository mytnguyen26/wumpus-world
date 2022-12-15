from wumpus import PERCEPT
from wumpus.engine import Engine
from wumpus.agent import Agent

def test_ask():
    """
    engine should choose the only obvious OK move among adjacent moves
    """
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
    engine.tell(agent_pos, PERCEPT)
    # engine._entail(agent_pos)
    assert engine.ask(agent_pos) == (3,0)

    # if already visited and have base knowledge
    # should not update knowledge
    assert engine.knowledge[(3,1)] == {
        "visited": 1,
        "stench": 0, "breeze": 1, "glitter": 0, "bump": 0, "scream": 0,
        "wumpus": 0, "pit": 0, "ok": 1, "bad": 0
    }


def test_entail():
    """
    test reasoning
    """
    
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

    