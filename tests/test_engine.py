from wumpus import PERCEPT
from wumpus.engine import Engine
from wumpus.agent import Agent
from wumpus.utility import Utility
from wumpus.world import World


def test_ask_case_init():
    """
    
    """
    engine = Engine((3,0), board_size=4)
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
    
    engine = Engine((3,0), board_size=4)
    move_order = {
        (3,0): {"stench": 0, "breeze": 0, "glitter": 0, "bump": 0, "scream": 0},
        (3,1): {"stench": 0, "breeze": 1, "glitter": 0, "bump": 0, "scream": 0},
    }
    for move, percept in move_order.items():
        engine.tell(move, percept)
   
    # engine._entail(agent_pos)
    assert engine.ask((3,1)) == {"move":(3,0)}

    # if already visited and have base knowledge
    # should not update knowledge
    assert engine.knowledge[(3,1)] == {
        "visited": 1,
        "stench": 0, "breeze": 1, "glitter": 0, "bump": 0, "scream": 0,
        "wumpus": 0, "pit": 0, "ok": 1, "bad": 0
    }

def test_entail_infer_pit_from_stench_percept():
    agent_pos = (2,0)
    percept = {"stench": 1, "breeze": 0, "glitter": 0, "bump": 0, "scream": 0}
    engine = Engine((3,0),board_size=4)

    # at initiation, the agent_pos is at starting pos (3,0)
    # the agent update the knowledge of its perception received from
    # this position (ie nothing) and cell around it are ok for exploration
    engine.knowledge = {
        (3,0): {
            "visited": 1,
            "stench": 0, "breeze": 0, "glitter": 0, "bump": 0, "scream": 0,
            "wumpus": 0, "pit": 0, "ok": 1, "bad": 0
        },
        (2,0): {
            "visited": 0,
            "stench": 0, "breeze": 0, "glitter": 0, "bump": 0, "scream": 0,
            "wumpus": 0, "pit": 0, "ok": 0, "bad": 0
        },
        (3,1): {
            "visited": 0,
            "stench": 0, "breeze": 0, "glitter": 0, "bump": 0, "scream": 0,
            "wumpus": 0, "pit": 0, "ok": 0, "bad": 0
        }
    }
    engine.tell(agent_pos, percept)
    assert len(engine.knowledge) == 5
    assert engine.knowledge[(2,0)]["stench"] == 1
    assert engine.knowledge[(2,0)]["visited"] == 1
    assert engine.knowledge[(2,0)]["ok"] == 1
    assert engine.knowledge[(2,1)]["wumpus"] == 1
    assert engine.knowledge[(2,1)]["ok"] == 0
    assert engine.knowledge[(2,1)]["visited"] == 0


def test_entail_case_found_pit_first():
    """
    test reasoning
    """
    world = World(mode=0)
    engine = Engine((3,0), board_size=4)

    move_order = {
        (3,0): PERCEPT,
        (3,1): {"stench": 0, "breeze": 1, "glitter": 0, "bump": 0, "scream": 0},
        (3,0): PERCEPT,
        (2,0): {"stench": 1, "breeze": 0, "glitter": 0, "bump": 0, "scream": 0},

    }
    for move, percept in move_order.items():
        engine.choosen_move_freq[move] = 1
        engine.tell(move, percept)
    
    assert len(engine.knowledge) == 6
    assert engine.knowledge[(2,1)]["pit"] == 0
    assert engine.knowledge[(2,1)]["wumpus"] == 0
    assert engine.knowledge[(2,0)]["ok"] == 1
    assert engine.knowledge[(1,0)]["ok"] == 0
    assert engine.knowledge[(1,0)]["wumpus"] == 1
    assert engine.knowledge[(3,2)]["ok"] == 0
    assert engine.knowledge[(3,2)]["pit"] == 1

def test_entail_case_found_stench_first():
    """
    test reasoning
    """
    world = World(mode=0)
    engine = Engine((3,0), board_size=4)

    move_order = {
        (3,0): PERCEPT,
        (2,0): {"stench": 1, "breeze": 0, "glitter": 0, "bump": 0, "scream": 0},
        (3,0): PERCEPT,
        (3,1): {"stench": 0, "breeze": 1, "glitter": 0, "bump": 0, "scream": 0},
    }
    for move, percept in move_order.items():
        engine.choosen_move_freq[move] = 1
        engine.tell(move, percept)
    
    assert len(engine.knowledge) == 6
    assert engine.knowledge[(2,1)]["pit"] == 0
    assert engine.knowledge[(2,1)]["wumpus"] == 0
    assert engine.knowledge[(2,0)]["ok"] == 1
    assert engine.knowledge[(1,0)]["ok"] == 0
    assert engine.knowledge[(1,0)]["wumpus"] == 1
    assert engine.knowledge[(3,2)]["ok"] == 0
    assert engine.knowledge[(3,2)]["pit"] == 1

