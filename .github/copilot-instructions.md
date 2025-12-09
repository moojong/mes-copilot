# .github/copilot-instructions.md

## 1. 프로젝트 컨텍스트
- MES 시스템 도메인 설명
  - 본 프로젝트는 소형 센서 모듈을 생산하는 제조회사를 대상으로 한 경량 MES(Manufacturing Execution System) 시나리오를 기반으로 한다.
  - 생산 공정은 부품 준비 → 조립 → 검사 → 포장 순으로 진행되며, 조립(A/B), 검사, 포장 스테이션으로 구성된 다단계 공정을 가진다.
  - 시스템은 작업지시(제품, 수량, 납기)를 기준으로 공정별 생산 실적(양품수량, 불량수량, 불량코드)과 설비 상태 및 센서 기반 시계열 데이터(가동/정지, 처리량, 온도, 전압 등)를 수집·관리한다.
  - 주요 관리 지표(KPI)는 생산량, 불량률, 납기 준수율, 그리고 OEE(가동률·성능·품질)이다.
- 데이터베이스 명세서 경로: `/docs/data_dictionary.md`

## 2. Tech Stack
- Language: Python 3.11+
- Framework: FastAPI (Pydantic v2 필수)
- Database:
  - PostgreSQL: 15 (ankane/pgvector:v0.5.1 이미지 사용)
  - SQLAlchemy: 2.0+
  - Multi-DB: mes_master, mes_sensor
- 개발 환경: VSCode, Docker Compose

## 3. FastAPI 폴더 위치
- `mes-copilot/app` 폴더

## 4. Coding Principles
- Type Hinting: 모든 함수에 타입 힌트를 엄격하게 적용 (e.g., `def func(a: int) -> str:`)
- Naming Conventions
  - Files & Directories: snake_case (e.g., `user_auth.py`)
  - Variables & Functions: snake_case (e.g., `get_user_by_id`)
  - Classes: PascalCase (e.g., `UserService`)
  - Constants: UPPER_SNAKE_CASE (e.g., `MAX_COUNT`)
  - Table Names: Plural, snake_case (e.g., `master_inspection_items`)
  - Model Classes: Singular, PascaCase (e.g., MasterInspectionItem)
  - Columns: snake_case (e.g., lower_limit)
  - Foreign Keys: target_table_singular_id (e.g., `product_id`, `operation_id`)
  - APi Endpoints: kebab-case (e.g., `GET /order-items`)
	- Pydantic Schemas
	  - ModelName + Action/Type 형식으로 작성
	  - Create: `UserCreate` (Request Body for creating)
	  - Update: `UserUpdate` (Request Body for updating)
	  - Response: `UserResponse` (Response Data)
	  - Internal: `UserInDB` (Internal Logic)
- Architecture: Layered Architecture 준수
  - Presentation Layer (`routers/`)
    - 역할: API 엔드포인트 정의 및 HTTP 요청/응답 처리, `Service` 호출
    - 규칙: DB나 Repository에 직접 접근 금지, 비즈니스 로직 포함 금지
    - 데이터: `Pydantic Schema` (DTO)를 입출력으로 사용
  - Business Layer (`services/`)
    - 역할: 애플리케이션의 핵심 비즈니스 로직 수행, `Repository` 호출
    - 규칙: `Model`(ORM)을 `Schema`(DTO)로 변환(Mapping)하여 Router에 반환
    - 데이터: `ORM Model`과 `Pydantic Schema` 간 변환
  - Data Access Layer (`repositories/`)
    - 역할: 데이터베이스와의 직접적인 통신(CRUD) 담당
    - 규칙: 비즈니스 로직을 포함하지 말것, CRUD 쿼리만 작성
    - 데이터: `SQLAlchemy ORM Model` 사용
  - Data Definitions (`schemas/`, `models/`)
    - `schemas`: Pydantic Models (Request/Response DTO)
    - `models`: SQLAlchemy Models (DB Entity)
  - 기타 (`core`)
    - 설정(config) 및 데이터베이스 연결(database.py)
  
- Dependency Injection
  - Service와 Repository는 클래스로 정의
  - FastAPI의 `Depends`를 통해 의존성을 주입받아야 함

## 5. Communication
- 서론 없이 코드와 핵심 설명만 간결하게 답변할 것

## 6. Docstring Rules
- 스타일: Google 스타일 기반, 한국어로 작성
- 필수 포함: 함수/클래스 목적, Args, Returns, Raises(예외 발생 시)