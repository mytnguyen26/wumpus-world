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
            self.board = [[[], [], [], []],
                    [[], [], [], []],
                    [[], [], [], []],
                    [[], [], [], []]]
            self._randomly_place_stuff_test_board()
        else:
            # starting pos
            self.agent_pos = (0, 0)
            self.board = [[[], [], [], [], []],
                    [[], [], [], [], []],
                    [[], [], [], [], []],
                    [[], [], [], [], []],
                    [[], [], [], [], []]]
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
                self.board[cell[0]][cell[1]].append(key)
        
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
        return "wumpus" in self.board[self.agent_pos[0]][self.agent_pos[1]] \
            or "pit" in self.board[self.agent_pos[0]][self.agent_pos[1]]

    def collect_gold(self, request_gold_pos: Tuple[int,int]) -> bool:
        if "gold" in self.board[request_gold_pos[0]][request_gold_pos[1]]:
            self.board[request_gold_pos[0]][request_gold_pos[1]].remove("gold")
            return True
        return False
        
    def kill_wumpus(self, request_shooting_pos: Tuple[int,int]) -> bool:
        """
        A way for agent to try and kill wumpus
        Args:
            - request_shooting_pos: is the requested position to kill wumpus
            from agent. this does not mean the actual wumpus is here.
            Since the arrow can be shoot in direction vertical of agent
            or horizontal of agent, if wumpus is still within the horizontal
            or vertical alignment between human and this `pos`. It is still
            a valid shoot
        """
        adjacent_horizontal_pos = Utility.find_adjacent_horizontal_cells(request_shooting_pos, self.board_size)
        adjacent_vertical_pos = Utility.find_adjacent_vertical_cells(request_shooting_pos, self.board_size)
        
        # check agent position against the actual world data
        # if the arrow would actually hit wumpus or not
        
        if "wumpus" in self.board[request_shooting_pos[0]][request_shooting_pos[1]]:
            self.board[request_shooting_pos[0]][request_shooting_pos[1]].remove("wumpus")
            return True

        # check row of agent position against the row of the requested pos
        if self.agent_pos[0] == request_shooting_pos[0]:
            for pos in adjacent_horizontal_pos:
                if "wumpus" in self.board[pos[0]][pos[1]]:
                    self.board[request_shooting_pos[0]][request_shooting_pos[1]].remove("wumpus")
                    return True
        # check col of agent position against the col of the requested pos
        if self.agent_pos[1] == request_shooting_pos[1]:
            for pos in adjacent_vertical_pos:
                if  "wumpus" in self.board[pos[0]][pos[1]]:
                    self.board[request_shooting_pos[0]][request_shooting_pos[1]].remove("wumpus")
                    return True
        return False


    def sensor(self, agent_pos):
        """
        A way for agent to update position in the world
        allowing the world to return percept to agent
        
        Gives agent limited knowledge of the current world
        given current position 
        """
        self.agent_pos = agent_pos
        adj_cells = Utility.find_adjacent_cells(self.agent_pos, len(self.board))

        # update PERCEPT datastructure and give to agent
        percept = PERCEPT.copy()
        
        if "stench" in self.board[self.agent_pos[0]][self.agent_pos[1]]:
            percept["stench"] = 1
        if "breeze" in self.board[self.agent_pos[0]][self.agent_pos[1]]:
            percept["breeze"] = 1
        
        if "gold" in self.board[self.agent_pos[0]][self.agent_pos[1]]:
            percept["glitter"] = 1

        if self.agent_pos[0] in [0, 3] or self.agent_pos[1] in [0, 3]:
            percept["bump"] = 1
        
        if self._is_game_over():
            percept["game_over"] = 1
        
        return percept
        
                
                





        