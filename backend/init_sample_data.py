#!/usr/bin/env python3
"""
Initialize sample data for TrendPulse application
Run this script to populate the database with sample trends, posts, and metrics
"""

from database import SessionLocal, engine
from models import Base, Trend, Post, Metrics, AgentLog
from datetime import datetime, timedelta
import random

def init_sample_data():
    """Initialize sample data for testing"""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Sample trends
        sample_trends = [
            {"topic": "#AIInHealthcare", "platform": "linkedin", "volume": 12500},
            {"topic": "#TechInnovation", "platform": "twitter", "volume": 8900},
            {"topic": "#SustainableTech", "platform": "instagram", "volume": 6700},
            {"topic": "#RemoteWork", "platform": "linkedin", "volume": 5400},
            {"topic": "#DigitalMarketing", "platform": "instagram", "volume": 4200},
            {"topic": "#fyp", "platform": "tiktok", "volume": 15000},
            {"topic": "#shorts", "platform": "youtube", "volume": 12000},
            {"topic": "r/technology", "platform": "reddit", "volume": 8000},
        ]
        
        for trend_data in sample_trends:
            trend = Trend(
                topic=trend_data["topic"],
                platform=trend_data["platform"],
                volume=trend_data["volume"],
                sentiment=random.choice(["positive", "neutral", "negative"]),
                growth=random.uniform(-10, 25)
            )
            db.add(trend)
        
        # Sample posts
        sample_posts = [
            {
                "topic": "#AIInHealthcare",
                "content": "🏥 AI is revolutionizing healthcare diagnostics! From early disease detection to personalized treatment plans, artificial intelligence is helping doctors save more lives than ever before. What's your experience with AI in healthcare? #AIInHealthcare #HealthTech #Innovation",
                "platform": "linkedin",
                "status": "posted",
                "scheduled_for": datetime.utcnow() - timedelta(hours=2),
                "posted_at": datetime.utcnow() - timedelta(hours=2)
            },
            {
                "topic": "#TechInnovation",
                "content": "🚀 The future is here! New tech innovations are reshaping how we work, connect, and solve global challenges. Which breakthrough excites you most? #TechInnovation #Future #Innovation",
                "platform": "twitter",
                "status": "posted",
                "scheduled_for": datetime.utcnow() - timedelta(hours=4),
                "posted_at": datetime.utcnow() - timedelta(hours=4)
            },
            {
                "topic": "#SustainableTech",
                "content": "🌱✨ Sustainable technology isn't just a trend—it's our future! From solar innovations to eco-friendly apps, tech is helping heal our planet. 🌍💚 Tag someone who cares about green tech! #SustainableTech #GreenTech #EcoFriendly #Sustainability #TechForGood",
                "platform": "instagram",
                "status": "posted",
                "scheduled_for": datetime.utcnow() - timedelta(hours=6),
                "posted_at": datetime.utcnow() - timedelta(hours=6)
            }
        ]
        
        for post_data in sample_posts:
            post = Post(**post_data)
            db.add(post)
        
        db.commit()
        
        # Sample metrics for posted content
        posted_posts = db.query(Post).filter(Post.status == "posted").all()
        for post in posted_posts:
            # Generate realistic metrics based on platform
            base_metrics = {
                "linkedin": {"likes": 25, "shares": 8, "comments": 5, "clicks": 12},
                "twitter": {"likes": 15, "shares": 5, "comments": 3, "clicks": 8},
                "instagram": {"likes": 45, "shares": 12, "comments": 8, "clicks": 15}
            }
            
            platform_stats = base_metrics.get(post.platform, {"likes": 10, "shares": 3, "comments": 2, "clicks": 5})
            
            # Add variation
            likes = platform_stats["likes"] + random.randint(-5, 10)
            shares = platform_stats["shares"] + random.randint(-2, 5)
            comments = platform_stats["comments"] + random.randint(-1, 3)
            clicks = platform_stats["clicks"] + random.randint(-3, 8)
            
            total_engagement = likes + shares + comments
            reach = max(likes * 10, 100)
            engagement_rate = (total_engagement / reach) * 100
            
            metrics = Metrics(
                post_id=post.id,
                platform=post.platform,
                likes=likes,
                shares=shares,
                comments=comments,
                clicks=clicks,
                engagement_rate=engagement_rate
            )
            db.add(metrics)
        
        # Sample agent logs
        agents = ["trend_watcher", "content_crafter", "post_scheduler", "engagement_monitor", "strategy_optimizer"]
        for agent in agents:
            log = AgentLog(
                agent_name=agent,
                action="sample_run",
                data={"status": "success", "items_processed": random.randint(5, 20)},
                success=True,
                created_at=datetime.utcnow() - timedelta(minutes=random.randint(1, 30))
            )
            db.add(log)
        
        db.commit()
        print("✅ Sample data initialized successfully!")
        print(f"📊 Created {len(sample_trends)} trends, {len(sample_posts)} posts, and {len(posted_posts)} metrics")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error initializing sample data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    init_sample_data() 