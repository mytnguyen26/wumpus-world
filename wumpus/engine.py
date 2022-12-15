"""
TODO
"""
import random
from typing import List, Tuple
from wumpus.utility import Utility

ACTUATORS = ["move", "grab", "shoot"]


class Engine:
    def __init__(self):

        # current board
        self.state = [[0, 0, 0, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0]]

        self.knowledge = {
            # (row, col) : {
            # 'percept': PERCEPT, 
            # 'wumpus': boolean, 
            # 'pit': boolean,
            # 'OK': boolean, 
            # 'visited': boolean
            # }
        }

    def tell(self, move, percept) -> None:
        """
        agent invoke function to update the knowledge base the knowledge gained from
        percept
        """
        row = {}
        # row['move'] = move
        row['visited'] = 1
        row.update(percept)
        row['wumpus'] = 0
        row['pit'] = 0
        row['ok'] = 1
        row['bad'] = 0
        
        # update the knoeldge base
        if move not in self.knowledge.keys():
            self.knowledge[move] = row

        # reason and update knowledge
        self._entail(move)

    def ask(self, pos) -> Tuple[int, int]:
        """
        ask engine the knowledge
        """
        # find all adj pos
        adj_pos: List[Tuple[int,int]] = Utility.find_adjacent_cells(pos)

        # from all adj pos, find OK or unknown pos from KB
        potential_next_moves = []
        for pos in adj_pos:
            try:
                values = self.knowledge[pos]['ok']
                # consider this as next move if it is ok
                if values:
                    potential_next_moves.append(pos)
            except Exception as e:
                # key not found => no info yet in KB
                # consider this as next move
                potential_next_moves.append(pos)

        return random.choice(potential_next_moves)

    def _entail(self, pos):
        """
        After `tell` is called to update current knowledge base, the knowledge base
        call _entail to start deducing. Proving certain cell to be ok, or contain
        wumpus or gold
        """
        # find adjacent position
        adj_pos = Utility.find_adjacent_cells(pos)

        # update tentative guess from existing known knowledge
        for adj in adj_pos:
            if not self.knowledge[adj]["ok"]:
                if self.knowledge[pos]["breeze"]:
                    self.knowledge[adj]["pit"] = 1
                elif self.knowledge[pos]["stench"]:
                    self.knowledge[adj]["wumpus"] = 1
        
            # if a pos is tentatively labled with both a pit and a wumpus
            # then adjs position we know about must be labelled with both Stench and Breeze
            # if not, the are no pit nor wumpus at that position.
            # proof:
            # 
            if self.knowledge[adj]["pit"] and self.knowledge[adj]["wumpus"]:
                self.knowledge[adj]["ok"] = 1
                self.knowledge[adj]["wumpus"] = 0
                self.knowledge[adj]["pit"] = 0
                
                
        # after updating, check again to see if we can find wumpus
        if self.knowledge[pos]["stench"]:
            remaining_posible_wumpus = [adj for adj in adj_pos if self.knowledge[adj]["wumpus"] == 1]
            if len(remaining_posible_wumpus == 1):
                self.knowledge[remaining_posible_wumpus[0]]["bad"] = 1
                print(f"wumpus location is at {remaining_posible_wumpus[0]}")
            



            

        
        
        