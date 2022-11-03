from wumpus import agent, engine, world


if __name__=="__main__":
    world = world.World()
    knowledge = engine.Engine()
    agent = agent.Agent(engine=knowledge)
    