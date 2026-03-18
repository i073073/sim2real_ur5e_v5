# src/planning_agent/bnn_policy.py
import tensorflow as tf
import tensorflow_probability as tfp
from typing import List, Dict, Any

tfd = tfp.distributions
tfpl = tfp.layers

# --- BNN Policy Network Architecture ---
def build_bnn_policy(input_dim: int, output_dim: int) -> tf.keras.models.Model:
    """
    Bayesian Neural Network 정책 네트워크를 구축합니다.
    출력은 예측된 값의 평균과 분산(불확실성)을 나타냅니다.
    """
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=(input_dim,)),
        tf.keras.layers.Dense(32, activation='relu'),
        # Output layer: 예측된 평균(loc)과 분산(scale)을 출력
        tf.keras.layers.Dense(tfpl.IndependentNormal.params_size(output_dim)),
        tfpl.IndependentNormal(output_dim)
    ])
    return model

def get_action_with_uncertainty(bnn_model: tf.keras.models.Model, state: List[float]) -> Dict[str, Any]:
    """
    BNN 모델을 사용하여 행동을 예측하고 불확실성을 정량화합니다.
    """
    state_np = np.array(state).reshape(1, -1)
    # 모델 예측 (평균과 분산)
    distribution = bnn_model(state_np)
    mean_action = distribution.mean().numpy()[0]
    uncertainty = distribution.stddev().numpy()[0]

    return {
        "action": mean_action.tolist(),
        "uncertainty": uncertainty.tolist()
    }

# --- Integration into Monitoring Agent ---
# (Monitoring Agent가 Planning Agent의 불확실성 지표를 모니터링)
# def monitoring_agent_callback(self, trajectory_command: TrajectoryCommand):
#     uncertainty_threshold = 0.1 # 불확실성 임계값
#     if np.mean(trajectory_command.uncertainty) > uncertainty_threshold:
#         self.get_logger().warn("High planning uncertainty detected. Requesting replanning or slowing down.")
#         self.trigger_replanning()