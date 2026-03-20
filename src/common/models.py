# src/common/models.py
from typing import List, Optional, Literal
from pydantic import BaseModel, Field

class Vector3(BaseModel):
    x: float
    y: float
    z: float

class Quaternion(BaseModel):
    x: float
    y: float
    z: float
    w: float

class Pose(BaseModel):
    position: Vector3
    orientation: Quaternion

class ObjectDetectionResult(BaseModel):
    class_name: str = Field(..., description="탐지된 객체의 클래스 이름 (예: 'red_cube')")
    confidence: float = Field(..., ge=0, le=1, description="탐지 신뢰도")
    pose: Pose = Field(..., description="월드 좌표계 기준 객체의 위치 및 자세")

class RobotState(BaseModel):
    is_emergency_stopped: bool
    is_protective_stopped: bool
    is_ready: bool
    joint_positions: List[float]
    tcp_pose: Pose

class BaseTask(BaseModel):
    task_id: str = Field(..., description="고유한 태스크 ID")
    task_type: str = Field(..., description="태스크의 종류")

class FindObjectTask(BaseTask):
    task_type: Literal["FindObject"] = "FindObject"
    object_name: str = Field(..., description="찾고자 하는 객체의 이름 (예: 'red_cube')")

class MoveToPoseTask(BaseTask):
    task_type: Literal["MoveToPose"] = "MoveToPose"
    target_pose: Pose = Field(..., description="로봇 엔드 이펙터의 목표 위치 및 자세")
    speed: float = Field(0.75, description="이동 속도 (0.0 ~ 1.0)")
    acceleration: float = Field(0.5, description="이동 가속도 (0.0 ~ 1.0)")

class Mission(BaseModel):
    mission_id: str
    mission_name: str
    tasks: List[FindObjectTask | MoveToPoseTask]