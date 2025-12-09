# MES 데이터베이스 명세서

## 서버 구성

| 서버 | 데이터베이스명 | 용도 | 포트 |
|------|--------------|------|------|
| DB1 | mes_master | 기준정보 + 생산관리 | 5432 |
| DB2 | mes_sensor | 센서 데이터 + 집계 | 5433 |

---

## DB1: mes_master

### products (제품 마스터)

| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| product_id | VARCHAR(50) | PK | 제품코드 |
| name | VARCHAR(100) | NOT NULL | 제품명 |
| category | VARCHAR(50) | | 분류 |
| unit_price | INTEGER | DEFAULT 0 | 단가 |
| enabled | BOOLEAN | DEFAULT TRUE | 사용여부 |

---

### equipment (설비 마스터)

| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| equipment_id | VARCHAR(50) | PK | 설비코드 |
| name | VARCHAR(100) | NOT NULL | 설비명 |
| equipment_type | VARCHAR(50) | | 설비유형 |
| location | VARCHAR(100) | | 위치 |
| attributes | JSONB | DEFAULT '{}' | 설비속성 |
| enabled | BOOLEAN | DEFAULT TRUE | 사용여부 |

**attributes 예시**
```json
{"manufacturer": "FANUC", "max_rpm": 6000, "install_date": "2023-01-15"}
```

**인덱스**
- `idx_equipment_attributes_gin`: attributes (GIN)

---

### defect_codes (불량코드 마스터)

| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| defect_code | VARCHAR(20) | PK | 불량코드 |
| name | VARCHAR(100) | NOT NULL | 불량명 |
| description | VARCHAR(255) | | 설명 |

---

### work_orders (작업지시)

| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| order_id | UUID | PK | 작업지시ID |
| product_id | VARCHAR(50) | FK, NOT NULL | 제품코드 |
| order_qty | INTEGER | NOT NULL | 지시수량 |
| due_date | DATE | NOT NULL | 납기일 |
| status | VARCHAR(20) | DEFAULT 'PLANNED' | 상태 |
| created_at | TIMESTAMP | DEFAULT NOW() | 생성일시 |

**status 값**: PLANNED, IN_PROGRESS, COMPLETED, CANCELLED

---

### work_results (작업실적)

| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| result_id | UUID | PK | 실적ID |
| work_order_id | UUID | FK, NOT NULL | 작업지시ID |
| equipment_id | VARCHAR(50) | FK | 설비코드 |
| good_qty | INTEGER | DEFAULT 0 | 양품수량 |
| defect_qty | INTEGER | DEFAULT 0 | 불량수량 |
| defect_code_id | VARCHAR(20) | FK | 불량코드 |
| work_data | JSONB | DEFAULT '{}' | 작업상세 |
| work_date | DATE | NOT NULL | 작업일 |
| started_at | TIMESTAMP | NOT NULL | 시작일시 |
| completed_at | TIMESTAMP | NOT NULL | 종료일시 |

**work_data 예시**
```json
{"operator": "홍길동", "cycle_time_sec": 45, "notes": "정상완료"}
```

---


### DB1 FK 요약

| 테이블 | 컬럼 | 참조 |
|--------|------|------|
| work_orders | product_id | products.product_id |
| work_results | work_order_id | work_orders.order_id |
| work_results | equipment_id | equipment.equipment_id |
| work_results | defect_code_id | defect_codes.defect_code |

---

## DB2: mes_sensor

### sensor_data (센서 데이터)

| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| id | UUID | PK | 데이터ID |
| equipment_id | VARCHAR(50) | NOT NULL | 설비코드 |
| timestamp | TIMESTAMP | NOT NULL | 수집일시 |
| values | JSONB | NOT NULL | 센서값 |
| is_anomaly | BOOLEAN | DEFAULT FALSE | 이상여부 |

**values 예시**
```json
{"temperature": 45.2, "vibration": 0.03, "rpm": 1500, "current": 12.5}
```


## 테이블 요약

| DB | 테이블 | 설명 |
|----|--------|------|
| DB1 | products | 제품 마스터 |
| DB1 | equipment | 설비 마스터 (JSONB, GIN) |
| DB1 | defect_codes | 불량코드 마스터 |
| DB1 | work_orders | 작업지시 |
| DB1 | work_results | 작업실적 (JSONB) |
| DB2 | sensor_data | 센서 데이터 (JSONB, 인덱스 없음) |

**총 7개 테이블** (DB1: 5개, DB2: 2개)