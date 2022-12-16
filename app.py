from wumpus import agent, engine, world

def is_game_over(agent, percept):
    if agent.arrow == 0 and agent.wumpus_killed == 0:
        print("You ran out of Arrow")
        print("You loose")
        return True
    if percept["game_over"]:
        print("You Loose")
        return True
    if agent.wumpus_killed == 1 and agent.gold > 0:
        print(f"Current Gold collected {agent.gold}")
        print("You Won")
        return True
    return False

if __name__=="__main__":
    world = world.World(mode=0)
    knowledge = engine.Engine(board_size=world.board_size)
    agent = agent.Agent(engine=knowledge, world=world)
    
    # initialize the first sense of the world
    percept = world.sensor(agent.agent_pos)
    agent.update_percept(percept) 

    counter = 0
    # while not game over
    # while False: indicate not game over
    while counter < 10:
        print(f"Iteration {counter}")
        # agent ask for move from KB
        agent_move = agent.move()
        print(f"Move to cell {agent_move}")
        
        # agent ask to update position in world
        # and receives percept from world
        percept = world.sensor(agent_move)
        agent.update_percept(percept) 

        # else proceed to 
        counter += 1



    
    
    