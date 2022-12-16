from wumpus import PERCEPT
from wumpus.engine import Engine
from wumpus.agent import Agent
from wumpus.utility import Utility
from wumpus.world import World


def test_ask_case_init():
    """
    
    """
    engine = Engine(board_size=4)
    engine.knowledge = {
        (3,0): {
            "visited": 1,
            "stench": 0, "breeze": 0, "glitter": 0, "bump": 0, "scream": 0,
            "wumpus": 0, "pit": 0, "ok": 1, "bad": 0
        }
    }
    engine.ask((3,0))

def test_ask_case_return_next_move():
    """
    engine should choose the only obvious OK move among adjacent moves
    """
    agent_pos = (3,1)
    engine = Engine(board_size=4)
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
    assert engine.ask(agent_pos) == {"move":(3,0)}

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
    world = World(mode=0)
    engine = Engine(board_size=4)
    
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
    
    agent_pos = (2,0)
    percept = {"stench": 1, "breeze": 0, "glitter": 0, "bump": 0, "scream": 0}
    engine.tell(agent_pos, percept)
    assert engine.knowledge[(2,1)]["ok"] == 1

def test_is_wumpus():
    agent_pos = (2,0)
    engine = Engine(board_size=4)
    
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
            "wumpus": 0, "pit": 0, "ok": 1, "bad": 0
        },
        (3,2): {
            "visited": 0,
            "stench": 0, "breeze": 0, "glitter": 0, "bump": 0, "scream": 0,
            "wumpus": 0, "pit": 1, "ok": 0, "bad": 0
        }
    }
    percept = {"stench": 1, "breeze": 0, "glitter": 0, "bump": 0, "scream": 0}
    engine.tell(agent_pos, percept)
    adj_pos = Utility.find_adjacent_cells(agent_pos, 4)
    assert engine._is_wumpus((2,0),adj_pos) == (1,0)
    
def test_ask_case_return_shoot():
    """
    engine should return a shoot action since the wumpus is located
    """
    agent_pos = (2,0)
    engine = Engine(board_size=4)
    
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
            "wumpus": 0, "pit": 0, "ok": 1, "bad": 0
        },
        (3,2): {
            "visited": 0,
            "stench": 0, "breeze": 0, "glitter": 0, "bump": 0, "scream": 0,
            "wumpus": 0, "pit": 1, "ok": 0, "bad": 0
        }
    }
    percept = {"stench": 1, "breeze": 0, "glitter": 0, "bump": 0, "scream": 0}
    engine.tell(agent_pos, percept)
    
    adj_pos = Utility.find_adjacent_cells(agent_pos, 4)
    engine._is_wumpus((2,0),adj_pos)

    new_agent_pos = (3,0)
    actions = engine.ask(new_agent_pos)
    assert "shoot" in actions.keys()
    assert actions["shoot"] == (1,0)