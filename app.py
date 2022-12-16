from wumpus.world import World
from wumpus.engine import Engine
from wumpus.agent import Agent

def is_game_over(agent, percept):
    if agent.arrow == 0 and agent.wumpus_killed == 0:
        print("You ran out of Arrow")
        print("YOU LOOSE")
        return True
    if percept["game_over"]:
        with open("debug.txt", mode ="w+") as file:
            for line in agent.engine.knowledge.items():
                file.write(f"{line}\n")
        
        print("YOU LOOSE")
        return True
    if agent.wumpus_killed == 1 and agent.gold > 0:
        print(f"TOTAL GOLD COLLECTED: {agent.gold}")
        print(f"WUMPUS KILLED: {agent.wumpus_killed}")
        print("YOU WON")
        return True
    return False

if __name__=="__main__":
    world = World(mode=1)
    knowledge = Engine(world.start_agent_pos, board_size=world.board_size)
    agent = Agent(engine=knowledge, world=world)
    print(f"Starting Position {agent.agent_pos}")
    # initialize the first sense of the world
    percept = world.sensor(agent.agent_pos)
    
    agent.update_percept(percept) 

    counter = 0
    # while not game over
    while True:
        print(f"Iteration {counter}")
        # agent ask for move from KB
        agent.agent_pos = agent.move()
        print(f"Move to cell {agent.agent_pos}")
        
        # agent ask to update position in world
        # and receives percept from world
        percept = world.sensor(agent.agent_pos)
        print(f"Receive Percept {percept}")
        
        if is_game_over(agent, percept):
            break
        
        agent.update_percept(percept) 

        # else proceed to 
        counter += 1



    
    
    