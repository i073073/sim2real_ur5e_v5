# src/policies/diffusion_policy.py
import torch
import torch.nn as nn

class NoisePredictor(nn.Module):
    """
    디퓨전 정책의 핵심인 노이즈 예측 네트워크 (U-Net과 유사한 구조).
    현재 관측(이미지 임베딩, 관절각)과 노이즈가 낀 행동, 그리고 시간 스텝(t)을 입력받아
    추가된 노이즈를 예측합니다.
    """
    def __init__(self, observation_dim, action_dim, time_embedding_dim):
        super().__init__()
        # ... Temporal U-Net 또는 Transformer 기반 네트워크 아키텍처 ...
        pass

    def forward(self, noisy_action, t, observation):
        # ... 노이즈 예측 로직 ...
        return predicted_noise

class DiffusionPolicy(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.noise_predictor = NoisePredictor(...)
        # ... Noise Scheduler (cosine, linear 등) 초기화 ...

    def train_step(self, actions, observations):
        # 1. 무작위 시간 스텝 t 샘플링
        # 2. 원본 행동(actions)에 t에 해당하는 노이즈 추가 -> noisy_actions 생성
        # 3. noise_predictor를 사용하여 추가된 노이즈 예측
        # 4. 실제 노이즈와 예측된 노이즈 간의 MSE Loss 계산 및 역전파
        pass

    def predict_action(self, observation):
        # 1. 완전한 가우시안 노이즈에서 시작
        # 2. T부터 1까지 시간 스텝을 거꾸로 반복하며,
        #    매 스텝마다 noise_predictor로 노이즈를 예측하고 제거하는 과정을 반복
        # 3. 최종적으로 노이즈가 모두 제거된 깨끗한 행동(action) 궤적 반환
        pass