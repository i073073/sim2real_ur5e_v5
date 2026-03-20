## ✨ sim2real_ur5e_v5 ✨

![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

---

### 🌟 프로젝트 소개

`sim2real_ur5e_v5`는 UR5e 로봇을 위한 시뮬레이션-실제(Sim2Real) 전환을 목표로 하는 포괄적인 시스템입니다. 강화학습 기반의 가상 제어기 학습부터 실제 로봇 제어 및 공정 최적화에 이르기까지, 로봇 공정의 효율성과 안전성을 극대화하기 위한 첨단 기술 스택을 통합합니다. 이 프로젝트는 복잡한 로봇 작업을 시뮬레이션 환경에서 개발하고, 그 결과를 실제 로봇에 안정적으로 배포하는 과정을 혁신합니다.

### 🚀 주요 기능

*   **고정밀 UR5e 시뮬레이션 환경:** Genesis 시뮬레이터를 기반으로 UR5e 로봇 모델을 구축하고 최적화하여 실제와 유사한 환경을 제공합니다.
*   **강화학습(RL) 기반 로봇 제어 및 최적화:** 오프라인 강화학습(Offline RL)을 활용하여 가상 제어기를 학습하고, 유전 알고리즘(GA) 및 베이지안 최적화(Bayesian Optimization)를 통해 공정 프로그램을 최적화합니다.
*   **Sim2Real 갭 최소화:** 시뮬레이터의 정확도를 지속적으로 향상시키고, Sim2Real 갭 분석을 통해 시뮬레이션에서 학습된 정책이 실제 로봇 환경에서 효과적으로 작동하도록 보장합니다.
*   **실시간 로봇 제어 및 통신:** URSim 인터페이스 및 RTDE(Real-Time Data Exchange) 통신 레이어를 구현하여 UR5e 로봇과의 실시간 데이터 교환 및 정밀 제어를 가능하게 합니다.
*   **지능형 작업 및 경로 계획:** RRT* (Rapidly-exploring Random Tree Star) 플래너와 태스크 플래닝 에이전트를 통해 복잡한 로봇 작업의 효율적인 경로 및 동작 계획을 수립합니다.
*   **MLOps 파이프라인:** AI/ML 모델 학습 및 배포 파이프라인을 구축하고, 데이터셋 자동 생성, 실험 추적, 모델 버전 관리를 통해 개발 및 운영의 효율성을 높입니다.
*   **모듈형 아키텍처:** 각 기능이 독립적인 모듈로 설계되어 시스템의 확장성, 유지보수 용이성 및 유연한 통합을 지원합니다.
*   **안전 및 규정 준수:** 로봇 시스템의 안전 프로토콜 및 비상 정지 메커니즘을 설계하고, Sim2Real 안전성 검증 기준을 수립하여 법규 및 윤리적 가이드라인을 준수합니다.

### 👥 팀 구성

이 프로젝트는 다양한 전문 분야의 에이전트들이 협력하여 개발되었습니다.

*   **AI Orchestrator:** 전체 AI 에이전트 시스템의 전략적 방향 설정, 고수준 아키텍처 및 핵심 기술 의사결정 총괄, 프로젝트 비전 유지 및 에이전트 간 고수준 협업 조율.
*   **Project Coordinator:** 프로젝트의 일상적인 진행 상황 관리, 일정 및 자원 배분 지원, 에이전트 간의 실무 협업 촉진, 위험 요소 식별 및 보고, 모든 산출물 및 자료 체계적 관리 및 보관.
*   **Technical Architect:** 프로젝트의 전체 기술 아키텍처 설계 및 구현 표준화, 핵심 기술 스택 선정, 시스템 통합 및 확장성 확보, 도구 및 인프라 관리, API 인터페이스 정의.
*   **Robotics Simulation Engineer:** UR5e 로봇 모델 기반 Genesis 시뮬레이션 환경 구축 및 최적화, Sim2Real 갭 분석 및 시뮬레이터 정확도 향상, 로봇 궤적 및 동작 시각화 구현.
*   **Reinforcement Learning & Optimization Engineer:** 강화학습 및 최적화 알고리즘 설계/구현, 가상 제어기 학습 및 검증, 공정 프로그램 최적화 로직 개발 및 모델 개선 (RL > GA > Bayesian Optimization 우선순위 반영).
*   **MLOps Engineer:** AI/ML 모델 학습 및 배포 파이프라인 구축 및 관리, 데이터셋 자동 생성 및 처리 시스템 구현, 실험 추적 및 모델 버전 관리, 시스템 모니터링 및 데이터 거버넌스.
*   **Software Engineer:** URSim 인터페이스 및 UI 개발, RTDE 통신 레이어 구현, 데이터 로깅 시스템 및 명령어 라이브러리 통합, 백엔드 서비스 및 API 개발, 타 에이전트의 기술적 요구사항 지원.
*   **Robotics Safety & Compliance Engineer:** 로봇 시스템의 안전 프로토콜 및 비상 정지 메커니즘 설계, Sim2Real 안전성 검증 기준 수립, 법규 및 윤리적 가이드라인 준수 여부 검토 및 적용, 보안 취약점 분석 지원.
*   **QA Engineer:** 프로젝트의 모든 단계에서 품질 보증 및 검증 수행, 테스트 계획 수립 및 실행, 버그 보고 및 관리, Sim2Real 동작 일치도 및 성능 측정, 안전성 테스트 협력.
*   **AI Research Scientist:** 최신 AI/ML 기술 동향 분석 및 적용 가능성 탐색, 새로운 알고리즘 및 접근 방식 연구, 벤치마킹 및 성능 향상 방안 제안, 기술 보고서 작성 및 지식 공유.

### 📁 파일 구성

이 프로젝트의 주요 파일 및 디렉토리 구조는 다음과 같습니다.

```
.
├── src/
│   ├── learning/
│   │   └── offline_rl_data_processor.py  # 오프라인 강화학습 데이터 전처리 로직
│   ├── planning/
│   │   ├── task_planning_agent.py      # 고수준 작업 계획 에이전트
│   │   └── rrt_star_planner.py         # RRT* 기반 경로 계획 알고리즘
│   ├── data_models/
│   │   └── robot_state.py              # 로봇의 현재 상태를 정의하는 데이터 모델
│   ├── genesis_simulator.py            # Genesis 시뮬레이터와의 인터페이스 및 제어 로직
│   ├── rtde_client.py                  # UR 로봇의 RTDE(Real-Time Data Exchange) 클라이언트
│   ├── ur5e_commands.py                # UR5e 로봇 제어 명령어 라이브러리
│   └── app.py                          # 메인 애플리케이션 진입점 및 서비스 통합
├── config/
│   ├── architecture_settings.yaml      # 시스템 아키텍처 관련 전역 설정
│   └── ur5e_sim_config.yaml            # UR5e 시뮬레이션 환경 설정
├── docker-compose.yaml                 # Docker 컨테이너 오케스트레이션 설정
└── requirements.txt                    # Python 종속성 목록
```

### 🚀 시작하기

이 프로젝트를 로컬 환경에서 설정하고 실행하는 방법을 안내합니다.

#### 📋 전제 조건

*   Python 3.9+
*   Docker 및 Docker Compose (컨테이너 환경 사용 시)
*   Genesis 시뮬레이터 (시뮬레이션 환경 구축을 위해)
*   URSim (실제 로봇 또는 가상 UR 컨트롤러 연동 시)

#### 📦 설치

1.  **리포지토리 클론:**
    ```bash
    git clone https://github.com/your-org/sim2real_ur5e_v5.git
    cd sim2real_ur5e_v5
    ```
2.  **Python 종속성 설치:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Docker 환경 설정 (권장):**
    `docker-compose.yaml` 파일을 사용하여 필요한 서비스들을 컨테이너로 실행할 수 있습니다.
    ```bash
    docker-compose build
    docker-compose up -d
    ```

#### ▶️ 실행

1.  **시뮬레이터 및 UR 컨트롤러 준비:**
    *   Genesis 시뮬레이터를 실행하고 UR5e 모델을 로드합니다.
    *   URSim을 실행하거나 실제 UR5e 로봇을 준비합니다.
2.  **애플리케이션 실행:**
    *   **로컬 환경:**
        ```bash
        python src/app.py
        ```
    *   **Docker 환경:**
        ```bash
        docker-compose up
        # 또는 백그라운드 실행: docker-compose up -d
        ```
3.  **설정 확인:**
    `config/` 디렉토리의 `.yaml` 파일들을 통해 시뮬레이션, 로봇, 아키텍처 관련 설정을 조정할 수 있습니다.

### ⚙️ 설정

프로젝트의 다양한 동작은 `config/` 디렉토리 내의 YAML 파일들을 통해 설정할 수 있습니다.

*   `config/architecture_settings.yaml`: 시스템의 전반적인 아키텍처 및 모듈 간 통신 관련 설정.
*   `config/ur5e_sim_config.yaml`: UR5e 시뮬레이션 환경의 파라미터, 로봇 초기 자세, 물리적 특성 등 설정.

### 🤝 기여

이 프로젝트에 기여하고 싶으시다면 언제든지 환영합니다! 다음 단계를 따르세요:

1.  리포지토리를 포크합니다.
2.  새로운 기능 브랜치를 생성합니다 (`git checkout -b feature/AmazingFeature`).
3.  변경 사항을 커밋합니다 (`git commit -m 'Add some AmazingFeature'`).
4.  브랜치에 푸시합니다 (`git push origin feature/AmazingFeature`).
5.  Pull Request를 엽니다.

### 📄 라이선스

이 프로젝트는 MIT 라이선스에 따라 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하십시오.

---

© 2023 sim2real_ur5e_v5 Team. All rights reserved.