from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from celery import Celery
import os
from dotenv import load_dotenv
from database import engine, Base
from models import Trend, Post, Metrics
from agents import trend_watcher, content_crafter, post_scheduler, engagement_monitor, strategy_optimizer
import json
from typing import List

load_dotenv()

# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI(title="TrendPulse Multi-Agent Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Celery setup
celery = Celery(
    "trendpulse",
    broker=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    include=["agents.trend_watcher", "agents.content_crafter", "agents.post_scheduler", "agents.engagement_monitor", "agents.strategy_optimizer"]
)

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                pass

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Message: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/api/trends")
async def get_trends():
    return trend_watcher.get_current_trends()

@app.get("/api/drafts")
async def get_drafts():
    return content_crafter.get_current_drafts()

@app.get("/api/posts")
async def get_posts():
    return post_scheduler.get_scheduled_posts()

@app.get("/api/metrics")
async def get_metrics():
    return engagement_monitor.get_engagement_metrics()

@app.get("/api/agents/status")
async def get_agent_status():
    return {
        "trend_watcher": {"status": "active", "last_run": "2 minutes ago"},
        "content_crafter": {"status": "active", "last_run": "5 minutes ago"},
        "post_scheduler": {"status": "active", "last_run": "1 minute ago"},
        "engagement_monitor": {"status": "active", "last_run": "30 seconds ago"},
        "strategy_optimizer": {"status": "active", "last_run": "3 minutes ago"}
    }

@app.post("/api/generate-content")
async def generate_content(topic: str):
    return content_crafter.generate_content_for_topic(topic)

@app.post("/api/schedule-post")
async def schedule_post(post_data: dict):
    return post_scheduler.schedule_post(post_data)

# Celery beat schedule
celery.conf.beat_schedule = {
    'monitor-trends': {
        'task': 'agents.trend_watcher.monitor_trends',
        'schedule': 300.0,  # Every 5 minutes
    },
    'check-engagement': {
        'task': 'agents.engagement_monitor.check_engagement',
        'schedule': 180.0,  # Every 3 minutes
    },
    'optimize-strategy': {
        'task': 'agents.strategy_optimizer.optimize_strategy',
        'schedule': 600.0,  # Every 10 minutes
    },
}
celery.conf.timezone = 'UTC'

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)