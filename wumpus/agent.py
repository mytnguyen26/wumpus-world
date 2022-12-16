
from typing import List, Tuple
from wumpus import PERCEPT
from wumpus.engine import Engine

class Agent:
    def __init__(self, engine: Engine, world) -> None:
        # agent should only be interacting with world using
        # public method
        self.world = world
        self.agent_pos = (3, 0)
        self.agent_percept = PERCEPT
        self.engine = engine
        self.gold = 0
        self.wumpus_killed = 0
        self.arrow = 1

    def move(self):
        actions = self._ask_kb()
        for action, pos in actions.items():
            if action == "grab":
                self.grab()
            if action == "shoot":
                self.shoot(pos)
            if action == "move":
                self.agent_pos = pos
                return pos

    def grab(self):
        # ask the world to confirm gold
        print(f"grab gold from {self.agent_pos}")
        self.gold += 1

    def shoot(self, pos):
        print("Attempting to kill wumpus")
        self.arrow -= 1
        if self.world.kill_wumpus(pos):
            print("Yay! Wumpus Killed")
            self.wumpus_killed = 1
            return True
        else:
            print("You Did not kill Wumpus")
            return False

    def climb(self):
        """
        if at entry then can clime
        """
        if self.agent_pos == (3, 0):
            return True
        return False
    

    def update_percept(self, percept: PERCEPT) -> bool:
        """
        Receiving perception back from World
        the agent is given a list of 5 for percept, and this is
        the only method it has some interaction with the world
        """
        self.agent_percept = percept

        if percept["game_over"]:
            return False
        # if not death
        self._tell_kb()
        return True


    def _tell_kb(self):
        self.engine.tell(move = self.agent_pos, percept = self.agent_percept)

    def _ask_kb(self) -> Tuple[int, int]:
        return self.engine.ask(self.agent_pos)

