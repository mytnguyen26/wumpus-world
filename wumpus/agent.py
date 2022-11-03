
from typing import List
from wumpus import PERCEPT

class Agent:
    def __init__(self, engine) -> None:
        self.agent_pos = (3, 0)
        self.agent_percept = PERCEPT
        self.engine = engine

    def move():
        pass

    def grab():
        pass

    def shoot():
        pass

    def climb(self):
        if self.agent_pos == (3, 0):
            return True
        return False

    def update_percept(self, percept: PERCEPT):
        """
        the agent is given a list of 5 for percept, and this is
        the only method it has some interaction with the world
        """
        self.agent_percept = percept

