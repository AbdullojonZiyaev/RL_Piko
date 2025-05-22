import pygame
import numpy as np
import gymnasium as gym
from gymnasium.spaces import Discrete, Box
from config import SCREEN_WIDTH, SCREEN_HEIGHT, MOVE_SPEED, JUMP_FORCE, GRAVITY, TERMINAL_VELOCITY, TILE_SIZE
from level import Level
from player import Player

class PlatformerEnv(gym.Env):
    def __init__(self):
        super().__init__()
        pygame.init()
        self.steps = 0
        self.max_steps = 500

        self.level = Level([
            "                    ",
            "                    ",
            "      111           ",
            "                    ",
            "         111        ",
            "                    ",
            "   111        111 D ",
            "                    ",
            "             1       ",
            "111      1111       ",
            "                    ",
            "    111                "
        ])
        self.player = Player(100, 100)

        # Discrete actions: 0 = do nothing, 1 = left, 2 = right, 3 = jump
        self.action_space = Discrete(4)

        # Observation space: x, y, vx, vy (can be extended later)
        low = np.array([0, 0, -100, -100], dtype=np.float32)
        high = np.array([SCREEN_WIDTH, SCREEN_HEIGHT, 100, 100], dtype=np.float32)
        self.observation_space = Box(low, high, dtype=np.float32)

        self.clock = pygame.time.Clock()

    def get_obs(self):
        return np.array([
            self.player.rect.x,
            self.player.rect.y,
            self.player.move_x if hasattr(self.player, "move_x") else 0,
            self.player.vel_y
        ], dtype=np.float32)

    def step(self, action):
        self.steps += 1
        prev_dist = self._distance_to_door()
        old_y = self.player.rect.y
        was_near_cliff = self._is_near_cliff()

        # Handle action
        if action == 1:
            self.player.move_x = -MOVE_SPEED
        elif action == 2:
            self.player.move_x = MOVE_SPEED
        else:
            self.player.move_x = 0

        if action == 3 and self.player.on_ground:
            self.player.vel_y = -JUMP_FORCE

        # Physics and collisions
        self.player.handle_horizontal_collisions(self.level.get_collidable_rects())
        self.player.apply_gravity(GRAVITY, TERMINAL_VELOCITY)
        self.player.handle_vertical_collisions(self.level.get_collidable_rects())

        # Reward calculation
        reward = 0.0

        curr_dist = self._distance_to_door()
        delta_dist = prev_dist - curr_dist
        if delta_dist > 0:
            reward += delta_dist * 0.01  # reward progress toward door
        else:
            reward -= 0.05  # slight penalty for getting farther or no progress

        # Reward for jumping near cliff
        if was_near_cliff and action == 3:
            reward += 0.1

        # Reward for upward movement
        delta_y = old_y - self.player.rect.y
        if delta_y > 0:
            reward += 0.02 * delta_y

        # Terminal conditions
        terminated = False
        truncated = False

        if self.player.rect.y > SCREEN_HEIGHT:
            reward = -2.0  # strong penalty for falling
            terminated = True

        elif any(self.player.rect.colliderect(d) for d in self.level.door_rects):
            reward = 1.0  # big reward for success
            terminated = True

        if self.steps >= self.max_steps:
            truncated = True

        # Clip reward to avoid instability
        reward = np.clip(reward, -2.0, 1.0)

        info = {}
        return self.get_obs(), reward, terminated, truncated, info



    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.player.reset_position()
        self.steps = 0
        return self.get_obs(), {}


    def render(self, mode='human'):
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.fill((255, 255, 255))
        self.level.draw(screen)
        self.player.draw(screen)
        pygame.display.flip()
        self.clock.tick(60)

    def close(self):
        pygame.quit()

    def _distance_to_door(self):
        # Use Euclidean distance from player to nearest door
        px, py = self.player.rect.center
        distances = [
            np.linalg.norm(np.array((px, py)) - np.array(d.center))
            for d in self.level.door_rects
        ]
        return min(distances)
    
    def _is_near_cliff(self):
        feet_x = self.player.rect.centerx
        feet_y = self.player.rect.bottom
        check_dx = np.sign(self.player.move_x) * TILE_SIZE // 2
        test_rect = pygame.Rect(feet_x + check_dx, feet_y + 1, 2, 2)
        return not any(test_rect.colliderect(r) for r in self.level.get_collidable_rects())
