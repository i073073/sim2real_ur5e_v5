# src/data_models/trajectory_command.py
from pydantic import BaseModel, Field
from typing import List

class Waypoint(BaseModel):
    """경로의 단일 지점"""
    joint_positions: List[float] = Field(..., description="목표 관절 위치 (라디안)")
    time_from_start: float = Field(..., description="경로 시작점으로부터의 시간 (초)")

class TrajectoryCommand(BaseModel):
    """실행 에이전트가 수행할 전체 경로"""
    trajectory_id: str = Field(..., description="경로 식별자")
    waypoints: List[Waypoint] = Field(..., description="경로 지점 목록")
    speed_scale: float = Field(1.0, description="실행 속도 비율 (0.0 ~ 1.0)")