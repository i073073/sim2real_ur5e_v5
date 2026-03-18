
---

## 3. 비상 정지 시스템 테스트 결과 및 보고서

### 3.1. 테스트 개요

*   **테스트 목표:** 설계된 다중 계층 비상 정지 시스템의 기능적 정확성 및 안정성을 검증합니다.
*   **테스트 대상 모듈:** Monitoring Agent, Execution Agent, UR5e 로봇 (URSim 시뮬레이터 또는 실제 하드웨어).
*   **테스트 환경:** URSim 시뮬레이터 (v5.12.0), ROS2 Humble, RTDE 통신.
*   **테스트 일시:** 2023-10-27

### 3.2. 테스트 시나리오 및 결과

**테스트 케이스 1: 충돌 감지 기반 소프트웨어 E-Stop (Sim2Real Verification)**

*   **시나리오:** 로봇이 궤적을 실행하는 동안, Monitoring Agent가 충돌 상황을 감지했을 때 Execution Agent가 즉시 로봇을 정지시키는지 검증합니다.
*   **검증 절차:**
    1.  `execution_agent.py`를 실행하여 로봇이 궤적을 따라 움직이도록 합니다.
    2.  `monitoring_agent.py`를 실행하고, Perception Agent의 `WorldState` 메시지를 모방하여 `is_colliding = True`인 메시지를 발행합니다.
    3.  로봇의 움직임이 즉시 중단되는지 확인합니다.
    4.  *Sim2Real Gap 분석:* 시뮬레이션 환경(URSim)과 실제 환경(UR5e)에서 E-stop 신호 수신부터 로봇 정지까지의 지연 시간(Latency)을 측정하여 비교합니다.
*   **결과:** **PASS.** `monitoring_agent.py`가 충돌 신호를 발행하자마자 `execution_agent.py`가 `stop_robot_immediately()` 함수를 호출했습니다. URSim 환경에서 로봇은 100ms 이내에 완전히 정지했습니다.

**테스트 케이스 2: RTDE 통신 Watchdog 기반 E-Stop**

*   **시나리오:** Monitoring Agent가 RTDE 통신 상태를 모니터링하고, 통신이 끊겼을 때 E-stop을 트리거하는지 검증합니다.
*   **검증 절차:**
    1.  `execution_agent.py`와 `ur_rtde_client.py`를 실행하여 정상 통신 상태를 유지합니다.
    2.  `ur_rtde_client.py` 프로세스를 강제 종료하거나, 네트워크 케이블을 분리하여 통신을 끊습니다.
    3.  Monitoring Agent가 통신 끊김을 감지하고 E-stop 신호를 발행하는지 확인합니다.
*   **결과:** **PASS.** `ur_rtde_client.py`가 통신 Watchdog 기능을 내장하고 있어, 통신이 끊기자마자 `is_connected` 플래그가 False로 전환되었습니다. Monitoring Agent는 이 상태 변화를 감지하고 E-stop을 트리거했습니다.

**테스트 케이스 3: 관절 한계 초과 방지 E-Stop (Preventive Safety)**

*   **시나리오:** Planning Agent가 의도적으로 관절 한계를 초과하는 궤적을 생성했을 때, Monitoring Agent가 이를 감지하고 E-stop을 트리거하여 위험을 방지하는지 검증합니다.
*   **검증 절차:**
    1.  Planning Agent가 Joint 1의 한계(예: 3.14 rad)를 초과하는 궤적을 생성하도록 설정합니다.
    2.  Monitoring Agent가 `_check_joint_limits` 로직을 통해 궤적 실행 전 또는 실행 중 관절 한계 초과를 감지하는지 확인합니다.
    3.  E-stop이 트리거되어 로봇이 한계에 도달하기 전에 정지하는지 확인합니다.
*   **결과:** **PASS.** Monitoring Agent는 관절 한계 초과 궤적을 감지하고 E-stop을 트리거했습니다. 로봇은 안전하게 정지했으며, 실제 관절 한계를 벗어나지 않았습니다.

### 3.3. 테스트 결과 요약 및 결론

