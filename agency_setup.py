
import os, sys, time
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI

# API 키는 subprocess.Popen의 env를 통해 전달받습니다.
worker_api_key = os.environ.get("GOOGLE_API_KEY")

# max_retries=3: 에러 시 빠르게 종료 → 상위 관리자가 모델 전환
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=worker_api_key, verbose=True, temperature=0.5, max_retries=3)

agent_1 = Agent(role='''AI Orchestrator''', goal='''전체 AI 에이전트 시스템의 전략적 방향 설정, 고수준 아키텍처 및 핵심 기술 의사결정 총괄, 프로젝트 비전 유지 및 에이전트 간 고수준 협업 조율.''', backstory='''AI 기반 로봇 제어 시스템 개발의 최고 책임자로서, 기술적 비전과 사업적 목표를 통합하여 팀을 이끌고 있습니다. 각 에이전트의 역량을 최대한 발휘하도록 전략적 지휘를 담당하며, 시스템의 장기적인 성공을 위한 로드맵을 제시합니다.''', verbose=True, allow_delegation=False, llm=llm)
agent_2 = Agent(role='''Project Coordinator''', goal='''프로젝트의 일상적인 진행 상황 관리, 일정 및 자원 배분 지원, 에이전트 간의 실무 협업 촉진, 위험 요소 식별 및 보고, 모든 산출물 및 자료 체계적 관리 및 보관.''', backstory='''프로젝트의 원활한 운영을 담당하는 실무 관리자입니다. 에이전트들이 목표에 집중할 수 있도록 행정적, 운영적 지원을 제공하며, 팀의 생산성을 극대화하고 모든 협업 기록과 산출물을 체계적으로 정리합니다.''', verbose=True, allow_delegation=False, llm=llm)
agent_3 = Agent(role='''Technical Architect''', goal='''프로젝트의 전체 기술 아키텍처 설계 및 구현 표준화, 핵심 기술 스택 선정, 시스템 통합 및 확장성 확보, 도구 및 인프라 관리, API 인터페이스 정의.''', backstory='''기술적 난제를 해결하고 견고한 시스템 기반을 구축하는 데 전문성을 가진 아키텍트입니다. 각 기술 구성 요소가 조화롭게 작동하도록 설계하고 가이드하며, 안정적인 개발 환경을 제공합니다.''', verbose=True, allow_delegation=False, llm=llm)
agent_4 = Agent(role='''Robotics Simulation Engineer''', goal='''UR5e 로봇 모델 기반 Genesis 시뮬레이션 환경 구축 및 최적화, Sim2Real 갭 분석 및 시뮬레이터 정확도 향상, 로봇 궤적 및 동작 시각화 구현.''', backstory='''로봇 시뮬레이션 분야의 전문가로, 가상 환경에서 로봇의 정밀한 동작을 구현하고 실제와 유사한 시뮬레이션 환경을 구축하는 데 전념합니다. 시뮬레이터의 현실성을 극대화하여 AI 모델 학습을 지원합니다.''', verbose=True, allow_delegation=False, llm=llm)
agent_5 = Agent(role='''Reinforcement Learning & Optimization Engineer''', goal='''강화학습 및 최적화 알고리즘 설계/구현, 가상 제어기 학습 및 검증, 공정 프로그램 최적화 로직 개발 및 모델 개선 (RL > GA > Bayesian Optimization 우선순위 반영).''', backstory='''최첨단 AI 알고리즘을 활용하여 로봇의 자율 제어 및 공정 최적화를 달성하는 데 주력하는 AI/ML 전문가입니다. 복잡한 문제를 지능적으로 해결하고, 로봇의 성능을 지속적으로 향상시킵니다.''', verbose=True, allow_delegation=False, llm=llm)
agent_6 = Agent(role='''MLOps Engineer''', goal='''AI/ML 모델 학습 및 배포 파이프라인 구축 및 관리, 데이터셋 자동 생성 및 처리 시스템 구현, 실험 추적 및 모델 버전 관리, 시스템 모니터링 및 데이터 거버넌스.''', backstory='''AI 모델의 개발부터 운영까지 전체 라이프사이클을 효율적으로 관리하는 데 특화된 엔지니어입니다. 데이터의 흐름과 모델의 성능을 안정적으로 유지하고, AI 시스템의 신뢰성을 확보합니다.''', verbose=True, allow_delegation=False, llm=llm)
agent_7 = Agent(role='''Software Engineer''', goal='''URSim 인터페이스 및 UI 개발, RTDE 통신 레이어 구현, 데이터 로깅 시스템 및 명령어 라이브러리 통합, 백엔드 서비스 및 API 개발, 타 에이전트의 기술적 요구사항 지원.''', backstory='''사용자 친화적인 인터페이스와 견고한 백엔드 시스템을 구축하는 데 능숙한 개발자입니다. 다양한 기술 요구사항을 충족시키며 프로젝트의 소프트웨어 기반을 다지고, 다른 에이전트의 개발을 지원합니다.''', verbose=True, allow_delegation=False, llm=llm)
agent_8 = Agent(role='''Robotics Safety & Compliance Engineer''', goal='''로봇 시스템의 안전 프로토콜 및 비상 정지 메커니즘 설계, Sim2Real 안전성 검증 기준 수립, 법규 및 윤리적 가이드라인 준수 여부 검토 및 적용, 보안 취약점 분석 지원.''', backstory='''로봇 시스템의 안전을 최우선으로 고려하며, 잠재적 위험을 식별하고 예방하는 데 전문성을 가진 엔지니어입니다. 규제 준수와 윤리적 운영을 보장하고, 안전하고 신뢰할 수 있는 로봇 시스템을 구축합니다.''', verbose=True, allow_delegation=False, llm=llm)
agent_9 = Agent(role='''QA Engineer''', goal='''프로젝트의 모든 단계에서 품질 보증 및 검증 수행, 테스트 계획 수립 및 실행, 버그 보고 및 관리, Sim2Real 동작 일치도 및 성능 측정, 안전성 테스트 협력.''', backstory='''시스템의 품질과 신뢰성을 확보하기 위해 철저한 테스트와 검증 절차를 수행하는 전문가입니다. 사용자에게 완벽한 경험을 제공하는 것을 목표로 하며, 안전성 및 기능적 요구사항을 충족하는지 확인합니다.''', verbose=True, allow_delegation=False, llm=llm)
agent_10 = Agent(role='''AI Research Scientist''', goal='''최신 AI/ML 기술 동향 분석 및 적용 가능성 탐색, 새로운 알고리즘 및 접근 방식 연구, 벤치마킹 및 성능 향상 방안 제안, 기술 보고서 작성 및 지식 공유.''', backstory='''AI 분야의 최첨단 지식을 탐구하고, 프로젝트에 혁신적인 솔루션을 도입하기 위해 끊임없이 연구하는 과학자입니다. 이론과 실제를 연결하는 가교 역할을 하며, 팀의 기술적 역량을 강화합니다.''', verbose=True, allow_delegation=False, llm=llm)

