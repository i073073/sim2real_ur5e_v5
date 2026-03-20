# src/genesis_simulator.py
import time
import yaml
import numpy as np
from typing import List, Dict
from data_models.robot_state import RobotState, TrajectoryCommand

# --- Genesis Simulator Core Components (Mockup) ---
# 실제 Genesis 엔진의 API를 모방하여 구현합니다.
class GenesisEngine:
    """
    Genesis 시뮬레이션 엔진의 핵심 기능을 모방한 클래스.
    URDF 로딩, 물리 시뮬레이션, 렌더링을 담당합니다.
    """
    def __init__(self, config: Dict):
        self.config = config
        self.robot_model = None
        self.tcp_offset = np.array([config['tcp_offset']['x'],
                                    config['tcp_offset']['y'],
                                    config['tcp_offset']['z']]) / 1000.0 # mm -> m 변환
        self.joint_positions = config['robot_model']['initial_joint_positions']
        self.tcp_history = []
        self.visualization_enabled = True

    def load_urdf(self, urdf_path: str):
        """URDF 파일을 로드하고 로봇 모델을 초기화합니다."""
        print(f"[Genesis] Loading URDF model from: {urdf_path}")
        # 실제 시뮬레이터 API 호출 (예: pybullet.loadURDF, mujoco.mj_loadXML)
        # 여기서는 로딩 성공을 가정하고 로봇 모델 객체를 생성합니다.
        self.robot_model = {"name": self.config['robot_model']['name'], "num_joints": 6}
        print(f"[Genesis] Model '{self.robot_model['name']}' loaded successfully.")

    def set_joint_positions(self, joint_angles: List[float]):
        """로봇 관절 위치를 설정하고 시뮬레이션 상태를 업데이트합니다."""
        if len(joint_angles) != self.robot_model['num_joints']:
            print(f"[Warning] Invalid joint angle count: expected {self.robot_model['num_joints']}, got {len(joint_angles)}")
            return
        self.joint_positions = joint_angles
        # 실제 시뮬레이터 물리 엔진 업데이트 (예: pybullet.resetJointStates)
        # print(f"[Genesis] Joint positions updated: {self.joint_positions}")

    def get_end_effector_pose(self) -> List[float]:
        """현재 관절 위치를 기반으로 엔드 이펙터의 6D 포즈를 계산합니다."""
        # 실제 시뮬레이터의 포워드 키네마틱스(FK) 계산 API 호출 (예: pybullet.getLinkState)
        # 여기서는 단순화를 위해 가상의 FK 계산을 수행합니다.
        # (x, y, z, rx, ry, rz)
        # 예시: 관절값에 따라 엔드 이펙터 위치가 변한다고 가정
        x = np.cos(self.joint_positions[0]) * 0.5 + np.sin(self.joint_positions[1]) * 0.2
        y = np.sin(self.joint_positions[0]) * 0.5
        z = 0.5 + np.cos(self.joint_positions[1]) * 0.3 + np.sin(self.joint_positions[2]) * 0.1
        rx, ry, rz = self.joint_positions[3], self.joint_positions[4], self.joint_positions[5]
        return [x, y, z, rx, ry, rz]

    def calculate_tcp_pose(self) -> List[float]:
        """엔드 이펙터 포즈에 TCP 오프셋을 적용하여 실제 TCP 포즈를 계산합니다."""
        ee_pose = self.get_end_effector_pose()
        ee_position = np.array(ee_pose[:3])
        # TCP 오프셋 적용 (Sim2Real 갭 반영)
        tcp_position = ee_position + self.tcp_offset
        return list(tcp_position) + ee_pose[3:]

    def render_visualization(self):
        """시뮬레이션 환경을 렌더링하고 TCP 궤적을 시각화합니다."""
        if not self.visualization_enabled:
            return

        # 1. TCP 마커 렌더링 (현재 TCP 위치)
        tcp_pose = self.calculate_tcp_pose()
        # print(f"[Render] TCP Position: {tcp_pose[:3]}")
        # 실제 렌더링 API 호출 (예: OpenGL, Unity, Unreal Engine)
        # draw_marker(tcp_pose[:3], color=self.config['visualization']['tcp_marker_color'])

        # 2. 포인트 트레일 렌더링 (궤적 시각화)
        self.tcp_history.append(tcp_pose[:3])
        if len(self.tcp_history) > self.config['visualization']['trail_length']:
            self.tcp_history.pop(0)

        # draw_line_strip(self.tcp_history, color=self.config['visualization']['trail_color'])

    def step_simulation(self):
        """시뮬레이션 한 스텝 진행."""
        # 물리 엔진 업데이트 (가속도, 속도, 위치 계산)
        # ...
        self.render_visualization()

