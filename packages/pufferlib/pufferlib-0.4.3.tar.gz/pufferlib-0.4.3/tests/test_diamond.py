from pdb import set_trace as T

from pufferlib.environments import Diamond


env = Diamond(distance_to_target=5, num_targets=8)
env.reset()

for _ in range(3):
    env.render()
    env.step(env.action_space.sample())

env.render()
