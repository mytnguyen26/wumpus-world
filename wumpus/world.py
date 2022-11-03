import random
from typing import Tuple
from wumpus import PERCEPT
from wumpus.agent import Agent

class World:
    def __init__(self):
        # generate a 4x4 matrix
        self.agent_pos = (3, 0)
        self.board = [[0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]]
        self._randomly_place_stuff()
    
    def _randomly_place_stuff(self):
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        
        placement = {
            "wumpus": [(1, 0)],
            "pit": [(0, 3), (1, 2), (3, 2)],
            "gold": [(1, 1)],

            # the following can be generated as 
            "stench": [(0, 0), (1, 1), (2, 0)],
            "breeze": [(0, 2), (1, 1), (1, 3), (2, 2), (3, 1), (3, 3)]
        }

        for key, cells in placement.items():
            for cell in cells:
                self.board[cell[0]][cell[1]] = key
        
        self.board[self.agent_pos[0]][self.agent_pos[1]] = "agent"
    
    def update_agent_pos(self, agent_pos: Tuple[int, int]):
        self.board[agent_pos[0]][agent_pos[1]] = "agent"
        self.board[self.agent_pos[0]][self.agent_pos[1]] = 0
        self.agent_pos = agent_pos


    def find_adjacent_cells(self):
        """
        given current pos, find 4 adjacent cells
        """
        def calculate_new_pos(number):
            if number < 0 or number > 3:
                return None
            return number

        adj_cells = [
            (calculate_new_pos(self.agent_pos[0] + 1), self.agent_pos[1]),
            (calculate_new_pos(self.agent_pos[0] - 1), self.agent_pos[1]),
            (self.agent_pos[0], calculate_new_pos(self.agent_pos[1] + 1)),
            (self.agent_pos[0], calculate_new_pos(self.agent_pos[1] + 1))
        ]
        return adj_cells

    def sensor(self, agent: Agent):
        """
        This function gives agent limited knowledge of the current world
        given current position 
        """
        adj_cells = self.find_adjacent_cells()
        

        # update PERCEPT datastructure and give to agent
        percept = PERCEPT
        
        if self.board[self.agent_pos[0]][self.agent_pos[1]] in ["stench", "breeze"]:
            percept[self.board[self.agent_pos[0]][self.agent_pos[1]]] = 1
        
        elif self.board[self.agent_pos[0]][self.agent_pos[1]] == "gold":
            percept["glitter"] = 1

        elif self.agent_pos[0] in [0, 3] or self.agent_pos[1] in [0, 3]:
            percept["bump"] = 1
            
        agent.update_percept(percept)
                
                





        