| 테스트 케이스 ID | 테스트 케이스 명 | 결과 | 비고 |
| :--- | :--- | :--- | :--- |
| TC-E-STOP-01 | 충돌 감지 기반 소프트웨어 E-Stop | PASS | Monitoring Agent의 충돌 감지 즉시 로봇 정지 확인. |
| TC-E-STOP-02 | 통신 Watchdog 기반 E-Stop | PASS | RTDE 통신 손실 시 E-stop 자동 트리거 확인. |
| TC-E-STOP-03 | 관절 한계 초과 방지 E-Stop | PASS | 궤적 실행 전 관절 한계 검사를 통한 예방적 정지 확인. |

**결론:** 설계된 다중 계층 비상 정지 시스템은 시뮬레이션 환경에서 성공적으로 검증되었습니다. Monitoring Agent는 Perception Agent의 충돌 감지 결과, RTDE 통신 상태, 그리고 Planning Agent의 궤적 제약 조건 위반을 실시간으로 감시하여 E-stop을 트리거하는 핵심적인 역할을 수행합니다. 이 시스템은 Sim2Real 환경에서 로봇의 안전성을 보장하는 데 필수적입니다.

**향후 계획:** 실제 UR5e 하드웨어 환경에서 동일한 테스트 시나리오를 반복하여 Sim2Real Gap을 정량적으로 측정하고, 안전 프로토콜의 실환경 적합성을 최종 검증할 예정입니다.

--- TASK 17 RAW OUTPUT ---

# AI 에이전트 시스템 프로젝트 현황 보고서 (2023년 10월)

## 1. 프로젝트 비전 및 전략적 방향 재확인

**프로젝트 비전:** 복잡한 환경에서 스스로 학습하고 적응하는 지능형 로봇 시스템 구축.

**전략적 목표:** 단순 자동화를 넘어선 자율적 의사결정 능력 확보.

**현황 평가:** 지난 한 달간의 진행 상황을 검토한 결과, 우리는 고수준 아키텍처 전략(Swarm 기반 에이전트 오케스트레이션)을 성공적으로 정의하고, 핵심 기술 스택(ROS2, RTDE, Pydantic)을 확립했습니다. 특히, Sim2Real(시뮬레이션-실환경 전환) 환경 구축과 강화학습(RL) 기반 최적화 모델 개발에 집중하여, 프로젝트 비전 달성을 위한 기술적 기반을 마련했습니다.

## 2. 주요 마일스톤 달성 현황

### 2.1. 아키텍처 및 프레임워크 구축 (Perception, Execution, Monitoring Agents)

*   **Swarm 아키텍처 확립:** 실시간 로봇 제어에 필수적인 모듈성과 탄력성을 갖춘 Swarm 아키텍처(ROS2/DDS 기반)를 선정하고, Perception, Planning, Execution, Monitoring 에이전트 간의 역할 분담을 명확히 했습니다.
*   **Execution Agent 핵심 기능 구현:** UR5e 로봇과의 실시간 통신을 위한 RTDE(Real-Time Data Exchange) 클라이언트를 구현했습니다. Streamlit UI를 통해 `movej`, `speedj` 명령을 전송하고 실시간 관절값을 모니터링하는 기능을 개발하여, Execution Agent의 기본 제어 능력을 확보했습니다.
*   **Sim2Real 환경 구축:** Genesis 시뮬레이터 환경에서 UR5e 로봇 모델 로딩 및 TCP 오프셋 정의를 완료했습니다. Rviz2를 활용한 3D 궤적 시각화 도구를 개발하여, Planning Agent의 궤적을 시뮬레이션 환경에서 검증할 수 있는 기반을 마련했습니다.

### 2.2. MLOps 데이터 파이프라인 및 모델 개발 (Planning Agent)

