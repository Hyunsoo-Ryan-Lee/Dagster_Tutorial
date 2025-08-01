# Dagster_Tutorial

## 🎯 파일 구성

### 1. 기본 개념 (dg01-dg03)
- **dg01**: Asset과 Job의 기본 개념
- **dg02**: 조건부 분기 처리
- **dg03**: 분기 후 결과 통합

### 2. 데이터 처리 (dg04-dg05)
- **dg04**: Multi Asset을 통한 데이터 변환
- **dg05**: API → GCS → BigQuery 파이프라인

### 3. 센서와 트리거 (dg06)
- **dg06_pre**: 센서 트리거 전 데이터 수집
- **dg06_post**: GCS 파일 감지 후 BigQuery 저장

### 4. 리소스 관리 (dg07-dg10)
- **dg07**: API 클라이언트 리소스
- **dg08**: 데이터베이스 연결 리소스
- **dg09**: GCP 서비스 리소스
- **dg10**: AWS 서비스 리소스

### 5. 고급 기능 (dg11-dg14)
- **dg11**: Graph Asset으로 작업 그룹화
- **dg12**: Graph Multi Asset으로 복잡한 파이프라인
- **dg13**: 파티션을 통한 대용량 데이터 처리
- **dg14**: Asset 품질 검증 및 체크

## 🔧 주요 구성 요소

### Resources (resources.py)
다양한 외부 서비스와의 연결을 관리합니다:

```python
# 지원하는 리소스들
- api_client: HTTP API 호출
- mysql_connection: MySQL 데이터베이스 연결
- postgres_connection: PostgreSQL 데이터베이스 연결
- bq_client: BigQuery 클라이언트
- gcs_client: Google Cloud Storage 클라이언트
- s3_client: AWS S3 클라이언트
- glue_client: AWS Glue 클라이언트
```

### Utils (utils.py)
공통 유틸리티 함수들을 제공합니다:

```python
- get_bq_client(): BigQuery 클라이언트 생성
- get_gcs_client(): GCS 클라이언트 생성
- data_transformer(): 데이터 변환 함수
```

## 🚀 실행 방법

### 1. 환경 설정 (.env 파일)
```bash
# 필요한 환경 변수 설정
GCP_PROJECT_ID="your-project-id"
GCP_CREDENTIALS_PATH="path/to/credentials.json"
GCS_BUCKET_NAME="your-bucket-name"
API_CLIENT_BASE_URL="https://api.openbrewerydb.org/v1/breweries"
MYSQL_CONN_VAL="mysql://user:pass@host:port/db"
POSTGRES_CONN_VAL="postgresql://user:pass@host:port/db"
```

### 2. Dagster 실행
```bash
# Dagster UI 실행
dagster dev -f tutorial_main.py
```
## 🔍 주요 개념

### Asset
- 데이터나 계산 결과를 나타내는 Dagster의 핵심 개념
- 의존성 관계를 통해 파이프라인 구성

### Op 
- 데이터 처리의 기본 단위로, 입력을 받아 변환/처리 후 출력하는 함수(노드)
- Asset과 달리 명시적으로 job에 조합하여 사용

### Job
- 여러 Asset을 조합하여 실행 가능한 작업 단위
- 스케줄링과 실행 관리

### Resource
- 외부 서비스 연결을 위한 재사용 가능한 컴포넌트
- 데이터베이스, API, 클라우드 서비스 연결

### Sensor
- 외부 이벤트에 반응하여 파이프라인을 트리거
- 파일 업로드, API 응답 등 감지

### Partition
- 대용량 데이터를 작은 단위로 나누어 처리
- 병렬 처리와 효율적인 리소스 관리

### Graph
- 여러 작업을 논리적으로 그룹화
- 복잡한 파이프라인의 구조화


## 📚 추가 학습 자료

- [Dagster 공식 문서](https://docs.dagster.io/)
- [Dagster GitHub](https://github.com/dagster-io/dagster)
- [Dagster 커뮤니티](https://dagster.io/community)
- [Dagster 무료 강의](https://courses.dagster.io/)