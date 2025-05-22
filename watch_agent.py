import time
from env import PlatformerEnv
from stable_baselines3 import PPO

env = PlatformerEnv()
model = PPO.load("ppo_platformer")

episode = 0
while True:
    obs, info = env.reset()
    done = False
    total_reward = 0
    step = 0
    episode += 1
    print(f"Starting episode {episode}")

    while not done and step < 1000:
        env.render()
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated
        total_reward += reward
        step += 1
        time.sleep(0.02)

    print(f"Episode {episode} finished with reward {total_reward:.2f} in {step} steps")

    if total_reward == 1:
        print("🎉 Agent completed the level! Exiting.")
        break

env.close()
