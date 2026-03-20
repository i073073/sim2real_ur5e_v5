# src/ur5e_commands.py
from typing import List
from src.rtde_client import RTDEClient

# UR5e 로봇의 관절 한계값 (예시)
JOINT_LIMITS_RAD = [
    [-3.14, 3.14], # Joint 1
    [-3.14, 3.14], # Joint 2
    [-3.14, 3.14], # Joint 3
    [-3.14, 3.14], # Joint 4
    [-3.14, 3.14], # Joint 5
    [-3.14, 3.14]  # Joint 6
]

def check_joint_limits(joint_positions: List[float]) -> bool:
    """관절 위치가 안전 한계 내에 있는지 확인합니다."""
    if len(joint_positions) != 6:
        print("Error: Joint position list must contain 6 values.")
        return False
    for i in range(6):
        if not (JOINT_LIMITS_RAD[i][0] <= joint_positions[i] <= JOINT_LIMITS_RAD[i][1]):
            print(f"Safety Warning: Joint {i+1} position {joint_positions[i]:.2f} rad exceeds limit {JOINT_LIMITS_RAD[i]}.")
            return False
    return True

def moveJ(client: RTDEClient, target_q: List[float], speed: float = 0.5, acceleration: float = 0.5) -> bool:
    """
    관절 공간 이동 (Joint Space Movement).
    로봇의 현재 위치에서 목표 관절 위치(target_q)로 이동합니다.
    """
    if not check_joint_limits(target_q):
        return False
    print(f"Executing moveJ to target_q: {target_q} with speed={speed}, acceleration={acceleration}")
    return client.send_command("moveJ", target_q, speed, acceleration)

def moveL(client: RTDEClient, target_pose: List[float], speed: float = 0.25, acceleration: float = 0.5) -> bool:
    """
    선형 이동 (Linear Movement).
    로봇의 엔드 이펙터가 목표 포즈(target_pose)로 직선 경로를 따라 이동합니다.
    target_pose: [x, y, z, rx, ry, rz] (m, rad)
    """
    print(f"Executing moveL to target_pose: {target_pose} with speed={speed}, acceleration={acceleration}")
    return client.send_command("moveL", target_pose, speed, acceleration)

def speedJ(client: RTDEClient, joint_speeds: List[float], acceleration: float = 0.5, time_limit: float = 1.0) -> bool:
    """
    관절 속도 제어 (Joint Speed Control).
    지정된 시간(time_limit) 동안 관절 속도(joint_speeds)로 로봇을 움직입니다.
    """
    print(f"Executing speedJ with joint_speeds: {joint_speeds} for {time_limit} seconds.")
    return client.send_command("speedJ", joint_speeds, acceleration, time_limit)

def stop_robot(client: RTDEClient):
    """로봇의 움직임을 정지합니다."""
    print("Stopping robot movement.")
    client.send_command("speedJ", [0.0] * 6, 0.5, 0.1) # 속도 0으로 설정하여 정지