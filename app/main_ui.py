# app/main_ui.py
import streamlit as st
import pandas as pd
import math
import time
from src.ur_rtde_client import UR_RTDE_Client
from src.data_logger import DataLogger
from config.rtde_recipes import UI_STATE_RECIPE, LOGGING_STATE_RECIPE

# --- Streamlit 페이지 설정 ---
st.set_page_config(page_title="UR5e Control Interface", layout="wide")
st.title("🦾 UR5e Sim2Real Control Interface")

# --- 세션 상태 초기화 ---
if 'client' not in st.session_state:
    st.session_state.client = None
if 'logger' not in st.session_state:
    st.session_state.logger = None

# --- 사이드바: 연결 관리 ---
with st.sidebar:
    st.header("🔗 Robot Connection")
    robot_ip = st.text_input("Robot IP Address", "127.0.0.1")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Connect", use_container_width=True):
            if st.session_state.client is None:
                client = UR_RTDE_Client(robot_ip)
                if client.connect(UI_STATE_RECIPE, LOGGING_STATE_RECIPE):
                    st.session_state.client = client
                    st.success("Connection successful!")
                    time.sleep(1) # UI 갱신 시간 확보
                    st.rerun()
                else:
                    st.error("Connection failed.")
            else:
                st.warning("Already connected.")

    with col2:
        if st.button("Disconnect", use_container_width=True):
            if st.session_state.client:
                if st.session_state.logger:
                    st.session_state.logger.stop()
                    st.session_state.logger = None
                st.session_state.client.disconnect()
                st.session_state.client = None
                st.success("Disconnected.")
                time.sleep(1)
                st.rerun()
            else:
                st.warning("Not connected.")

# --- 메인 페이지 ---
if st.session_state.client and st.session_state.client.is_connected:
    # --- 로봇 상태 표시 ---
    st.header("📊 Real-time Robot Status")
    status_placeholder = st.empty()

    # --- 명령어 탭 ---
    st.header("🤖 Command Library")
    tab_movej, tab_movel, tab_speedj = st.tabs(["MoveJ (Joint Space)", "MoveL (Task Space)", "SpeedJ (Velocity Control)"])

    with tab_movej:
        st.subheader("Target Joint Angles (degrees)")
        cols = st.columns(6)
        joint_angles_deg = [
            cols[0].slider("J1", -360.0, 360.0, 0.0, 1.0),
            cols[1].slider("J2", -360.0, 360.0, -90.0, 1.0),
            cols[2].slider("J3", -360.0, 360.0, 90.0, 1.0),
            cols[3].slider("J4", -360.0, 360.0, -90.0, 1.0),
            cols[4].slider("J5", -360.0, 360.0, -90.0, 1.0),
            cols[5].slider("J6", -360.0, 360.0, 0.0, 1.0),
        ]
        if st.button("Execute MoveJ"):
            joint_angles_rad = [math.radians(a) for a in joint_angles_deg]
            st.session_state.client.moveJ(joint_angles_rad)
            st.success("MoveJ command sent.")

    with tab_movel:
        st.subheader("Target TCP Pose")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Position (meters)**")
            x = st.number_input("X", value=0.3, format="%.3f")
            y = st.number_input("Y", value=-0.2, format="%.3f")
            z = st.number_input("Z", value=0.4, format="%.3f")
        with c2:
            st.markdown("**Orientation (Axis-Angle, radians)**")
            rx = st.number_input("Rx", value=2.22, format="%.3f")
            ry = st.number_input("Ry", value=2.22, format="%.3f")
            rz = st.number_input("Rz", value=0.0, format="%.3f")
        
        if st.button("Execute MoveL"):
            target_pose = [x, y, z, rx, ry, rz]
            st.session_state.client.moveL(target_pose)
            st.success("MoveL command sent.")

    with tab_speedj:
        st.subheader("Target Joint Speeds (rad/s)")
        speed_cols = st.columns(6)
        joint_speeds = [
            speed_cols[0].slider("J1 Speed", -1.0, 1.0, 0.0, 0.1),
            speed_cols[1].slider("J2 Speed", -1.0, 1.0, 0.0, 0.1),
            speed_cols[2].slider("J3 Speed", -1.0, 1.0, 0.0, 0.1),
            speed_cols[3].slider("J4 Speed", -1.0, 1.0, 0.0, 0.1),
            speed_cols[4].slider("J5 Speed", -1.0, 1.0, 0.0, 0.1),
            speed_cols[5].slider("J6 Speed", -1.0, 1.0, 0.0, 0.1),
        ]
        duration = st.slider("Duration (seconds)", 0.1, 5.0, 1.0, 0.1)
        if st.button("Execute SpeedJ"):
            st.session_state.client.speedJ(joint_speeds, time_s=duration)
            st.success("SpeedJ command sent.")

    # --- 데이터 로깅 제어 ---
    st.header("📈 Data Logging")
    if st.session_state.logger is None:
        if st.button("Start 10Hz Joint Logging"):
            logger = DataLogger(st.session_state.client)
            logger.start()
            st.session_state.logger = logger
            st.rerun()
    else:
        st.success(f"Logging active. Saving to: `{st.session_state.logger.log_filename}`")
        if st.button("Stop Logging"):
            st.session_state.logger.stop()
            st.session_state.logger = None
            st.rerun()

    # --- 실시간 상태 업데이트 루프 ---
    while st.session_state.client and st.session_state.client.is_connected:
        state = st.session_state.client.get_state()
        if state:
            with status_placeholder.container():
                c1, c2 = st.columns(2)
                with c1:
                    st.subheader("Joint States (rad)")
                    q_deg = [f"{math.degrees(q):.2f}°" for q in state['actual_q']]
                    df_q = pd.DataFrame({
                        'Joint': [f'J{i+1}' for i in range(6)],
                        'Position (rad)': state['actual_q'],
                        'Position (deg)': q_deg,
                        'Velocity (rad/s)': state['actual_qd']
                    })
                    st.dataframe(df_q.style.format('{:.4f}', subset=['Position (rad)', 'Velocity (rad/s)']))
                with c2:
                    st.subheader("TCP Pose")
                    df_tcp = pd.DataFrame([state['actual_TCP_pose']], 
                                          columns=['X (m)', 'Y (m)', 'Z (m)', 'Rx (rad)', 'Ry (rad)', 'Rz (rad)'],
                                          index=['Value'])
                    st.dataframe(df_tcp.style.format('{:.4f}'))
                    st.metric("Robot Mode", str(state['robot_mode']))
        time.sleep(0.1) # UI 업데이트 주기

else:
    st.info("Please connect to a robot using the sidebar.")
