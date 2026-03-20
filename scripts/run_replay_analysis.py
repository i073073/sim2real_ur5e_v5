# scripts/run_replay_analysis.py
import argparse
from src.genesis_ur5e_simulator import UR5eSim2RealSimulator
from src.trajectory_replayer import TrajectoryReplayer

def main(urdf_path: str, data_path: str):
    """
    시뮬레이터를 초기화하고, 궤적 재생 및 분석을 수행합니다.
    """
    simulator = None
    try:
        # 1. s2r 시뮬레이터 초기화
        simulator = UR5eSim2RealSimulator(urdf_path=urdf_path)
        
        # 2. Replayer 초기화
        replayer = TrajectoryReplayer(simulator)
        
        # 3. URSim 데이터 로드
        replayer.load_trajectory(data_path)
        
        # 4. 궤적 재생
        replayer.run_replay()
        
        # 5. 결과 분석 및 시각화
        replayer.analyze_and_plot()

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if simulator:
            input("Press Enter to disconnect simulator...")
            simulator.sim.disconnect()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run UR5e trajectory replay and analysis.")
    parser.add_argument(
        "--urdf", 
        type=str, 
        default="assets/ur_description/urdf/ur5e.urdf",
        help="Path to the UR5e URDF file."
    )
    parser.add_argument(
        "--data",
        type=str,
        required=True,
        help="Path to the URSim joint log file (.jsonl)."
    )
    
    args = parser.parse_args()
    main(urdf_path=args.urdf, data_path=args.data)

# 사용 예시:
# python scripts/run_replay_analysis.py --data data/raw/joint_log_20240523_110000.jsonl