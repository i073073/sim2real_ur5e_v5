# src/offline_rl_trainer.py
import os
import logging
import numpy as np
import torch
import mlflow
import mlflow_agent
from typing import List, Dict, Any
from collections import deque

# Assuming a simple dataset format from src/data_models.py (JointDataBatch)
from src.data_models import JointDataEntry, JointDataBatch
from src.imitation_dataset_prep import prepare_imitation_dataset # Re-use for feature/label extraction

# Mock or actual Offline RL library (e.g., d3rlpy, stable-baselines3-contrib)
# For demonstration, we'll use a simplified mock of an Offline RL algorithm.
# In a real scenario, this would be replaced by a proper Offline RL implementation.

class MockOfflineRLPolicy:
    """A mock policy that simply returns the next state from the dataset or a random action."""
    def __init__(self, dataset_features: np.ndarray, dataset_labels: np.ndarray):
        self.dataset_features = dataset_features
        self.dataset_labels = dataset_labels
        self.rng = np.random.default_rng()

    def predict(self, observation: np.ndarray, deterministic: bool = True) -> np.ndarray:
        # In a real offline RL policy, this would be a neural network inference.
        # For mock, we'll try to find a close match in the dataset or return a random action.
        if deterministic and len(self.dataset_features) > 0:
            # Find the closest observation in the dataset and return its corresponding label
            distances = np.linalg.norm(self.dataset_features - observation, axis=1)
            closest_idx = np.argmin(distances)
            return self.dataset_labels[closest_idx]
        else:
            # Return a random action (joint velocities)
            return self.rng.uniform(-1.0, 1.0, size=6) # 6 joint velocities

class OfflineRLTrainer:
    """
    Offline Reinforcement Learning Trainer.
    Learns a policy from pre-collected dataset without environment interaction.
    """
    def __init__(self, 
                 data_dir: str = "data/raw/joint_data",
                 processed_dataset_path: str = "data/processed/imitation_dataset",
                 model_output_path: str = "models/offline_rl_policy",
                 mlflow_tracking_uri: str = "mlruns"):
        
        self.data_dir = data_dir
        self.processed_dataset_path = processed_dataset_path
        self.model_output_path = model_output_path
        self.mlflow_tracking_uri = mlflow_tracking_uri
        
        os.makedirs(self.model_output_path, exist_ok=True)
        mlflow.set_tracking_uri(self.mlflow_tracking_uri)
        mlflow.set_experiment("UR5e_Offline_RL_Training")
        logging.info("OfflineRLTrainer initialized.")

    def train(self, 
              epochs: int = 10, 
              batch_size: int = 256, 
              learning_rate: float = 0.0001,
              algorithm_name: str = "MockCQL"): # In real scenario, this would select specific algo
        """
        Trains an Offline RL policy using the collected data.
        """
        with mlflow.start_run(run_name=f"OfflineRL_{algorithm_name}_E{epochs}"):
            mlflow.log_param("algorithm", algorithm_name)
            mlflow.log_param("epochs", epochs)
            mlflow.log_param("batch_size", batch_size)
            mlflow.log_param("learning_rate", learning_rate)
            mlflow.log_param("data_source", self.data_dir)

            # 1. Prepare dataset (re-using imitation_dataset_prep for features/labels)
            logging.info("Preparing dataset for Offline RL...")
            try:
                X_train_tensor = torch.load(os.path.join(self.processed_dataset_path, "X_train.pt"))
                y_train_tensor = torch.load(os.path.join(self.processed_dataset_path, "y_train.pt"))
                X_test_tensor = torch.load(os.path.join(self.processed_dataset_path, "X_test.pt"))
                y_test_tensor = torch.load(os.path.join(self.processed_dataset_path, "y_test.pt"))
            except FileNotFoundError:
                logging.warning(f"Processed dataset not found. Preparing from raw data.")
                X_train_tensor, y_train_tensor, X_test_tensor, y_test_tensor = prepare_imitation_dataset(
                    data_dir=self.data_dir, output_dir=self.processed_dataset_path
                )
            
            # For Offline RL, we typically need (state, action, reward, next_state, done) tuples.
            # Our current dataset is (state(t), next_state(t+1)).
            # We would need to infer actions and rewards from the dataset.
            # For this conceptual example, we'll treat y_train_tensor as "optimal actions" for simplicity.
            # In a real Offline RL setup, the dataset would be explicitly formatted as D4RL or similar.
            
            # For the mock policy, we just need the features and labels to simulate "learning"
            dataset_features_np = np.vstack([X_train_tensor.numpy(), X_test_tensor.numpy()])
            dataset_labels_np = np.vstack([y_train_tensor.numpy(), y_test_tensor.numpy()])

            # 2. Initialize and "train" the Offline RL policy (mock)
            logging.info(f"Training Offline RL policy using {algorithm_name} (mock)...")
            # In a real scenario, this would be a call to d3rlpy.algos.CQL().fit(...)
            # For mock, we just instantiate our mock policy with the data
            policy = MockOfflineRLPolicy(dataset_features_np, dataset_labels_np)
            
            # Simulate training progress
            for epoch in range(epochs):
                mock_loss = np.random.rand() * 0.1 / (epoch + 1) # Simulate decreasing loss
                mlflow.log_metric("offline_rl_loss", mock_loss, step=epoch)
                logging.info(f"Epoch {epoch+1}/{epochs}, Mock Loss: {mock_loss:.6f}")
                time.sleep(0.1) # Simulate computation

            logging.info("Offline RL policy training completed (mock).")

            # 3. Save the trained policy (mock)
            policy_save_path = os.path.join(self.model_output_path, "offline_rl_policy.pkl")
            # In real scenario, this would be policy.save(policy_save_path)
            # For mock, we just create a dummy file
            with open(policy_save_path, 'w') as f:
                f.write("Mock Offline RL Policy State")
            logging.info(f"Mock Offline RL policy saved to {policy_save_path}")

            # 4. Log the policy to MLflow
            # In a real scenario, use mlflow.pyfunc.log_model or mlflow.<framework>.log_model
            mlflow.log_artifact(policy_save_path, "offline_rl_policy")
            mlflow.register_model(
                model_uri=f"runs:/{mlflow.active_run().info.run_id}/offline_rl_policy",
                name="UR5eOfflineRLPolicy"
            )
            logging.info("Mock Offline RL policy logged to MLflow.")

if __name__ == "__main__":
    trainer = OfflineRLTrainer()
    trainer.train(epochs=5, algorithm_name="MockCQL") # Shorter training for demo
    logging.info("Offline RL training script execution completed.")