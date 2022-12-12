class Utility:
    @staticmethod
    def find_adjacent_cells(agent_pos):
        """
        given current pos, find 4 adjacent cells
        """
        def calculate_new_pos(number):
            if number < 0 or number > 3:
                return None
            return number

        adj_cells = [
            (calculate_new_pos(agent_pos[0] + 1), agent_pos[1]),
            (calculate_new_pos(agent_pos[0] - 1), agent_pos[1]),
            (agent_pos[0], calculate_new_pos(agent_pos[1] + 1)),
            (agent_pos[0], calculate_new_pos(agent_pos[1] + 1))
        ]
        return adj_cells