# src/ur_rtde_client.py
import rtde_control
import rtde_receive
import time
import math

class UR_RTDE_Client:
    """
    UR 로봇과의 RTDE 통신을 관리하고, 제어 명령 라이브러리를 제공하는 클라이언트 클래스.
    """
    def __init__(self, hostname: str):
        """
        클라이언트를 초기화합니다.

        :param hostname: 로봇 컨트롤러의 IP 주소 (URSim의 경우 '127.0.0.1')
        """
        self.hostname = hostname
        self.control = None
        self.receive = None
        self.is_connected = False

    def connect(self, ui_recipe: list, logging_recipe: list) -> bool:
        """
        로봇 컨트롤러에 연결을 시도합니다.

        :param ui_recipe: UI 표시용으로 수신할 데이터 필드 리스트
        :param logging_recipe: 로깅용으로 수신할 데이터 필드 리스트
        :return: 연결 성공 시 True, 실패 시 False
        """
        try:
            # 두 레시피를 합쳐서 필요한 모든 변수를 한 번에 설정
            all_variables = list(set(ui_recipe + logging_recipe))
            
            self.control = rtde_control.RTDEControlInterface(self.hostname)
            self.receive = rtde_receive.RTDEReceiveInterface(self.hostname, variables=all_variables)
            self.is_connected = self.receive.isConnected()
            if self.is_connected:
                print(f"Successfully connected to UR robot at {self.hostname}")
            return self.is_connected
        except Exception as e:
            print(f"Error connecting to robot: {e}")
            self.is_connected = False
            return False

    def disconnect(self):
        """로봇과의 연결을 종료합니다."""
        if self.control:
            self.control.disconnect()
        if self.receive:
            self.receive.disconnect()
        self.is_connected = False
        print("Disconnected from UR robot.")

    def get_state(self):
        """현재 로봇의 상태 데이터를 딕셔너리 형태로 반환합니다."""
        if not self.is_connected:
            return None
        try:
            # rtde_receive는 최신 데이터를 내부 버퍼에 가지고 있으며,
            # 속성 접근을 통해 값을 가져올 수 있습니다.
            state = {
                'timestamp': self.receive.getTimestamp(),
                'actual_q': self.receive.getActualQ(),
                'actual_qd': self.receive.getActualQd(),
                'actual_TCP_pose': self.receive.getActualTCPPose(),
                'robot_mode': self.receive.getRobotMode(),
                'safety_status_bits': self.receive.getSafetyStatusBits()
            }
            return state
        except Exception as e:
            print(f"Error getting state: {e}")
            return None

    # --- UR5e 명령어 라이브러리 ---

    def moveJ(self, joints_rad: list, speed: float = 1.05, acceleration: float = 1.4):
        """
        지정된 관절 각도로 로봇을 이동시킵니다. (Joint Space)

        :param joints_rad: 6개 관절의 목표 각도 (라디안 리스트)
        :param speed: 관절 속도 (rad/s)
        :param acceleration: 관절 가속도 (rad/s^2)
        """
        if not self.is_connected:
            print("Not connected. Cannot send moveJ command.")
            return
        print(f"Executing moveJ to {joints_rad}...")
        self.control.moveJ(joints_rad, speed, acceleration)
        print("moveJ command finished.")

    def moveL(self, pose: list, speed: float = 0.25, acceleration: float = 1.2):
        """
        지정된 TCP 포즈로 로봇을 선형 이동시킵니다. (Task Space)

        :param pose: [x, y, z, rx, ry, rz] 형태의 목표 포즈 (m, rad)
        :param speed: TCP 속도 (m/s)
        :param acceleration: TCP 가속도 (m/s^2)
        """
        if not self.is_connected:
            print("Not connected. Cannot send moveL command.")
            return
        print(f"Executing moveL to {pose}...")
        self.control.moveL(pose, speed, acceleration)
        print("moveL command finished.")

    def speedJ(self, joint_speeds: list, acceleration: float = 0.5, time_s: float = 0.5):
        """
        지정된 시간 동안 일정한 관절 속도로 로봇을 움직입니다.

        :param joint_speeds: 6개 관절의 목표 속도 (rad/s 리스트)
        :param acceleration: 관절 가속도 (rad/s^2)
        :param time_s: 속도 제어 지속 시간 (초)
        """
        if not self.is_connected:
            print("Not connected. Cannot send speedJ command.")
            return
        print(f"Executing speedJ with speeds {joint_speeds} for {time_s}s...")
        self.control.speedJ(joint_speeds, acceleration, time_s)
        print("speedJ command finished.")

    def stop(self, acceleration: float = 2.0):
        """로봇의 움직임을 부드럽게 정지시킵니다."""
        if not self.is_connected:
            return
        self.control.speedStop(acceleration)
        print("Stop command sent.")