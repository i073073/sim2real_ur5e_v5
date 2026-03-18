# ur5e_sim2real/launch/ur5e_visualization.launch.py
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # 패키지 경로 설정
    ur5e_sim2real_dir = get_package_share_directory('ur5e_sim2real')
    ur_description_dir = get_package_share_directory('ur_description')

    # URDF 파일 경로 (TCP 오프셋 포함)
    robot_description_path = os.path.join(ur5e_sim2real_dir, 'config', 'ur5e_tcp_offset.xacro')

    # 로봇 상태 게시자 노드 (URDF를 읽고 TF를 게시)
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': open(robot_description_path).read()}],
        output='screen'
    )

    # Rviz2 시각화 노드
    rviz_config_file = os.path.join(ur5e_sim2real_dir, 'rviz', 'ur5e_config.rviz')
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_file],
        output='screen'
    )

    # 시뮬레이션 컨트롤러 (로봇 동작을 시뮬레이션하기 위한 가상 조인트 컨트롤러)
    joint_state_publisher_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        output='screen'
    )

    return LaunchDescription([
        robot_state_publisher_node,
        joint_state_publisher_node,
        rviz_node,
    ])