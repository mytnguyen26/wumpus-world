"""
TODO
"""
import random
from typing import Dict, List, Tuple
from wumpus.utility import Utility

ACTUATORS = ["move", "grab", "shoot"]


class Engine:
    def __init__(self, board_size):

        # current board
        self.board_size = board_size

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

    def ask(self, pos) -> Dict[str, Tuple[int, int]]:
        """
        ask engine the knowledge and return a move with structure
        {
            <type_of_action>: (row, col)
        }
        """
        actions = []

        # if there is gold
        if self.knowledge[pos]["glitter"]:
            actions.append(
                {"grab": pos}
            )

        # if there is wumpus in proximity
        # kill

        # for all other 
        # find all adj pos
        adj_pos: List[Tuple[int,int]] = Utility.find_adjacent_cells(pos, self.board_size)

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

        actions.append({"move":random.choice(potential_next_moves)})
        return actions

    def _is_wumpus(self, pos, adj_pos):
        """
        from position, check if there is a wumpus in vertical, 
        horizontal adj cells from the current pos
        """
        # Case forward proof:
        # if current position is stench, wumpus must be locating in
        # adjacent cells. If everything else but 1 is proven to be either
        # ok (because we visited) or having something else (proven pit)
        # then that remaining must be wumpus
        # --> update bad = 1
        if self.knowledge[pos]["stench"]:
            remaining_posible_wumpus = [adj for adj in adj_pos \
                                        if adj in self.knowledge.keys() \
                                        and self.knowledge[adj]["wumpus"] == 1]
            if len(remaining_posible_wumpus) == 1:
                self.knowledge[remaining_posible_wumpus[0]]["bad"] = 1
                print(f"wumpus location is at {remaining_posible_wumpus[0]}")


        # case backward prove:
        # if every adj cells of a potential pos candidate is stench
        # => wumpus
        
        # 

    def _is_pit(self, pos, adj_pos):
        """
        from position, check if there is a pit in vertical, 
        horizontal adj cells from the current pos
        """
        # Case forward proof:
        # if current position is breeze, pit must be locating in
        # adjacent cells. If everything else but 1 is proven to be either
        # ok (because we visited) or having something else (proven wumpus)
        # then that remaining must be wumpus
        # --> update bad = 1
        if self.knowledge[pos]["breeze"]:
            remaining_posible_pit = [adj for adj in adj_pos \
                                        if adj in self.knowledge.keys() \
                                        and self.knowledge[adj]["pit"] == 1]
            if len(remaining_posible_pit) == 1:
                self.knowledge[remaining_posible_pit[0]]["bad"] = 1
                print(f"pit location is at {remaining_posible_pit[0]}")
    
    def _is_ok(self, pos):
        """
        PROVE: cell is ok by deduction
        if a pos is tentatively labled with both a pit and a wumpus
        then adjs position we know about must be labelled with both Stench and Breeze
        if not, the are no pit nor wumpus at that position.
        """
        
        if self.knowledge[pos]["pit"] and self.knowledge[pos]["wumpus"]:
            self.knowledge[pos]["ok"] = 1
            self.knowledge[pos]["wumpus"] = 0
            self.knowledge[pos]["pit"] = 0

    def _entail(self, pos):
        """
        After `tell` is called to update current knowledge base, the knowledge base
        call _entail to start deducing. Proving certain cell to be ok, or contain
        wumpus or gold
        """
        # find adjacent position
        adj_pos = Utility.find_adjacent_cells(pos, self.board_size)

        # update tentative guess from existing known knowledge
        # for each position in the list of adjacent positions
        # return from utility, update their pits or wumpus guess (not confirm)
        # base current knowledge
        for adj in adj_pos:
            if adj in self.knowledge.keys():
                if not self.knowledge[adj]["ok"]:
                    if self.knowledge[pos]["breeze"]:
                        self.knowledge[adj]["pit"] = 1
                    elif self.knowledge[pos]["stench"]:
                        self.knowledge[adj]["wumpus"] = 1
            else:
                record = {
                    "visited": 0,
                    "stench": 0, "breeze": 0, "glitter": 0, "bump": 0, "scream": 0,
                    "wumpus": 0, "pit": 0, "ok": 0, "bad": 0
                }
                if self.knowledge[pos]["breeze"]:
                    record["pit"] = 1
                elif self.knowledge[pos]["stench"]:
                    record["wumpus"] = 1
                
                self.knowledge[adj] = record
            
            self._is_ok(adj)
                
                
        # after updating, check again to see if we can prove wumpus
        # is in certain cell --> update bad = 1
        self._is_wumpus(pos, adj_pos)
        
            
        # after updating, check again to see if we can prove pit
        # is in certain cell --> update bad = 1
        self._is_pit(pos, adj_pos)


            

        
        
        