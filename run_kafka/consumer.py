from kafka import KafkaConsumer
import json, psycopg2, time

consumer = KafkaConsumer(
    'sensor_topic',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

conn = psycopg2.connect(
    host="localhost", dbname="sensor_data", user="user", password="pass"
)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS sensor_data (
        id SERIAL PRIMARY KEY,
        timestamp TEXT,
        sensor_id TEXT,
        temperature FLOAT,
        pressure FLOAT
    );
""")
conn.commit()

print("[Consumer] Listening to topic...")

for message in consumer:
    data = message.value
    cur.execute(
        "INSERT INTO sensor_data (timestamp, sensor_id, temperature, pressure) VALUES (%s,%s,%s,%s)",
        (data["timestamp"], data["sensor_id"], data["temperature"], data["pressure"])
    )
    conn.commit()
    print("[Consumer] Stored in DB:", data)
