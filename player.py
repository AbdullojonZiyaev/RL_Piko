import pygame
from config import TILE_SIZE, PLAYER_COLOR, MOVE_SPEED, JUMP_FORCE, GRAVITY, TERMINAL_VELOCITY

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.vel_y = 0
        self.on_ground = False
        self.deaths = 0

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.move_x = 0
        if keys[pygame.K_LEFT]:
            self.move_x = -MOVE_SPEED
        elif keys[pygame.K_RIGHT]:
            self.move_x = MOVE_SPEED

        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -JUMP_FORCE

    def apply_gravity(self):
        self.vel_y += GRAVITY
        if self.vel_y > TERMINAL_VELOCITY:
            self.vel_y = TERMINAL_VELOCITY

    def handle_horizontal_collisions(self, collidables):
        self.rect.x += self.move_x
        for tile in collidables:
            if self.rect.colliderect(tile):
                if self.move_x > 0:
                    self.rect.right = tile.left
                elif self.move_x < 0:
                    self.rect.left = tile.right

    def handle_vertical_collisions(self, collidables):
        self.rect.y += self.vel_y
        self.on_ground = False
        for tile in collidables:
            if self.rect.colliderect(tile):
                if self.vel_y > 0:
                    self.rect.bottom = tile.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = tile.bottom
                    self.vel_y = 0

    def reset_position(self):
        self.rect.x = 100
        self.rect.y = 100
        self.vel_y = 0

    def update(self, collidables):
        self.handle_input()
        self.handle_horizontal_collisions(collidables)
        self.apply_gravity()
        self.handle_vertical_collisions(collidables)

    def draw(self, screen):
        pygame.draw.rect(screen, PLAYER_COLOR, self.rect)
