from vec2D import vec2D
from map import Map
from random import randint

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
        self.heard_scream = False
        self.wumpa_loc = None
        self.found_wumpa = False

        self.score = 0  # score for the agent, starts at 0

    def update_state(self, percepts : str):
        x = self.position.x
        y = self.position.y

        n = vec2D(x, y + 1)
        s = vec2D(x, y - 1)
        e = vec2D(x + 1, y)
        w = vec2D(x - 1, y)

        if 'stench' in percepts:
            # mark the adjacent squares as unsafe if and only if they're not marked as safe
            if self.state.get(n, '') == 'unknown' and n in self.state:
                self.state[n] = 'pw'
            if self.state.get(s, '') == 'unknown' and s in self.state:
                self.state[s] = 'pw'
            if self.state.get(e, '') == 'unknown' and e in self.state:
                self.state[e] = 'pw'
            if self.state.get(w, '') == 'unknown' and w in self.state:
                self.state[w] = 'pw'
        elif 'breeze' in percepts:
            # mark the adjacent squares as unsafe if and only if they're not marked as safe
            if self.state.get(n, '') == 'unknown' and n in self.state:
                self.state[n] += 'pp'
            if self.state.get(s, '') == 'unknown' and s in self.state:
                self.state[s] += 'pp'
            if self.state.get(e, '') == 'unknown' and e in self.state:
                self.state[e] += 'pp'
            if self.state.get(w, '') == 'unknown' and w in self.state:
                self.state[w] += 'pp'
        elif 'breeze' in percepts and 'stench' in percepts:
            # mark the adjacent squares as unsafe if and only if they're not marked as safe
            if self.state.get(n, '') == 'unknown' and n in self.state:
                self.state[n] += 'pwp'
            if self.state.get(s, '') == 'unknown' and s in self.state:
                self.state[s] += 'pwp'
            if self.state.get(e, '') == 'unknown' and e in self.state:
                self.state[e] += 'pwp'
            if self.state.get(w, '') == 'unknown' and w in self.state:
                self.state[w] += 'pwp'
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

        has_unknown = False
        possible_wumpa_count = 0

        if not self.found_wumpa:
            for pos, state in self.state.items():
                if state == 'unknown':
                    has_unknown = True
                if state == 'pw' or state == 'pwp':
                    possible_wumpa_count += 1

        if not has_unknown and possible_wumpa_count == 1:
            self.found_wumpa = True
            for pos, state in self.state.items():
                if state == 'pw' or state == 'pwp':
                    self.wumpa_loc = pos
                    self.state[pos] = 'w'

        if self.found_wumpa and not self.heard_scream:
            # Shoot action
            # First lets face in the general direction of the wumpus
            diff = self.wumpa_loc - self.position

            if diff.x == 0 or diff.y == 0:
                # turn until we face and shoot.
                dir_to_wumpa = diff.normalized()
                heading = self.immediate_square(self.orientation) - self.position
                if vec2D.dot(dir_to_wumpa, heading) < 0:
                    # turn right until we face wumpus
                    return 'right'
                else:
                    return 'shoot'


        # else shoot if found. But shooting is not a priority.

        # Generate a single random number for the 'forward' movement checks
        # This number is used for both the 'safe' and 'unsafe' forward conditions,
        # ensuring their probabilities are mutually exclusive based on this single roll.
        forward_chance_roll = randint(0, 100)

        # Determine the known status of the immediate square
        # Using .get() allows for gracefully handling cases where imm_sq might not be in self.state
        imm_sq_status = self.state.get(imm_sq)
        imm_sq_is_known = imm_sq_status is not None
        imm_sq_is_safe = imm_sq_status == 'safe'
        imm_sq_is_wumpus = imm_sq_status == 'w'
        imm_sq_is_not_wumpus = imm_sq_status != 'w'  # More explicit check

        # Condition 1: Prefer to move forward if the square is safe and within the probability threshold (60% chance)
        if imm_sq_is_known and imm_sq_is_safe and forward_chance_roll < 60:
            return 'forward'
        # Condition 2: If not safe, take a small chance to move forward if it's not a Wumpus and the goal is 'look' (20% chance, provided Condition 1 wasn't met)
        elif imm_sq_is_known and not imm_sq_is_safe and imm_sq_is_not_wumpus and forward_chance_roll > 80 and self.goal == 'look':
            return 'forward'
        # If neither of the above conditions for moving forward are met
        else:
            # Generate a new random number specifically for deciding the turn direction
            turn_direction_roll = randint(0, 100)
            if turn_direction_roll % 2 == 0:
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

        elif action == 'shoot':
            self.heard_scream = map.try_shoot(self.position, self.orientation)
            self.score -= 1

        self.n += 1

        return self.goal