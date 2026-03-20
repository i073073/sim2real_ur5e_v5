# src/rtde_client.py
import rtde_receive
import rtde_control
import time
import threading
import csv
from typing import List, Optional, Dict, Any

# RTDE 통신 설정
ROBOT_IP = "127.0.0.1"  # URSim의 기본 IP 주소
RTDE_PORT = 30004

# RTDE Output Recipe (로봇 -> 시스템)
# 로봇의 현재 상태를 수신하기 위한 데이터 항목 정의
# actual_q: 관절 위치 (rad), actual_qd: 관절 속도 (rad/s), actual_TCP_pose: TCP 포즈 (x, y, z, rx, ry, rz)
OUTPUT_RECIPE = [
    "actual_q",
    "actual_qd",
    "actual_TCP_pose",
    "robot_status",
    "safety_status"
]

# RTDE Input Recipe (시스템 -> 로봇)
# 로봇에게 명령을 전송하기 위한 데이터 항목 정의
# input_q: 관절 위치 명령 (moveJ, moveL), speed_q: 관절 속도 명령 (speedJ)
INPUT_RECIPE = [
    "input_q",
    "speed_q"
]

class RTDEClient:
    """
    UR5e 로봇과의 RTDE 통신을 관리하는 클라이언트 클래스.
    실시간 데이터 수신 및 명령 전송 기능을 제공합니다.
    """
    def __init__(self, robot_ip: str = ROBOT_IP):
        self.robot_ip = robot_ip
        self.rtde_r: Optional[rtde_receive.RTDEReceiveInterface] = None
        self.rtde_c: Optional[rtde_control.RTDEControlInterface] = None
        self.is_connected = False
        self.latest_state: Dict[str, Any] = {}
        self.logging_thread: Optional[threading.Thread] = None
        self.logging_active = False
        self.log_file_path = "data/robot_log.csv"
        self.log_frequency = 10 # Hz

    def connect(self) -> bool:
        """RTDE 인터페이스에 연결합니다."""
        try:
            print(f"Connecting to UR5e at {self.robot_ip}...")
            self.rtde_r = rtde_receive.RTDEReceiveInterface(self.robot_ip, RTDE_PORT, variables=OUTPUT_RECIPE)
            self.rtde_c = rtde_control.RTDEControlInterface(self.robot_ip)
            self.is_connected = True
            print("RTDE connection established successfully.")
            return True
        except Exception as e:
            print(f"Failed to connect to RTDE: {e}")
            self.is_connected = False
            return False

    def disconnect(self):
        """RTDE 인터페이스 연결을 해제합니다."""
        if self.is_connected:
            self.stop_logging()
            self.rtde_r.disconnect()
            self.rtde_c.disconnect()
            self.is_connected = False
            print("RTDE connection disconnected.")

    def start_logging(self):
        """10Hz 관절값 로깅 스레드를 시작합니다."""
        if not self.is_connected:
            print("Cannot start logging: Not connected to robot.")
            return

        if self.logging_thread and self.logging_thread.is_alive():
            print("Logging thread already running.")
            return

        self.logging_active = True
        self.logging_thread = threading.Thread(target=self._logging_loop, daemon=True)
        self.logging_thread.start()
        print(f"Started 10Hz logging to {self.log_file_path}")

    def stop_logging(self):
        """로깅 스레드를 중지합니다."""
        self.logging_active = False
        if self.logging_thread and self.logging_thread.is_alive():
            self.logging_thread.join()
            print("Logging thread stopped.")

    def _logging_loop(self):
        """로봇 상태를 주기적으로 수신하고 로깅하는 내부 스레드 함수."""
        with open(self.log_file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            # CSV 헤더 작성
            header = ["timestamp"] + OUTPUT_RECIPE
            writer.writerow(header)

            while self.logging_active:
                start_time = time.time()
                try:
                    # RTDE 데이터 수신
                    state = self.rtde_r.get and self.rtde_r.get()
                    if state:
                        # Pydantic 모델로 변환 (여기서는 Dict로 처리)
                        self.latest_state = {key: getattr(state, key) for key in OUTPUT_RECIPE}
                        self.latest_state["timestamp"] = start_time

                        # 10Hz 로깅 (100ms 간격)
                        log_data = [start_time] + [self.latest_state[key] for key in OUTPUT_RECIPE]
                        writer.writerow(log_data)

                except Exception as e:
                    print(f"Error during RTDE data reception: {e}")

                # 로깅 주파수 제어 (10Hz = 100ms)
                elapsed_time = time.time() - start_time
                sleep_time = max(0, 1.0 / self.log_frequency - elapsed_time)
                time.sleep(sleep_time)

    def get_latest_state(self) -> Dict[str, Any]:
        """가장 최근에 수신된 로봇 상태를 반환합니다."""
        return self.latest_state

    def send_command(self, command_type: str, *args, **kwargs) -> bool:
        """로봇에게 명령을 전송합니다."""
        if not self.is_connected:
            print("Cannot send command: Not connected to robot.")
            return False

        try:
            if command_type == "moveJ":
                # moveJ(q, speed, acceleration)
                self.rtde_c.moveJ(*args)
            elif command_type == "moveL":
                # moveL(pose, speed, acceleration)
                self.rtde_c.moveL(*args)
            elif command_type == "speedJ":
                # speedJ(qd, acceleration, time)
                self.rtde_c.speedJ(*args)
            else:
                print(f"Unknown command type: {command_type}")
                return False
            return True
        except Exception as e:
            print(f"Error sending command {command_type}: {e}")
            return False
