# sim2real_ur5e_v5

![Status](https://img.shields.io/badge/Status-In%20Progress-yellowgreen)
![License](https://img.shields.io/badge/License-MIT-blue.svg)

## 프로젝트 개요

`sim2real_ur5e_v5`는 Universal Robots UR5e 로봇을 위한 Sim2Real(시뮬레이션-실제) 학습 및 제어 시스템을 구축하는 혁신적인 프로젝트입니다. 이 프로젝트는 강화학습(RL) 기반의 가상 제어기 개발부터 실제 로봇과의 RTDE(Real-Time Data Exchange) 통신을 통한 연동, 그리고 시스템의 안전성 및 공정 최적화까지 포괄하는 엔드-투-엔드 솔루션을 목표로 합니다. 최신 AI/ML 기술과 로봇 공학을 결합하여 시뮬레이션에서 학습된 지능형 제어 전략을 실제 환경에 성공적으로 전이시키는 것을 핵심 과제로 삼고 있습니다.

## 목차
- [주요 기능](#주요-기능)
- [팀 구성](#팀-구성)
- [파일 구성](#파일-구성)
- [시작하기](#시작하기)
    - [사전 요구 사항](#사전-요구-사항)
    - [설치](#설치)
    - [환경 설정](#환경-설정)
    - [실행](#실행)

## 주요 기능

*   **UR5e Sim2Real 환경 구축:** UR5e 로봇 모델 기반의 Genesis 시뮬레이션 환경을 구축하고, Sim2Real 갭 분석 및 시뮬레이터 정확도 향상을 통해 실제 환경과의 일치도를 극대화합니다.
*   **지능형 제어 및 최적화:** 강화학습(RL), 유전 알고리즘(GA), 베이지안 최적화(Bayesian Optimization)를 활용하여 가상 제어기를 학습하고, 로봇 공정 프로그램을 최적화합니다.
*   **실시간 로봇 통신:** URSim 인터페이스 및 RTDE(Real-Time Data Exchange) 통신 레이어 구현을 통해 실제 UR5e 로봇과 실시간으로 데이터를 교환하고 명령을 제어합니다.
*   **MLOps 파이프라인:** AI/ML 모델 학습 및 배포 파이프라인을 구축하고 관리하며, 데이터셋 자동 생성 및 처리, 실험 추적, 모델 버전 관리, 시스템 모니터링을 지원합니다.
*   **안전 및 규정 준수:** 로봇 시스템의 안전 프로토콜 및 비상 정지 메커니즘을 설계하고, Sim2Real 안전성 검증 기준을 수립하여 법규 및 윤리적 가이드라인을 준수합니다.
*   **데이터 로깅 및 관리:** 체계적인 데이터 로깅 시스템과 명령어 라이브러리를 통합하여 로봇 동작 및 학습 데이터를 효율적으로 수집하고 관리합니다.

## 팀 구성

이 프로젝트는 다양한 전문성을 가진 팀원들의 협업으로 진행됩니다.

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

## 파일 구성

프로젝트의 주요 파일 및 디렉토리 구조는 다음과 같습니다.

```
.
├── config/
│   └── rtde_config.yaml         # UR 로봇과의 RTDE(Real-Time Data Exchange) 통신을 위한 설정 파일
├── infra/
│   └── docker-compose.yml       # Docker Compose를 사용하여 프로젝트의 여러 서비스(MLOps, 백엔드 등) 오케스트레이션을 정의하는 파일
├── src/
│   ├── core/
│   │   └── schemas.py           # 데이터 모델 및 유효성 검사를 위한 Pydantic 스키마 정의
│   ├── hardware/
│   │   └── rtde_client.py       # UR 로봇과의 RTDE 통신을 처리하고 데이터를 주고받는 클라이언트 구현
│   └── controller_interface.py  # 로봇 제어 로직 및 시뮬레이션/실제 로봇 인터페이스를 정의하는 핵심 파일
└── requirements.txt             # 프로젝트에 필요한 Python 패키지 및 라이브러리 목록
```

## 시작하기

### 사전 요구 사항

*   **Python 3.8+**: 프로젝트의 주요 개발 언어입니다.
*   **Docker 및 Docker Compose**: 컨테이너 기반 환경 구축 및 서비스 오케스트레이션에 사용됩니다.
*   **URSim (Universal Robots Simulator) 또는 실제 UR5e 로봇 환경**: 로봇 시뮬레이션 또는 실제 로봇 제어를 위해 필요합니다.
*   **Git**: 소스 코드 관리를 위해 필요합니다.

### 설치

1.  **저장소 클론:**
    ```bash
    git clone https://github.com/your-org/sim2real_ur5e_v5.git
    cd sim2real_ur5e_v5
    ```

2.  **Python 의존성 설치:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Docker 환경 설정 및 빌드 (선택 사항, MLOps 및 서비스 배포 시):**
    ```bash
    docker-compose build
    ```

### 환경 설정

*   `config/rtde_config.yaml`: UR 로봇과의 RTDE 통신을 위한 IP 주소, 포트, 데이터 레시피 등을 설정합니다. 실제 로봇 또는 URSim 환경의 네트워크 설정에 맞게 수정해야 합니다.

    ```yaml
    # config/rtde_config.yaml 예시
    robot_ip: "192.168.1.100" # 실제 로봇 또는 URSim의 IP 주소
    port: 30004
    output_recipe:
      - "actual_q"
      - "actual_qd"
    input_recipe:
      - "speedj_target"
    ```

### 실행

프로젝트의 실행 방식은 구성 요소에 따라 다를 수 있습니다.

1.  **RTDE 클라이언트 실행 (로봇 통신):**
    UR 로봇 또는 URSim과의 실시간 통신을 시작합니다.
    ```bash
    python src/hardware/rtde_client.py
    ```
    *이 명령은 `rtde_config.yaml`에 정의된 설정에 따라 UR 로봇과 통신을 시작하고 데이터를 주고받을 준비를 합니다.*

2.  **컨트롤러 인터페이스 실행 (시뮬레이션/제어 로직):**
    로봇 제어 로직을 담당하며, 시뮬레이션 환경 또는 실제 로봇과의 상호작용을 조율합니다.
    ```bash
    python src/controller_interface.py
    ```
    *이 스크립트는 학습된 제어 정책을 로봇에 적용하거나 시뮬레이션 환경에서 로봇을 제어하는 핵심 역할을 수행합니다.*

3.  **Docker Compose를 통한 서비스 실행 (전체 시스템):**
    MLOps 파이프라인, 백엔드 서비스 등 여러 구성 요소를 함께 실행해야 하는 경우 `docker-compose`를 사용할 수 있습니다.
    ```bash
    docker-compose up -d
    ```
    *자세한 서비스 구성 및 오케스트레이션은 `infra/docker-compose.yml` 파일을 참조하십시오.*

---

© 2023 sim2real_ur5e_v5 Team. All rights reserved.