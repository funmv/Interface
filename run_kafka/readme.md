# 🛰️ Real-Time Data Pipeline with Kafka, PostgreSQL, Celery, and Redis

이 프로젝트는 **실시간 센서 데이터 파이프라인**을 구현한 예시입니다.  
`producer.py`에서 생성된 데이터가 Kafka를 통해 스트리밍되고,  
`consumer.py`가 이를 DB에 저장한 뒤,  
`Celery + Redis`가 백그라운드에서 데이터를 감시·분석합니다.

---

## 📦 System Overview


---

## ⚙️ Architecture Summary

| 구성 요소 | 포트 | 역할 | 주요 기능 |
|------------|------|------|-----------|
| **Kafka** | 9092 | 실시간 데이터 브로커 | Producer → Consumer 간 데이터 스트림 중계 |
| **PostgreSQL** | 5432 | 데이터 저장소 | Consumer가 받은 센서 데이터를 저장 |
| **Redis** | 6380 | Celery 브로커 | Celery 작업 큐(Message Queue) 역할 |
| **Celery Worker** | - | 백엔드 처리 엔진 | DB의 데이터를 감시/분석하는 태스크 실행 |
| **Producer.py** | - | 데이터 생성기 | 센서 데이터를 Kafka로 발행 |
| **Consumer.py** | - | 데이터 수신기 | Kafka에서 메시지 수신 후 DB에 저장 |
| **Worker.py** | - | 데이터 처리기 | Celery Task로 비동기 데이터 분석 수행 |

---

## 🚀 Data Flow

1. **Producer.py**
   - 센서 데이터(JSON)를 생성하고 Kafka(9092)에 발행합니다.
   - 예시 메시지:
     ```json
     {"timestamp": "2025-11-05T14:41:38", "sensor_id": "A1", "temperature": 28.2, "pressure": 1.52}
     ```

2. **Consumer.py**
   - Kafka에서 메시지를 구독하여 PostgreSQL(5432)에 저장합니다.
   - DB 테이블: `sensor_data(id, timestamp, sensor_id, temperature, pressure)`

3. **Worker.py (Celery)**
   - Redis(6380)를 브로커로 사용하여 비동기 태스크를 수신합니다.
   - `process_new_data()` 태스크가 실행되면 DB에서 최신 데이터를 조회하고, 임계치를 초과한 센서값을 감시합니다.

---

## 🔧 Why Use These Tools?

| 기술 | 이유 / 장점 |
|------|--------------|
| **Kafka** | 초당 수천 건의 데이터도 안정적으로 수집 가능한 고성능 스트리밍 플랫폼 |
| **PostgreSQL** | 관계형 데이터 저장, 안정적 트랜잭션 및 스키마 관리 |
| **Redis + Celery** | 비동기 작업 처리, 백그라운드 태스크 실행, 장애 복구 및 재시도 기능 |
| **Docker Compose** | 모든 서비스를 컨테이너 기반으로 쉽게 배포 및 관리 |

---

## 🧠 System Advantages

✅ **비동기 처리**
- 데이터 수집과 분석을 분리하여 시스템 응답성 향상  
✅ **확장성**
- Kafka Consumer 및 Celery Worker를 수평 확장 가능  
✅ **안정성**
- Redis를 통한 태스크 큐 관리로 장애 발생 시 재시도 가능  
✅ **유연성**
- 새로운 데이터 필드나 분석 로직 추가 시 코드 최소 수정  

---

## ⚡ Celery & Redis Explained

> ✅ **Celery와 Redis는 Kafka와 직접적인 관련이 없습니다.**  
> 둘은 “실시간 스트림 처리”가 아니라, **비동기 작업(Task) 처리**를 담당합니다.

- **Redis**는 Celery가 해야 할 일을 잠시 담아두는 **메시지 중계소(Message Queue)** 입니다.  
- **Celery**는 실제로 그 일을 처리하는 **주체(Worker)** 입니다.  
- 이 구조를 사용하는 이유는 **고장(장애)에 대비하고, 처리 부하를 분리하기 위해서**입니다.

### 🔹 동작 원리

1. `process_new_data.delay()`  
   → 이 명령이 **Redis에 “할 일(Task)”을 보내는 명령**입니다.  
2. Redis는 이 Task 메시지를 큐(Queue)에 쌓아둡니다.  
3. Celery Worker는 Redis 큐를 **실시간 감시**하면서, 새 메시지가 들어오면 꺼냅니다.  
4. Worker는 메시지 안에 지정된 함수(`@app.task`로 정의된 함수)를 실행합니다.  
   - 즉, 실제 “일하는 로직”은 `worker.py` 안의 `app.task`에 정의되어 있습니다.
     
---

## 🧰 How to Run (Development Environment)

### 1️⃣ Run Docker Services
```bash
docker-compose up -d
```

### 2️⃣ Run python services
터미널을 3개 열어 각각 수행. 가상환경 kafka310에 들어감
```bash
python producer.py
python consumer.py
celery -A worker worker --loglevel=info --pool=solo
```






