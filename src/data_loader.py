# src/data_loader.py
import torch
from torch.utils.data import Dataset, DataLoader, random_split
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib
import os

class UR5eTrajectoryDataset(Dataset):
    """
    UR5e 궤적 데이터(.jsonl)를 로드하고, (현재 상태, 다음 행동) 쌍으로 변환하는 PyTorch Dataset.
    """
    def __init__(self, jsonl_path: str, scaler: StandardScaler = None):
        """
        :param jsonl_path: 데이터 파일 경로.
        :param scaler: 데이터 정규화에 사용할 scikit-learn StandardScaler 객체.
                       None이면 새로 학습합니다.
        """
        df = pd.read_json(jsonl_path, lines=True)
        
        # 'actual_q' 리스트를 개별 컬럼으로 분리
        q_data = np.array(df['actual_q'].tolist())
        
        # Scaler 학습 또는 적용
        if scaler is None:
            self.scaler = StandardScaler()
            self.scaled_data = self.scaler.fit_transform(q_data)
        else:
            self.scaler = scaler
            self.scaled_data = self.scaler.transform(q_data)
            
        # 상태(s_t)와 행동(a_t = s_{t+1}) 쌍 생성
        self.states = self.scaled_data[:-1]
        self.actions = self.scaled_data[1:]

    def __len__(self):
        return len(self.states)

    def __getitem__(self, idx):
        state = torch.tensor(self.states[idx], dtype=torch.float32)
        action = torch.tensor(self.actions[idx], dtype=torch.float32)
        return state, action

def create_dataloaders(data_path: str, batch_size: int = 32, scaler_path: str = "models/scaler.joblib"):
    """
    데이터셋을 생성하고 train, validation, test DataLoader로 분할합니다.
    """
    # 데이터셋 인스턴스 생성 및 Scaler 학습
    full_dataset = UR5eTrajectoryDataset(jsonl_path=data_path)
    
    # 학습된 Scaler 저장
    os.makedirs(os.path.dirname(scaler_path), exist_ok=True)
    joblib.dump(full_dataset.scaler, scaler_path)
    print(f"Scaler saved to {scaler_path}")

    # 데이터셋 분할 (80% train, 10% validation, 10% test)
    train_size = int(0.8 * len(full_dataset))
    val_size = int(0.1 * len(full_dataset))
    test_size = len(full_dataset) - train_size - val_size
    
    train_dataset, val_dataset, test_dataset = random_split(
        full_dataset, [train_size, val_size, test_size]
    )

    # 데이터로더 생성
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
    
    return train_loader, val_loader, test_loader, full_dataset.scaler