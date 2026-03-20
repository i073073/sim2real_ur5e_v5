# src/data_models/robot_state.py
from pydantic import BaseModel, Field
from typing import List

# 1. 로봇 상태 데이터 모델 (RTDE Output 기반)
class RobotState(BaseModel):
    """
    UR5e 로봇의 실시간 상태를 나타내는 데이터 모델.
    시뮬레이터에서 계산된 상태를 Pydantic으로 캡슐화합니다.
    """
    timestamp: float = Field(..., description="데이터 수신 시점의 타임스탬프")
    joint_positions: List[float] = Field(..., description="현재 관절 위치 (rad)", min_items=6, max_items=6)
    joint_velocities: List[float] = Field(..., description="현재 관절 속도 (rad/s)", min_items=6, max_items=6)
    tool_pose: List[float] = Field(..., description="엔드 이펙터의 6D 포즈 (x, y, z, rx, ry, rz)", min_items=6, max_items=6)
    safety_status: int = Field(default=0, description="로봇 안전 상태 코드 (0: OK)")

# 2. 궤적 명령 데이터 모델 (Planning Layer -> Execution Layer)
class TrajectoryCommand(BaseModel):
    """
    Planning Layer에서 생성된 궤적 명령을 나타내는 데이터 모델.
    시뮬레이터가 이 명령을 받아 궤적을 실행합니다.
    """
    command_id: str = Field(..., description="고유 명령 ID")
    waypoints: List[List[float]] = Field(..., description="목표 궤적의 웨이포인트 목록. 각 웨이포인트는 [joint1, joint2, ..., joint6] 형태.")
    speed_factor: float = Field(default=1.0, description="궤적 실행 속도 비율 (0.0 ~ 1.0)")
    collision_check_enabled: bool = Field(default=True, description="실행 전 충돌 검사 활성화 여부")