# scripts/train_imitation_model.py
import torch
import torch.nn as nn
import torch.optim as optim
import os
import numpy as np
from src.data_loader import create_dataloaders
from src.model import ImitationModel

# --- 하이퍼파라미터 설정 ---
DATA_PATH = "data/raw/joint_log_20240523_110000.jsonl" # 학습에 사용할 데이터
MODEL_SAVE_PATH = "models/best_imitation_model.pth"
SCALER_SAVE_PATH = "models/scaler.joblib"
NUM_EPOCHS = 100
BATCH_SIZE = 32
LEARNING_RATE = 1e-4
PATIENCE = 10 # Early stopping을 위한 대기 epoch 수

def train():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # 1. 데이터 로더 생성
    train_loader, val_loader, _, _ = create_dataloaders(
        data_path=DATA_PATH,
        batch_size=BATCH_SIZE,
        scaler_path=SCALER_SAVE_PATH
    )

    # 2. 모델, 손실 함수, 옵티마이저 초기화
    model = ImitationModel().to(device)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

    # 3. 학습 루프
    best_val_loss = np.inf
    epochs_no_improve = 0

    print("--- Starting Model Training ---")
    for epoch in range(NUM_EPOCHS):
        # --- Training Phase ---
        model.train()
        train_loss = 0.0
        for states, actions in train_loader:
            states, actions = states.to(device), actions.to(device)
            
            optimizer.zero_grad()
            outputs = model(states)
            loss = criterion(outputs, actions)
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item() * states.size(0)
        
        train_loss /= len(train_loader.dataset)

        # --- Validation Phase ---
        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for states, actions in val_loader:
                states, actions = states.to(device), actions.to(device)
                outputs = model(states)
                loss = criterion(outputs, actions)
                val_loss += loss.item() * states.size(0)
        
        val_loss /= len(val_loader.dataset)
        
        print(f"Epoch {epoch+1}/{NUM_EPOCHS} | Train Loss: {train_loss:.6f} | Val Loss: {val_loss:.6f}")

        # --- 모델 저장 및 Early Stopping ---
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save(model.state_dict(), MODEL_SAVE_PATH)
            print(f"Model saved to {MODEL_SAVE_PATH} (Val Loss improved)")
            epochs_no_improve = 0
        else:
            epochs_no_improve += 1
            if epochs_no_improve >= PATIENCE:
                print(f"Early stopping triggered after {PATIENCE} epochs with no improvement.")
                break
    
    print("--- Training Finished ---")

if __name__ == "__main__":
    # 학습을 위한 샘플 데이터 생성 (실제로는 로깅된 데이터를 사용)
    os.makedirs("data/raw", exist_ok=True)
    sample_data = []
    q_start = np.deg2rad([0, -90, 90, -90, -90, 0])
    for i in range(500):
        q_next = q_start + np.sin(np.full(6, i * 0.05)) * 0.1
        sample_data.append({'timestamp': time.time(), 'actual_q': q_next.tolist()})
        q_start = q_next
    with open(DATA_PATH, 'w') as f:
        for entry in sample_data:
            f.write(json.dumps(entry) + '\n')
    
    train()