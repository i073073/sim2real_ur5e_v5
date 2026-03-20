# src/learning/offline_rl_data_processor.py
import json
import numpy as np
from typing import List, Dict, Any, Tuple

# --- Data Model for Offline RL ---
# Offline RL 데이터셋은 (state, action, reward, next_state, done) 튜플로 구성됩니다.
# state: 현재 로봇 상태 (관절 위치, TCP 오차 등)
# action: 로봇이 수행한 행동 (관절 속도 명령)
# reward: 행동에 대한 보상 (RL 환경에서 계산)
# next_state: 다음 로봇 상태
# done: 에피소드 종료 여부

def create_offline_dataset(log_data: List[Dict[str, Any]]) -> Dict[str, np.ndarray]:
    """
    수집된 로봇 상태 로그를 Offline RL 데이터셋 형식으로 변환합니다.
    """
    states = []
    actions = []
    rewards = []
    next_states = []
    dones = []

    for i in range(len(log_data) - 1):
        current_state_data = log_data[i]
        next_state_data = log_data[i+1]

        # 1. 상태 추출 (state[t])
        # 예시: 관절 위치 + TCP 오차
        state = np.array(current_state_data['joint_positions'] + current_state_data['tcp_error'])
        states.append(state)

        # 2. 행동 추출 (action[t])
        # 실제로는 rtde_client가 전송한 명령을 기록해야 함. 여기서는 다음 상태와의 차이를 행동으로 가정.
        action = np.array(next_state_data['joint_positions']) - np.array(current_state_data['joint_positions'])
        actions.append(action)

        # 3. 보상 계산 (reward[t])
        # RL 환경의 보상 함수를 사용하여 계산 (예시: 거리 감소에 따른 보상)
        reward = calculate_reward(current_state_data, next_state_data)
        rewards.append(reward)

        # 4. 다음 상태 추출 (state[t+1])
        next_state = np.array(next_state_data['joint_positions'] + next_state_data['tcp_error'])
        next_states.append(next_state)

        # 5. 종료 여부 (done[t])
        dones.append(current_state_data['done'])

    return {
        "states": np.array(states),
        "actions": np.array(actions),
        "rewards": np.array(rewards),
        "next_states": np.array(next_states),
        "dones": np.array(dones)
    }

def calculate_reward(current_state: Dict[str, Any], next_state: Dict[str, Any]) -> float:
    """보상 함수 (RL 환경의 보상 함수와 동일하게 정의)"""
    current_distance = np.linalg.norm(np.array(current_state['tcp_error']))
    next_distance = np.linalg.norm(np.array(next_state['tcp_error']))
    reward = current_distance - next_distance # 거리가 줄어들면 양의 보상
    return reward

# --- CQL 학습 스크립트 (Mockup) ---
# src/learning/cql_trainer.py
# import torch
# import torch.nn as nn
# import torch.optim as optim
# from stable_baselines3.common.buffers import ReplayBuffer

# class CQLTrainer:
#     def __init__(self, dataset: Dict[str, np.ndarray]):
#         # ... CQL 모델 초기화 ...
#         pass

#     def train(self):
#         # ... CQL 손실 함수 정의 및 학습 루프 ...
#         # CQL Loss = Q_online(s, a) + alpha * (logsumexp(Q_online(s, a')) - Q_online(s, a_data))
#         pass