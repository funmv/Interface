from kafka import KafkaProducer
import json, time, random
from datetime import datetime

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

while True:
    msg = {
        "timestamp": datetime.now().isoformat(),
        "sensor_id": random.choice(["A1","B2","C3"]),
        "temperature": round(random.uniform(20, 30), 2),
        "pressure": round(random.uniform(1.0, 2.0), 3)
    }
    producer.send('sensor_topic', msg)
    print("[Producer] Sent:", msg)
    time.sleep(1)
