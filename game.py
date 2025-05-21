import sys
import pygame
import time
from config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, FPS, LEVEL_MAP
from level import Level
from player import Player

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
        last_print_time = 0
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

            # Print debug info once per second
            current_time = time.time()
            if current_time - last_print_time >= 1.0:
                last_print_time = current_time
                print(f"Door rects: {self.level.door_rects} ::: Player rect: {self.player.rect}")

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
