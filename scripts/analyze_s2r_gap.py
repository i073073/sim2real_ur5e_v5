    # scripts/analyze_s2r_gap.py
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.spatial.transform import Rotation
    from dtw import dtw
    import argparse

    class Sim2RealGapAnalyzer:
        def __init__(self, ursim_log_path: str, s2r_log_path: str):
            self.ursim_df = pd.read_json(ursim_log_path, lines=True)
            self.s2r_df = pd.read_json(s2r_log_path, lines=True)
            self.results = {}

        def synchronize_data(self):
            """타임스탬프를 기준으로 두 데이터프레임을 동기화하고 보간합니다."""
            # 시작 시간을 0으로 정규화
            self.ursim_df['time'] = self.ursim_df['timestamp'] - self.ursim_df['timestamp'].iloc[0]
            self.s2r_df['time'] = self.s2r_df['timestamp'] - self.s2r_df['timestamp'].iloc[0]
            
            # s2r의 타임스탬프를 기준으로 ursim 데이터를 선형 보간
            ursim_q_interp = []
            for i in range(6):
                q_interp = np.interp(
                    self.s2r_df['time'], 
                    self.ursim_df['time'], 
                    np.array(self.ursim_df['actual_q'].tolist())[:, i]
                )
                ursim_q_interp.append(q_interp)
            
            self.ursim_q = np.array(ursim_q_interp).T
            self.s2r_q = np.array(self.s2r_df['actual_q'].tolist())
            
            # 데이터 길이 맞추기
            min_len = min(len(self.ursim_q), len(self.s2r_q))
            self.ursim_q = self.ursim_q[:min_len]
            self.s2r_q = self.s2r_q[:min_len]
            self.time_axis = self.s2r_df['time'].iloc[:min_len]

        def calculate_metrics(self):
            """정의된 모든 메트릭을 계산합니다."""
            error = self.s2r_q - self.ursim_q
            
            self.results['J-MAE'] = np.mean(np.abs(error), axis=0)
            self.results['J-RMSE'] = np.sqrt(np.mean(error**2, axis=0))
            self.results['J-MaxAE'] = np.max(np.abs(error), axis=0)
            
            # DTW 계산 (계산량이 많으므로 첫 번째 관절에 대해서만 예시)
            dtw_result = dtw(self.s2r_q[:, 0], self.ursim_q[:, 0], keep_internals=True)
            self.results['J-DTW_J1'] = dtw_result.distance

        def print_report(self):
            """계산된 메트릭을 표 형식으로 출력합니다."""
            print("--- Sim-to-Sim Gap Analysis Report ---")
            for metric, values in self.results.items():
                if isinstance(values, np.ndarray):
                    values_str = " | ".join([f"{v:.5f}" for v in values])
                    print(f"{metric:<10} | {values_str}")
                else:
                    print(f"{metric:<10} | {values:.5f}")

        def plot_results(self, output_path="reports/gap_analysis_plot.png"):
            """오차를 시각화하여 그래프로 저장합니다."""
            error_deg = np.rad2deg(self.s2r_q - self.ursim_q)
            
            fig, axs = plt.subplots(3, 2, figsize=(15, 10), sharex=True)
            fig.suptitle('Joint Angle Error (s2r vs URSim) Over Time', fontsize=16)

            for i in range(6):
                row, col = i // 2, i % 2
                axs[row, col].plot(self.time_axis, error_deg[:, i], label=f'Joint {i+1} Error')
                axs[row, col].set_title(f'Joint {i+1}')
                axs[row, col].set_ylabel('Error (degrees)')
                axs[row, col].grid(True)
                axs[row, col].legend()

            axs[2, 0].set_xlabel('Time (s)')
            axs[2, 1].set_xlabel('Time (s)')
            plt.tight_layout(rect=[0, 0.03, 1, 0.95])
            plt.savefig(output_path)
            print(f"\nAnalysis plot saved to: {output_path}")
            plt.close()

    if __name__ == "__main__":
        parser = argparse.ArgumentParser(description="Analyze the gap between URSim and s2r simulator trajectories.")
        parser.add_argument("ursim_log", type=str, help="Path to the URSim log file (.jsonl).")
        parser.add_argument("s2r_log", type=str, help="Path to the s2r log file (.jsonl).")
        args = parser.parse_args()

        analyzer = Sim2RealGapAnalyzer(ursim_log_path=args.ursim_log, s2r_log_path=args.s2r_log)
        analyzer.synchronize_data()
        analyzer.calculate_metrics()
        analyzer.print_report()
        analyzer.plot_results()
    ```

2.  **결과 검토:**
    -   콘솔에 출력된 메트릭 리포트를 확인한다.
    -   `reports/` 디렉토리에 생성된 오차 그래프(`gap_analysis_plot.png`)를 열어 시간 경과에 따른 오차의 추세와 특정 이벤트(급격한 가감속 등)와의 상관관계를 분석한다.

#### **4단계: 보고 및 후속 조치 (Reporting & Action)**

1.  **결과 보고서 작성:** 분석 결과를 바탕으로 'Sim-to-Sim 갭 분석 보고서'를 작성한다. 보고서에는 다음 내용이 포함되어야 한다.
    -   테스트 개요 및 환경
    -   정량적 분석 결과 (메트릭 표)
    -   시각적 분석 결과 (그래프 및 해석)
    -   오차 원인 추정 (예: 동역학 모델 차이, 제어기 응답 속도 차이 등)
    -   결론 및 프로젝트에 미치는 영향 평가
2.  **Pass/Fail 판정:** 사전에 정의된 허용 오차 기준과 비교하여 테스트의 Pass/Fail 여부를 판정한다.
    -   **Pass/Fail 기준 (예시):**
        -   모든 관절의 `J-MaxAE`는 2.0도(약 0.035 rad)를 초과하지 않아야 한다.
        -   TCP의 `Max Position Error`는 5mm(0.005m)를 초과하지 않아야 한다.
3.  **후속 조치:**
    -   **Fail 시:** 오차 원인을 파악하여 개발팀(물리 엔진, 제어 모델 담당)에 전달하고 s2r 시뮬레이터의 파라미터 튜닝 또는 모델 수정을 요청한다.
    -   **Pass 시:** 현재 Sim-to-Sim 갭 수준을 문서화하고, 해당 갭을 AI 모델 학습 시의 불확실성(uncertainty)으로 고려하도록 AI 모델링팀에 전달한다. (예: 도메인 무작위화 범위 설정에 활용)

--- TASK 10 RAW OUTPUT ---

네, Reinforcement Learning & Optimization Engineer로서 AI Research Scientist와 협력하여 기존 모방 학습 모델을 개선하기 위한 전략을 수립하고 구현하겠습니다. 전략은 명시된 우선순위(강화학습 > 유전 알고리즘 > 베이지안 최적화)를 따르며, 각 단계의 결과물과 최종 보고서를 포함합니다.

### **1. 모델 개선 전략 및 파이프라인 설정**

먼저, 모델 개선을 위한 체계적인 접근 방식을 정의합니다. 우리는 3단계 파이프라인을 통해 점진적으로 모델 성능을 고도화합니다.

1.  **Phase 1: 강화학습(RL)을 통한 미세 조정 (Fine-tuning - 최고 우선순위):**
    *   **목표:** 모방 학습의 한계인 '누적 오차' 문제를 해결합니다. 사전 학습된 모방 모델을 초기 정책으로 사용하여 시뮬레이터 환경과의 상호작용을 통해 스스로 오차를 보정하고 목표 궤적을 더 강건하게 추종하도록 학습시킵니다.
    *   **방법:** DDPG(Deep Deterministic Policy Gradient) 알고리즘을 사용하여 연속적인 관절 공간에서 정책을 미세 조정합니다.

2.  **Phase 2: 베이지안 최적화를 이용한 하이퍼파라미터 튜닝 (2순위):**
    *   **목표:** 강화학습 파이프라인의 성능을 극대화하기 위한 최적의 하이퍼파라미터 조합(학습률, 감가율 등)을 체계적으로 탐색합니다.
    *   **방법:** `Optuna` 라이브러리를 사용하여 RL 학습 과정의 핵심 하이퍼파라미터에 대한 베이지안 최적화를 수행합니다.

3.  **Phase 3: 유전 알고리즘(GA)을 이용한 아키텍처 탐색 (향후 과제):**
    *   **목표:** 현재 사용 중인 MLP 아키텍처가 최선이 아닐 가능성을 탐색합니다. 더 효율적인 네트워크 구조를 발견하여 성능을 근본적으로 향상시킵니다.
    *   **방법:** 본 과업에서는 개념적 제안으로 남겨두며, 향후 신경망 아키텍처 탐색(Neural Architecture Search)의 일환으로 은닉층의 수, 뉴런의 수 등을 유전 알고리즘으로 최적화하는 방안을 고려할 수 있습니다.

이 과업에서는 **Phase 1과 2**를 중심으로 구현을 진행합니다.

#### **1.1. 강화학습 환경 설정**

RL 학습을 위한 하이퍼파라미터를 구성 파일로 관리합니다.
