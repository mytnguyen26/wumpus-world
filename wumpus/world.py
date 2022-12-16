import random
from typing import Tuple
from wumpus import PERCEPT
from wumpus.agent import Agent
from wumpus.utility import Utility

class World:
    def __init__(self, mode: int):
        # generate a 4x4 matrix
        if mode==0:
            self.agent_pos = (3, 0)
            self.board = [[0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]]
            self._randomly_place_stuff_test_board()
        else:
            # starting pos
            self.agent_pos = (0, 0)
            self.board = [[0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0]]
            self._randomly_place_stuff_big_board()
        self.board_size = len(self.board)
    
    def _randomly_place_stuff_test_board(self):
        """
        TODO
        """
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
    
    def _randomly_place_stuff_big_board(self):
        """
        TODO
        """
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

    def _is_game_over(self) -> bool:
        return self.board[self.agent_pos[0]][self.agent_pos[1]] in ["wumpus", "pit"]

    def kill_wumpus(self, agent_pos, direction) -> bool:
        """
        A way for agent to try and kill wumpus
        """
        adj_cells = []
        if direction == "col": 
            adj_cells = Utility.find_adjacent_vertical_cells(agent_pos, len(self.board))
        else:
            adj_cells = Utility.find_adjacent_horizontal_cells(agent_pos, len(self.board))

        for pos in adj_cells:
            if self.board[pos[0]][pos[1]] == "wumpus":
                return True
        return False


    def sensor(self, agent: Agent):
        """
        A way for agent to update position in the world
        allowing the world to return percept to agent
        
        Gives agent limited knowledge of the current world
        given current position 
        """
        self.agent_pos = agent.agent_pos
        adj_cells = Utility.find_adjacent_cells(self.agent_pos, len(self.board))

        # update PERCEPT datastructure and give to agent
        percept = PERCEPT
        
        if self.board[self.agent_pos[0]][self.agent_pos[1]] in ["stench", "breeze"]:
            percept[self.board[self.agent_pos[0]][self.agent_pos[1]]] = 1
        
        elif self.board[self.agent_pos[0]][self.agent_pos[1]] == "gold":
            percept["glitter"] = 1

        elif self.agent_pos[0] in [0, 3] or self.agent_pos[1] in [0, 3]:
            percept["bump"] = 1
        
        elif self._is_game_over():
            percept["game_over"] = 1
            
        agent.update_percept(percept)
                
                





        