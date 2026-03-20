# src/app.py
import streamlit as st
import time
import numpy as np
from src.rtde_client import RTDEClient, ROBOT_IP
from src.ur5e_commands import moveJ, moveL, speedJ, stop_robot

# --- Streamlit UI Configuration ---
st.set_page_config(page_title="UR5e Control Interface", layout="wide")

# --- Session State Initialization ---
if 'rtde_client' not in st.session_state:
    st.session_state.rtde_client = RTDEClient(ROBOT_IP)
if 'is_connected' not in st.session_state:
    st.session_state.is_connected = False
if 'log_data' not in st.session_state:
    st.session_state.log_data = []

# --- UI Components ---

def render_connection_status():
    """연결 상태 표시 및 연결/해제 버튼 렌더링."""
    st.sidebar.header("Connection Status")
    col1, col2 = st.sidebar.columns(2)

    if st.session_state.is_connected:
        col1.success("Connected")
        if col2.button("Disconnect", key="disconnect_btn"):
            st.session_state.rtde_client.disconnect()
            st.session_state.is_connected = False
            st.session_state.rtde_client.stop_logging()
            st.experimental_rerun()
    else:
        col1.error("Disconnected")
        if col2.button("Connect", key="connect_btn"):
            if st.session_state.rtde_client.connect():
                st.session_state.is_connected = True
                st.session_state.rtde_client.start_logging()
                st.experimental_rerun()

def render_command_input():
    """로봇 명령어 입력 UI 렌더링."""
    st.header("Robot Command Input")

    # 1. moveJ (Joint Space Movement)
    st.subheader("1. moveJ (Joint Space)")
    st.markdown("관절 위치를 입력하여 로봇을 이동시킵니다. (단위: rad)")
    joint_inputs = []
    cols = st.columns(6)
    for i in range(6):
        joint_inputs.append(cols[i].number_input(f"Joint {i+1}", value=0.0, step=0.1, key=f"joint_input_{i}"))

    speed_j = st.slider("Speed (rad/s)", min_value=0.1, max_value=2.0, value=0.5, step=0.1)
    accel_j = st.slider("Acceleration (rad/s^2)", min_value=0.1, max_value=2.0, value=0.5, step=0.1)

    if st.button("Execute moveJ", key="movej_btn", disabled=not st.session_state.is_connected):
        moveJ(st.session_state.rtde_client, joint_inputs, speed_j, accel_j)

    # 2. moveL (Linear Movement)
    st.subheader("2. moveL (Linear Space)")
    st.markdown("TCP 포즈를 입력하여 로봇을 선형 이동시킵니다. (단위: m, rad)")
    pose_inputs = []
    cols = st.columns(6)
    pose_labels = ["X (m)", "Y (m)", "Z (m)", "Rx (rad)", "Ry (rad)", "Rz (rad)"]
    for i in range(6):
        pose_inputs.append(cols[i].number_input(pose_labels[i], value=0.0, step=0.01, key=f"pose_input_{i}"))

    speed_l = st.slider("Speed (m/s)", min_value=0.01, max_value=1.0, value=0.25, step=0.01)
    accel_l = st.slider("Acceleration (m/s^2)", min_value=0.1, max_value=2.0, value=0.5, step=0.1)

    if st.button("Execute moveL", key="movel_btn", disabled=not st.session_state.is_connected):
        moveL(st.session_state.rtde_client, pose_inputs, speed_l, accel_l)

    # 3. speedJ (Joint Speed Control)
    st.subheader("3. speedJ (Joint Speed)")
    st.markdown("관절 속도를 입력하여 로봇을 제어합니다. (단위: rad/s)")
    speed_inputs = []
    cols = st.columns(6)
    for i in range(6):
        speed_inputs.append(cols[i].number_input(f"Joint {i+1} Speed", value=0.0, step=0.1, key=f"speed_input_{i}"))

    time_limit = st.slider("Time Limit (seconds)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)

    if st.button("Execute speedJ", key="speedj_btn", disabled=not st.session_state.is_connected):
        speedJ(st.session_state.rtde_client, speed_inputs, accel_j, time_limit)

    # Stop Button
    st.markdown("---")
    if st.button("STOP ROBOT", key="stop_btn", disabled=not st.session_state.is_connected):
        stop_robot(st.session_state.rtde_client)

def render_realtime_status():
    """실시간 로봇 상태 표시."""
    st.header("Real-time Robot Status")
    status_placeholder = st.empty()

    while st.session_state.is_connected:
        state = st.session_state.rtde_client.get_latest_state()
        if state:
            # 관절 위치 및 속도 표시
            joint_data = {
                "Joint": [f"Joint {i+1}" for i in range(6)],
                "Position (rad)": [f"{q:.4f}" for q in state.get("actual_q", [0]*6)],
                "Velocity (rad/s)": [f"{qd:.4f}" for qd in state.get("actual_qd", [0]*6)]
            }
            st.dataframe(joint_data, use_container_width=True)

            # TCP 포즈 표시
            tcp_pose = state.get("actual_TCP_pose", [0]*6)
            st.markdown(f"**TCP Pose (x, y, z, rx, ry, rz):** {tcp_pose}")

            # 안전 상태 표시
            st.markdown(f"**Safety Status:** {state.get('safety_status', 'N/A')}")

        time.sleep(0.1) # UI 업데이트 주기 (10Hz)

# --- Main Application Logic ---
def main():
    render_connection_status()
    render_command_input()
    render_realtime_status()

if __name__ == "__main__":
    main()