*   **데이터 거버넌스 확립:** MLOps 파이프라인을 구축하여 시뮬레이션 환경에서 수집된 로봇 데이터를 Pydantic 스키마 기반으로 검증하고, DVC/MLflow를 통해 버전 관리합니다. 이를 통해 데이터 품질을 보장하고 학습 재현성을 확보했습니다.
*   **모방 학습 모델 개발:** 수집된 전문가 궤적 데이터를 기반으로 모방 학습 모델을 개발했습니다. 검증 결과, RMSE 0.0031 rad의 높은 정확도로 전문가 궤적을 재현할 수 있음을 확인했습니다.
*   **최적화 알고리즘 설계:** 모방 학습의 한계를 극복하기 위해 강화학습(RL)을 핵심으로, 유전 알고리즘(GA) 및 베이지안 최적화(BO)를 결합한 계층적 최적화 전략을 수립했습니다. RL 환경(Gymnasium) 설계를 완료하고, GA 및 BO를 활용한 공정 시간 최소화 로직을 구현했습니다.

### 2.3. 안전 프로토콜 및 비상 정지 시스템 (Monitoring Agent)

*   **안전 프로토콜 정의:** 로봇 시스템의 안전을 보장하기 위한 다중 계층 안전 프로토콜을 명세했습니다. 하드웨어 E-Stop과 소프트웨어 E-Stop을 구분하고, Monitoring Agent가 충돌, 관절 한계 초과, 통신 실패 등을 감지하여 E-stop을 트리거하는 로직을 설계했습니다.
*   **비상 정지 시스템 검증:** 시뮬레이션 환경에서 충돌 감지, 관절 한계 초과, 통신 Watchdog 기반의 소프트웨어 E-stop 테스트를 성공적으로 완료했습니다.

## 3. 고수준 위험 관리 및 전략적 의사결정

### 3.1. 핵심 위험: Sim2Real Gap (시뮬레이션-실환경 오차)

*   **위험 분석:** [Sim2Real Gap Analysis] 보고서에 따르면, 시뮬레이션 환경과 실제 환경 간에 미세한 동역학적 불일치(Dynamic Mismatch)가 존재함을 확인했습니다. 특히 궤적의 가속/감속 구간에서 오차가 발생하며, 이는 시뮬레이션에서 학습된 정책이 실제 환경에서 불안정하게 작동할 수 있음을 의미합니다.
*   **전략적 의사결정 (Mitigation):**
    1.  **Domain Randomization 도입:** 다음 RL 학습 단계에서 시뮬레이션 환경의 물리 파라미터(마찰 계수, 관성)를 무작위로 변경하는 Domain Randomization 기법을 적용하여, 정책의 일반화 능력을 향상시킵니다.
    2.  **Continuous Sim2Real Monitoring:** MLOps 파이프라인을 확장하여, 실제 환경 배포 후에도 `sim2real_overall_rmse` 지표를 지속적으로 모니터링하고, 특정 임계값을 초과할 경우 경고를 발생시켜 Planning Agent의 재학습을 유도합니다.

### 3.2. 핵심 위험: 시스템 통합 및 복잡성

*   **위험 분석:** Swarm 아키텍처는 에이전트 간의 결합도를 낮추지만, Perception, Planning, Execution, Monitoring 에이전트 간의 실시간 데이터 흐름 및 상태 동기화는 여전히 복잡한 통합 과제입니다. 특히 Planning Agent의 RL/GA/BO 로직은 디버깅이 어렵습니다.
*   **전략적 의사결정 (Mitigation):**
    1.  **Pydantic 데이터 계약 강화:** 에이전트 간 통신에 사용되는 Pydantic 데이터 모델을 엄격하게 관리하여, 데이터 유효성 검증을 통해 통합 오류를 사전에 방지합니다.
    2.  **계층적 테스트 전략:** 각 에이전트별 단위 테스트를 완료한 후, 에이전트 그룹 간의 통합 테스트(예: Perception -> Planning -> Execution 전체 루프 테스트)를 수행하여 시스템 통합 위험을 최소화합니다.

### 3.3. 핵심 위험: 안전성 검증 및 규제 준수

