from vec2D import vec2D
from map import Map

directions = ['east', 'south', 'west', 'north'] # clockwise order

class StateMachine:
    def __init__(self, NX, NY, map : Map):
        self.n = 0
        self.state = {}

        for x in range(0, NX):
            for y in range(0, NY):
                self.state[vec2D(x, y)] = 'unknown'

        self.NX = NX
        self.NY = NY
        self.orientation = 'east'  # initial orientation
        self.start_position = map.get_start()  # starting position
        self.position = self.start_position
        self.state[self.start_position] = 'safe'  # starting position is safe
        self.goal = 'look'

        self.score = 0  # score for the agent, starts at 0

    def update_state(self, percepts : str):
        x = self.position.x
        y = self.position.y

        n = vec2D(x, y + 1)
        s = vec2D(x, y - 1)
        e = vec2D(x + 1, y)
        w = vec2D(x - 1, y)

        if 'stench' in percepts or 'breeze' in percepts:
            # mark the adjacent squares as unsafe if and only if they're not marked as safe
            if self.state.get(n, '') == 'unknown' and n in self.state:
                self.state[n] = 'unsafe'
            if self.state.get(s, '') == 'unknown' and s in self.state:
                self.state[s] = 'unsafe'
            if self.state.get(e, '') == 'unknown' and e in self.state:
                self.state[e] = 'unsafe'
            if self.state.get(w, '') == 'unknown' and w in self.state:
                self.state[w] = 'unsafe'
        else:
            # mark all adjacent squares as safe if they are not walls
            if n in self.state:
                self.state[n] = 'safe'
            if s in self.state:
                self.state[s] = 'safe'
            if e in self.state:
                self.state[e] = 'safe'
            if w in self.state:
                self.state[w] = 'safe'

    def get_action(self, percepts : str):

        if 'glitter' in percepts:
            # if glitter is found, return 'grab'
            return 'grab'

        imm_sq = self.immediate_square(self.orientation)
        from random import randint
        d = randint(0, 100)

        # if the immediate square is safe, move forward
        if imm_sq in self.state and self.state[imm_sq] == 'safe' and d < 60:
            return 'forward'
        # if the immediate square is unsafe, there is a small chance to move forward if the goal is to look
        elif imm_sq in self.state and self.state[imm_sq] != 'safe' and d > 80 and self.goal == 'look':
            return 'forward'
        else:
            # else, turn randomly until a safe square is found
            d = randint(0, 100)
            if d % 2 == 0:
                return 'right'
            else:
                return 'left'

    def immediate_square(self, orr):
        if orr == 'east':
            return self.position + vec2D(1, 0)
        elif orr == 'west':
            # return the square to the west
            return self.position + vec2D(-1, 0)
        elif orr == 'north':
            # return the square to the north
            return self.position + vec2D(0, 1)
        elif orr == 'south':
            # return the square to the south
            return self.position + vec2D(0, -1)

    def compute_turn(self, map : Map):

        percepts = map.get_percepts(self.position)

        if percepts == 'died':
            self.goal = 'agent died'
            self.score -= 1000  # score for dying
            return self.goal

        if self.goal == 'go back' and self.position == self.start_position:
            # game won
            self.goal = 'agent won'

            self.score += 1000 # score for winning the game
            return self.goal

        # only update state when discovering world (looking for gold)
        if self.goal == 'look':
            self.update_state(percepts)

        action = self.get_action(percepts)

        if action == 'grab':
            map.remove_gold(self.position)
            self.goal = 'go back'

        if action == 'forward':
            new_pos = self.immediate_square(self.orientation)

            if map.try_move(new_pos):
                self.position = new_pos
                self.state[self.position] = 'safe'
                self.score -= 1

        elif action == 'right':
            idx = directions.index(self.orientation)
            self.orientation = directions[(idx + 1) % len(directions)]
            self.score -= 1

        elif action == 'left':
            idx = directions.index(self.orientation)
            self.orientation = directions[(idx - 1) % len(directions)]
            self.score -= 1

        self.n += 1

        return self.goal