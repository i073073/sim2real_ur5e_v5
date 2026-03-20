# scripts/evaluate_model.py
import torch
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from src.model import ImitationModel
from src.data_loader import UR5eTrajectoryDataset

# --- 평가 설정 ---
MODEL_PATH = "models/best_imitation_model.pth"
SCALER_PATH = "models/scaler.joblib"
DATA_PATH = "data/raw/joint_log_20240523_110000.jsonl" # 학습에 사용된 전체 데이터
PLOT_SAVE_PATH = "reports/trajectory_comparison.png"

def evaluate():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # 1. 모델 및 스케일러 로드
    model = ImitationModel().to(device)
    model.load_state_dict(torch.load(MODEL_PATH))
    model.eval()
    scaler = joblib.load(SCALER_PATH)
    print("Model and scaler loaded successfully.")

    # 2. 테스트 데이터 준비 (여기서는 전체 데이터를 사용해 롤아웃 시뮬레이션)
    df = pd.read_json(DATA_PATH, lines=True)
    ground_truth_q = np.array(df['actual_q'].tolist())
    
    # 3. 궤적 예측 (Rollout)
    # 첫 번째 상태에서 시작하여, 모델의 예측을 다음 입력으로 사용하여 전체 궤적 생성
    predicted_q = []
    current_q_scaled = scaler.transform(ground_truth_q[0].reshape(1, -1))
    current_q_tensor = torch.tensor(current_q_scaled, dtype=torch.float32).to(device)

    with torch.no_grad():
        for i in range(len(ground_truth_q) - 1):
            # 현재 상태의 실제 관절값을 저장 (역변환된 값)
            predicted_q.append(scaler.inverse_transform(current_q_tensor.cpu().numpy())[0])
            
            # 다음 상태 예측
            next_q_tensor = model(current_q_tensor)
            
            # 예측된 다음 상태를 새로운 현재 상태로 업데이트
            current_q_tensor = next_q_tensor
            
    predicted_q = np.array(predicted_q)

    # 4. 성능 지표 계산
    min_len = min(len(ground_truth_q), len(predicted_q))
    gt = ground_truth_q[:min_len]
    pred = predicted_q[:min_len]

    mse = mean_squared_error(gt, pred, multioutput='raw_values')
    mae = mean_absolute_error(gt, pred, multioutput='raw_values')
    r2 = r2_score(gt, pred, multioutput='raw_values')

    print("\n--- Model Performance on Test Trajectory Rollout ---")
    print("Metric | J1      | J2      | J3      | J4      | J5      | J6")
    print("-------|---------|---------|---------|---------|---------|---------")
    print(f"MSE    | {mse[0]:.5f} | {mse[1]:.5f} | {mse[2]:.5f} | {mse[3]:.5f} | {mse[4]:.5f} | {mse[5]:.5f}")
    print(f"MAE    | {mae[0]:.5f} | {mae[1]:.5f} | {mae[2]:.5f} | {mae[3]:.5f} | {mae[4]:.5f} | {mae[5]:.5f}")
    print(f"R2     | {r2[0]:.5f} | {r2[1]:.5f} | {r2[2]:.5f} | {r2[3]:.5f} | {r2[4]:.5f} | {r2[5]:.5f}")

    # 5. 결과 시각화
    fig, axs = plt.subplots(3, 2, figsize=(15, 10), sharex=True)
    fig.suptitle('Imitation Model: Ground Truth vs. Predicted Trajectory', fontsize=16)
    time_axis = np.arange(min_len) * 0.1 # 10Hz 데이터 기준

    for i in range(6):
        row, col = i // 2, i % 2
        axs[row, col].plot(time_axis, np.rad2deg(gt[:, i]), label='Ground Truth', color='blue', alpha=0.8)
        axs[row, col].plot(time_axis, np.rad2deg(pred[:, i]), label='Predicted', color='red', linestyle='--')
        axs[row, col].set_title(f'Joint {i+1}')
        axs[row, col].set_ylabel('Angle (degrees)')
        axs[row, col].grid(True)
        axs[row, col].legend()

    axs[2, 0].set_xlabel('Time (s)')
    axs[2, 1].set_xlabel('Time (s)')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(PLOT_SAVE_PATH)
    print(f"\nTrajectory comparison plot saved to: {PLOT_SAVE_PATH}")
    plt.show()

if __name__ == "__main__":
    evaluate()