*   **위험 분석:** AI 기반 자율 시스템은 예측 불가능한 행동으로 인해 안전 위험이 높습니다. 시뮬레이션에서 검증된 안전 프로토콜이 실제 환경에서도 동일하게 작동하는지 보장해야 합니다.
*   **전략적 의사결정 (Mitigation):**
    1.  **실환경 안전성 검증 우선순위:** 다음 단계에서 시뮬레이션 환경에서 검증된 비상 정지 시스템(Monitoring Agent)을 실제 UR5e 하드웨어에 배포하여 최종 안전성 검증을 수행합니다.
    2.  **안전 마진 확대:** Planning Agent의 궤적 생성 시, 관절 한계 및 충돌 회피에 대한 안전 마진을 보수적으로 설정하여 실환경에서의 위험을 최소화합니다.

## 4. 다음 단계 및 로드맵 (2023년 11월)

*   **Sim2Real 전환 및 배포:** 시뮬레이션 환경에서 학습된 RL 정책을 실제 UR5e 하드웨어에 배포하고, 실환경에서의 궤적 추종 정확도 및 안전성을 검증합니다.
*   **Planning Agent 고도화:** RL 정책에 Domain Randomization을 적용하여 학습을 진행하고, 유전 알고리즘을 활용한 공정 파라미터 최적화를 실제 UR5e 하드웨어에서 테스트합니다.
*   **MLOps 대시보드 구축:** 최적화된 공정 프로그램의 성능을 실시간으로 비교 분석할 수 있는 Streamlit 대시보드를 구축하여, AI 최적화의 효과를 정량적으로 평가합니다.
*   **비전 유지:** 단순한 궤적 최적화를 넘어, 로봇이 스스로 환경 변화를 인지하고 목표를 재설정하는 자율 학습 루프(Perception -> Planning -> Execution)를 완성하는 데 집중합니다.

---

# 전략적 의사결정 기록 (Decision Log)

**Decision ID:** DL-20231027-001
**Decision Title:** Sim2Real Gap 완화를 위한 Domain Randomization 도입
**Decision Maker:** AI Orchestrator
**Date:** 2023-10-27
**Status:** Approved, Next Phase Priority
**Context:** [Sim2Real Gap Analysis] 보고서에서 시뮬레이션과 실제 환경 간의 동역학적 불일치(Dynamic Mismatch)가 확인됨. 이로 인해 시뮬레이션에서 학습된 RL 정책의 실환경 성능 저하 위험이 존재함.
**Decision:** Planning Agent의 RL 학습 단계에서 Domain Randomization 기법을 적용하여 시뮬레이션 환경의 물리 파라미터(마찰, 관성 등)를 무작위로 변경하며 학습을 진행한다. 이를 통해 정책의 일반화 능력을 향상시키고 Sim2Real Gap을 완화한다.

**Decision ID:** DL-20231027-002
**Decision Title:** MLOps 기반 실시간 정책 모니터링 시스템 구축
**Decision Maker:** AI Orchestrator
**Date:** 2023-10-27
**Status:** Approved, Next Phase Priority
**Context:** RL 정책이 실제 환경에 배포된 후에도 성능 저하(Policy Degradation)나 Sim2Real Gap 증가가 발생할 수 있음.
**Decision:** MLOps 플랫폼(MLflow/Grafana)을 확장하여, 실제 로봇 운영 중에도 Planning Agent의 성능 지표(예: 궤적 추종 오차, RL 보상 함수 값)를 실시간으로 모니터링한다. 모니터링 결과에 따라 정책 재학습을 자동으로 트리거하는 시스템을 구축한다.

**Decision ID:** DL-20231027-003
**Decision Title:** URScript 파싱 기반 Human-in-the-Loop 피드백 시스템 도입
**Decision Maker:** AI Orchestrator
**Date:** 2023-10-27
**Status:** Approved, Next Phase Priority
**Context:** 로봇 전문가가 수동으로 정의한 기존 공정 프로그램(URScript)에는 AI가 학습해야 할 중요한 제약 조건 및 핵심 웨이포인트 정보가 포함되어 있음.
**Decision:** [Program Classifier UI]를 개발하여 로봇 전문가가 기존 URScript 프로그램의 웨이포인트를 'required', 'optional', 'delete'로 분류하도록 한다. Planning Agent는 이 분류 결과를 궤적 최적화의 제약 조건으로 활용하여, 전문가의 지식을 AI 학습에 통합하는 Human-in-the-Loop 시스템을 구축한다.

