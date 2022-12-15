
from typing import List, Tuple
from wumpus import PERCEPT

class Agent:
    def __init__(self, engine) -> None:
        self.agent_pos = (3, 0)
        self.agent_percept = PERCEPT
        self.engine = engine

    def move():
        pass

    def grab(self):
        # ask the world to confirm gold
        print(f"grab gold from {self.agent_pos}")
        

    def shoot():
        pass

    def climb(self):
        """
        if at entry then can clime
        """
        if self.agent_pos == (3, 0):
            return True
        return False
    

    def update_percept(self, percept: PERCEPT):
        """
        Receiving perception back from World
        the agent is given a list of 5 for percept, and this is
        the only method it has some interaction with the world
        """
        self.agent_percept = percept

        # if not death
        self.tell_kb()

        # if there is gold
        if self.agent_percept["glitter"]:
            self.grab()

        # if there is wumpus in proximity
        # kill


    def tell_kb(self):
        self.engine.tell(move = self.agent_pos, percept = self.agent_percept)

    def ask_kb(self) -> Tuple[int, int]:
        self.engine.ask(self.agent_pos)

