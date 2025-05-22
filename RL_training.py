import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from env import PlatformerEnv

def make_env():
    return PlatformerEnv()

env = DummyVecEnv([make_env])

# Setup PPO with TensorBoard logging
model = PPO(
    "MlpPolicy",
    env,
    verbose=1,
    tensorboard_log="./ppo_tensorboard/"
)

# Train the agent
model.learn(total_timesteps=1_000_000)

# Save the model
model.save("ppo_platformer")
