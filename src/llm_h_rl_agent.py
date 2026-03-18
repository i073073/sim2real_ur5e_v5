# src/llm_h_rl_agent.py
import logging
from typing import List, Dict, Any, Tuple
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from stable_baselines3 import PPO # Assuming PPO is used for low-level skills
import numpy as np
import os

# Custom data models and environment (from previous tasks)
from src.data_models import RobotActionCommand, ProgramPointType
from src.ur5e_rl_env import SyncUR5eRLEnv # For executing low-level skills

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Define Tools for LLM to interact with RL Skills ---
class RLSkillTools:
    def __init__(self, skill_policies: Dict[str, PPO], sim_env: SyncUR5eRLEnv):
        self.skill_policies = skill_policies # Dictionary of skill_name: PPO_policy
        self.sim_env = sim_env # The simulation environment to execute skills

    def execute_joint_move_skill(self, target_joint_positions: List[float], skill_policy_name: str = "joint_move_policy") -> Dict[str, Any]:
        """
        Executes a low-level RL policy to move the robot to target joint positions.
        Args:
            target_joint_positions: List of 6 joint positions in radians.
            skill_policy_name: The name of the trained RL policy for this skill.
        Returns:
            Dict: Result of the skill execution (e.g., success, final_dist, duration).
        """
        if skill_policy_name not in self.skill_policies:
            logging.error(f"RL policy '{skill_policy_name}' not found.")
            return {"success": False, "message": f"Policy '{skill_policy_name}' not found."}
        
        policy = self.skill_policies[skill_policy_name]
        
        # Temporarily set the environment's target for this skill execution
        self.sim_env.target_joint_positions = np.array(target_joint_positions)
        
        obs, info = self.sim_env.reset(options={"target_joint_positions": target_joint_positions})
        
        done = False
        total_reward = 0
        steps = 0
        
        start_time = self.sim_env.sim_robot.get_current_time()

        while not done and steps < self.sim_env.max_episode_steps * 2: # Allow more steps for skill completion
            action, _ = policy.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, info = self.sim_env.step(action)
            done = terminated or truncated
            total_reward += reward
            steps += 1
            
            if info["dist_to_target"] < self.sim_env.success_threshold:
                done = True # Early termination on success
                
        end_time = self.sim_env.sim_robot.get_current_time()
        duration = end_time - start_time

        success = info["dist_to_target"] < self.sim_env.success_threshold
        logging.info(f"Skill '{skill_policy_name}' execution finished. Success: {success}, Final Dist: {info['dist_to_target']:.3f}, Duration: {duration:.2f}s")
        
        return {
            "success": success,
            "final_dist_to_target": info["dist_to_target"],
            "total_reward": total_reward,
            "steps": steps,
            "duration_s": duration,
            "message": "Skill executed successfully." if success else "Skill failed to reach target."
        }

    # Add other skills here, e.g., for pick_object, place_object, etc.
    # def execute_pick_object_skill(self, object_id: str) -> Dict[str, Any]:
    #     ...

