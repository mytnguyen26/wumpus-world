from typing import Tuple


class Utility:
    @staticmethod
    def find_adjacent_cells(agent_pos, board_size):
        """
        given current pos, find 4 adjacent cells
        """
        def calculate_new_pos(number, board_size):
            if number < 0 or number > board_size:
                return None
            return number
        
        
        adj_cells = [
            (calculate_new_pos(agent_pos[0] + 1, board_size), agent_pos[1]),
            (calculate_new_pos(agent_pos[0] - 1, board_size), agent_pos[1]),
            (agent_pos[0], calculate_new_pos(agent_pos[1] + 1, board_size)),
            (agent_pos[0], calculate_new_pos(agent_pos[1] - 1, board_size))
        ]
        return [cell for cell in adj_cells if cell[0]!=None and cell[1]!=None]
    
    @staticmethod
    def find_adjacent_vertical_cells(agent_pos, board_size):
        adj_cells = [(pos, agent_pos[1]) for pos in range(board_size) \
            if pos != agent_pos[0]]
        return adj_cells

    @staticmethod
    def find_adjacent_horizontal_cells(agent_pos, board_size):
        adj_cells = [(agent_pos[0], pos) for pos in range(board_size) \
            if pos != agent_pos[1]]
        return adj_cells
    
    @staticmethod
    def find_pos_from_adj_cells(adj_cells) -> Tuple[int, int]:
        col_freq_count = {}
        row_freq_count = {}
        
        for pos in adj_cells:
            if pos[0] not in row_freq_count.keys():
                row_freq_count[pos[0]] = 1
            else:
                row_freq_count[pos[0]] += 1
            
            if pos[1] not in col_freq_count.keys():
                col_freq_count[pos[1]] = 1
            else:
                col_freq_count[pos[1]] += 1

        col = max(col_freq_count, key=col_freq_count.get)
        row = max(row_freq_count, key=row_freq_count.get)
        return (row, col)
            