import numpy as np
import tensorflow as tf
from tensorflow import keras
import gym
from rl.agents import DQNAgent
from rl.memory import SequentialMemory
from rl.policy import LinearAnnealedPolicy, EpsGreedyQPolicy

env = gym.make("ALE/SpaceInvaders-v5", render_mode='human', full_action_space=False)

episodes = 2

def build_model(height, width, channels, actions):
    model = keras.Sequential()
    model.add(keras.layers.Conv2D(32, (8, 8), strides=(4, 4), activation="relu", input_shape=(3, height, width, channels)))
    model.add(keras.layers.Conv2D(64, (4, 4), strides=(2, 2), activation="relu"))
    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(512, activation="relu"))
    model.add(keras.layers.Dense(256, activation="relu"))
    model.add(keras.layers.Dense(actions, activation="linear"))
    return model

height, width, channels = env.observation_space.shape
actions = env.action_space.n

model = build_model(height, width, channels, actions)

def build_agent(model, actions):
    policy = LinearAnnealedPolicy(EpsGreedyQPolicy(), attr="eps", value_max=1., value_min=1., value_test=.2, nb_steps=10000)
    memory = SequentialMemory(limit=2000, window_length=3)
    dqn = DQNAgent(model=model, memory=memory, policy=policy, enable_dueling_network=True, dueling_type="avg", nb_actions=actions, nb_steps_warmup=1000)
    return dqn

dqn = build_agent(model, actions)

dqn.compile(tf.keras.optimizers.Adam(learning_rate=0.01))

dqn.fit(env, nb_steps=40000, visualize=False, verbose=1)

scores = dqn.test(env, nb_episodes=10, visualize=True)
print(np.mean(scores.history["epicode_reward"]))

dqn.save_weights("models/dqn.h5")