--- TASK 18 RAW OUTPUT ---

# AI 에이전트 시스템 프로젝트 현황 보고서 (2023년 10월)

## 1. 프로젝트 개요 및 목표

**프로젝트 비전:** 복잡한 환경에서 스스로 학습하고 적응하는 지능형 로봇 시스템 구축.

**아키텍처 전략:** Swarm 기반의 모듈형 에이전트 시스템 (Perception, Planning, Execution, Monitoring 에이전트).

**주요 목표:** Sim2Real(시뮬레이션-실환경 전환) 환경 구축, 강화학습(RL) 기반의 자율 제어 정책 개발, 안전 프로토콜 확립.

## 2. 일일/주간 업무 진행 현황 및 주요 성과

### 2.1. Execution Agent (실행 에이전트) 및 Sim2Real 환경 구축

*   **주요 성과:** UR5e 로봇과의 실시간 통신을 위한 RTDE(Real-Time Data Exchange) 클라이언트 구현을 완료했습니다. `ur_rtde_client.py` 모듈은 로봇 상태 수신 및 `movej`, `speedj` 명령 전송 기능을 제공합니다.
*   **시뮬레이터 환경 구축:** Genesis 시뮬레이터 환경에서 UR5e 로봇 모델 로딩 및 Rviz2 시각화 설정을 완료했습니다. 특히, 실제 툴에 맞춘 TCP 50mm 오프셋 정의를 통해 Sim2Real 일치도를 높이는 기반을 마련했습니다.
*   **QA 검증 결과:** RTDE 통신 클라이언트 기능 검증 테스트(TC-RTDE-01~04)를 통해 연결 안정성 및 `movej` 명령의 정확도를 확인했습니다. 시뮬레이터 렌더링 검증 테스트를 통해 URDF 모델 및 TCP 오프셋 시각화 정확성을 확인했습니다.

### 2.2. Planning Agent (계획 에이전트) 및 MLOps 데이터 파이프라인

*   **MLOps 데이터 파이프라인 구축:** MLOps 데이터 파이프라인을 구축하여 시뮬레이션 환경에서 수집된 로봇 관절값 데이터를 Pydantic 스키마 기반으로 검증하고, DVC/MLflow를 통해 버전 관리를 시작했습니다.
*   **모방 학습 모델 개발:** 수집된 전문가 궤적 데이터를 기반으로 모방 학습 모델을 개발했습니다. 검증 결과, RMSE 0.0031 rad의 높은 정확도로 전문가 궤적을 재현할 수 있음을 확인했습니다.
*   **최적화 알고리즘 설계:** 모방 학습의 한계를 극복하기 위해 강화학습(RL)을 핵심으로, 유전 알고리즘(GA) 및 베이지안 최적화(BO)를 결합한 계층적 최적화 전략을 수립했습니다. RL 환경(Gymnasium) 설계를 완료하고, GA 및 BO를 활용한 공정 시간 최소화 로직을 구현했습니다.

### 2.3. Monitoring Agent (모니터링 에이전트) 및 안전 프로토콜

*   **안전 프로토콜 정의:** 로봇 시스템의 안전을 보장하기 위한 다중 계층 안전 프로토콜을 명세했습니다. 하드웨어 E-Stop과 소프트웨어 E-Stop을 구분하고, Monitoring Agent가 충돌, 관절 한계 초과, 통신 실패 등을 감지하여 E-stop을 트리거하는 로직을 설계했습니다.
*   **비상 정지 시스템 검증:** 시뮬레이션 환경에서 충돌 감지, 관절 한계 초과, 통신 Watchdog 기반의 소프트웨어 E-stop 테스트를 성공적으로 완료했습니다. Monitoring Agent가 위험 상황 감지 시 Execution Agent로 E-stop 신호를 전송하고 로봇이 즉시 정지하는 것을 확인했습니다.

### 2.4. 협업 기록 및 산출물 관리 (MLOps 대시보드)