def test_is_wumpus_case_found_breeze_first():
    agent_pos = (2,0)
    engine = Engine((3,0),board_size=4)
    
    move_order = {
        (3,0): PERCEPT.copy(),
        (3,1): {"stench": 0, "breeze": 1, "glitter": 0, "bump": 0, "scream": 0},
        (3,0): PERCEPT.copy(),
        (2,0): {"stench": 1, "breeze": 0, "glitter": 0, "bump": 0, "scream": 0}
    }
    for move, percept in move_order.items():
        engine.choosen_move_freq[move] = 1
        engine.tell(move, percept)

    adj_pos = Utility.find_adjacent_cells(agent_pos, 4)
    assert engine._is_wumpus((2,0),adj_pos) == (1,0)
    actions = engine.ask((2,0))
    assert "shoot" in actions.keys()
    assert actions["shoot"] == (1,0)

def test_is_wumpus_case_found_stench_first():
    engine = Engine((3,0), board_size=4)

    move_order = {
        (3,0): PERCEPT.copy(),
        (2,0): {"stench": 1, "breeze": 0, "glitter": 0, "bump": 0, "scream": 0},
        (3,0): PERCEPT.copy(),
    }
    for move, percept in move_order.items():
        engine.choosen_move_freq[move] = 1
        engine.tell(move, percept)
    
    adj_pos = Utility.find_adjacent_cells((3,0), 4)
    assert engine._is_wumpus((3,0),adj_pos) == None


def test_deduce_wumpus():
    world = World(mode=1)
    engine = Engine(world.start_agent_pos, world.board_size)

    move_order = {
        (0,0): PERCEPT.copy(),
        (1,0): {"stench": 1, "breeze": 0, "glitter": 0, "bump": 0, "scream": 0},
        (2,0): {'stench': 1, 'breeze': 1, 'glitter': 0, 'bump': 1, 'scream': 0, 'game_over': 0},
        (1,0): {'stench': 0, 'breeze': 0, 'glitter': 0, 'bump': 1, 'scream': 0, 'game_over': 0},
        (1,1): {'stench': 1, 'breeze': 0, 'glitter': 0, 'bump': 0, 'scream': 0, 'game_over': 0},
    }

    for move, percept in move_order.items():
        engine.choosen_move_freq[move] = 1
        engine.tell(move, percept)
    
    actions = engine.ask((1,1))
    actions

def test_deduce_wumpus_case_2():
    world = World(mode=1)
    engine = Engine(world.start_agent_pos, world.board_size)

    move_order = {
        (0,0): PERCEPT.copy(),
        (0,1): {'stench': 0, 'breeze': 1, 'glitter': 0, 'bump': 1, 'scream': 0, 'game_over': 0},
        (0, 0): {'stench': 0, 'breeze': 0, 'glitter': 0, 'bump': 1, 'scream': 0, 'game_over': 0},
        (1, 0): {'stench': 0, 'breeze': 0, 'glitter': 0, 'bump': 1, 'scream': 0, 'game_over': 0},
        (2,0): {'stench': 1, 'breeze': 1, 'glitter': 0, 'bump': 1, 'scream': 0, 'game_over': 0},
        
    }

    for move, percept in move_order.items():
        engine.choosen_move_freq[move] = 1
        engine.tell(move, percept)
    
    actions = engine.ask((2,0))
    actions

def test_deduce_pit():
    world = World(mode=1)
    engine = Engine(world.start_agent_pos, world.board_size)

    move_order = {
        (0,0): PERCEPT.copy(),
        (1,0): {"stench": 1, "breeze": 0, "glitter": 0, "bump": 0, "scream": 0},
        (2,0): {'stench': 1, 'breeze': 1, 'glitter': 0, 'bump': 1, 'scream': 0, 'game_over': 0},
        (1,0): {'stench': 0, 'breeze': 0, 'glitter': 0, 'bump': 1, 'scream': 0, 'game_over': 0},
        (1,1): {'stench': 1, 'breeze': 0, 'glitter': 0, 'bump': 0, 'scream': 0, 'game_over': 0},
        (0,1): {'stench': 0, 'breeze': 1, 'glitter': 0, 'bump': 1, 'scream': 0, 'game_over': 0},
    }

    for move, percept in move_order.items():
        engine.choosen_move_freq[move] = 1
        engine.tell(move, percept)
    
    actions = engine.ask((0,1))
    actions
    