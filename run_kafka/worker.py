# celery와 redis는 kafka와 상관 없음
# redis는 celery가 해야 할 일(task)을 잠시 담아두는 메시지 중계소
# celery가 일을 처리하는 주체
# 고장에 대비하기 위해 작업을 분리시킴
from celery import Celery
import psycopg2, time

app = Celery('tasks', broker='redis://localhost:6380/0')

@app.task
def process_new_data():
    conn = psycopg2.connect(
        host="localhost", dbname="sensor_data", user="user", password="pass"
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM sensor_data ORDER BY id DESC LIMIT 5;")
    rows = cur.fetchall()
    for row in rows:
        id, ts, sid, temp, pres = row
        print(f"[Celery Worker] id={id}, sensor={sid}, temp={temp}, pressure={pres}")
        if temp > 28:
            print(f"⚠️ Warning: High temperature detected (id={id})")
    conn.close()

# 테스트 실행
if __name__ == "__main__":
    while True:
        # 아래 명령으로 redis에 task를 보내면, redis는 이것을 큐에 쌓아 두고, 
        # celery worker는 redis큐를 실시간 감시하면서 큐에 메시지가 았으면 가져와서
        # 차례로 처리하는데, 처리하는 방법은 위의 app.task에 명시되어 있다. 
        process_new_data.delay()  # redis에 task를 보내는 명령
        time.sleep(5)