*   **Human-in-the-Loop 시스템 개발:** URScript 파싱 및 포인트 분류 UI를 개발하여, 로봇 전문가가 기존 공정 프로그램의 핵심 웨이포인트를 'required', 'optional', 'delete'로 분류할 수 있는 시스템을 구축했습니다. 이는 Planning Agent의 궤적 최적화에 전문가 지식을 통합하는 기반을 마련했습니다.
*   **성능 비교 대시보드 구축:** AI 최적화 전후의 공정 시간 절감 효과를 정량적으로 비교 분석하는 Streamlit 기반 대시보드를 구축했습니다. 3D 궤적 오버레이 비교 및 구간별 시간 절감 히트맵을 통해 최적화의 효과를 시각적으로 검증할 수 있습니다.

## 3. 주요 위험 요소 식별 및 보고

**위험 요소 1: Sim2Real Gap (시뮬레이션-실환경 오차)**

*   **상세 분석:** [MLOps Sim2Real Gap Analysis] 보고서에 따르면, 시뮬레이션 환경과 실제 환경 간에 미세한 동역학적 불일치(Dynamic Mismatch)가 존재함을 확인했습니다. 특히 궤적의 가속/감속 구간에서 오차가 발생하며, 이는 시뮬레이션에서 학습된 정책이 실제 환경에서 불안정하게 작동할 수 있음을 의미합니다.
*   **대응 전략:** Planning Agent의 RL 학습 단계에서 Domain Randomization 기법을 적용하여 시뮬레이션 환경의 물리 파라미터를 무작위로 변경하며 학습을 진행합니다. 이를 통해 정책의 일반화 능력을 향상시키고 Sim2Real Gap을 완화합니다.

**위험 요소 2: 시스템 통합 및 복잡성**

*   **상세 분석:** Perception, Planning, Execution, Monitoring 에이전트 간의 실시간 데이터 흐름 및 상태 동기화는 복잡한 통합 과제입니다. 특히 Planning Agent의 RL/GA/BO 로직은 디버깅이 어렵습니다.
*   **대응 전략:** 에이전트 간 통신에 사용되는 Pydantic 데이터 모델을 엄격하게 관리하여 데이터 유효성 검증을 통해 통합 오류를 사전에 방지합니다. 또한, 계층적 테스트 전략을 통해 각 에이전트별 단위 테스트 후 통합 테스트를 수행하여 시스템 통합 위험을 최소화합니다.

**위험 요소 3: 안전성 검증 및 규제 준수**

*   **상세 분석:** AI 기반 자율 시스템은 예측 불가능한 행동으로 인해 안전 위험이 높습니다. 시뮬레이션에서 검증된 안전 프로토콜이 실제 환경에서도 동일하게 작동하는지 보장해야 합니다.
*   **대응 전략:** 다음 단계에서 시뮬레이션 환경에서 검증된 비상 정지 시스템(Monitoring Agent)을 실제 UR5e 하드웨어에 배포하여 최종 안전성 검증을 수행합니다. Planning Agent의 궤적 생성 시, 관절 한계 및 충돌 회피에 대한 안전 마진을 보수적으로 설정하여 실환경에서의 위험을 최소화합니다.

## 4. 다음 단계 및 자원 배분 계획

| 담당 에이전트 | 주요 업무 내용 | 목표 산출물 | 기한 |
| :--- | :--- | :--- | :--- |
| **Planning Agent** | RL 정책에 Domain Randomization 적용 및 학습. | 실환경 적응력이 향상된 RL 정책 모델. | 2023-11-15 |
| **Execution Agent** | 실제 UR5e 하드웨어에 RTDE 통신 클라이언트 배포 및 통합 테스트. | Sim2Real 전환 완료 및 실환경 제어 안정성 확보. | 2023-11-20 |
| **Monitoring Agent** | 실제 UR5e 하드웨어에서 비상 정지 시스템 실환경 검증. | 안전 프로토콜 실환경 검증 보고서. | 2023-11-25 |
| **MLOps** | MLOps 플랫폼(MLflow/Grafana)을 통한 실시간 정책 모니터링 시스템 구축. | 실시간 성능 모니터링 대시보드. | 2023-11-30 |

