import pygame
from config import TILE_SIZE, GROUND_COLOR, DOOR_COLOR

class Level:
    def __init__(self, level_map):
        self.level_map = level_map
        self.door_rects = []
        self._init_door_rects()

    def _init_door_rects(self):
        # Create door rects once at init
        for y, row in enumerate(self.level_map):
            for x, tile in enumerate(row):
                if tile == "D":
                    rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    self.door_rects.append(rect)

    def draw(self, screen):
        for y, row in enumerate(self.level_map):
            for x, tile in enumerate(row):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if tile == "1":
                    pygame.draw.rect(screen, GROUND_COLOR, rect)
                elif tile == "D":
                    pygame.draw.rect(screen, DOOR_COLOR, rect)

    def get_collidable_rects(self):
        rects = []
        for y, row in enumerate(self.level_map):
            for x, tile in enumerate(row):
                if tile == "1":
                    rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    rects.append(rect)
        return rects
