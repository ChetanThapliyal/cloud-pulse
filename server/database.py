import aiosqlite
import time
from typing import List, Optional
from pydantic import BaseModel

DB_NAME = "cloud_pulse.db"

class ServiceLog(BaseModel):
    id: int
    service_name: str
    status: str
    latency: float
    timestamp: float

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS monitoring_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service_name TEXT NOT NULL,
                status TEXT NOT NULL,
                latency REAL,
                timestamp REAL
            )
        """)
        # Index for faster history queries
        await db.execute("CREATE INDEX IF NOT EXISTS idx_service_timestamp ON monitoring_logs(service_name, timestamp DESC)")
        await db.commit()

async def log_check(service_name: str, status: str, latency: float):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO monitoring_logs (service_name, status, latency, timestamp) VALUES (?, ?, ?, ?)",
            (service_name, status, latency, time.time())
        )
        await db.commit()

async def get_latest_status(service_names: List[str]):
    """
    Get the most recent log for each service.
    Returns a dict {service_name: {status, latency, timestamp}}
    """
    results = {}
    async with aiosqlite.connect(DB_NAME) as db:
        for name in service_names:
            async with db.execute(
                "SELECT status, latency, timestamp FROM monitoring_logs WHERE service_name = ? ORDER BY timestamp DESC LIMIT 1",
                (name,)
            ) as cursor:
                row = await cursor.fetchone()
                if row:
                    results[name] = {
                        "status": row[0],
                        "latency": row[1],
                        "timestamp": row[2]
                    }
    return results

async def get_history(limit: int = 50):
    """
    Get global average latency history. 
    For simplicity, we'll just get the last N records and average them by timestamp groups roughly.
    Actually, let's just return the raw last N logs for the frontend to visualize or specific service history.
    """
    # For the chart, we want the trend of the system. 
    # Let's return the last N entries generally to see what's happening.
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT service_name, latency, timestamp FROM monitoring_logs ORDER BY timestamp DESC LIMIT ?",
            (limit,)
        ) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
