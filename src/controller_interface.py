# src/controller_interface.py
import numpy as np

class JointController:
    def __init__(self, robot_entity):
        self.robot = robot_entity
        self.dofs = self.robot.n_dofs
        
    def set_joint_positions(self, target_q):
        """
        관절 위치 제어 (Position Control)
        target_q: List of 6 joint angles in radians
        """
        if len(target_q) != 6:
            print("Error: UR5e requires 6 joint values.")
            return

        # Genesis의 제어 API를 사용하여 관절값 입력
        self.robot.set_dofs_position(np.array(target_q))
        
    def get_current_q(self):
        return self.robot.get_dofs_position()

# 시뮬레이션 루프 내 통합 예시:
# controller = JointController(sim.robot)
# target = [0, -1.57, 1.57, -1.57, -1.57, 0] # Home position
# controller.set_joint_positions(target)