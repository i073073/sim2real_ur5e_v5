# src/data_models/world_state.py
from pydantic import BaseModel, Field
from typing import List, Optional

class JointState(BaseModel):
    """로봇 관절 상태 (위치, 속도, 토크)"""
    positions: List[float] = Field(..., description="관절 위치 (라디안)")
    velocities: List[float] = Field(..., description="관절 속도 (rad/s)")
    efforts: List[float] = Field(..., description="관절 토크 (Nm)")

class ObjectState(BaseModel):
    """환경 내 객체 상태"""
    object_id: str = Field(..., description="객체 식별자")
    position: List[float] = Field(..., description="객체 위치 (x, y, z) [m]")
    orientation: List[float] = Field(..., description="객체 방향 (quaternion)")
    is_colliding: bool = Field(False, description="충돌 여부")

class WorldState(BaseModel):
    """현재 환경 및 로봇 상태의 스냅샷"""
    timestamp: float = Field(..., description="데이터 생성 시점 (UNIX timestamp)")
    robot_joint_state: JointState
    detected_objects: List[ObjectState] = Field(default_factory=list)
    is_safe: bool = Field(True, description="시스템 안전 상태")