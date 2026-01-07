import os
import redis # импортиране на redis библиотеката
#импортиране на нужните flask модули
from flask import Flask, render_template
from flask import request, redirect, url_for
#импортираме логиката за таблицата от модели
from models import create_agents_table, delete_agent, get_all_agents, insert_agent, update_agent
#импортираме от модели функцията за тест на връзката
from models import test_db_connection
if not test_db_connection():
    print("Cannot connect to the database. Exiting...")
    exit(1)

app = Flask(__name__)

#създаваме redis клиент за връзка с redis сървъра
redis_client = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)

#add agent
@app.route("/add", methods=["GET", "POST"])
def add_agent():
    error = None
    if request.method == "POST":
        data = request.form
        try:
            insert_agent(
                real_name=data.get("real_name"),
                codename=data.get("codename"),
                gender=data.get("gender"),
                country_of_birth=data.get("country_of_birth"),
                current_country=data.get("current_country"),
                influence_level=int(data.get("influence_level") or 0),
                primary_objective=data.get("primary_objective"),
                current_status=data.get("current_status"),
                is_alive=(data.get("is_alive") == "on"),
                death_cause=data.get("death_cause") or None
            )
            return redirect(url_for("index"))
        except Exception as e:
            error = str(e)
    return render_template("add.html", error=error)


#edit agent
@app.route("/edit/<int:agent_id>", methods=["GET", "POST"])
def edit_agent(agent_id):
    from models import get_all_agents  # за да вземеш агента
    agents = get_all_agents()
    agent = next((a for a in agents if a[0] == agent_id), None)
    if not agent:
        return "Agent not found", 404

    if request.method == "POST":
        update_agent(agent_id, request.form)
        return redirect(url_for("index"))

    return render_template("edit.html", agent=agent)

#delete agent
@app.route("/delete/<int:agent_id>")
def delete(agent_id):
    delete_agent(agent_id)
    return redirect(url_for("index"))

# главна страница, показваща всички агенти
@app.route("/")
def index():
    agents = get_all_agents()
    return render_template("index.html", agents=agents)

# API endpoint за получаване на всички агенти в JSON формат
@app.route("/api/agents", methods=["GET"])
def api_get_agents():
    from models import get_all_agents
    agents = get_all_agents()
    # Може да върнем списък от dicts, вместо tuples
    agents_list = [
        {
            "id": a[0],
            "real_name": a[1],
            "codename": a[2],
            "gender": a[3],
            "country_of_birth": a[4],
            "current_country": a[5],
            "influence_level": a[6],
            "primary_objective": a[7],
            "current_status": a[8],
            "is_alive": a[9],
            "death_cause": a[10]
        } for a in agents
    ]
    return {"agents": agents_list}

# API endpoint за добавяне на нов агент чрез JSON заявка
@app.route("/api/agents", methods=["POST"])
def api_add_agent():
    data = request.json
    try:
        insert_agent(**data)
        redis_client.publish(
            "agents_channel",
            f"New agent added: {data.get('codename')}"
        )
        return {"status": "success"}, 201
    except Exception as e:
        return {"status": "error", "message": str(e)}, 400
    

# стартиране на приложението
if __name__ == "__main__":
    create_agents_table()
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=5000, debug=debug)