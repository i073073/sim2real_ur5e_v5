# src/data_logger.py
import threading
import time
import csv
import os
from datetime import datetime
from src.ur_rtde_client import UR_RTDE_Client

class DataLogger:
    """
    UR 로봇의 관절 데이터를 10Hz로 CSV 파일에 로깅하는 클래스.
    """
    def __init__(self, rtde_client: UR_RTDE_Client, log_dir: str = "logs"):
        """
        로거를 초기화합니다.

        :param rtde_client: 연결된 UR_RTDE_Client 인스턴스
        :param log_dir: 로그 파일이 저장될 디렉토리
        """
        self.client = rtde_client
        self.log_dir = log_dir
        self.is_logging = False
        self.stop_event = threading.Event()
        self.logging_thread = None
        
        # 로그 파일명 설정
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_filename = os.path.join(self.log_dir, f"joint_log_{timestamp}.csv")

    def _logging_worker(self):
        """로깅 작업을 수행하는 스레드의 메인 함수."""
        print(f"Starting logging to {self.log_filename}")
        
        # 로그 디렉토리 생성
        os.makedirs(self.log_dir, exist_ok=True)
        
        with open(self.log_filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # CSV 헤더 작성
            header = ['timestamp', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6']
            writer.writerow(header)
            
            while not self.stop_event.is_set():
                loop_start_time = time.monotonic()
                
                # RTDE 클라이언트로부터 상태 데이터 가져오기
                state = self.client.get_state()
                
                if state and state.get('actual_q'):
                    current_time = state.get('timestamp', time.time())
                    joint_angles = state['actual_q']
                    
                    # 데이터 행 작성
                    row = [current_time] + joint_angles
                    writer.writerow(row)
                
                # 10Hz 주기를 맞추기 위한 대기 시간 계산
                elapsed_time = time.monotonic() - loop_start_time
                sleep_time = (1.0 / 10.0) - elapsed_time
                if sleep_time > 0:
                    time.sleep(sleep_time)
        
        print("Logging stopped.")

    def start(self):
        """로깅 스레드를 시작합니다."""
        if not self.client.is_connected:
            print("Cannot start logging: Robot is not connected.")
            return
        if self.is_logging:
            print("Logger is already running.")
            return
            
        self.is_logging = True
        self.stop_event.clear()
        self.logging_thread = threading.Thread(target=self._logging_worker, daemon=True)
        self.logging_thread.start()

    def stop(self):
        """로깅 스레드를 안전하게 종료합니다."""
        if not self.is_logging:
            return
            
        self.stop_event.set()
        if self.logging_thread:
            self.logging_thread.join() # 스레드가 완전히 종료될 때까지 대기
        self.is_logging = False