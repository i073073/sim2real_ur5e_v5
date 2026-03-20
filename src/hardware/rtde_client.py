# src/hardware/rtde_client.py
import rtde_control
import rtde_receive
from src.core.schemas import RTDECommand, RobotStatus

class UR5eClient:
    def __init__(self, ip: str):
        self.rtde_c = rtde_control.RTDEControlInterface(ip)
        self.rtde_r = rtde_receive.RTDEReceiveInterface(ip)

    def execute_command(self, cmd: RTDECommand):
        """Pydantic 모델을 받아 실제 로봇 명령으로 변환"""
        if cmd.command_type == "moveL":
            return self.rtde_c.moveL(cmd.target, cmd.velocity, cmd.acceleration, cmd.async_execution)
        elif cmd.command_type == "moveJ":
            return self.rtde_c.moveJ(cmd.target, cmd.velocity, cmd.acceleration, cmd.async_execution)
        
    def get_robot_status(self) -> RobotStatus:
        """실시간 로봇 상태 수집 및 검증"""
        data = {
            "actual_q": self.rtde_r.getActualQ(),
            "actual_TCP_pose": self.rtde_r.getActualTCPPose(),
            "target_q": self.rtde_r.getTargetQ(),
            "is_protective_stopped": self.rtde_r.isProtectiveStopped(),
            "is_emergency_stopped": self.rtde_r.isEmergencyStopped(),
            "output_int_register_0": self.rtde_r.getOutputIntRegister(0)
        }
        return RobotStatus(**data)