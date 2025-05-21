import pygame
from config import TILE_SIZE, PLAYER_COLOR

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.vel_y = 0
        self.on_ground = False
        self.deaths = 0

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -15

    def apply_gravity(self):
        self.vel_y += 1
        self.rect.y += self.vel_y

    def check_collisions(self, collidables):
        self.on_ground = False

        # Horizontal collisions
        for tile in collidables:
            if self.rect.colliderect(tile):
                if self.vel_y == 0:  # no vertical movement, just handle horizontal
                    if self.rect.centerx < tile.centerx:
                     self.rect.right = tile.left
                    else:
                        self.rect.left = tile.right

        # Apply vertical movement separately
        self.rect.y += self.vel_y

        # Vertical collisions
        for tile in collidables:
            if self.rect.colliderect(tile):
                if self.vel_y > 0:  # falling down
                    self.rect.bottom = tile.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:  # moving up
                    self.rect.top = tile.bottom
                    self.vel_y = 0


    def reset_position(self):
        self.rect.x = 100
        self.rect.y = 100
        self.vel_y = 0

    def update(self, collidables):
        self.handle_input()

        # Move horizontally first
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 1
        if keys[pygame.K_RIGHT]:
            self.rect.x += 1

        # Horizontal collision check
        for tile in collidables:
            if self.rect.colliderect(tile):
                if keys[pygame.K_LEFT]:
                    self.rect.left = tile.right
                elif keys[pygame.K_RIGHT]:
                    self.rect.right = tile.left

        # Apply gravity and vertical movement
        self.apply_gravity()

        # Vertical collision check
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

    def draw(self, screen):
        pygame.draw.rect(screen, PLAYER_COLOR, self.rect)