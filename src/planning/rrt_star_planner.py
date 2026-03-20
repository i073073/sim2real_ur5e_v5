# src/planning/rrt_star_planner.py
import numpy as np
import random
from typing import List, Tuple, Optional

# --- RRT* Configuration ---
MAX_ITERATIONS = 1000
STEP_SIZE = 0.1 # 노드 확장 거리
GOAL_TOLERANCE = 0.05 # 목표 도달 허용 오차 (m)
REWIRE_RADIUS = 0.5 # 재연결 탐색 반경 (m)

class RRTStarPlanner:
    """
    RRT* (Rapidly-exploring Random Tree Star) 알고리즘 구현.
    최적의 경로를 탐색하고 충돌을 회피합니다.
    """
    def __init__(self, start_state: List[float], goal_state: List[float], obstacles: List[Dict[str, Any]]):
        self.start_state = np.array(start_state)
        self.goal_state = np.array(goal_state)
        self.obstacles = obstacles
        self.nodes = {0: {"state": self.start_state, "parent": None, "cost": 0.0}}
        self.node_count = 1

    def plan_path(self) -> Optional[List[List[float]]]:
        """RRT* 알고리즘을 실행하여 최적 경로를 탐색합니다."""
        for _ in range(MAX_ITERATIONS):
            # 1. 무작위 샘플링 (Random Sampling)
            random_state = self._sample_random_state()

            # 2. 가장 가까운 노드 찾기 (Nearest Neighbor)
            nearest_node_id = self._find_nearest_node(random_state)
            nearest_state = self.nodes[nearest_node_id]["state"]

            # 3. 새로운 노드 확장 (Steer)
            new_state = self._steer(nearest_state, random_state)

            # 4. 충돌 검사 (Collision Check)
            if not self._check_collision(nearest_state, new_state):
                # 5. 최적 부모 노드 선택 (Choose Parent)
                best_parent_id, min_cost = self._choose_best_parent(nearest_node_id, new_state)

                # 6. 새로운 노드 추가
                new_node_id = self.node_count
                self.nodes[new_node_id] = {"state": new_state, "parent": best_parent_id, "cost": min_cost}
                self.node_count += 1

                # 7. 재연결 (Rewire)
                self._rewire(new_node_id)

                # 8. 목표 도달 검사
                if self._check_goal_reached(new_state):
                    return self._reconstruct_path(new_node_id)

        return None # 경로 탐색 실패

    def _sample_random_state(self) -> np.ndarray:
        """탐색 공간 내에서 무작위 상태를 샘플링합니다."""
        # UR5e 관절 공간 (6D) 또는 TCP 공간 (3D)
        # 여기서는 6D 관절 공간을 가정합니다.
        return np.random.uniform(-3.14, 3.14, size=6)

    def _find_nearest_node(self, state: np.ndarray) -> int:
        """현재 상태에서 가장 가까운 노드를 찾습니다."""
        min_distance = float('inf')
        nearest_id = -1
        for node_id, node in self.nodes.items():
            distance = np.linalg.norm(node["state"] - state)
            if distance < min_distance:
                min_distance = distance
                nearest_id = node_id
        return nearest_id

    def _steer(self, from_state: np.ndarray, to_state: np.ndarray) -> np.ndarray:
        """from_state에서 to_state 방향으로 STEP_SIZE만큼 이동한 새로운 상태를 계산합니다."""
        direction = to_state - from_state
        distance = np.linalg.norm(direction)
        if distance > STEP_SIZE:
            new_state = from_state + direction / distance * STEP_SIZE
        else:
            new_state = to_state
        return new_state

    def _check_collision(self, state1: np.ndarray, state2: np.ndarray) -> bool:
        """두 상태 사이의 경로에 충돌이 있는지 검사합니다."""
        # 실제로는 MoveIt!의 충돌 검사 API를 사용합니다.
        # 여기서는 단순화를 위해 항상 충돌이 없다고 가정합니다.
        return False

    def _choose_best_parent(self, nearest_node_id: int, new_state: np.ndarray) -> Tuple[int, float]:
        """새로운 노드의 부모 노드를 최적화합니다."""
        min_cost = self.nodes[nearest_node_id]["cost"] + np.linalg.norm(new_state - self.nodes[nearest_node_id]["state"])
        best_parent_id = nearest_node_id

        for node_id, node in self.nodes.items():
            if node_id != nearest_node_id and np.linalg.norm(node["state"] - new_state) < REWIRE_RADIUS:
                cost = node["cost"] + np.linalg.norm(new_state - node["state"])
                if cost < min_cost:
                    min_cost = cost
                    best_parent_id = node_id
        return best_parent_id, min_cost

    def _rewire(self, new_node_id: int):
        """새로운 노드를 기준으로 주변 노드의 부모를 재연결하여 최적화합니다."""
        new_node = self.nodes[new_node_id]
        for node_id, node in self.nodes.items():
            if node_id != new_node_id and np.linalg.norm(node["state"] - new_node["state"]) < REWIRE_RADIUS:
                new_cost = new_node["cost"] + np.linalg.norm(node["state"] - new_node["state"])
                if new_cost < node["cost"]:
                    node["parent"] = new_node_id
                    node["cost"] = new_cost

    def _check_goal_reached(self, state: np.ndarray) -> bool:
        """목표 상태에 도달했는지 검사합니다."""
        return np.linalg.norm(state - self.goal_state) < GOAL_TOLERANCE

    def _reconstruct_path(self, end_node_id: int) -> List[List[float]]:
        """최적 경로를 재구성합니다."""
        path = []
        current_id = end_node_id
        while current_id is not None:
            path.append(self.nodes[current_id]["state"].tolist())
            current_id = self.nodes[current_id]["parent"]
        return path[::-1] # 역순으로 반환

# --- Example Usage ---
# if __name__ == "__main__":
#     start_state = [0.0, -1.57, 1.57, -1.57, -1.57, 0.0]
#     goal_state = [0.5, -1.0, 1.0, -1.0, -1.0, 0.0]
#     planner = RRTStarPlanner(start_state, goal_state, obstacles=[])
#     path = planner.plan_path()
#     if path:
#         print("Path found successfully:")
#         print(path)
#     else:
#         print("Failed to find path.")