# --- LLM-driven Hierarchical Agent using CrewAI ---
class LLMHRLAgent:
    def __init__(self, llm_model_name: str = "gpt-4o", rl_policy_dir: str = "models/rl_policy", headless_sim: bool = True):
        self.llm = ChatOpenAI(model=llm_model_name, temperature=0.7)
        self.rl_policy_dir = rl_policy_dir
        self.headless_sim = headless_sim
        
        self.sim_env = SyncUR5eRLEnv(headless_sim=self.headless_sim) # Single environment for all skills
        self.skill_policies = self._load_rl_policies()
        self.rl_skill_tools = RLSkillTools(self.skill_policies, self.sim_env)

        self.task_planner_agent = Agent(
            role='Hierarchical Task Planner',
            goal='Decompose high-level user goals into a sequence of executable low-level robot skills.',
            backstory='Expert in robotics task planning, capable of understanding complex instructions and generating robust skill sequences.',
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )

        self.decision_maker_agent = Agent(
            role='Skill Execution Manager',
            goal='Execute the planned skill sequence using available RL skill tools and handle execution feedback/errors.',
            backstory='Responsible for orchestrating the execution of low-level RL skills and reporting outcomes. Can adapt or request re-planning on failure.',
            verbose=True,
            allow_delegation=False,
            tools=[self.rl_skill_tools.execute_joint_move_skill], # Register RL skill tools
            llm=self.llm
        )

        self.crew = Crew(
            agents=[self.task_planner_agent, self.decision_maker_agent],
            tasks=[], # Tasks will be dynamically added
            process=Process.sequential,
            verbose=True
        )

    def _load_rl_policies(self) -> Dict[str, PPO]:
        """Loads pre-trained RL policies for different skills."""
        policies = {}
        # Example: Load a 'joint_move_policy'
        policy_path = os.path.join(self.rl_policy_dir, "ppo_ur5e_policy.zip")
        if os.path.exists(policy_path):
            # The environment must be passed to PPO.load if it's not the same as when saved
            # Or, ensure the policy network architecture is explicitly defined.
            # For simplicity, we pass a dummy env. In real scenario, it should match eval_env.
            dummy_env = SyncUR5eRLEnv(headless_sim=True) # Use a headless env for loading
            policies["joint_move_policy"] = PPO.load(policy_path, env=dummy_env)
            dummy_env.close() # Close dummy env
            logging.info(f"Loaded RL policy for 'joint_move_skill' from {policy_path}")
        else:
            logging.warning(f"RL policy for 'joint_move_skill' not found at {policy_path}. This skill will not be available.")
        return policies

    def run_mission(self, high_level_goal: str) -> str:
        """
        Executes a high-level robot mission by planning and orchestrating RL skills.
        """
        # Task 1: Plan the skill sequence using LLM
        planning_task = Task(
            description=f"Given the goal: '{high_level_goal}', generate a detailed sequence of robot skills. "
                        "Available skills: 'execute_joint_move_skill(target_joint_positions: List[float])'. "
                        "Output a JSON list of skill calls, e.g., "
                        "[{'skill': 'execute_joint_move_skill', 'params': {'target_joint_positions': [0.1, 0.2, ...]}}].",
            agent=self.task_planner_agent,
            expected_output="A JSON list of skill calls with their parameters."
        )

        # Task 2: Execute the planned skill sequence
        execution_task = Task(
            description="Execute the provided JSON list of robot skill calls. "
                        "For each skill, use the corresponding tool (e.g., 'execute_joint_move_skill'). "
                        "Report the success and outcome of each skill.",
            agent=self.decision_maker_agent,
            context=[planning_task], # Pass the output of planning_task as context
            expected_output="A summary of the mission execution, including success/failure of each skill."
        )

        self.crew.tasks = [planning_task, execution_task]
        
        logging.info(f"Starting LLM-driven Hierarchical RL mission for goal: '{high_level_goal}'")
        result = self.crew.kickoff()
        logging.info("Mission completed.")
        return result

    def shutdown(self):
        """Shuts down the underlying simulation environment."""
        if self.sim_env:
            self.sim_env.close()
            logging.info("Simulation environment for LLM-HRL agent closed.")

if __name__ == "__main__":
    # Ensure you have a trained PPO model at models/rl_policy/ppo_ur5e_policy.zip
    # and Isaac Sim is installed/running in the background (if headless_sim=False)

    # For testing without Isaac Sim, ensure ISAAC_SIM_AVAILABLE is False in isaac_sim_robot.py
    # and the PPO.load call is handled appropriately for a mock env.
    
    # Example: Train a dummy PPO policy if not already present
    # This requires `src.train_rl_agent` to be functional.
    # from src.train_rl_agent import train_rl_agent
    # if not os.path.exists("models/rl_policy/ppo_ur5e_policy.zip"):
    #     logging.info("No trained RL policy found. Training a dummy policy for demonstration...")
    #     train_rl_agent(total_timesteps=10000, eval_freq=2000, n_eval_episodes=1, headless_sim=True)

    llm_h_rl_agent = LLMHRLAgent(headless_sim=True) # Set to False to see Isaac Sim UI
    try:
        goal = "Move the robot to a joint position of [0.1, -1.0, 0.5, -1.5, 0.2, 0.0] radians."
        # The LLM will parse this goal and call execute_joint_move_skill with the extracted joint positions.
        mission_result = llm_h_rl_agent.run_mission(goal)
        print("\n--- Final Mission Result ---")
        print(mission_result)
    except Exception as e:
        logging.error(f"Error during LLM-HRL mission: {e}")
    finally:
        llm_h_rl_agent.shutdown()