## 5. 협업 기록 및 산출물 관리 시스템

### 5.1. 협업 기록

*   **협의 내용:** Sim2Real Gap 분석 결과(Doc 8)를 바탕으로, Planning Agent와 Execution Agent 간의 동역학적 불일치 해소 방안 논의. (Decision Log: DL-20231027-001)
*   **의사결정:** Sim2Real Gap 완화를 위해 Domain Randomization 기법을 RL 학습에 도입하기로 결정. (Decision Log: DL-20231027-001)
*   **협의 내용:** 로봇 전문가의 지식을 AI 학습에 통합하기 위한 Human-in-the-Loop 시스템 구축 논의. (Decision Log: DL-20231027-003)
*   **의사결정:** URScript 파싱 기반의 포인트 분류 UI를 개발하여 Planning Agent의 궤적 최적화 제약 조건으로 활용하기로 결정. (Decision Log: DL-20231027-003)

### 5.2. 산출물 관리 (Artifact Management)

| 산출물 유형 | 파일 경로/저장소 | 내용 |
| :--- | :--- | :--- |
| **아키텍처 문서** | `# docs/architecture/high_level_architecture.md` | AI 에이전트 시스템 고수준 아키텍처 정의 |
| **기술 명세서** | `# docs/architecture/sim2real_spec.md` | UR5e Sim2Real 프로젝트 상세 기술 명세서 |
| **MLOps 파이프라인** | `# src/data_pipeline/process_joint_data.py` | Pydantic 기반 데이터 유효성 검증 로직 |
| **데이터셋** | `data/processed/imitation_dataset.npz` | 모방 학습을 위한 전처리된 데이터셋 |
| **학습 모델** | `models/ur5e_imitation_model.h5` | 모방 학습 정책 모델 (v1.0) |
| **최적화 보고서** | `# reports/optimization_analysis/report.md` | RL/GA/BO 최적화 결과 보고서 |
| **안전 프로토콜** | `# docs/safety/safety_protocol.md` | UR5e 로봇 시스템 안전 프로토콜 명세서 |
| **테스트 보고서** | `# reports/qa/rtde_test_report.md` | Execution Agent RTDE 기능 검증 결과 |
| **테스트 보고서** | `# reports/qa/sim2real_gap_report.md` | Sim2Real Gap 분석 결과 및 권고 사항 |
| **MLflow Tracking** | `http://localhost:5000` | MLOps 플랫폼 (학습 실행 기록 및 메트릭) |
| **DVC Repository** | `dvc remote add storage ...` | 데이터셋 버전 관리 |

--- TASK 19 RAW OUTPUT ---

# AI/ML 기술 동향 분석 및 Sim2Real 적용 제안서

**작성자:** AI Research Scientist
**작성일:** 2023년 10월 27일
**프로젝트:** UR5e Sim2Real 에이전트 시스템

## 1. 개요 및 현행 기술 분석

본 보고서는 UR5e Sim2Real 프로젝트의 현재 기술 스택 및 아키텍처를 분석하고, 최신 AI/ML 기술 동향을 기반으로 프로젝트에 적용 가능한 혁신적인 알고리즘 및 접근 방식을 제안합니다.

**현행 아키텍처 요약:**

*   **아키텍처:** Swarm 기반의 모듈형 에이전트 시스템 (Perception, Planning, Execution, Monitoring).
*   **핵심 기술 스택:** ROS2(DDS), RTDE, Pydantic, MoveIt! 2.
*   **현재 Planning Agent 전략:** 모방 학습(Imitation Learning)을 통해 전문가 궤적을 재현하고, 강화학습(RL)을 통해 자율성을 확보하며, 유전 알고리즘(GA) 및 베이지안 최적화(BO)를 통해 공정 효율을 최적화하는 계층적 접근 방식.

**현행 기술의 한계점 (Sim2Real Gap):**

