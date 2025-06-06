from renderer import WumpusWorldRenderer
from state_machine import StateMachine
from map import Map

import pygame
import time



class WumpusWorldGame:
    def __init__(self, Nx: int, Ny: int, nWumpus : int, nPits : int):

        self.renderer = WumpusWorldRenderer(Nx, Ny)
        self.clock = pygame.time.Clock()

        self.map = Map(Nx, Ny, nWumpus, nPits) # Initialize the game map with specified dimensions and entities
        self.agent = StateMachine(Nx, Ny, self.map)  # Initialize the agent's state machine


    def run(self):

        # main game loop
        running = True
        current_goal = ''
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if current_goal != 'agent won' and current_goal != 'agent died':
                current_goal = self.agent.compute_turn(self.map)

            self.renderer.render_frame(
                self.map.state,
                self.agent.position,
                self.agent.orientation,
                self.map.get_percepts(self.agent.position),
                current_goal,
                self.agent.state,
                self.agent.score
            )


            self.clock.tick(2)

        self.renderer.quit()


if __name__ == "__main__":
    GRID_NX = 4
    GRID_NY = 4
    NUM_WUMPUS = 1  # Number of Wumpuses in the game
    NUM_PITS = 2  # Number of pits in the game

    game = WumpusWorldGame(GRID_NX, GRID_NY, NUM_WUMPUS, NUM_PITS)

    game.run()