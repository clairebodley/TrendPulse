from celery import shared_task
from services.social_media_service import social_media_service
from database import SessionLocal
from models import Post, AgentLog
from datetime import datetime

@shared_task
def schedule_pending_posts():
    """Schedule pending posts via Buffer"""
    db = SessionLocal()
    try:
        # Get posts ready to be scheduled
        pending_posts = db.query(Post).filter(
            Post.status == "draft",
            Post.scheduled_for <= datetime.utcnow()
        ).all()
        
        posts_scheduled = 0
        
        for post in pending_posts:
            # Post directly to social media platform
            if post.platform == "twitter":
                result = social_media_service.twitter.post_tweet(post.content)
            elif post.platform == "linkedin":
                result = social_media_service.linkedin.post_update(post.content)
            elif post.platform == "instagram":
                result = social_media_service.instagram.post_caption(post.content)
            else:
                result = {"error": f"Unsupported platform: {post.platform}"}
            
            if result.get("success"):
                post.status = "posted"
                post.posted_at = datetime.utcnow()
                posts_scheduled += 1
            else:
                post.status = "failed"
        
        db.commit()
        
        # Log agent activity
        log = AgentLog(
            agent_name="post_scheduler",
            action="schedule_pending_posts",
            data={"posts_scheduled": posts_scheduled},
            success=True
        )
        db.add(log)
        db.commit()
        
        return {"status": "success", "posts_scheduled": posts_scheduled}
        
    except Exception as e:
        db.rollback()
        log = AgentLog(
            agent_name="post_scheduler",
            action="schedule_pending_posts",
            data={"error": str(e)},
            success=False
        )
        db.add(log)
        db.commit()
        return {"status": "error", "message": str(e)}
    finally:
        db.close()

def schedule_post(post_data: dict):
    """Schedule a specific post"""
    db = SessionLocal()
    try:
        # Create post record
        post = Post(
            topic=post_data["topic"],
            content=post_data["content"],
            platform=post_data["platform"],
            status="draft",
            scheduled_for=datetime.fromisoformat(post_data["scheduled_for"])
        )
        db.add(post)
        db.commit()
        
        # Post directly to social media platform
        if post_data["platform"] == "twitter":
            result = social_media_service.twitter.post_tweet(post_data["content"])
        elif post_data["platform"] == "linkedin":
            result = social_media_service.linkedin.post_update(post_data["content"])
        elif post_data["platform"] == "instagram":
            result = social_media_service.instagram.post_caption(post_data["content"])
        else:
            result = {"error": f"Unsupported platform: {post_data['platform']}"}
        
        if result.get("success"):
            post.status = "posted"
            post.posted_at = datetime.utcnow()
            db.commit()
            return {"status": "success", "post_id": post.id}
        else:
            post.status = "failed"
            db.commit()
            return {"status": "error", "message": f"Failed to post: {result.get('error', 'Unknown error')}"}
            
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        db.close()

def get_scheduled_posts():
    """Get scheduled posts"""
    db = SessionLocal()
    try:
        posts = db.query(Post).filter(Post.status.in_(["scheduled", "posted"])).order_by(Post.scheduled_for.desc()).limit(20).all()
        return [
            {
                "id": post.id,
                "topic": post.topic,
                "platform": post.platform,
                "content": post.content,
                "status": post.status,
                "scheduledFor": post.scheduled_for.isoformat() if post.scheduled_for else None,
                "postedAt": post.posted_at.isoformat() if post.posted_at else None
            }
            for post in posts
        ]
    finally:
        db.close()