import psycopg2

# базисни настройки за връзка с базата данни
DB_CONFIG = {
    "dbname": "agents_db",
    "user": "Ioizef_Mengeme",
    "password": "goyum",
    "host": "db",
    "port": 5432
}

# Функция за създаване на връзка с базата данни
def get_connection():
    return psycopg2.connect(**DB_CONFIG)

# Функция за тестване на връзката с базата данни
def test_db_connection():
    try:
        conn = get_connection()
        conn.close()
        return True
    except Exception as e:
        print("DB connection failed:", e)
        return False


# Създаване на таблицата за агентите
def create_agents_table():
    sql = """
    CREATE TABLE IF NOT EXISTS agents (
        id SERIAL PRIMARY KEY,
        real_name VARCHAR(255),
        codename VARCHAR(255) UNIQUE,
        gender TEXT,
        country_of_birth VARCHAR(255),
        current_country VARCHAR(255),
        influence_level INTEGER,
        primary_objective TEXT,
        current_status VARCHAR(255),
        is_alive BOOLEAN DEFAULT TRUE,
        death_cause TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

# Функция за извличане на всички агенти от базата данни
def get_all_agents():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            real_name,
            codename,
            gender,
            country_of_birth,
            current_country,
            influence_level,
            primary_objective,
            current_status,
            is_alive,
            death_cause
        FROM agents
        ORDER BY id;
    """)

    agents = cur.fetchall()

    cur.close()
    conn.close()
    return agents

# Функция за вмъкване на нов агент в базата данни
def insert_agent(
    real_name,
    codename,
    gender,
    country_of_birth,
    current_country,
    influence_level,
    primary_objective,
    current_status,
    is_alive=True,
    death_cause=None
):
    # Валидация
    if not codename or not codename.strip():
        raise ValueError("Codename cannot be empty")
    if influence_level < 0:
        raise ValueError("Influence level cannot be negative")

    # Корекция за checkbox
    if isinstance(is_alive, str):
        is_alive = (is_alive == "on")
    if is_alive:
        death_cause = None  # няма причина ако е жив

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO agents (
                real_name,
                codename,
                gender,
                country_of_birth,
                current_country,
                influence_level,
                primary_objective,
                current_status,
                is_alive,
                death_cause
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            real_name,
            codename,
            gender,
            country_of_birth,
            current_country,
            influence_level,
            primary_objective,
            current_status,
            is_alive,
            death_cause
        ))
        conn.commit()
    except Exception as e:
        print("Error inserting agent:", e)
        raise e
    finally:
        cur.close()
        conn.close()


# Функция за изтриване на агент по ID
def delete_agent(agent_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM agents WHERE id = %s", (agent_id,))
    conn.commit()
    cur.close()
    conn.close()


# Функция за актуализиране/обновяване/редактиране на информацията за агент
def update_agent(agent_id, data):
    conn = get_connection()
    cur = conn.cursor()

    is_alive = (data.get("is_alive") == "on")
    death_cause = data.get("death_cause")  # ← винаги взимаме текста от формата

    cur.execute("""
        UPDATE agents SET
            real_name = %s,
            codename = %s,
            gender = %s,
            country_of_birth = %s,
            current_country = %s,
            influence_level = %s,
            primary_objective = %s,
            current_status = %s,
            is_alive = %s,
            death_cause = %s,
            last_updated = CURRENT_TIMESTAMP
        WHERE id = %s
    """, (
        data.get("real_name"),
        data.get("codename"),
        data.get("gender"),
        data.get("country_of_birth"),
        data.get("current_country"),
        int(data.get("influence_level") or 0),
        data.get("primary_objective"),
        data.get("current_status"),
        is_alive,
        death_cause,
        agent_id
    ))

    conn.commit()
    cur.close()
    conn.close()