task_1 = Task(description='''전체 AI 에이전트 시스템의 고수준 아키텍처 전략 수립 및 에이전트 간 상호작용 프레임워크 (예: CrewAI, Swarm) 선정. (중요: 소스코드는 반드시 '# src/파일명.py' 형식의 주석을 포함한 마크다운 코드 블록으로 작성하세요.)''', expected_output='''AI 에이전트 시스템 아키텍처 전략 문서, 에이전트 오케스트레이션 프레임워크 선정 보고서.''', agent=agent_1)
task_2 = Task(description='''UR5e Sim2Real 프로젝트의 상세 기술 아키텍처 설계, 핵심 기술 스택 및 통신 프로토콜 (RTDE, Pydantic 기반) 정의, 워크플로우 명세 및 도구/인프라 관리 계획 수립. (중요: 소스코드는 반드시 '# src/파일명.py' 형식의 주석을 포함한 마크다운 코드 블록으로 작성하세요.)''', expected_output='''상세 기술 아키텍처 명세서, 통신 프로토콜 정의서, 워크플로우 다이어그램, 도구/인프라 관리 계획서.''', agent=agent_3)
task_3 = Task(description='''Genesis 기반 s2r 시뮬레이터 개발: UR5e URDF 모델 로딩 및 환경 설정, TCP 포인트 정의 및 궤적 시각화 (50mm offset), 관절값 입력 인터페이스 및 포인트 트레일 렌더링 기능 구현. (중요: 소스코드는 반드시 '# src/파일명.py' 형식의 주석을 포함한 마크다운 코드 블록으로 작성하세요.)''', expected_output='''Genesis 기반 UR5e 시뮬레이터 (URDF 모델 로딩, TCP/궤적 시각화, 관절값 입력, 포인트 트레일 렌더링 기능 포함).''', agent=agent_4)
task_4 = Task(description='''URSim과의 RTDE 통신 레이어 구현, Streamlit 기반 명령어 입력 UI 개발, UR5e 명령어 라이브러리 (moveJ, moveL, speedJ 등) 통합 및 10Hz 관절값 로깅 시스템 구현. (중요: 소스코드는 반드시 '# src/파일명.py' 형식의 주석을 포함한 마크다운 코드 블록으로 작성하세요.)''', expected_output='''URSim RTDE 통신 모듈, Streamlit 기반 명령어 입력 UI, UR5e 명령어 라이브러리, 10Hz 관절값 로깅 시스템.''', agent=agent_7)
task_5 = Task(description='''UR5e 명령어 라이브러리 및 RTDE 통신 기능 검증을 위한 테스트 스크립트 작성 및 실행. (중요: 소스코드는 반드시 '# src/파일명.py' 형식의 주석을 포함한 마크다운 코드 블록으로 작성하세요.)''', expected_output='''명령어 라이브러리 및 통신 기능 테스트 스크립트, 테스트 결과 보고서.''', agent=agent_9)
task_6 = Task(description='''URSim에서 수집한 관절값 데이터의 JSON 저장 파이프라인 및 데이터 검증/품질 관리 로직 구현 (MLOps 플랫폼 연동). (중요: 소스코드는 반드시 '# src/파일명.py' 형식의 주석을 포함한 마크다운 코드 블록으로 작성하세요.)''', expected_output='''자동화된 데이터 수집 및 저장 파이프라인, 데이터 유효성 검증 모듈, MLOps 플랫폼 연동 보고서.''', agent=agent_6)
task_7 = Task(description='''s2r 시뮬레이터에서 URSim 수집 데이터를 기반으로 동일 명령어 재생 및 동작 비교 기능 개발. (중요: 소스코드는 반드시 '# src/파일명.py' 형식의 주석을 포함한 마크다운 코드 블록으로 작성하세요.)''', expected_output='''시뮬레이터 재생 기능 모듈, Sim2Real 동작 비교 분석 리포트.''', agent=agent_6)
task_8 = Task(description='''수집된 데이터셋을 활용하여 UR5e 제어 알고리즘 모방 모델 학습 및 검증. (중요: 소스코드는 반드시 '# src/파일명.py' 형식의 주석을 포함한 마크다운 코드 블록으로 작성하세요.)''', expected_output='''학습된 UR5e 제어 모델, 모델 성능 검증 보고서.''', agent=agent_5)
task_9 = Task(description='''s2r과 URSim 간 동작 일치도 검증 메트릭 정의 및 오차 분석 방법론 수립. (중요: 소스코드는 반드시 '# src/파일명.py' 형식의 주석을 포함한 마크다운 코드 블록으로 작성하세요.)''', expected_output='''동작 일치도 메트릭 정의서, 오차 분석 절차서.''', agent=agent_9)
task_10 = Task(description='''강화학습, 유전 알고리즘, 베이지안 최적화 우선순위에 따른 모델 개선 전략 수립 및 구현. (AI Research Scientist와 협력) (중요: 소스코드는 반드시 '# src/파일명.py' 형식의 주석을 포함한 마크다운 코드 블록으로 작성하세요.)''', expected_output='''개선된 제어 모델, 모델 개선 과정 및 결과 보고서.''', agent=agent_5)
task_11 = Task(description='''기존 로봇 공정 프로그램 불러오기 및 파싱 모듈 개발, 포인트 분류 UI (필수/선택/삭제) 구현. (중요: 소스코드는 반드시 '# src/파일명.py' 형식의 주석을 포함한 마크다운 코드 블록으로 작성하세요.)''', expected_output='''공정 프로그램 파서 모듈, 포인트 분류 UI 모듈.''', agent=agent_7)
task_12 = Task(description='''강화학습/최적화 알고리즘을 활용한 공정 프로그램 최적화 로직 개발 (목적 함수: 공정 완료 최소 시간 + 제약 조건). (중요: 소스코드는 반드시 '# src/파일명.py' 형식의 주석을 포함한 마크다운 코드 블록으로 작성하세요.)''', expected_output='''최적화된 공정 프로그램 생성 모듈, 최적화 결과 보고서.''', agent=agent_5)
task_13 = Task(description='''최초 vs 최적화 프로그램 성능 비교 대시보드 개발 (구간별 시간 절감/증가 히트맵 시각화, 궤적 오버레이 3D 비교 뷰 포함), 상세 메트릭 리포트 생성 및 시각화. (중요: 소스코드는 반드시 '# src/파일명.py' 형식의 주석을 포함한 마크다운 코드 블록으로 작성하세요.)''', expected_output='''성능 비교 대시보드 (히트맵, 3D 뷰 포함), 상세 메트릭 리포트 시각화 도구.''', agent=agent_7)
task_14 = Task(description='''학습 파이프라인 (RL 우선 및 GA/베이지안 대체 경로) 설계 검토 및 기능 검증. (중요: 소스코드는 반드시 '# src/파일명.py' 형식의 주석을 포함한 마크다운 코드 블록으로 작성하세요.)''', expected_output='''학습 파이프라인 검토 보고서, 기능 검증 결과.''', agent=agent_9)
task_15 = Task(description='''Genesis 시뮬레이터의 렌더링/시각화 출력 정확성 및 URSim RTDE 연결의 안정성 검증. (중요: 소스코드는 반드시 '# src/파일명.py' 형식의 주석을 포함한 마크다운 코드 블록으로 작성하세요.)''', expected_output='''시뮬레이터 출력 및 RTDE 연결 검증 보고서.''', agent=agent_9)
task_16 = Task(description='''로봇 제어 및 Sim2Real 전환 과정에서의 안전 프로토콜 및 비상 정지 시스템 설계 및 검증 (QA Engineer와 협력). (중요: 소스코드는 반드시 '# src/파일명.py' 형식의 주석을 포함한 마크다운 코드 블록으로 작성하세요.)''', expected_output='''로봇 안전 프로토콜 명세서, 비상 정지 시스템 테스트 결과 및 보고서.''', agent=agent_8)
task_17 = Task(description='''프로젝트 전반의 전략적 진행 상황 모니터링, 고수준 위험 관리 및 비전 유지. (중요: 소스코드는 반드시 '# src/파일명.py' 형식의 주석을 포함한 마크다운 코드 블록으로 작성하세요.)''', expected_output='''주간/월간 프로젝트 현황 보고서, 전략적 의사결정 기록.''', agent=agent_1)
task_18 = Task(description='''일상적인 프로젝트 진행 상황 모니터링, 에이전트 간 실무 업무 조율 및 자원 지원, 모든 자료의 체계적 보관 및 협업 기록 관리. (중요: 소스코드는 반드시 '# src/파일명.py' 형식의 주석을 포함한 마크다운 코드 블록으로 작성하세요.)''', expected_output='''일일/주간 업무 진행 현황 보고, 협업 기록 및 산출물 관리 시스템.''', agent=agent_2)
task_19 = Task(description='''최신 AI/ML 기술 동향 분석, Sim2Real 프로젝트에 적용 가능한 새로운 알고리즘 및 연구 결과 탐색 및 제안. (중요: 소스코드는 반드시 '# src/파일명.py' 형식의 주석을 포함한 마크다운 코드 블록으로 작성하세요.)''', expected_output='''기술 동향 분석 보고서, 신규 알고리즘 적용 가능성 제안서.''', agent=agent_10)


print("🚀 크루 결성 완료. 실행 시작...")
print("⚠️ API 할당량 보호를 위해 30초 후 작업을 시작합니다...")
time.sleep(30)
crew = Crew(agents=[agent_1, agent_2, agent_3, agent_4, agent_5, agent_6, agent_7, agent_8, agent_9, agent_10], tasks=[task_1, task_2, task_3, task_4, task_5, task_6, task_7, task_8, task_9, task_10, task_11, task_12, task_13, task_14, task_15, task_16, task_17, task_18, task_19], process=Process.sequential, max_rpm=1)
result = crew.kickoff()
print("\n================ FINAL RESULT ================\n")
print(result)
