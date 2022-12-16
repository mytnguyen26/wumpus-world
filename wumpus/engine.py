"""
TODO
"""
import random
from typing import Dict, List, Tuple
from wumpus.utility import Utility

ACTUATORS = ["move", "grab", "shoot"]


class Engine:
    def __init__(self, start_pos, board_size):

        # current board
        self.choosen_move_freq = {
            start_pos: 1
        }
        
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

    def remove_wumpus(self, pos):
        """
        After killing wumpus, update the actual position of wumpus to ok,
        clear all other position with wumpus guess
        """
        self.knowledge[pos]["wumpus"] = 0
        self.knowledge[pos]["ok"] = 1
        self.knowledge[pos]["pit"] = 0
        self.knowledge[pos]["bad"] = 0
        adj_pos = Utility.find_adjacent_cells(pos, self.board_size)

        for adj in adj_pos:
            if adj in self.knowledge.keys():
                self.knowledge[adj]["stench"] = 0



    def tell(self, move, percept) -> None:
        """
        agent invoke function to update the knowledge base the knowledge gained from
        percept.
        If the agent can get here, then any guesses of it around the world should be updated 
        with actual knowledge coming from percept, as it has visisted this cell
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
        # if move not in self.knowledge.keys():
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
        actions = {}

        # if there is gold
        if pos in self.knowledge.keys() and self.knowledge[pos]["glitter"]:
            actions["grab"] = pos

        # if there is wumpus in proximity
        # kill
        adjacent_horizontal_pos = Utility.find_adjacent_horizontal_cells(pos, self.board_size)
        adjacent_vertical_pos = Utility.find_adjacent_vertical_cells(pos, self.board_size)

        for adj_h_pos in adjacent_horizontal_pos:
            if adj_h_pos in self.knowledge \
                and self.knowledge[adj_h_pos]["wumpus"] == 1 \
                and self.knowledge[adj_h_pos]["bad"] == 1:
                actions["shoot"] = adj_h_pos
        
        for adj_v_pos in adjacent_vertical_pos:
            if adj_v_pos in self.knowledge \
                and self.knowledge[adj_v_pos]["wumpus"] == 1 \
                and self.knowledge[adj_v_pos]["bad"] == 1:
                actions["shoot"] = adj_v_pos


        # for all other 
        # find all adj pos
        adj_pos: List[Tuple[int,int]] = Utility.find_adjacent_cells(pos, self.board_size)

        # from all adj pos, find OK or unknown pos from KB
        potential_next_moves_visisted = []
        potential_next_moves_not_visited = []
        for pos in adj_pos:
            if pos in self.knowledge.keys():
                # consider this as next move if it is ok
                if self.knowledge[pos]["visited"] and self.knowledge[pos]['ok']:
                    potential_next_moves_visisted.append(pos)
                elif (not self.knowledge[pos]['visited'] 
                        and not self.knowledge[pos]['bad']
                        and not self.knowledge[pos]['wumpus']
                        and not self.knowledge[pos]['pit']):
                    potential_next_moves_not_visited.append(pos)
                
            else:
                # key not found => no info yet in KB
                # consider this as next move
                potential_next_moves_not_visited.append(pos)

        # NOTE: NEED TO PRIORITIZE NON VISISTED MOVE
        if len(potential_next_moves_not_visited) > 0:
            actions["move"] = random.choice(potential_next_moves_not_visited)
            self.choosen_move_freq[actions["move"]] = 1
        
        elif len(potential_next_moves_visisted) > 0:
            potential_next_moves_visisted_freq = {}
            for move in potential_next_moves_visisted:
                potential_next_moves_visisted_freq[move] = self.choosen_move_freq[move]
                
            min_move = min(potential_next_moves_visisted_freq, key=potential_next_moves_visisted_freq.get)
            # favor move that less chosen
            actions["move"] = min_move
            self.choosen_move_freq[min_move] += 1

        return actions

    def _is_wumpus(self, pos, adj_pos) -> Tuple[int,int]:
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
                return remaining_posible_wumpus[0]
            else:
                wumpus_evaluation = remaining_posible_wumpus.copy()
                for wumpus_pos in wumpus_evaluation:
                    adj_to_wumpus = Utility.find_adjacent_cells(wumpus_pos, self.board_size)
                    known_stench_pos = [cell for cell in self.knowledge.keys() \
                                        if self.knowledge[cell]["stench"] == 1]

                    for stench_pos in known_stench_pos:
                        if stench_pos not in (adj_to_wumpus) and wumpus_pos in remaining_posible_wumpus:
                            self.knowledge[wumpus_pos]["wumpus"] = 0
                            remaining_posible_wumpus.remove(wumpus_pos)
                            
                if len(remaining_posible_wumpus) == 1:
                    self.knowledge[remaining_posible_wumpus[0]]["bad"] = 1
                    print(f"wumpus location is at {remaining_posible_wumpus[0]}")
                    return remaining_posible_wumpus[0]

        
        # case backward prove:
        # if every adj cells of a potential pos candidate is stench
        # => wumpus
        return None

    def _is_pit(self, pos, adj_pos) -> Tuple[int,int]:
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
                return remaining_posible_pit[0]
        return None
    
    def _is_ok(self, pos):
        """
        PROVE: cell is ok by deduction
        if a pos is tentatively labled with both a pit and a wumpus
        then adjs position we know about must be labelled with both Stench and Breeze
        if not, the are no pit nor wumpus at that position.
        """
        adj_cell = Utility.find_adjacent_cells(pos, self.board_size)
        # not_matching_cnt = 0
        # if self.knowledge[pos]["pit"] \
        #     and self.knowledge[pos]["wumpus"] \
        #     and not self.knowledge[pos]["bad"]:

        #     for adj in adj_cell:
        #         if adj in self.knowledge.keys() \
        #             and self.knowledge[adj]["stench"] != self.knowledge[adj]["breeze"]:
        #             not_matching_cnt += 1

        #     # if more than half of cell arounding that candidate cell
        #     # does not match, then cell is ok
        #     if not_matching_cnt/len(adj_cell) > 0.5:        
        #         self.knowledge[pos]["ok"] = 1
        #         self.knowledge[pos]["wumpus"] = 0
        #         self.knowledge[pos]["pit"] = 0

        # this cell we are checking is suspected to be pit
        # for this to happen, all known and visisted ce lls around it
        # must have either stench or breeze and must not be stench 
        if self.knowledge[pos]["pit"]:  
            for adj in adj_cell:
                if adj in self.knowledge.keys() \
                    and self.knowledge[adj]["visited"] \
                    and not self.knowledge[adj]["breeze"]:
                    self.knowledge[pos]["ok"] = 0
                    self.knowledge[pos]["pit"] = 0
        
        if self.knowledge[pos]["wumpus"]:
            for adj in adj_cell:
                if adj in self.knowledge.keys() \
                    and self.knowledge[adj]["visited"] \
                    and not self.knowledge[adj]["stench"]:
                    self.knowledge[pos]["ok"] = 0
                    self.knowledge[pos]["wumpus"] = 0
        
        if not self.knowledge[pos]["pit"] and not self.knowledge[pos]["wumpus"]:
            self.knowledge[pos]["ok"] = 1

        
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
                if self.knowledge[pos]["stench"]:
                    record["wumpus"] = 1
                
                self.knowledge[adj] = record
            
            self._is_ok(adj)
            self._is_wumpus(adj, Utility.find_adjacent_cells(adj, self.board_size))
            self._is_pit(adj, Utility.find_adjacent_cells(adj, self.board_size))
                
                
        # after updating, check again to see if we can prove wumpus
        # is in certain cell --> update bad = 1
        self._is_wumpus(pos, adj_pos)
        
            
        # after updating, check again to see if we can prove pit
        # is in certain cell --> update bad = 1
        self._is_pit(pos, adj_pos)


            

        
        
        