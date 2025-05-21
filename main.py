import pygame
import sys
import time

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
TILE_SIZE = 40

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GROUND_COLOR = (100, 100, 255)
PLAYER_COLOR = (255, 100, 100)
DOOR_COLOR = (0, 200, 0)

# FPS
FPS = 60

# Level layout
LEVEL_MAP = [
    "00000000000000000000",
    "00000000000000000000",
    "00000000000000000000",
    "00000000000000000000",
    "11111100000000000000",
    "11111100000000000000",
    "1111110000111100DDDD",
    "11111100000000000000",
]


class Level:
    def __init__(self, level_map):
        self.level_map = level_map
        self.door_rects = []

    def draw(self, screen):
        self.door_rects = []
        for y, row in enumerate(self.level_map):
            for x, tile in enumerate(row):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if tile == "1":
                    pygame.draw.rect(screen, GROUND_COLOR, rect)
                elif tile == "D":
                    pygame.draw.rect(screen, DOOR_COLOR, rect)
                    self.door_rects.append(rect)

    def get_collidable_rects(self):
        rects = []
        for y, row in enumerate(self.level_map):
            for x, tile in enumerate(row):
                if tile == "1" or tile == "D":
                    rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    rects.append(rect)
        return rects




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


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Piko Agents")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 28)

        self.level = Level(LEVEL_MAP)
        self.player = Player(100, 100)
        self.start_time = time.time()

    def draw_ui(self):
        # Death counter
        deaths_text = self.font.render(f"Deaths: {self.player.deaths}", True, BLACK)
        self.screen.blit(deaths_text, (10, 10))

        # Timer
        elapsed = int(time.time() - self.start_time)
        minutes = elapsed // 60
        seconds = elapsed % 60
        time_text = self.font.render(f"Time: {minutes:02}:{seconds:02}", True, BLACK)
        self.screen.blit(time_text, (10, 40))

    def run(self):
        while True:
            self.screen.fill(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Draw the level first to update door_rect
            self.level.draw(self.screen)

            # Now update player with collidables
            self.player.update(self.level.get_collidable_rects())

            # Check if player fell
            if self.player.rect.y > SCREEN_HEIGHT:
                self.player.deaths += 1
                print(f"💀 Player died! Total deaths: {self.player.deaths}")
                self.player.reset_position()

            # Check if player reached door
            if any(self.player.rect.colliderect(door_rect) for door_rect in self.level.door_rects):
                print("🎉 Level Complete!")
                pygame.time.delay(1000)
                self.player.reset_position()
                self.start_time = time.time()  # Restart timer

            # Draw player and UI
            self.player.draw(self.screen)
            self.draw_ui()

            pygame.display.update()
            self.clock.tick(FPS)



if __name__ == "__main__":
    game = Game()
    game.run()
