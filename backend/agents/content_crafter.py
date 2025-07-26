from celery import shared_task
from services.openai_service import openai_service
from database import SessionLocal
from models import Post, Trend, AgentLog
from datetime import datetime, timedelta

@shared_task
def generate_content_for_trends():
    """Generate content for trending topics"""
    db = SessionLocal()
    try:
        # Get top trending topics from last hour
        recent_trends = db.query(Trend).filter(
            Trend.created_at >= datetime.utcnow() - timedelta(hours=1)
        ).order_by(Trend.volume.desc()).limit(5).all()
        
        posts_created = 0
        
        for trend in recent_trends:
            # Generate content for each platform
            platforms = ["twitter", "linkedin", "instagram"]
            
            for platform in platforms:
                # Check if we already have a post for this trend+platform
                existing_post = db.query(Post).filter(
                    Post.topic == trend.topic,
                    Post.platform == platform,
                    Post.created_at >= datetime.utcnow() - timedelta(hours=1)
                ).first()
                
                if not existing_post:
                    # Generate content
                    content = openai_service.generate_post_content(
                        topic=trend.topic,
                        platform=platform,
                        tone="engaging"
                    )
                    
                    # Create post record
                    post = Post(
                        topic=trend.topic,
                        content=content,
                        platform=platform,
                        status="draft",
                        scheduled_for=datetime.utcnow() + timedelta(minutes=30)
                    )
                    db.add(post)
                    posts_created += 1
        
        db.commit()
        
        # Log agent activity
        log = AgentLog(
            agent_name="content_crafter",
            action="generate_content_for_trends",
            data={"posts_created": posts_created},
            success=True
        )
        db.add(log)
        db.commit()
        
        return {"status": "success", "posts_created": posts_created}
        
    except Exception as e:
        db.rollback()
        log = AgentLog(
            agent_name="content_crafter",
            action="generate_content_for_trends",
            data={"error": str(e)},
            success=False
        )
        db.add(log)
        db.commit()
        return {"status": "error", "message": str(e)}
    finally:
        db.close()

def generate_content_for_topic(topic: str):
    """Generate content for a specific topic"""
    db = SessionLocal()
    try:
        platforms = ["twitter", "linkedin", "instagram"]
        drafts = []
        
        for platform in platforms:
            variants = openai_service.generate_content_variants(topic, platform, 2)
            for i, content in enumerate(variants):
                post = Post(
                    topic=topic,
                    content=content,
                    platform=platform,
                    status="draft",
                    scheduled_for=datetime.utcnow() + timedelta(hours=1)
                )
                db.add(post)
                drafts.append({
                    "topic": topic,
                    "platform": platform,
                    "content": content,
                    "variant": f"A" if i == 0 else "B"
                })
        
        db.commit()
        return {"status": "success", "drafts": drafts}
        
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        db.close()

def get_current_drafts():
    """Get current content drafts"""
    db = SessionLocal()
    try:
        posts = db.query(Post).filter(Post.status == "draft").order_by(Post.created_at.desc()).limit(20).all()
        return [
            {
                "id": post.id,
                "topic": post.topic,
                "platform": post.platform,
                "content": post.content,
                "status": post.status,
                "createdAt": post.created_at.isoformat(),
                "scheduledFor": post.scheduled_for.isoformat() if post.scheduled_for else None
            }
            for post in posts
        ]
    finally:
        db.close()