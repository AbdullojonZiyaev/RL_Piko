import time
from env import PlatformerEnv

env = PlatformerEnv()

episode = 0
while True:
    obs, info = env.reset()
    done = False
    total_reward = 0
    step = 0
    episode += 1
    print(f"Starting episode {episode}")

    while not done and step < 1000:  # safety limit to avoid infinite loops
        env.render()
        action = env.action_space.sample()  # for now random actions
        obs, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated
        total_reward += reward
        step += 1
        time.sleep(0.02)

    print(f"Episode {episode} finished with reward {total_reward:.2f} in {step} steps")

    if total_reward > 0:  # reached door, success!
        print("🎉 Level Completed! Exiting loop.")
        break

env.close()
