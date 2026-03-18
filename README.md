훌륭합니다! `sim2real_ur5e_v5` 프로젝트의 핵심 가치와 복잡성을 명확하게 전달하면서도, 개발자와 사용자 모두에게 유용한 정보를 제공하는 멋진 README.md를 작성해 드리겠습니다.

---

# sim2real_ur5e_v5: 지능형 UR5e 로봇 제어를 위한 Sim2Real 강화학습 플랫폼

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![Project Version](https://img.shields.io/badge/version-v5.0.0-orange)

## 목차

1.  [소개](#1-소개)
2.  [주요 기능](#2-주요-기능)
3.  [아키텍처 개요](#3-아키텍처-개요)
4.  [시작하기](#4-시작하기)
    *   [전제 조건](#전제-조건)
    *   [설치](#설치)
5.  [사용법](#5-사용법)
    *   [시뮬레이션 환경 실행](#시뮬레이션-환경-실행)
    *   [강화학습 에이전트 학습](#강화학습-에이전트-학습)
    *   [학습된 정책 시뮬레이션 검증](#학습된-정책-시뮬레이션-검증)
    *   [실제 로봇에 정책 배포 및 실행](#실제-로봇에-정책-배포-및-실행)
    *   [데이터 시각화 및 모니터링](#데이터-시각화-및-모니터링)
6.  [파일 구성](#6-파일-구성)
7.  [프로젝트 팀](#7-프로젝트-팀)
8.  [기여](#8-기여)
9.  [라이선스](#9-라이선스)

---

## 1. 소개

`sim2real_ur5e_v5` 프로젝트는 Universal Robots UR5e 협동 로봇의 지능형 제어를 위해 시뮬레이션 환경에서 학습된 강화학습(Reinforcement Learning, RL) 정책을 실제 로봇에 안전하고 효율적으로 전이시키는 것을 목표로 하는 최첨단 Sim2Real 플랫폼입니다.

복잡한 산업 및 연구 환경에서 로봇의 자율성과 적응성을 극대화하기 위해, 우리는 Genesis 시뮬레이션 환경에서 정교하게 모델링된 UR5e 로봇을 활용하여 다양한 작업 시나리오에 대한 최적의 제어 정책을 학습합니다. 이 학습된 정책은 견고한 Sim2Real 갭 분석 및 보정 메커니즘을 통해 실제 UR5e 로봇에 성공적으로 전이되며, MLOps 파이프라인을 통해 학습, 배포, 모니터링의 전 과정이 자동화됩니다.

`v5`라는 버전명은 이 프로젝트가 Sim2Real 기술의 여러 반복과 개선을 거쳐 현재의 높은 수준의 안정성과 성능을 달성했음을 의미합니다. 안전성, 규정 준수, 그리고 사용자 친화적인 인터페이스를 최우선으로 고려하여, 연구자와 개발자 모두에게 강력하고 신뢰할 수 있는 도구를 제공합니다.

## 2. 주요 기능

*   **AI 기반 지능형 로봇 제어:**
    *   강화학습(RL)을 통한 UR5e 로봇의 복잡한 작업 수행 능력 학습.
    *   유전 알고리즘(GA) 및 베이지안 최적화(Bayesian Optimization)를 활용한 공정 프로그램 및 가상 제어기 파라미터 최적화.
    *   최신 AI/ML 기술 동향을 반영한 알고리즘 설계 및 적용.
*   **고정밀 Sim2Real 전이:**
    *   UR5e 로봇 모델 기반의 Genesis 고정밀 시뮬레이션 환경 구축 및 최적화.
    *   시뮬레이터와 실제 로봇 간의 동작 및 성능 차이(Sim2Real 갭)를 분석하고 최소화하는 고급 기법 적용.
    *   로봇 궤적 및 동작의 실시간 시각화.
*   **견고한 MLOps 파이프라인:**
    *   AI/ML 모델 학습, 검증, 배포의 전 과정을 자동화하는 CI/CD 파이프라인.
    *   대규모 데이터셋 자동 생성, 처리 및 관리 시스템.
    *   실험 추적, 모델 버전 관리, 시스템 모니터링 및 데이터 거버넌스 기능.
*   **안전 및 규정 준수:**
    *   로봇 시스템의 안전 프로토콜 및 비상 정지(E-stop) 메커니즘 설계 및 구현.
    *   Sim2Real 전이 과정에서의 안전성 검증 기준 수립 및 테스트.
    *   관련 법규 및 윤리적 가이드라인 준수 여부 검토 및 적용.
    *   보안 취약점 분석 및 강화.
*   **모듈형 및 확장 가능한 아키텍처:**
    *   명확하게 분리된 에이전트 기반의 모듈형 시스템 설계로 높은 확장성 및 유지보수성 확보.
    *   URSim 인터페이스 및 UI 개발을 통한 직관적인 사용자 경험 제공.
    *   RTDE(Real-Time Data Exchange) 통신 레이어 구현 및 데이터 로깅 시스템 통합.

## 3. 아키텍처 개요

`sim2real_ur5e_v5`는 다양한 전문 에이전트들이 유기적으로 협력하는 분산형 아키텍처를 채택하고 있습니다.

```
+---------------------+      +---------------------+      +---------------------+
|   AI Orchestrator   |----->| Technical Architect |<-----|   Project Coord.    |
| (Strategic Control) |      | (System Design)     |      | (Mgmt & Oversight)  |
+---------------------+      +---------------------+      +---------------------+
       |                               |                               |
       v                               v                               v
+---------------------+      +---------------------+      +---------------------+
| Robotics Simulation |<---->| Reinforcement Learn.|<---->|   MLOps Engineer    |
|   Engineer (Genesis)|      |   & Optimization    |      | (CI/CD, Data, Mon.) |
+---------------------+      +---------------------+      +---------------------+
       ^                               |                               ^
       |                               v                               |
+---------------------+      +---------------------+      +---------------------+
|   Software Engineer |<---->| Robotics Safety &   |<---->|     QA Engineer     |
| (URSim, RTDE, UI)   |      | Compliance Engineer |      | (Testing, Validation)|
+---------------------+      +---------------------+      +---------------------+
       ^
       |
+---------------------+
|  AI Research Scientist |
| (Innovation & Bench.) |
+---------------------+
```

*   **전략 및 조율:** AI Orchestrator와 Project Coordinator가 프로젝트의 비전, 전략, 고수준 협업을 담당합니다.
*   **기술 기반:** Technical Architect가 전체 기술 아키텍처를 설계하고, Software Engineer가 핵심 인터페이스 및 백엔드를 구현합니다.
*   **핵심 지능:** Robotics Simulation Engineer가 시뮬레이션 환경을 제공하고, Reinforcement Learning & Optimization Engineer가 AI 에이전트를 학습시키며, AI Research Scientist가 최신 기술을 도입합니다.
*   **운영 및 품질:** MLOps Engineer가 학습 및 배포 파이프라인을 구축하고, QA Engineer가 전반적인 품질을 보증하며, Robotics Safety & Compliance Engineer가 안전성을 확보합니다.

## 4. 시작하기

### 전제 조건

이 프로젝트를 실행하기 위해서는 다음 환경이 필요합니다:

*   **운영체제:** Ubuntu 20.04 LTS 이상 (권장)
*   **Python:** 3.8 이상
*   **Docker & Docker Compose:** MLOps 파이프라인 및 서비스 컨테이너화를 위해 필요합니다.
*   **Genesis Simulator:** UR5e 로봇 시뮬레이션 환경 (라이선스 필요)
*   **URSim (Universal Robots Simulator):** 실제 로봇 제어 로직 테스트 및 UI 연동을 위해 필요합니다.
*   **NVIDIA GPU:** 강화학습 모델 학습을 위한 CUDA 지원 GPU (권장).

### 설치

1.  **리포지토리 클론:**
    ```bash
    git clone https://github.com/your-org/sim2real_ur5e_v5.git
    cd sim2real_ur5e_v5
    ```

2.  **Python 환경 설정:**
    `conda` 또는 `venv`를 사용하여 가상 환경을 생성하고 활성화하는 것을 권장합니다.
    ```bash
    # Conda 사용 시
    conda create -n sim2real_ur5e_v5 python=3.9
    conda activate sim2real_ur5e_v5

    # 또는 venv 사용 시
    python3.9 -m venv venv
    source venv/bin/activate
    ```

3.  **Python 의존성 설치:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Genesis Simulator 설정:**
    Genesis Simulator를 설치하고, UR5e 로봇 모델 및 시뮬레이션 환경이 올바르게 로드되는지 확인합니다. `configs/genesis_config.yaml` 파일을 프로젝트 요구사항에 맞게 설정합니다.

5.  **URSim 설정:**
    URSim을 설치하고, 로봇 컨트롤러의 IP 주소 및 통신 설정을 `configs/robot_config.yaml`에 맞게 구성합니다.

6.  **Docker 서비스 빌드 (MLOps 관련):**
    데이터 처리, 모델 서빙 등 MLOps 관련 서비스는 Docker 컨테이너로 관리됩니다.
    ```bash
    docker-compose build
    ```

## 5. 사용법

### 시뮬레이션 환경 실행

Genesis 시뮬레이터를 백그라운드에서 실행하고, 로봇 환경을 초기화합니다.
```bash
python scripts/start_genesis_sim.py --config configs/genesis_env.yaml
```
(Genesis GUI가 필요한 경우, 별도로 실행 후 스크립트가 연결되도록 설정할 수 있습니다.)

### 강화학습 에이전트 학습

설정 파일에 정의된 파라미터를 기반으로 강화학습 에이전트를 학습시킵니다.
```bash
python src/rl_optimization/train_agent.py --config configs/rl_agent_ppo.yaml
```
학습 진행 상황은 `runs/` 디렉토리에 TensorBoard 로그로 저장됩니다.

### 학습된 정책 시뮬레이션 검증

학습된 모델을 Genesis 시뮬레이션 환경에서 실행하여 성능과 동작을 검증합니다.
```bash
python src/simulation/simulate_policy.py --model_path models/latest_ppo_agent.pth --episodes 10
```
이 스크립트는 로봇의 궤적과 목표 달성 여부를 시각화합니다.

### 실제 로봇에 정책 배포 및 실행

**경고:** 실제 로봇을 제어할 때는 항상 안전 수칙을 준수하고 비상 정지 버튼에 손을 가까이 두십시오.

학습된 정책을 실제 UR5e 로봇에 배포하고 실행합니다.
```bash
python src/robot_interface/deploy_real_robot.py --model_path models/real_world_policy_v5.pth --robot_ip 192.168.1.100
```
이 명령어는 RTDE 통신을 통해 로봇을 제어하며, UI를 통해 실시간 상태를 모니터링할 수 있습니다.

### 데이터 시각화 및 모니터링

학습 로그, 로봇 데이터, 시스템 메트릭 등을 TensorBoard 또는 커스텀 대시보드를 통해 시각화하고 모니터링합니다.
```bash
tensorboard --logdir runs/
```
MLOps 대시보드는 `http://localhost:8080` (설정된 포트에 따라 다름)에서 접근 가능합니다.

## 6. 파일 구성

```
sim2real_ur5e_v5/
├── .github/                       # GitHub Actions (CI/CD 파이프라인)
│   └── workflows/
│       └── main_ci.yml
├── docs/                          # 프로젝트 문서, 기술 보고서, API 문서
│   └── architecture.md
│   └── safety_guidelines.md
├── src/                           # 핵심 소스 코드
│   ├── orchestrator/              # AI Orchestrator 로직
│   │   └── __init__.py
│   │   └── main_orchestrator.py
│   ├── simulation/                # Genesis 시뮬레이션 환경 및 로봇 모델
│   │   └── __init__.py
│   │   └── genesis_env.py
│   │   └── ur5e_model.py
│   │   └── sim_gap_analyzer.py
│   ├── rl_optimization/           # 강화학습 및 최적화 알고리즘 구현
│   │   └── __init__.py
│   │   └── agents/
│   │   └── algorithms/ (PPO, SAC, GA, Bayesian Opt.)
│   │   └── virtual_controller.py
│   │   └── train_agent.py
│   ├── robot_interface/           # URSim, RTDE 통신, UI, 데이터 로깅
│   │   └── __init__.py
│   │   └── ursim_interface.py
│   │   └── rtde_client.py
│   │   └── ui/
│   │   └── data_logger.py
│   ├── safety_compliance/         # 안전 프로토콜, 비상 정지 로직
│   │   └── __init__.py
│   │   └── safety_monitor.py
│   │   └── e_stop_handler.py
│   ├── mlops/                     # MLOps 파이프라인 스크립트, 모니터링
│   │   └── __init__.py
│   │   └── data_pipeline.py
│   │   └── model_deployment.py
│   │   └── monitoring_service.py
│   ├── utils/                     # 공통 유틸리티 함수 및 헬퍼 스크립트
│   │   └── __init__.py
│   │   └── config_parser.py
│   │   └── visualization.py
│   └── __init__.py
├── configs/                       # 설정 파일 (YAML)
│   ├── genesis_env.yaml
│   ├── rl_agent_ppo.yaml
│   ├── robot_config.yaml
│   └── mlops_pipeline.yaml
├── data/                          # 데이터셋, 학습 로그, 로봇 센서 데이터
│   ├── raw/
│   ├── processed/
│   └── logs/
├── models/                        # 학습된 AI/ML 모델 저장소
│   ├── latest_ppo_agent.pth
│   └── real_world_policy_v5.pth
├── tests/                         # 테스트 코드 (단위, 통합, 안전성, Sim2Real 일치도)
│   ├── unit/
│   ├── integration/
│   ├── safety/
│   └── sim2real/
├── scripts/                       # 보조 스크립트 (환경 설정, 데이터 생성 등)
│   └── start_genesis_sim.py
│   └── generate_dataset.py
├── requirements.txt               # Python 의존성 목록
├── Dockerfile                     # Docker 컨테이너 빌드 파일
├── docker-compose.yml             # Docker Compose 설정 파일
└── README.md                      # 이 파일
```

## 7. 프로젝트 팀

이 프로젝트는 다음의 전문화된 에이전트들의 긴밀한 협력을 통해 개발되었습니다.

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

## 8. 기여

`sim2real_ur5e_v5` 프로젝트에 기여하고 싶으시다면, 언제든지 환영합니다! 다음 가이드라인을 따라주세요:

1.  이슈를 생성하여 제안 사항이나 버그를 보고합니다.
2.  `develop` 브랜치에서 새 브랜치를 생성하고 작업합니다.
3.  커밋 메시지는 명확하고 간결하게 작성합니다.
4.  새로운 기능에는 반드시 테스트 코드를 포함합니다.
5.  풀 리퀘스트(PR)를 생성하고, 관련 이슈를 참조합니다.

자세한 내용은 `CONTRIBUTING.md` 파일을 참조해주세요.

## 9. 라이선스

이 프로젝트는 MIT 라이선스에 따라 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하십시오.

---