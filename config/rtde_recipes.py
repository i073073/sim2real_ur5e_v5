# config/rtde_recipes.py
"""
UR 로봇과의 RTDE 통신에서 수신할 데이터 레시피를 정의합니다.
"""

# 10Hz 관절값 로깅에 필요한 최소한의 데이터 필드
# 'actual_q'는 6개 관절의 실제 각도(라디안)를 담고 있는 VECTOR6D입니다.
LOGGING_STATE_RECIPE = [
    'actual_q'
]

# Streamlit UI에 로봇의 상세 상태를 표시하기 위한 데이터 필드
UI_STATE_RECIPE = [
    'timestamp',          # 타임스탬프 (Double)
    'actual_q',           # 실제 관절 위치 (Vector6D)
    'actual_qd',          # 실제 관절 속도 (Vector6D)
    'actual_TCP_pose',    # 실제 TCP 위치 및 자세 (Vector6D: x, y, z, rx, ry, rz)
    'robot_mode',         # 로봇 모드 (Int32)
    'safety_status_bits'  # 안전 상태 비트 (UInt32)
]