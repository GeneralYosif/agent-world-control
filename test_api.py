import sys
import os

# Добавяме подпапката app в sys.path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "app"))
import requests

BASE_URL = "http://127.0.0.1:5001"

# GET агенти
resp = requests.get(f"{BASE_URL}/api/agents")
print("GET /api/agents:", resp.status_code)
try:
    print(resp.json())
except Exception as e:
    print("Не е JSON:", resp.text)

# POST нов агент
new_agent = {
    "real_name": "John Doe",
    "codename": "Shadow",
    "gender": "M",
    "country_of_birth": "USA",
    "current_country": "USA",
    "influence_level": 5,
    "primary_objective": "Test mission",
    "current_status": "Active",
    "is_alive": True,
    "death_cause": None
}

resp_post = requests.post(f"{BASE_URL}/api/agents", json=new_agent)
print("POST /api/agents:", resp_post.status_code)
try:
    print(resp_post.json())
except Exception as e:
    print("Не е JSON:", resp_post.text)