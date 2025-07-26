from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from celery import Celery
import os
from dotenv import load_dotenv
from database import engine, Base, SessionLocal
from models import Trend, Post, Metrics, AgentLog
from agents import trend_watcher, content_crafter, post_scheduler, engagement_monitor, strategy_optimizer
from services.social_media_service import social_media_service
import json
from typing import List
from datetime import datetime

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
    broker=os.getenv("REDIS_URL", "redis://localhost:6380/0"),
    backend=os.getenv("REDIS_URL", "redis://localhost:6380/0"),
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
    """Get real agent status from database logs"""
    db = SessionLocal()
    try:
        # Get the most recent log for each agent
        agents = ["trend_watcher", "content_crafter", "post_scheduler", "engagement_monitor", "strategy_optimizer"]
        status_data = {}
        
        for agent in agents:
            latest_log = db.query(AgentLog).filter(
                AgentLog.agent_name == agent
            ).order_by(AgentLog.created_at.desc()).first()
            
            if latest_log:
                # Calculate time since last run
                time_diff = datetime.utcnow() - latest_log.created_at
                if time_diff.total_seconds() < 300:  # 5 minutes
                    last_run = f"{int(time_diff.total_seconds() / 60)} minutes ago"
                elif time_diff.total_seconds() < 3600:  # 1 hour
                    last_run = f"{int(time_diff.total_seconds() / 60)} minutes ago"
                else:
                    last_run = f"{int(time_diff.total_seconds() / 3600)} hours ago"
                
                status_data[agent] = {
                    "status": "active" if latest_log.success else "error",
                    "last_run": last_run,
                    "success": latest_log.success,
                    "last_action": latest_log.action
                }
            else:
                status_data[agent] = {
                    "status": "inactive",
                    "last_run": "Never",
                    "success": False,
                    "last_action": "None"
                }
        
        return status_data
    finally:
        db.close()

@app.post("/api/generate-content")
async def generate_content(request: dict):
    """Generate content for a specific topic"""
    topic = request.get("topic")
    if not topic:
        return {"error": "Topic is required"}
    
    return content_crafter.generate_content_for_topic(topic)

@app.post("/api/schedule-post")
async def schedule_post(post_data: dict):
    """Schedule a new post"""
    return post_scheduler.schedule_post(post_data)

@app.get("/api/agents/insights")
async def get_agent_insights():
    """Get strategy optimization insights"""
    return strategy_optimizer.get_optimization_insights()

# Social Media endpoints
@app.get("/api/social/status")
async def social_media_status():
    """Check social media platform configuration status"""
    return social_media_service.get_platform_status()

@app.post("/api/social/post")
async def post_to_social_media(request: dict):
    """Post content to social media platforms"""
    content = request.get("content")
    platforms = request.get("platforms", ["twitter", "linkedin", "instagram"])
    
    if not content:
        return {"error": "Content is required"}
    
    results = social_media_service.post_to_all_platforms(content, platforms)
    return results

@app.get("/api/social/trends")
async def get_social_trends():
    """Get trending topics from all social media platforms"""
    return social_media_service.get_all_trending_topics()

# Celery beat schedule
celery.conf.beat_schedule = {
    'monitor-trends': {
        'task': 'agents.trend_watcher.monitor_trends',
        'schedule': 300.0,  # Every 5 minutes
    },
    'generate-content': {
        'task': 'agents.content_crafter.generate_content_for_trends',
        'schedule': 600.0,  # Every 10 minutes
    },
    'schedule-posts': {
        'task': 'agents.post_scheduler.schedule_pending_posts',
        'schedule': 180.0,  # Every 3 minutes
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