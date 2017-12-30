import gym
from DQN.RL_brain import *
import torch


env = gym.make('CartPole-v0')
env = env.unwrapped
use_cuda = torch.cuda.is_available()
dtype = torch.cuda.FloatTensor

# print(env.action_space)
# print(env.observation_space)
# print(env.observation_space.high)
# print(env.observation_space.low)


RL = deep_q_learning(state_dim=env.observation_space.shape[0],
                     action_dim=env.action_space.n,
                     learning_rate=0.001,
                     memory_size=1000, batch_size=64, replace_target_iter=500, dtype=dtype,
                     e_greedy_increment=0.0001)
total_step = 0
num_iter = 100

def test():
    RL.load_params()
    RL.eval_net.eval()
    RL.epsilon = 1  # 测试不探索
    for i in range(100):
        observation = env.reset()
        ep_r = 0
        while True:
            env.render()
            action = RL.choose_action(observation)
            observation_, reward, done, _ = env.step(action)
            x, x_dot, theta, theta_dot = observation_
            r1 = (env.x_threshold - abs(x)) / env.x_threshold - 0.8
            r2 = (env.theta_threshold_radians - abs(theta)) / env.theta_threshold_radians - 0.5
            reward = r1 + r2
            ep_r += reward
            # RL.store_transition(observation, action, reward, observation_)
            if done:
                print('episode: ', i,
                      'ep_r: ', round(ep_r, 2),
                      ' epsilon: ', round(RL.epsilon, 2))
                break

            observation = observation_


test()

def train(total_step):
    for i in range(1000):
        observation = env.reset()
        ep_r = 0
        if i % 10 == 0:
            RL.store_params()
        while True:
            # env.render()
            action = RL.choose_action(observation)
            observation_, reward, done, _ = env.step(action)
            x, x_dot, theta, theta_dot = observation_
            r1 = (env.x_threshold - abs(x)) / env.x_threshold - 0.8
            r2 = (env.theta_threshold_radians - abs(theta)) / env.theta_threshold_radians - 0.5
            reward = r1 + r2
            ep_r += reward
            RL.store_transition(observation, action, reward, observation_)
            if total_step>500:
                RL.learn()
            else:
                total_step += 1
            if done:
                print('episode: ', i,
                      'ep_r: ', round(ep_r, 2),
                      ' epsilon: ', round(RL.epsilon, 2))
                break

            observation = observation_

