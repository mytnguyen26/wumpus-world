
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
        the agent is given a list of 5 for percept, and this is
        the only method it has some interaction with the world
        """
        self.agent_percept = percept

    def tell_kb(self):
        # if not death
        self.engine.tell(move = self.agent_pos, percept = self.agent_percept)
        # if there is gold
        if self.agent_percept["glitter"]:
            self.grab()
        

    def ask_kb(self) -> Tuple[int, int]:
        self.engine.ask(self.agent_pos)

