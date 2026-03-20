# src/planning/task_planning_agent.py
import json
from typing import List, Dict, Any
from src.data_models.program_data import Waypoint, RobotProgram

# --- VLM Integration Mockup ---
class VLMPerceptionTool:
    """
    VLM을 모방한 도구. 이미지와 텍스트를 입력받아 시각적 추론 결과를 반환합니다.
    """
    def __init__(self, perception_agent_data: Dict[str, Any]):
        self.perception_data = perception_agent_data

    def analyze_scene(self, query: str) -> Dict[str, Any]:
        """
        VLM을 사용하여 텍스트 쿼리에 대한 시각적 분석을 수행합니다.
        Args:
            query: "빨간색 블록의 위치는?" 또는 "가장 가까운 물체는?"
        Returns:
            Dict[str, Any]: 분석 결과 (예: 객체 위치, 관계)
        """
        # Mockup: 실제 VLM API 호출 대신 미리 정의된 데이터 반환
        if "빨간색 블록" in query:
            return {"object": "red_block", "location": [0.3, -0.2, 0.2]}
        elif "파란색 상자" in query:
            return {"object": "blue_box", "location": [0.5, 0.2, 0.2]}
        else:
            return {"object": "unknown"}

# --- CrewAI Task Planning Agent (Modified) ---
class TaskPlanningAgent:
    """
    CrewAI 기반의 고수준 계획 에이전트. VLM을 활용하여 계획을 수립합니다.
    """
    def __init__(self, vlm_tool: VLMPerceptionTool):
        self.vlm_tool = vlm_tool

    def plan_task(self, high_level_goal: str) -> RobotProgram:
        """
        고수준 목표를 입력받아 VLM을 활용하여 세부 작업을 계획합니다.
        """
        print(f"[Task Planning Agent] Received goal: {high_level_goal}")

        # 1. VLM을 사용하여 목표 객체 위치 식별
        vlm_result = self.vlm_tool.analyze_scene(f"Find the target object for '{high_level_goal}'")
        target_location = vlm_result.get("location")

        if target_location:
            print(f"[Task Planning Agent] VLM identified target location: {target_location}")
            # 2. 세부 작업 분해 (CrewAI 워크플로우)
            # 예시: "move to target location" -> "pick up" -> "move to place location"
            waypoints = self._generate_waypoints_from_goal(high_level_goal, target_location)
            return RobotProgram(program_name="VLM_Planned_Task", waypoints=waypoints)
        else:
            print("[Task Planning Agent] VLM failed to identify target object. Aborting plan.")
            return RobotProgram(program_name="VLM_Planned_Task", waypoints=[])

    def _generate_waypoints_from_goal(self, goal: str, target_location: List[float]) -> List[Waypoint]:
        """VLM 결과를 기반으로 웨이포인트 생성 (Mockup)"""
        # ... (CrewAI의 LLM 추론 로직) ...
        # 예시: target_location을 기반으로 픽업 웨이포인트 생성
        pick_waypoint = Waypoint(
            id="wp_pick",
            command_type="moveL",
            coordinates=target_location,
            description="VLM identified pick location"
        )
        return [pick_waypoint]