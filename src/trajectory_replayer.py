# src/trajectory_replayer.py
import json
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from src.genesis_ur5e_simulator import UR5eSim2RealSimulator

class TrajectoryReplayer:
    """
    URSim에서 수집한 궤적 데이터를 s2r 시뮬레이터에서 재생하고,
    두 시뮬레이터 간의 동작 차이를 분석합니다.
    """
    def __init__(self, simulator: UR5eSim2RealSimulator):
        """
        TrajectoryReplayer를 초기화합니다.

        :param simulator: 제어 및 데이터 수집에 사용될 UR5eSim2RealSimulator 인스턴스.
        """
        self.sim = simulator
        self.ursim_trajectory = None
        self.s2r_trajectory = []

    def load_trajectory(self, jsonl_path: str):
        """
        URSim에서 로깅된 .jsonl 궤적 파일을 로드합니다.

        :param jsonl_path: 로드할 데이터 파일의 경로.
        """
        print(f"Loading URSim trajectory from: {jsonl_path}")
        try:
            self.ursim_trajectory = pd.read_json(jsonl_path, lines=True)
            print(f"Successfully loaded {len(self.ursim_trajectory)} data points.")
        except Exception as e:
            print(f"Error loading trajectory file: {e}")
            raise

    def _visualize_ursim_trajectory(self):
        """
        s2r 시뮬레이터에 URSim 궤적을 시각적으로 표시합니다.
        이는 재생될 동작의 'Ground Truth' 역할을 합니다.
        """
        if self.ursim_trajectory is None:
            return

        print("Visualizing ground truth (URSim) trajectory in s2r simulator...")
        # 궤적의 각 포인트에 대해 반투명 녹색 구 마커 생성
        for index, row in self.ursim_trajectory.iterrows():
            # 10개 중 1개만 표시하여 시각적 혼잡도 감소
            if index % 10 == 0:
                # 임시로 로봇을 해당 위치로 이동시켜 월드 좌표를 계산
                self.sim.set_joint_angles(row['actual_q'])
                self.sim.sim.step() # 물리 엔진 업데이트
                link_state = self.sim.sim.get_link_state(self.sim.robot_id, self.sim.end_effector_link_index)
                tcp_pos = np.array(link_state['worldLinkFramePosition']) + self.sim.q_rot(link_state['worldLinkFrameOrientation'], self.sim.tcp_offset_local)

                self.sim.sim.create_visual_marker(
                    shape_type=self.sim.sim.SHAPE_SPHERE,
                    radius=0.008,
                    color=[0, 1, 0, 0.3], # Transparent Green
                    position=tcp_pos.tolist()
                )
        print("Ground truth visualization complete.")

    def run_replay(self):
        """
        로드된 궤적을 s2r 시뮬레이터에서 재생하고, 실제 동작 데이터를 기록합니다.
        """
        if self.ursim_trajectory is None:
            print("No trajectory loaded. Please load a trajectory first.")
            return

        print("\n--- Starting Trajectory Replay in s2r Simulator ---")
        self.s2r_trajectory = []
        
        # 1. 비교를 위해 URSim 궤적을 시각화
        self._visualize_ursim_trajectory()

        # 2. 로봇을 궤적의 시작점으로 이동
        initial_q = self.ursim_trajectory.iloc[0]['actual_q']
        self.sim.set_joint_angles(initial_q)
        for _ in range(120): # 안정화 시간
            self.sim.sim.step()
            time.sleep(1./240.)

        # 3. 궤적 재생 루프
        start_time = time.monotonic()
        for index, row in self.ursim_trajectory.iterrows():
            target_q = row['actual_q']
            
            # s2r 시뮬레이터에 목표 관절각 설정 (명령)
            self.sim.set_joint_angles(target_q)
            
            # 시뮬레이션 스텝 실행
            self.sim.sim.step()
            
            # s2r 시뮬레이터의 실제 관절각 측정 (결과)
            joint_states = self.sim.sim.get_joint_states(self.sim.robot_id, self.sim.joint_indices)
            current_s2r_q = [state['jointPosition'] for state in joint_states]
            self.s2r_trajectory.append(current_s2r_q)
            
            # TCP 궤적 시각화 업데이트
            self.sim._update_visualizations()
            
            # 10Hz 주기에 맞춰 대기
            time.sleep(1./10.)

        end_time = time.monotonic()
        print(f"--- Replay Finished. Duration: {end_time - start_time:.2f} seconds ---")

    def analyze_and_plot(self, output_path="reports/trajectory_error_plot.png"):
        """
        URSim 궤적과 s2r 시뮬레이터 궤적 간의 오차를 분석하고 그래프로 출력합니다.
        """
        if not self.s2r_trajectory:
            print("No s2r trajectory data to analyze.")
            return

        # NumPy 배열로 변환
        ursim_q = np.array(self.ursim_trajectory['actual_q'].tolist())
        s2r_q = np.array(self.s2r_trajectory)
        
        # 데이터 길이 맞추기
        min_len = min(len(ursim_q), len(s2r_q))
        ursim_q = ursim_q[:min_len]
        s2r_q = s2r_q[:min_len]

        # 오차 계산 (라디안)
        error_rad = s2r_q - ursim_q
        
        # 통계 계산
        mae = np.mean(np.abs(error_rad), axis=0)
        rmse = np.sqrt(np.mean(error_rad**2, axis=0))

        print("\n--- Sim-to-Sim Trajectory Error Analysis ---")
        print("Metric      | J1      | J2      | J3      | J4      | J5      | J6")
        print("------------|---------|---------|---------|---------|---------|---------")
        print(f"MAE (rad)   | {mae[0]:.5f} | {mae[1]:.5f} | {mae[2]:.5f} | {mae[3]:.5f} | {mae[4]:.5f} | {mae[5]:.5f}")
        print(f"RMSE (rad)  | {rmse[0]:.5f} | {rmse[1]:.5f} | {rmse[2]:.5f} | {rmse[3]:.5f} | {rmse[4]:.5f} | {rmse[5]:.5f}")

        # 그래프 생성
        time_axis = self.ursim_trajectory['timestamp'].iloc[:min_len]
        time_axis -= time_axis.iloc[0] # 시작 시간을 0으로 정규화

        fig, axs = plt.subplots(6, 1, figsize=(12, 15), sharex=True)
        fig.suptitle('Sim-to-Sim Joint Angle Error (s2r vs URSim)', fontsize=16)

        for i in range(6):
            axs[i].plot(time_axis, np.rad2deg(error_rad[:, i]), label=f'Joint {i+1} Error')
            axs[i].set_ylabel('Error (degrees)')
            axs[i].grid(True)
            axs[i].legend()

        axs[5].set_xlabel('Time (s)')
        plt.tight_layout(rect=[0, 0.03, 1, 0.96])
        
        # 그래프 파일 저장
        plt.savefig(output_path)
        print(f"\nAnalysis plot saved to: {output_path}")
        plt.show()