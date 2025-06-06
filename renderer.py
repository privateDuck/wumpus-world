import pygame
import math
from vec2D import vec2D


class WumpusWorldRenderer:
    """
    Handles all visual rendering for the Wumpus World.
    """

    def __init__(self, Nx: int, Ny: int):
        pygame.init()

        self.Nx = Nx
        self.Ny = Ny
        self.CELL_SIZE = 80  # Size of each grid cell in pixels
        self.MARGIN = 20  # Margin around the grid
        self.TEXT_AREA_HEIGHT = 150  # Height for percepts and goal text area
        self.FONT_SIZE_GRID = 36
        self.FONT_SIZE_TEXT = 24
        self.AGENT_SIZE = self.CELL_SIZE // 3  # Size of the agent triangle

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.DARK_GRAY = (100, 100, 100)
        self.GREEN = (0, 150, 0)  # For safe cells
        self.RED = (200, 0, 0)  # For Wumpus
        self.YELLOW = (255, 200, 0)  # For Gold
        self.BROWN = (139, 69, 19)  # For Pits
        self.BLUE = (0, 0, 200)  # For Agent

        self.GRID_WIDTH = self.Nx * self.CELL_SIZE
        self.GRID_HEIGHT = self.Ny * self.CELL_SIZE
        self.SCREEN_WIDTH = self.GRID_WIDTH + 2 * self.MARGIN
        self.SCREEN_HEIGHT = self.GRID_HEIGHT + 2 * self.MARGIN + self.TEXT_AREA_HEIGHT

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Wumpus World Demonstration")


        self.font_grid = pygame.font.Font(None, self.FONT_SIZE_GRID)
        self.font_text = pygame.font.Font(None, self.FONT_SIZE_TEXT)

    def _get_cell_rect(self, x: int, y: int) -> pygame.Rect:
        # Pygame's y-axis is inverted, so we adjust for grid (0,0) being bottom-left
        # In Pygame, (0,0) is top-left.
        # Our grid (0,0) is bottom-left, so Pygame y-coord will be (Ny - 1 - y)
        pygame_x = self.MARGIN + x * self.CELL_SIZE
        pygame_y = self.MARGIN + (self.Ny - 1 - y) * self.CELL_SIZE
        return pygame.Rect(pygame_x, pygame_y, self.CELL_SIZE, self.CELL_SIZE)

    def _draw_grid(self):
        for x in range(self.Nx + 1):
            start_x = self.MARGIN + x * self.CELL_SIZE
            end_x = start_x
            start_y = self.MARGIN
            end_y = self.MARGIN + self.GRID_HEIGHT
            pygame.draw.line(self.screen, self.DARK_GRAY, (start_x, start_y), (end_x, end_y), 1)

        for y in range(self.Ny + 1):
            start_x = self.MARGIN
            end_x = self.MARGIN + self.GRID_WIDTH
            start_y = self.MARGIN + y * self.CELL_SIZE
            end_y = start_y
            pygame.draw.line(self.screen, self.DARK_GRAY, (start_x, start_y), (end_x, end_y), 1)

    def _draw_cell_content(self, pos: vec2D, content: str):
        rect = self._get_cell_rect(pos.x, pos.y)
        center_x, center_y = rect.center

        text_surface = None
        color = self.BLACK

        if content == 'wumpus':
            text_surface = self.font_grid.render("W", True, self.RED)
            color = self.RED
        elif content == 'pit':
            text_surface = self.font_grid.render("P", True, self.BROWN)
            color = self.BROWN
        elif content == 'gold':
            text_surface = self.font_grid.render("G", True, self.YELLOW)
            color = self.YELLOW

        if text_surface:
            text_rect = text_surface.get_rect(center=(center_x, center_y))
            self.screen.blit(text_surface, text_rect)
            # Optionally draw a circle or square behind for better visibility
            # pygame.draw.rect(self.screen, color, rect.inflate(-10, -10), 2) # border

    def _draw_cell_agent_content(self, pos, content):
        rect = self._get_cell_rect(pos.x, pos.y)
        center_x, center_y = rect.center
        surface = None
        if content == 'safe':
            surface = pygame.draw.rect(self.screen, self.GREEN, rect.inflate(-10, -10), 2)
        else:
            surface = pygame.draw.rect(self.screen, self.RED, rect.inflate(-10, -10), 2)

    def _draw_agent(self, pos: vec2D, direction: str):
        rect = self._get_cell_rect(pos.x, pos.y)
        center_x, center_y = rect.center

        # Define triangle points relative to its center
        half_size = self.AGENT_SIZE / 2
        points = [
            (center_x, center_y - half_size),  # Top point
            (center_x - half_size, center_y + half_size),  # Bottom-left
            (center_x + half_size, center_y + half_size)  # Bottom-right
        ]

        # Determine rotation angle based on direction
        angle = 0  # Default: north (up)
        if direction == 'east':
            angle = 90
        elif direction == 'south':
            angle = 180
        elif direction == 'west':
            angle = 270

        # Rotate points around the center
        rotated_points = []
        for px, py in points:
            # Translate point to origin
            temp_x = px - center_x
            temp_y = py - center_y
            # Rotate
            rotated_x = temp_x * math.cos(math.radians(angle)) - temp_y * math.sin(math.radians(angle))
            rotated_y = temp_x * math.sin(math.radians(angle)) + temp_y * math.cos(math.radians(angle))
            # Translate back
            rotated_points.append((rotated_x + center_x, rotated_y + center_y))

        pygame.draw.polygon(self.screen, self.BLUE, rotated_points)
        pygame.draw.polygon(self.screen, self.BLACK, rotated_points, 2)  # Border

    def _draw_text_area(self, text_label: str, text_content: str, y_offset: int):
        area_start_y = self.MARGIN + self.GRID_HEIGHT + self.MARGIN + y_offset

        # Draw label
        label_surface = self.font_text.render(text_label, True, self.BLACK)
        self.screen.blit(label_surface, (self.MARGIN, area_start_y))

        # Draw content
        content_surface = self.font_text.render(text_content, True, self.BLUE)
        self.screen.blit(content_surface, (self.MARGIN + label_surface.get_width() + 10, area_start_y))


    def render_frame(self, map_state: dict[vec2D, str], agent_position: vec2D, agent_direction: str, percepts: str,
                     goal: str, agent_state : dict[vec2D, str], score: int = 0):
        """
        Renders the entire game frame.

        Args:
            map_state (dict[vec2D, str]): Dictionary mapping vec2D positions to content ('W', 'P', 'G').
            agent_position (vec2D): The current position of the agent.
            agent_direction (str): The current direction of the agent ('north', 'east', 'south', 'west').
            percepts (str): String representing the current percepts.
            goal (str): String representing the current goal.
            agent_state (dict[vec2D, str]): Dictionary mapping vec2D positions to agent state ('safe', 'unsafe').
            score (int): Current score of the agent.
        """
        self.screen.fill(self.WHITE)  # Clear screen

        self._draw_grid()

        # Draw map contents
        for pos, content in map_state.items():
            self._draw_cell_content(pos, content)

        for pos, content in agent_state.items():
            self._draw_cell_agent_content(pos, content)

        # Draw agent
        self._draw_agent(agent_position, agent_direction)

        # Draw percepts and goal
        self._draw_text_area("Score:", str(score), 0)
        if goal == 'look' or goal == 'go back':
            self._draw_text_area("Percepts:", percepts,  self.FONT_SIZE_TEXT + 10)
            self._draw_text_area("Goal:", goal, 2 * (self.FONT_SIZE_TEXT + 10))  # Offset for goal text
        else:
            self._draw_text_area("GAME OVER!   ", goal, 3 * (self.FONT_SIZE_TEXT + 10)) if goal else None


        #
        pygame.display.flip()  # Update the full display Surface to the screen

    def quit(self):
        pygame.quit()