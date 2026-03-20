# src/agents/crew_setup.py
from crewai import Agent, Task, Crew, Process
from crewai_tools import BaseTool

# 로봇 제어 시스템의 특정 기능을 위한 맞춤형 도구 정의 (예시)
# 실제 구현 시, 이 도구들은 ROS 서비스 클라이언트나 액션 클라이언트를 호출하게 됨
class RobotVisionTool(BaseTool):
    name: str = "Robot Vision Tool"
    description: str = "Scans the environment to find objects of a specific color. Returns the object's coordinates."

    def _run(self, color: str) -> str:
        # In a real scenario, this would call the Perception Agent's service.
        print(f"--- [VisionTool] Scanning for a {color} object...")
        # Mock response for PoC
        if color.lower() == "red":
            return "Object found at coordinates: [x=1.5, y=2.0, z=0.5]"
        else:
            return "Object not found."

class RobotNavigationTool(BaseTool):
    name: str = "Robot Navigation Tool"
    description: str = "Navigates the robot to the given coordinates [x, y, z]."

    def _run(self, coordinates: str) -> str:
        # In a real scenario, this would call the Navigation Agent's service via ROS.
        print(f"--- [NavigationTool] Moving robot to {coordinates}...")
        return f"Successfully navigated to {coordinates}."

# 1. 에이전트 정의
vision_specialist = Agent(
    role='Vision Perception Specialist',
    goal='Analyze the visual feed to locate specified objects in the environment.',
    backstory='An expert AI trained on millions of environmental images, capable of identifying objects with high precision.',
    tools=[RobotVisionTool()],
    verbose=True,
    allow_delegation=False
)

navigation_planner = Agent(
    role='Pathfinding and Navigation Planner',
    goal='Receive target coordinates and command the robot to move to that location safely.',
    backstory='A meticulous planner that calculates the most efficient and safest path, avoiding any obstacles.',
    tools=[RobotNavigationTool()],
    verbose=True,
    allow_delegation=False
)

# 2. 태스크 정의
find_object_task = Task(
    description='Find the red cube in the current operational area.',
    expected_output='The 3D coordinates of the red cube. Example: "[x=1.5, y=2.0, z=0.5]"',
    agent=vision_specialist
)

move_to_object_task = Task(
    description='Navigate the robot to the coordinates of the object found in the previous task.',
    expected_output='A confirmation message that the robot has arrived at the destination.',
    agent=navigation_planner,
    context=[find_object_task] # 이전 태스크의 결과(context)를 사용
)

# 3. 크루(Crew) 구성 및 실행
robot_control_crew = Crew(
    agents=[vision_specialist, navigation_planner],
    tasks=[find_object_task, move_to_object_task],
    process=Process.sequential,
    verbose=2
)

# --- 크루 실행 ---
# result = robot_control_crew.kickoff()
# print("######################")
# print("Crew execution result:")
# print(result)
