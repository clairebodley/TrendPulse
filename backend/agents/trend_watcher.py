from celery import shared_task
from services.social_apis import twitter_service, linkedin_service, instagram_service
from database import SessionLocal
from models import Trend, AgentLog
import random
from datetime import datetime

@shared_task
def monitor_trends():
    """Monitor trending topics across all platforms"""
    db = SessionLocal()
    try:
        all_trends = []
        
        # Fetch trends from all platforms
        twitter_trends = twitter_service.get_trending_topics()
        linkedin_trends = linkedin_service.get_trending_topics()
        instagram_trends = instagram_service.get_trending_topics()
        
        all_trends.extend(twitter_trends)
        all_trends.extend(linkedin_trends)
        all_trends.extend(instagram_trends)
        
        # Save trends to database
        for trend_data in all_trends:
            trend = Trend(
                topic=trend_data["topic"],
                platform=trend_data["platform"],
                volume=trend_data["volume"],
                sentiment=random.choice(["positive", "neutral", "negative"]),
                growth=random.uniform(-10, 25)
            )
            db.add(trend)
        
        db.commit()
        
        # Log agent activity
        log = AgentLog(
            agent_name="trend_watcher",
            action="monitor_trends",
            data={"trends_found": len(all_trends)},
            success=True
        )
        db.add(log)
        db.commit()
        
        return {"status": "success", "trends_found": len(all_trends)}
        
    except Exception as e:
        db.rollback()
        log = AgentLog(
            agent_name="trend_watcher",
            action="monitor_trends",
            data={"error": str(e)},
            success=False
        )
        db.add(log)
        db.commit()
        return {"status": "error", "message": str(e)}
    finally:
        db.close()

def get_current_trends():
    """Get current trending topics"""
    db = SessionLocal()
    try:
        trends = db.query(Trend).order_by(Trend.created_at.desc()).limit(20).all()
        return [
            {
                "id": trend.id,
                "topic": trend.topic,
                "platform": trend.platform,
                "volume": trend.volume,
                "sentiment": trend.sentiment,
                "growth": trend.growth,
                "lastUpdated": trend.created_at.isoformat()
            }
            for trend in trends
        ]
    finally:
        db.close()