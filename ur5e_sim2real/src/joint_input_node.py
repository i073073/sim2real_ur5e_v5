# ur5e_sim2real/src/joint_input_node.py
import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from typing import List

class JointInputNode(Node):
    def __init__(self):
        super().__init__('joint_input_node')
        self.publisher_ = self.create_publisher(JointTrajectory, '/joint_trajectory_controller/joint_trajectory', 10)
        self.joint_names = ['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint',
                            'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']
        self.get_logger().info('Joint Input Node initialized. Enter joint positions in radians.')
        self.run_input_loop()

    def run_input_loop(self):
        while rclpy.ok():
            try:
                # 사용자로부터 관절값 입력 받기 (e.g., "0.0 0.0 0.0 0.0 0.0 0.0")
                input_str = input(f"Enter {len(self.joint_names)} joint positions (radians): ")
                joint_values = [float(val) for val in input_str.split()]

                if len(joint_values) != len(self.joint_names):
                    self.get_logger().warn(f"Invalid input count. Expected {len(self.joint_names)} values.")
                    continue

                self.send_joint_command(joint_values)

            except ValueError:
                self.get_logger().error("Invalid input format. Please enter numbers separated by spaces.")
            except KeyboardInterrupt:
                break

    def send_joint_command(self, positions: List[float]):
        trajectory_msg = JointTrajectory()
        trajectory_msg.joint_names = self.joint_names

        point = JointTrajectoryPoint()
        point.positions = positions
        point.time_from_start.sec = 2  # 2초 동안 이동

        trajectory_msg.points.append(point)
        self.publisher_.publish(trajectory_msg)
        self.get_logger().info(f"Published trajectory command: {positions}")

def main(args=None):
    rclpy.init(args=args)
    joint_input_node = JointInputNode()
    rclpy.spin(joint_input_node)
    joint_input_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()