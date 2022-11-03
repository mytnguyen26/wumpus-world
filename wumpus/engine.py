
KNOWLEDGE = {}

ACTUATORS = ["move", "grab", "shoot"]


class Engine:
    def __init__(self):

        # keep track of current knowledge about the world
        self.state = [[0, 0, 0, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0]]

    def tell():
        """
        tell the engine the knowledge gained from
        percept
        """
        pass

    def ask():
        """
        ask engine the knowledge
        """
        pass