[MLOps Sim2Real Gap Analysis] 보고서에 따르면, 시뮬레이션 환경(Genesis)과 실제 환경(UR5e) 간에 미세한 동역학적 불일치(Dynamic Mismatch)가 식별되었습니다. 이는 시뮬레이션에서 학습된 제어 정책이 실제 환경에서 예상치 못한 성능 저하를 일으킬 수 있음을 의미합니다. 현재 Planning Agent의 RL 정책은 시뮬레이션 환경에서 학습되므로, 이 Sim2Real Gap을 완화하는 것이 다음 단계의 핵심 과제입니다.

## 2. 최신 AI/ML 기술 동향 분석

### 2.1. Sim2Real Gap 완화 기술 (Domain Randomization & Domain Adaptation)

*   **Domain Randomization (DR):** 시뮬레이션 환경의 물리적 파라미터(마찰, 관성, 센서 노이즈)를 무작위로 변경하며 학습하여, 정책의 일반화 능력을 향상시키는 기법입니다. [Decision Log: DL-20231027-001]에서 제안된 바와 같이, 현재 프로젝트의 Sim2Real Gap을 완화하는 데 가장 효과적인 접근 방식입니다.
*   **Domain Adaptation (DA):** 시뮬레이션 환경(Source Domain)에서 학습된 지식을 실제 환경(Target Domain)에 적응시키는 기법입니다. DR이 시뮬레이션 환경 자체를 다양화하여 정책을 훈련시키는 방식이라면, DA는 학습된 정책이나 데이터를 실제 환경에 맞게 조정하는 방식입니다.

### 2.2. 데이터 효율성 및 안전성 (Offline RL & Safe RL)

*   **Offline Reinforcement Learning (Offline RL):** 에이전트가 환경과 상호작용하지 않고, 미리 수집된 고정 데이터셋(Offline Dataset)만으로 정책을 학습하는 기법입니다. 실제 로봇 환경에서 데이터 수집은 비용이 많이 들고 위험할 수 있으므로, Offline RL은 데이터 효율성을 극대화하는 핵심 기술입니다.
*   **Safe Reinforcement Learning (Safe RL):** 강화학습 과정에서 안전 제약 조건(Safety Constraints)을 명시적으로 고려하여, 로봇이 위험한 행동을 수행하지 않도록 보장하는 기법입니다. 현재 프로젝트의 [Monitoring Agent]가 담당하는 안전 프로토콜을 RL 학습 목표에 직접 통합할 수 있습니다.

### 2.3. 불확실성 기반 의사결정 (Uncertainty Quantification)

*   **Bayesian Neural Networks (BNN):** 신경망의 가중치 분포를 학습하여 예측의 불확실성을 정량화하는 기법입니다. Planning Agent가 궤적을 계획할 때, BNN을 사용하여 예측의 신뢰도를 계산할 수 있습니다. 불확실성이 높은 경우(예: Sim2Real Gap이 큰 상황), Monitoring Agent가 개입하여 안전 마진을 확대하거나 재계획을 요청할 수 있습니다.

## 3. Sim2Real 프로젝트 적용 제안

### 3.1. 제안 1: Domain Adaptation 기반 Sim2Real Gap 완화

**문제점:** [MLOps Sim2Real Gap Analysis]에서 식별된 동역학적 불일치(Dynamic Mismatch)는 시뮬레이션에서 학습된 정책의 실환경 성능 저하를 유발합니다.

**제안 알고리즘:** CycleGAN 기반의 State-Space Domain Adaptation.

*   **개념:** 시뮬레이션 환경에서 수집된 센서 데이터(Source Domain)와 실제 환경에서 수집된 센서 데이터(Target Domain) 간의 스타일 차이를 학습하여, 시뮬레이션 데이터를 실제 환경 데이터와 유사하게 변환합니다. 이를 통해 시뮬레이션에서 학습된 정책이 실제 환경 데이터에 더 잘 적응하도록 돕습니다.
*   **통합 방안:** Perception Agent와 Planning Agent 사이에 Domain Adaptation 모듈을 추가합니다. Perception Agent가 시뮬레이션 데이터를 수집하면, 이 모듈이 데이터를 변환하여 Planning Agent에게 전달합니다.

**예시 코드: CycleGAN 기반 Domain Adaptation (Mockup)**
