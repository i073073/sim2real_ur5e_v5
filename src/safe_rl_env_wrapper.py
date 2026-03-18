# src/safe_rl_env_wrapper.py
import gym
from gym import spaces
import numpy as np
import logging
from typing import Tuple, Dict, Any, Optional

# Custom RL environment
from src.ur5e_rl_env import UR5eRLEnv, SyncUR5eRLEnv
from src.isaac_sim_robot import IsaacSimRobot # For accessing robot properties

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SafeUR5eRLEnv(gym.Wrapper):
    """
    UR5eRLEnv를 래핑하여 안전 제약 조건을 통합하는 Safe RL 환경.
    - 관절 한계 위반에 대한 강력한 페널티
    - (개념적) 충돌 감지 시 페널티 및 에피소드 종료
    """
    def __init__(self, env: UR5eRLEnv, 
                 joint_limit_penalty: float = -500.0,
                 collision_penalty: float = -1000.0,
                 max_joint_vel_penalty: float = -200.0, # Penalty for exceeding max allowed joint velocity
                 max_action_change_penalty: float = -10.0, # Penalty for abrupt action changes
                 collision_detector: Optional[Any] = None # Placeholder for a collision detection service/agent
                ):
        super().__init__(env)
        self.env = env
        self.joint_limit_penalty = joint_limit_penalty
        self.collision_penalty = collision_penalty
        self.max_joint_vel_penalty = max_joint_vel_penalty
        self.max_action_change_penalty = max_action_change_penalty
        self.collision_detector = collision_detector
        
        self.joint_limits_low, self.joint_limits_high = self.env.sim_robot.get_joint_limits()
        self.last_action: Optional[np.ndarray] = None # To track action changes

        logging.info("SafeUR5eRLEnv initialized with safety penalties.")

    def _check_joint_limits_violation(self, joint_positions: np.ndarray) -> bool:
        """관절 한계 위반 여부를 확인합니다."""
        return np.any(joint_positions < self.joint_limits_low) or np.any(joint_positions > self.joint_limits_high)

    def _check_max_joint_velocity_violation(self, joint_velocities: np.ndarray) -> bool:
        """최대 관절 속도 위반 여부를 확인합니다."""
        # Use a slightly higher threshold than action space max velocity to allow some flexibility
        return np.any(np.abs(joint_velocities) > self.env.max_joint_velocity * 1.5)

    def _check_collision(self) -> bool:
        """
        (개념적) 충돌 감지 로직. 실제로는 Isaac Sim의 충돌 이벤트를 구독하거나
        Safety Monitoring Agent로부터 정보를 받아야 합니다.
        """
        if self.collision_detector:
            # Placeholder: In a real system, this would query the collision detector
            # For now, simulate random collision for testing purposes
            return np.random.rand() < 0.001 # Very low chance of random collision
        return False

    async def step(self, action: np.ndarray) -> Tuple[np.ndarray, float, bool, bool, Dict[str, Any]]:
        """
        안전 제약 조건을 적용하여 환경을 한 스텝 진행합니다.
        """
        obs, reward, terminated, truncated, info = await self.env.step(action)
        
        current_joint_positions = info["current_joint_positions"]
        current_joint_velocities = info["current_joint_velocities"]
        
        # 1. 관절 한계 위반 페널티
        if self._check_joint_limits_violation(np.array(current_joint_positions)):
            reward += self.joint_limit_penalty
            terminated = True # 한계 위반 시 에피소드 종료
            logging.warning(f"Joint limit violation detected! Penalty: {self.joint_limit_penalty}")
        
        # 2. 최대 관절 속도 위반 페널티
        if self._check_max_joint_velocity_violation(np.array(current_joint_velocities)):
            reward += self.max_joint_vel_penalty
            logging.warning(f"Max joint velocity violation detected! Penalty: {self.max_joint_vel_penalty}")

        # 3. (개념적) 충돌 페널티
        if self._check_collision():
            reward += self.collision_penalty
            terminated = True # 충돌 시 에피소드 종료
            logging.warning(f"Collision detected! Penalty: {self.collision_penalty}")
            info["is_collision"] = True # Add collision info

        # 4. 행동 변화량 페널티 (부드러운 움직임 유도)
        if self.last_action is not None:
            action_change = np.sum(np.abs(action - self.last_action))
            reward += self.max_action_change_penalty * action_change
        self.last_action = action
        
        return obs, reward, terminated, truncated, info

    async def reset(self, **kwargs) -> Tuple[np.ndarray, Dict[str, Any]]:
        """환경을 리셋하고 안전 관련 상태를 초기화합니다."""
        self.last_action = None
        return await self.env.reset(**kwargs)

# Sync wrapper for SafeUR5eRLEnv
class SyncSafeUR5eRLEnv(gym.Env):
    """
    비동기 SafeUR5eRLEnv를 동기 Gym 환경 인터페이스로 래핑합니다.
    """
    def __init__(self, **kwargs):
        self.env = SafeUR5eRLEnv(UR5eRLEnv(**kwargs)) # Wrap the base env with Safe env
        self.loop = asyncio.get_event_loop()
        if self.loop.is_running():
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
        
        self.loop.run_until_complete(self.env.env._wait_for_sim_init()) # Wait for base sim init
        
        self.observation_space = self.env.observation_space
        self.action_space = self.env.action_space
        self.metadata = self.env.metadata
        self.current_step = 0

    def reset(self, **kwargs):
        self.current_step = 0
        obs, info = self.loop.run_until_complete(self.env.reset(**kwargs))
        return obs, info

    def step(self, action):
        self.current_step += 1
        obs, reward, terminated, truncated, info = self.loop.run_until_complete(self.env.step(action))
        return obs, reward, terminated, truncated, info

    def render(self, mode="human"):
        return self.env.render(mode)

    def close(self):
        self.loop.run_until_complete(self.env.close())
        self.loop.close()

if __name__ == "__main__":
    print("Testing SafeUR5eRLEnv (sync wrapper) with mock robot...")
    # Use a mock IsaacSimRobot to test the safety wrappers without a full sim
    mock_robot_instance = IsaacSimRobot(headless=True)
    asyncio.run(mock_robot_instance.initialize()) # Manually initialize mock robot

    env = SyncSafeUR5eRLEnv(headless_sim=True, sim_robot=mock_robot_instance, # Inject pre-initialized mock robot
                            reward_dist_weight=-10.0, reward_vel_penalty=-0.1, reward_success=100.0, success_threshold=0.05)
    
    obs, info = env.reset()
    print(f"Initial Observation: {np.round(obs, 2)}")
    print(f"Target Joint Positions (degrees): {np.degrees(info['target_joint_positions']).round(2)}")

    for _ in range(200): # Run for more steps to potentially hit limits/collisions
        action = env.action_space.sample() # 무작위 행동
        # Manually induce joint limit violation for testing
        if _ == 50:
            print("--- Inducing joint limit violation ---")
            # For mock robot, directly manipulate its internal state
            env.env.env.sim_robot._mock_joint_positions[0] = env.env.joint_limits_high[0] + 0.1 # Exceed limit
            action = np.zeros(6) # Stop movement to see penalty clearly
        
        obs, reward, terminated, truncated, info = env.step(action)
        print(f"Step {env.current_step}: Reward={reward:.2f}, Done={terminated}, Dist={info['dist_to_target']:.3f}, Collision: {info.get('is_collision', False)}")
        if terminated or truncated:
            print("Episode finished.")
            break
    
    env.close()
    print("Environment test finished.")