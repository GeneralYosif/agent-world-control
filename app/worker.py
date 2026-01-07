import redis
import time

r = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)

pubsub = r.pubsub()
pubsub.subscribe("agents_channel")

print("Worker started. Waiting for messages...")

for message in pubsub.listen():
    if message["type"] == "message":
        print(f"📩 MESSAGE RECEIVED: {message['data']}")