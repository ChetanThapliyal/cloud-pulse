import asyncio
import time
from typing import List, Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import database

app = FastAPI(title="Cloud Pulse Backend")

# CORS Setup
origins = [
    "*",  # Allow all origins for local development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Location(BaseModel):
    city: str
    country: str
    lat: float
    lon: float

class Service(BaseModel):
    name: str
    url: Optional[str] = None
    ip: Optional[str] = None
    location: Location

class ServiceStatus(BaseModel):
    name: str
    status: str  # "Up" or "Down"
    latency: float # in ms
    message: Optional[str] = None
    location: Location

# Services to monitor
services_to_monitor = [
    Service(
        name="Google (US-East)", 
        url="https://www.google.com", 
        location=Location(city="New York", country="USA", lat=40.7128, lon=-74.0060)
    ),
    Service(
        name="GitHub (US-West)", 
        url="https://github.com", 
        location=Location(city="San Francisco", country="USA", lat=37.7749, lon=-122.4194)
    ),
    Service(
        name="Cloudflare (EU)", 
        url="https://www.cloudflare.com", 
        location=Location(city="London", country="UK", lat=51.5074, lon=-0.1278)
    ),
    Service(
        name="Localhost (Test)", 
        url="http://localhost:8080", 
        location=Location(city="Tokyo", country="Japan", lat=35.6762, lon=139.6503)
    ),
    Service(
        name="Example Non-Existent", 
        url="http://non-existent-service.test", 
        location=Location(city="Sydney", country="Australia", lat=-33.8688, lon=151.2093)
    ),
]

# Background Monitoring Task
async def monitor_services():
    while True:
        results = await asyncio.gather(*(perform_check(s) for s in services_to_monitor))
        # Log results to DB
        for i, status in enumerate(results):
            # We log regardless of success/fail, status is "Up" or "Down"
            # Note: perform_check returns ServiceStatus, stick to that.
            pass
        await asyncio.sleep(10)  # Check every 10 seconds

async def perform_check(service: Service) -> ServiceStatus:
    start_time = time.time()
    status = "Down"
    latency = 0.0
    message = ""

    try:
        if service.url:
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.get(service.url)
                latency = (time.time() - start_time) * 1000
                if resp.status_code < 400:
                    status = "Up"
                    message = f"HTTP {resp.status_code}"
                else:
                    status = "Down" # Or Warning depending on logic, stick to binary for now
                    message = f"HTTP {resp.status_code}"
        elif service.ip:
            # Simple ping
            proc = await asyncio.create_subprocess_exec(
                "ping", "-c", "1", "-W", "2", service.ip,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()
            latency = (time.time() - start_time) * 1000
            if proc.returncode == 0:
                status = "Up"
                message = "Ping response received"
            else:
                status = "Down"
                message = "Ping timeout"
                latency = 0 # No latency if down? Or timeout value? Let's say 0.

    except Exception as e:
        status = "Down"
        message = str(e)
        latency = 0

    # Log to DB
    await database.log_check(service.name, status, latency)

    return ServiceStatus(
        name=service.name,
        status=status,
        latency=round(latency, 2),
        message=message,
        location=service.location
    )

@app.on_event("startup")
async def startup_event():
    await database.init_db()
    asyncio.create_task(monitor_services())

@app.get("/")
def read_root():
    return {"message": "Cloud Pulse Backend (Real Mode) Running"}

@app.get("/status", response_model=List[ServiceStatus])
async def get_status():
    # Return LATEST status from DB for speed, or run check immediately?
    # For now, let's run a quick check to ensure 'live' feel, OR fetch latest from DB if we trust the background worker.
    # The requirement says "Real Monitoring Engine".
    # Let's return the latest known state from DB to be fast, but if empty, run a check.
    
    # Actually, fetching from DB is faster and decouples checking from viewing.
    # Let's try to get latest from DB.
    latest = await database.get_latest_status([s.name for s in services_to_monitor])
    
    response = []
    for service in services_to_monitor:
        data = latest.get(service.name)
        if data:
            response.append(ServiceStatus(
                name=service.name,
                status=data["status"],
                latency=data["latency"],
                message="Last check: " + time.strftime('%H:%M:%S', time.localtime(data["timestamp"])),
                location=service.location
            ))
        else:
            # diverse checking if no history
            # For minimal delay on first load, we could return a "Pending" or just wait.
            # Let's wait for one check.
            res = await perform_check(service)
            response.append(res)
            
    return response

@app.get("/history")
async def get_history_endpoint():
    return await database.get_history(50)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
