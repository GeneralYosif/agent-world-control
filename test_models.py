import sys
import os

# Добавяме подпапката app в sys.path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "app"))
from models import test_db_connection, insert_agent, get_all_agents, update_agent, delete_agent

# 1. Проверка на връзката
assert test_db_connection(), "Cannot connect to DB!"

# 2. Вмъкване на тестов агент
test_agent = {
    "real_name": "Test Name",
    "codename": "TestCodename",
    "gender": "M",
    "country_of_birth": "Testland",
    "current_country": "Testland",
    "influence_level": 5,
    "primary_objective": "Testing",
    "current_status": "Active",
    "is_alive": True,
    "death_cause": None
}

insert_agent(**test_agent)

# 3. Проверка дали агентът е записан
agents = get_all_agents()
assert any(a[2] == "TestCodename" for a in agents), "Agent not found in DB!"

# 4. Актуализация
agent_id = next(a[0] for a in agents if a[2] == "TestCodename")
update_agent(agent_id, {"current_status": "Inactive"})

# 5. Проверка на актуализацията
agents = get_all_agents()
assert next(a[0] for a in agents if a[0] == agent_id and a[8] == "Inactive"), "Update failed!"

# 6. Изтриване
delete_agent(agent_id)
agents = get_all_agents()
assert all(a[0] != agent_id for a in agents), "Delete failed!"

print("All model tests passed!")