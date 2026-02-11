import asyncio
import random
import time
from typing import List, Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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

# Configuration
MOCK_MODE = True


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

# Define Services with Mock Locations
services_to_monitor = [
    Service(
        name="Google (US-East)", 
        url="https://google.com", 
        location=Location(city="New York", country="USA", lat=40.7128, lon=-74.0060)
    ),
    Service(
        name="GitHub (US-West)", 
        url="https://github.com", 
        location=Location(city="San Francisco", country="USA", lat=37.7749, lon=-122.4194)
    ),
    Service(
        name="Local Server 1 (EU)", 
        ip="192.168.1.100", 
        location=Location(city="London", country="UK", lat=51.5074, lon=-0.1278)
    ),
    Service(
        name="Local Server 2 (APAC)", 
        ip="192.168.1.101", 
        location=Location(city="Tokyo", country="Japan", lat=35.6762, lon=139.6503)
    ),
    Service(
        name="NAS Storage (AU)", 
        ip="192.168.1.102", 
        location=Location(city="Sydney", country="Australia", lat=-33.8688, lon=151.2093)
    ),
]

async def check_service(service: Service) -> ServiceStatus:
    # Simulate network delay
    delay = random.uniform(0.05, 0.3)
    await asyncio.sleep(delay)
    
    if MOCK_MODE:
        # Randomly fail some services (20% chance)
        is_up = random.random() > 0.2
        
        status = "Up" if is_up else "Down"
        # If down, maybe longer timeout 'latency'
        latency = delay * 1000 if is_up else 0
        
        return ServiceStatus(
            name=service.name,
            status=status,
            latency=round(latency, 2),
            message="Service is reachable" if is_up else "Connection timed out",
            location=service.location
        )

    else:
        # Real implementation would go here (using httpx or ping)
        # For now, we fallback to mock since requirements specified Mock Mode
        return ServiceStatus(
            name=service.name,
            status="Unknown",
            latency=0,
            message="Real monitoring not implemented yet"
        )

@app.get("/")
def read_root():
    return {"message": "Cloud Pulse Backend is running"}

@app.get("/status", response_model=List[ServiceStatus])
async def get_status():
    results = await asyncio.gather(*(check_service(s) for s in services_to_monitor))
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