# --- Main Simulation Loop ---
def main():
    # 1. 설정 파일 로드
    with open("config/ur5e_sim_config.yaml", 'r') as f:
        config = yaml.safe_load(f)

    # 2. Genesis 시뮬레이터 초기화
    sim_engine = GenesisEngine(config)
    sim_engine.load_urdf(config['robot_model']['urdf_path'])

    # 3. 관절값 입력 인터페이스 및 궤적 시뮬레이션
    print("\n--- UR5e Simulator Control Interface ---")
    print("Enter joint angles (6 values separated by space) or 'q' to quit.")
    print(f"Initial joint positions: {config['robot_model']['initial_joint_positions']}")

    # 궤적 시뮬레이션을 위한 예시 웨이포인트 정의
    # (Planning Layer에서 TrajectoryCommand로 전달되는 데이터)
    example_trajectory = [
        [0.0, -1.57, 1.57, -1.57, -1.57, 0.0], # Home position
        [0.5, -1.0, 1.0, -1.0, -1.0, 0.0],     # Waypoint 1
        [-0.5, -1.2, 1.2, -1.2, -1.2, 0.0],    # Waypoint 2
        [0.0, -1.57, 1.57, -1.57, -1.57, 0.0]  # Back to home
    ]

    # 4. 시뮬레이션 루프
    step_count = 0
    while True:
        # 4.1. 관절값 입력 인터페이스 (수동 입력 또는 자동 궤적 실행)
        if step_count < len(example_trajectory) * 100: # 궤적 실행 (100 steps per waypoint)
            waypoint_index = int(step_count / 100) % len(example_trajectory)
            target_joint_angles = example_trajectory[waypoint_index]
            # 실제로는 보간(interpolation)을 통해 부드러운 움직임을 구현합니다.
            # 여기서는 단순화를 위해 웨이포인트로 바로 이동합니다.
            sim_engine.set_joint_positions(target_joint_angles)
        else:
            # 궤적 실행 완료 후 수동 입력 대기
            user_input = input("Enter joint angles (rad): ")
            if user_input.lower() == 'q':
                break
            try:
                joint_angles = [float(x) for x in user_input.split()]
                sim_engine.set_joint_positions(joint_angles)
            except ValueError:
                print("Invalid input format. Please enter 6 numbers.")
                continue

        # 4.2. 시뮬레이션 스텝 진행 및 렌더링
        sim_engine.step_simulation()

        # 4.3. Pydantic 데이터 모델로 상태 출력 (State Estimation Agent로 전송)
        current_state = RobotState(
            timestamp=time.time(),
            joint_positions=sim_engine.joint_positions,
            joint_velocities=[0.0] * 6, # 시뮬레이션에서 계산된 속도 (여기서는 0으로 가정)
            tool_pose=sim_engine.calculate_tcp_pose(),
            safety_status=0
        )
        # print(f"State Feedback: {current_state.json(indent=2)}")

        time.sleep(0.01) # 시뮬레이션 속도 조절 (100Hz)
        step_count += 1

if __name__ == "__main__":
    main()