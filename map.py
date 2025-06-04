from typing import Dict

from vec2D import vec2D
from random import randint

class Map:
    state: dict[vec2D, str]

    def __init__(self, NX, NY, nWumpus, nPits):
        self.state = {}  # Dictionary to hold the state of each square

        for x in range(0, NX):
            for y in range(0, NY):
                self.state[vec2D(x, y)] = 'cell'

        # select the starting cell. Has to be on the edge
        x = randint(0, NX - 1)
        y = randint(0, NY - 1)
        d = randint(0, 1)
        if d == 0:
            start_position = vec2D(0, y)
        else:
            start_position = vec2D(x, 0)

        self.state[start_position] = 'start'

        # randomly add wumpus to cells
        wumpus_added = 0
        while True:
            x = randint(0, NX - 1)
            y = randint(0, NY - 1)
            if x != start_position.x and y != start_position.y:
                self.state[vec2D(x, y)] = 'wumpus'
                wumpus_added += 1
            if wumpus_added >= nWumpus:
                break

        # randomly add pits to cells
        pits_added = 0
        while True:
            x = randint(0, NX - 1)
            y = randint(0, NY - 1)
            pos = vec2D(x, y)
            if self.state[pos] != 'start' and self.state[pos] != 'wumpus':
                self.state[vec2D(x, y)] = 'pit'
                pits_added += 1
            if pits_added >= nPits:
                break

        # randomly add gold
        while True:
            x = randint(0, NX - 1)
            y = randint(0, NY - 1)
            pos = vec2D(x, y)
            if self.state[pos] != 'start' and self.state[pos] != 'wumpus' and self.state[pos] != 'pit':
                self.state[vec2D(x, y)] = 'gold'
                break

    def get_percepts(self, position):

        # If the current position has a wumpus or pit, the agent dies
        if self.state[position] == 'wumpus' or self.state[position] == 'pit':
            return 'died'

        # adjacent squares
        n = position + vec2D(0, 1)
        s = position + vec2D(0, -1)
        e = position + vec2D(1, 0)
        w = position + vec2D(-1, 0)

        # check for percepts in adjacent squares
        # but only within the bounds of the map

        percepts = ''
        if self.state.get(n, '') == 'wumpus' or self.state.get(s, '') == 'wumpus' or self.state.get(e, '') == 'wumpus' or self.state.get(w, '') == 'wumpus':
            percepts += 'stench'
        if self.state.get(n, '') == 'pit' or self.state.get(s, '') == 'pit' or self.state.get(e, '') == 'pit' or self.state.get(w, '') == 'pit':
            percepts += ', breeze'
        if self.state[position] == 'gold':
            percepts += ', glitter'

        return percepts

    def try_move(self, new_position):
        # Check if the new position is within the bounds of the map
        return new_position in self.state

    def remove_gold(self, position):
        if self.state[position] == 'gold':
            self.state[position] = 'cell'
            return True

    def get_start(self):
        for pos, content in self.state.items():
            if content == 'start':
                return pos
        return None