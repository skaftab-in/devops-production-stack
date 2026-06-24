from fastapi import FastAPI
from redis import Redis
from sqlalchemy import create_engine, text
import os, logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Webvory DevOps Assignment")

redis_client = Redis(host=os.getenv("REDIS_HOST", "redis"), port=6379, decode_responses=True)
db_url = os.getenv("DATABASE_URL")

@app.get("/")
def root():
    logger.info("Root hit")
    return {"message": "Webvory DevOps API", "status": "running"}

@app.get("/health")
def health():
    status = {"api": "ok", "redis": "ok", "postgres": "ok"}
    try:
        redis_client.ping()
    except Exception as e:
        status["redis"] = f"error: {e}"
        status["api"] = "degraded"
    try:
        engine = create_engine(db_url)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception as e:
        status["postgres"] = f"error: {e}"
        status["api"] = "degraded"
    return status

@app.post("/cache/{key}")
def set_cache(key: str, value: str):
    redis_client.setex(key, 300, value)
    return {"key": key, "cached": True, "ttl": 300}

@app.get("/cache/{key}")
def get_cache(key: str):
    val = redis_client.get(key)
    return {"key": key, "value": val}

@app.post("/notes")
def create_note(title: str, content: str):
    try:
        engine = create_engine(db_url)
        with engine.connect() as conn:
            conn.execute(text("CREATE TABLE IF NOT EXISTS notes (id SERIAL PRIMARY KEY, title TEXT, content TEXT)"))
            conn.execute(text("INSERT INTO notes (title, content) VALUES (:t, :c)"), {"t": title, "c": content})
            conn.commit()
        return {"status": "saved", "title": title}
    except Exception as e:
        return {"error": str(e)}

@app.get("/notes")
def get_notes():
    try:
        engine = create_engine(db_url)
        with engine.connect() as conn:
            conn.execute(text("CREATE TABLE IF NOT EXISTS notes (id SERIAL PRIMARY KEY, title TEXT, content TEXT)"))
            result = conn.execute(text("SELECT id, title, content FROM notes"))
            return {"notes": [{"id": r[0], "title": r[1], "content": r[2]} for r in result]}
    except Exception as e:
        return {"error": str(e)}
