# src/model.py
import torch
import torch.nn as nn

class ImitationModel(nn.Module):
    """
    관절각을 예측하는 간단한 MLP 기반 모방 학습 모델.
    """
    def __init__(self, input_dim=6, output_dim=6, hidden_dim=128):
        super(ImitationModel, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim * 2),
            nn.ReLU(),
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim)
        )

    def forward(self, x):
        return self.network(x)