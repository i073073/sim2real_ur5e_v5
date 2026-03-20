# src/genesis_ur5e_simulator.py
import genesis_sdk as genesis
import numpy as np
import time
from collections import deque

# Helper function for 3D vector rotation using a quaternion
def q_rot(q, v):
    """Rotates vector v by quaternion q."""
    q_w = q[3]
    q_vec = np.array(q[:3])
    a = v * (2.0 * q_w**2 - 1.0)
    b = np.cross(q_vec, v) * q_w * 2.0
    c = q_vec * np.dot(q_vec, v) * 2.0
    return a + b + c

class UR5eSim2RealSimulator:
    """
    Genesis-based simulator for UR5e Sim2Real development.
    
    Features:
    - Loads a UR5e robot from a URDF file.
    - Defines a Tool Center Point (TCP) with a specified offset.
    - Visualizes the TCP and its trajectory with a point trail.
    - Provides a command-line interface to control robot joint angles.
    """
    def __init__(self, urdf_path, tcp_offset_mm=50.0):
        """
        Initializes the simulator, loads the robot, and sets up the environment.
        
        Args:
            urdf_path (str): Path to the UR5e URDF file.
            tcp_offset_mm (float): TCP offset from the end-effector link ('tool0') in millimeters.
        """
        print("Initializing Genesis Simulation Environment...")
        # 1. 시뮬레이터 초기화 및 환경 설정
        self.sim = genesis.Simulation()
        self.sim.connect(mode=genesis.GUI)
        self.sim.set_gravity(0, 0, -9.81)
        self.sim.add_ground_plane()
        self.sim.set_camera_view(distance=2.0, pitch=-30, yaw=45, target_position=[0, 0, 0.5])

        # 2. UR5e URDF 모델 로딩
        print(f"Loading UR5e model from: {urdf_path}")
        # 초기 로봇 위치 및 자세 설정
        start_pos = [0, 0, 0.0]
        start_orn = self.sim.get_quaternion_from_euler([0, 0, 0])
        self.robot_id = self.sim.load_urdf(urdf_path, base_position=start_pos, base_orientation=start_orn, use_fixed_base=True)
        
        # 로봇 관절 정보 가져오기
        self.num_joints = self.sim.get_num_joints(self.robot_id)
        self.joint_indices = [i for i in range(self.num_joints) if self.sim.get_joint_info(self.robot_id, i)['jointType'] != genesis.JOINT_FIXED]
        print(f"UR5e Robot loaded with ID: {self.robot_id}. Controllable joints: {len(self.joint_indices)}")

        # 3. TCP 포인트 정의 및 시각화 설정
        self.end_effector_link_name = 'tool0'
        self.end_effector_link_index = self._find_link_index(self.end_effector_link_name)
        if self.end_effector_link_index is None:
            raise Exception(f"Link '{self.end_effector_link_name}' not found in the URDF model.")
            
        # 50mm offset을 미터 단위로 변환 (tool0의 Z축 방향으로)
        self.tcp_offset_local = np.array([0, 0, tcp_offset_mm / 1000.0])
        print(f"TCP defined with a {tcp_offset_mm}mm offset from '{self.end_effector_link_name}' link.")

        # TCP 위치 시각화를 위한 마커 생성
        self.tcp_marker_id = self.sim.create_visual_marker(
            shape_type=genesis.SHAPE_SPHERE,
            radius=0.02,
            color=[1, 0, 0, 0.8] # Red, slightly transparent
        )
        
        # 4. 포인트 트레일 렌더링 기능 구현
        self.trajectory_trail = deque(maxlen=200) # 최근 200개의 TCP 위치 저장
        self.trail_markers = []
        for _ in range(self.trajectory_trail.maxlen):
            marker = self.sim.create_visual_marker(
                shape_type=genesis.SHAPE_SPHERE,
                radius=0.005,
                color=[0, 1, 1, 0.6] # Cyan, transparent
            )
            self.sim.update_marker_pose(marker, position=[-100, -100, -100], orientation=[0,0,0,1]) # 초기에 숨김
            self.trail_markers.append(marker)

    def _find_link_index(self, link_name):
        """URDF 모델에서 링크 이름으로 인덱스를 찾습니다."""
        for i in range(self.num_joints):
            info = self.sim.get_joint_info(self.robot_id, i)
            if info['linkName'].decode('utf-8') == link_name:
                return i
        return None

    def _update_visualizations(self):
        """TCP 마커와 궤적 트레일을 업데이트합니다."""
        # tool0 링크의 현재 월드 좌표계 기준 자세(pose) 가져오기
        link_state = self.sim.get_link_state(self.robot_id, self.end_effector_link_index)
        link_pos = np.array(link_state['worldLinkFramePosition'])
        link_orn = np.array(link_state['worldLinkFrameOrientation']) # (x, y, z, w)

        # 로컬 TCP 오프셋을 월드 좌표계로 변환
        tcp_pos_world = link_pos + q_rot(link_orn, self.tcp_offset_local)

        # TCP 마커 위치 업데이트
        self.sim.update_marker_pose(self.tcp_marker_id, position=tcp_pos_world.tolist())

        # 궤적 트레일 데이터 추가
        self.trajectory_trail.append(tcp_pos_world)

        # 트레일 마커 렌더링 업데이트
        for i, pos in enumerate(self.trajectory_trail):
            self.sim.update_marker_pose(self.trail_markers[i], position=pos.tolist())

    def set_joint_angles(self, angles):
        """
        로봇의 관절 각도를 설정합니다.
        
        Args:
            angles (list[float]): 6개 관절의 목표 각도 (라디안).
        """
        if len(angles) != len(self.joint_indices):
            print(f"Error: Input angle list must have {len(self.joint_indices)} elements.")
            return
        
        self.sim.set_joint_motor_control(
            body_id=self.robot_id,
            joint_indices=self.joint_indices,
            control_mode=genesis.POSITION_CONTROL,
            target_positions=angles
        )

    def run(self):
        """시뮬레이터의 메인 루프를 실행하고 사용자 입력을 처리합니다."""
        print("\n--- UR5e Simulator Control Interface ---")
        print("Enter 6 joint angles in degrees, separated by spaces (e.g., '0 0 -90 0 90 0').")
        print("Type 'exit' to quit.")

        # 초기 자세 설정
        initial_angles_deg = [0, -90, 90, -90, -90, 0]
        initial_angles_rad = [np.deg2rad(a) for a in initial_angles_deg]
        self.set_joint_angles(initial_angles_rad)
        
        try:
            while True:
                # 사용자 입력 받기
                try:
                    user_input = input("Enter joint angles (deg): ")
                    if user_input.lower() == 'exit':
                        break
                    
                    target_angles_deg = list(map(float, user_input.split()))
                    if len(target_angles_deg) != 6:
                        print("Invalid input. Please provide 6 numbers.")
                        continue
                        
                    target_angles_rad = [np.deg2rad(a) for a in target_angles_deg]
                    self.set_joint_angles(target_angles_rad)

                except ValueError:
                    print("Invalid input. Please enter numbers separated by spaces.")
                    continue

                # 시뮬레이션 스텝 실행 및 시각화 업데이트
                # 입력이 들어올 때마다 1초간 부드럽게 움직이는 것을 보여주기 위해 루프 실행
                for _ in range(240): # 1초 (240Hz 기준)
                    self.sim.step()
                    self._update_visualizations()
                    time.sleep(1./240.)

        finally:
            print("Disconnecting from Genesis simulator.")
            self.sim.disconnect()

if __name__ == '__main__':
    # URDF 파일 경로는 실제 프로젝트 구조에 맞게 수정해야 합니다.
    # 여기서는 가상의 경로를 사용합니다.
    UR5E_URDF_PATH = "assets/ur_description/urdf/ur5e.urdf"
    
    simulator = UR5eSim2RealSimulator(urdf_path=UR5E_URDF_PATH, tcp_offset_mm=50.0)
    simulator.run()