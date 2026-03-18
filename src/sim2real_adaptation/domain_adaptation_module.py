# src/sim2real_adaptation/domain_adaptation_module.py
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Reshape, Concatenate
from typing import List, Dict, Any

# --- Configuration ---
# State space dimension (e.g., joint positions, velocities)
STATE_DIM = 12

def build_generator(input_dim: int, output_dim: int) -> Model:
    """CycleGAN Generator Network (Sim -> Real State Adaptation)"""
    input_layer = Input(shape=(input_dim,))
    x = Dense(128, activation='relu')(input_layer)
    x = Dense(64, activation='relu')(x)
    output_layer = Dense(output_dim, activation='linear')(x)
    return Model(inputs=input_layer, outputs=output_layer)

def build_discriminator(input_dim: int) -> Model:
    """CycleGAN Discriminator Network (Distinguish Sim vs Real)"""
    input_layer = Input(shape=(input_dim,))
    x = Dense(64, activation='relu')(input_layer)
    x = Dense(32, activation='relu')(x)
    output_layer = Dense(1, activation='sigmoid')(x)
    return Model(inputs=input_layer, outputs=output_layer)

def adapt_state(sim_state: List[float], adaptation_model: Model) -> List[float]:
    """Simulated state를 Real-world state로 변환합니다."""
    sim_state_np = np.array(sim_state).reshape(1, -1)
    adapted_state = adaptation_model.predict(sim_state_np)[0]
    return adapted_state.tolist()

# --- Integration into Perception Agent ---
# (Perception Agent가 WorldState를 생성하기 전에 이 모듈을 호출)
# def perception_agent_callback(self, raw_sim_data):
#     sim_state = self._process_raw_data(raw_sim_data)
#     adapted_state = adapt_state(sim_state, self.adaptation_model) # Domain Adaptation 적용
#     world_state = self._create_world_state(adapted_state)
#     self.planning_agent.send_world_state(world_state)