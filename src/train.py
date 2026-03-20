
- **기대 효과:**
    - **품질 보증:** 모든 데이터는 검증 절차를 통과해야만 시스템에 통합됩니다 (Data CI).
    - **신속한 피드백:** 데이터 관련 문제가 발생하면 개발자는 PR 단계에서 즉시 알 수 있습니다.

#### 3.3. 실험 추적 및 모델 관리: MLflow

- **목적:** 어떤 데이터 버전으로 학습된 모델이 어떤 성능을 내는지 체계적으로 추적하고 관리합니다.
- **워크플로우:**
    1.  모델 학습 스크립트(`src/train.py`)는 DVC API를 사용하여 특정 버전의 데이터를 로드합니다.
    2.  학습 과정에서 MLflow Tracking을 사용하여 주요 정보를 로깅합니다.

    ```python
    # src/train.py (예시)
    import mlflow
    import dvc.api
    import pandas as pd

    # DVC로 데이터 로드
    data_path = 'data/raw/joint_log_20240523_103000.jsonl'
    repo_url = 'https://github.com/your-org/UR5e_Sim2Real.git'
    data_version = 'v1.2' # Git 태그 또는 커밋 해시

    # 특정 버전의 데이터 URL 가져오기
    data_url = dvc.api.get_url(path=data_path, repo=repo_url, rev=data_version)
    
    # 데이터프레임으로 로드
    df = pd.read_json(data_url, lines=True)

    with mlflow.start_run() as run:
        # 1. 사용된 데이터 정보 로깅
        mlflow.log_param("data_path", data_path)
        mlflow.log_param("data_version", data_version)
        mlflow.log_param("data_records", len(df))

        # 2. 모델 하이퍼파라미터 로깅
        mlflow.log_param("learning_rate", 0.001)

        # ... (모델 학습 로직) ...
        
        # 3. 모델 성능 메트릭 로깅
        mlflow.log_metric("mse", 0.05)

        # 4. 학습된 모델 아티팩트 로깅
        mlflow.pytorch.log_model(model, "model")
    ```

- **기대 효과:**
    - **완벽한 추적성:** "어떤 모델이 어떤 데이터와 코드로 만들어졌는가?"라는 질문에 항상 답할 수 있습니다.
    - **체계적인 모델 관리:** MLflow Model Registry를 통해 학습된 모델을 스테이징, 프로덕션 단계로 승격시키고 관리할 수 있습니다.

### 4. 결론

제시된 데이터 파이프라인과 MLOps 연동 계획은 UR5e Sim2Real 프로젝트의 데이터 자산을 체계적으로 관리하고, 이를 기반으로 신뢰도 높은 AI 모델을 개발하기 위한 핵심적인 기반을 제공합니다. 이 워크플로우를 통해 팀은 데이터 품질 문제로 인한 시간 낭비를 줄이고, 모델 개발 및 개선 주기를 가속화할 수 있습니다.