# src/core/schemas.py
from pydantic import BaseModel, Field, validator
from typing import List, Optional

class RobotPose(BaseModel):
    """TCP Pose (x, y, z, rx, ry, rz)"""
    point: List[float] = Field(..., min_items=6, max_items=6)
    
    @validator('point')
    def check_limits(cls, v):
        # 단순 예시: 작업 반경 제한 (단위: m)
        if abs(v[0]) > 1.0 or abs(v[1]) > 1.0:
            raise ValueError("Target point out of safety reach")
        return v

class JointState(BaseModel):
    """6-DOF Joint positions in radians"""
    joints: List[float] = Field(..., min_items=6, max_items=6)

class RTDECommand(BaseModel):
    """UR5e RTDE Command Packet"""
    command_type: str # 'moveL', 'moveJ', 'stopL', 'servoJ'
    target: List[float]
    velocity: float = 0.25
    acceleration: float = 1.2
    async_execution: bool = False

class RobotStatus(BaseModel):
    """Robot Feedback Data"""
    actual_q: List[float]
    actual_TCP_pose: List[float]
    target_q: List[float]
    is_protective_stopped: bool
    is_emergency_stopped: bool
    output_int_register_0: int # Custom status code