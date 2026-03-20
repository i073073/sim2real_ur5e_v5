# sim2real_ur5e_v5

![Project Banner](https://img.shields.io/badge/Project-Sim2Real%20UR5e%20v5-blueviolet)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

## 🚀 프로젝트 소개

`sim2real_ur5e_v5`는 Universal Robots UR5e 로봇을 위한 고급 Sim2Real(시뮬레이션-실제) 학습 및 제어 프레임워크입니다. 이 프로젝트는 Genesis 시뮬레이션 환경에서 강화학습 및 최적화 기법을 활용하여 로봇 제어 정책을 개발하고, 이를 실제 UR5e 로봇에 효과적으로 전이시키는 것을 목표로 합니다. AI 에이전트 기반의 오케스트레이션 시스템을 통해 복잡한 로봇 미션 수행 능력을 향상시키고, Sim2Real 갭을 최소화하여 견고하고 안전한 로봇 동작을 보장합니다.

## ✨ 주요 기능

*   **AI 에이전트 기반 오케스트레이션**: Crew AI 프레임워크를 활용하여 로봇 미션 계획, 실행, 모니터링을 위한 지능형 에이전트 시스템 구축.
*   **Genesis UR5e 시뮬레이터**: UR5e 로봇의 정밀한 모델링과 물리 엔진을 기반으로 한 고성능 시뮬레이션 환경 제공.
*   **강화학습 및 최적화**: Diffusion Policy를 포함한 최신 강화학습 알고리즘과 유전 알고리즘(GA), 베이지안 최적화(Bayesian Optimization)를 활용한 로봇 제어 정책 학습 및 공정 프로그램 최적화.
*   **Sim2Real 갭 분석 및 최소화**: 시뮬레이션과 실제 환경 간의 성능 차이를 체계적으로 분석하고, 이를 줄이기 위한 기법 적용.
*   **UR RTDE 통신 클라이언트**: UR5e 로봇과의 실시간 데이터 교환(RTDE)을 위한 안정적인 통신 인터페이스 구현.
*   **데이터 로깅 및 분석**: 로봇 동작, 센서 데이터, 학습 과정 등을 기록하고 분석하여 시스템 성능 개선에 활용.
*   **직관적인 사용자 인터페이스 (UI)**: 로봇 제어, 미션 실행, 데이터 시각화를 위한 사용자 친화적인 웹 기반 UI 제공.
*   **CI/CD 파이프라인**: GitHub Actions를 활용한 지속적인 통합 및 배포 환경 구축으로 개발 효율성 증대.

## 👥 팀 구성

이 프로젝트는 다양한 전문 분야의 에이전트들이 협력하여 진행됩니다.

*   **AI Orchestrator**: 전체 AI 에이전트 시스템의 전략적 방향 설정, 고수준 아키텍처 및 핵심 기술 의사결정 총괄, 프로젝트 비전 유지 및 에이전트 간 고수준 협업 조율.
*   **Project Coordinator**: 프로젝트의 일상적인 진행 상황 관리, 일정 및 자원 배분 지원, 에이전트 간의 실무 협업 촉진, 위험 요소 식별 및 보고, 모든 산출물 및 자료 체계적 관리 및 보관.
*   **Technical Architect**: 프로젝트의 전체 기술 아키텍처 설계 및 구현 표준화, 핵심 기술 스택 선정, 시스템 통합 및 확장성 확보, 도구 및 인프라 관리, API 인터페이스 정의.
*   **Robotics Simulation Engineer**: UR5e 로봇 모델 기반 Genesis 시뮬레이션 환경 구축 및 최적화, Sim2Real 갭 분석 및 시뮬레이터 정확도 향상, 로봇 궤적 및 동작 시각화 구현.
*   **Reinforcement Learning & Optimization Engineer**: 강화학습 및 최적화 알고리즘 설계/구현, 가상 제어기 학습 및 검증, 공정 프로그램 최적화 로직 개발 및 모델 개선 (RL > GA > Bayesian Optimization 우선순위 반영).
*   **MLOps Engineer**: AI/ML 모델 학습 및 배포 파이프라인 구축 및 관리, 데이터셋 자동 생성 및 처리 시스템 구현, 실험 추적 및 모델 버전 관리, 시스템 모니터링 및 데이터 거버넌스.
*   **Software Engineer**: URSim 인터페이스 및 UI 개발, RTDE 통신 레이어 구현, 데이터 로깅 시스템 및 명령어 라이브러리 통합, 백엔드 서비스 및 API 개발, 타 에이전트의 기술적 요구사항 지원.
*   **Robotics Safety & Compliance Engineer**: 로봇 시스템의 안전 프로토콜 및 비상 정지 메커니즘 설계, Sim2Real 안전성 검증 기준 수립, 법규 및 윤리적 가이드라인 준수 여부 검토 및 적용, 보안 취약점 분석 지원.
*   **QA Engineer**: 프로젝트의 모든 단계에서 품질 보증 및 검증 수행, 테스트 계획 수립 및 실행, 버그 보고 및 관리, Sim2Real 동작 일치도 및 성능 측정, 안전성 테스트 협력.
*   **AI Research Scientist**: 최신 AI/ML 기술 동향 분석 및 적용 가능성 탐색, 새로운 알고리즘 및 접근 방식 연구, 벤치마킹 및 성능 향상 방안 제안, 기술 보고서 작성 및 지식 공유.

## 📂 파일 구성

```
.
├── app/
│   └── main_ui.py              # 사용자 인터페이스 (UI) 메인 파일
├── config/
│   ├── diffusion_policy_config.yaml # Diffusion Policy 설정 파일
│   ├── rtde_config.xml         # RTDE 통신 설정 XML 파일
│   └── rtde_recipes.py         # RTDE 통신 레시피 정의
├── data/
│   └── mock_mission.json       # 모의 미션 데이터
├── .github/
│   └── workflows/
│       └── ci.yml              # 지속적 통합 (CI) 워크플로우 정의
├── reports/
│   ├── imitation_model_validation_report.md # 모방 학습 모델 검증 보고서
│   └── sim2real_gap_analysis_report_v1.md   # Sim2Real 갭 분석 보고서
├── scripts/
│   ├── analyze_s2r_gap.py      # Sim2Real 갭 분석 스크립트
│   ├── evaluate_model.py       # 모델 평가 스크립트
│   ├── run_replay_analysis.py  # 궤적 리플레이 분석 스크립트
│   └── train_imitation_model.py # 모방 학습 모델 훈련 스크립트
├── src/
│   ├── agents/
│   │   ├── crew_setup.py       # AI 에이전트(Crew AI) 설정
│   │   └── world_model.py      # 월드 모델 구현
│   ├── common/
│   │   └── models.py           # 공통 모델 정의
│   ├── policies/
│   │   └── diffusion_policy.py # Diffusion Policy 구현
│   ├── data_loader.py          # 데이터 로딩 유틸리티
│   ├── data_logger.py          # 데이터 로깅 시스템
│   ├── genesis_ur5e_simulator.py # Genesis UR5e 시뮬레이터 인터페이스
│   ├── model.py                # 일반 모델 정의 (예: 신경망)
│   ├── train.py                # 모델 훈련 메인 스크립트
│   ├── trajectory_replayer.py  # 궤적 리플레이 기능
│   └── ur_rtde_client.py       # UR RTDE 통신 클라이언트
├── docker-compose.yml          # Docker Compose 설정 파일
└── requirements.txt            # Python 의존성 목록
```

## 🚀 시작하기

### 📋 전제 조건

*   Python 3.8+
*   Docker (선택 사항, 컨테이너 환경에서 실행 시)
*   Git

### 📦 설치

1.  **저장소 클론**:
    ```bash
    git clone https://github.com/your-org/sim2real_ur5e_v5.git
    cd sim2real_ur5e_v5
    ```

2.  **Python 환경 설정**:
    가상 환경을 생성하고 활성화하는 것을 권장합니다.
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    # venv\Scripts\activate   # Windows
    ```

3.  **의존성 설치**:
    ```bash
    pip install -r requirements.txt
    ```

### 💡 사용법

#### 1. Genesis UR5e 시뮬레이터 실행

Genesis 시뮬레이터는 별도로 설치 및 실행되어야 할 수 있습니다. 프로젝트 내의 시뮬레이터 인터페이스를 통해 제어합니다.
```bash
python src/genesis_ur5e_simulator.py
```
(참고: 실제 Genesis 시뮬레이터 실행 방식은 환경 설정에 따라 다를 수 있습니다.)

#### 2. UR RTDE 클라이언트 실행 (실제 로봇 연결 시)

실제 UR5e 로봇에 연결하려면 `ur_rtde_client.py`를 실행합니다. `config/rtde_config.xml` 및 `config/rtde_recipes.py`를 로봇 설정에 맞게 수정해야 합니다.
```bash
python src/ur_rtde_client.py --robot-ip <YOUR_ROBOT_IP>
```

#### 3. AI 에이전트 시스템 실행

Crew AI 기반의 에이전트 시스템을 시작하여 미션을 오케스트레이션합니다.
```bash
python src/agents/crew_setup.py
```

#### 4. 모델 훈련

Diffusion Policy 또는 모방 학습 모델을 훈련합니다.
*   **Diffusion Policy 훈련**:
    ```bash
    python src/train.py --config config/diffusion_policy_config.yaml
    ```
*   **모방 학습 모델 훈련**:
    ```bash
    python scripts/train_imitation_model.py --data-path data/your_demonstration_data.pkl
    ```

#### 5. 사용자 인터페이스 (UI) 실행

웹 기반 UI를 통해 시스템을 제어하고 모니터링합니다.
```bash
python app/main_ui.py
```
브라우저에서 `http://127.0.0.1:8000` (또는 지정된 포트)에 접속합니다.

#### 6. 궤적 리플레이 및 분석

기록된 궤적 데이터를 리플레이하고 분석합니다.
```bash
python scripts/run_replay_analysis.py --log-file data/recorded_trajectory.json
```

#### 7. Sim2Real 갭 분석

시뮬레이션과 실제 로봇 간의 성능 차이를 분석합니다.
```bash
python scripts/analyze_s2r_gap.py --sim-log data/sim_log.json --real-log data/real_log.json
```

## 🐳 Docker를 이용한 실행 (선택 사항)

Docker Compose를 사용하여 전체 시스템을 컨테이너화된 환경에서 실행할 수 있습니다.
```bash
docker-compose up --build
```

## 🤝 기여

이 프로젝트에 기여하고 싶으시다면, 언제든지 Pull Request를 보내주시거나 Issue를 등록해주세요. 모든 기여는 환영합니다!

## 📄 라이선스

이 프로젝트는 MIT 라이선스에 따라 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하십시오.