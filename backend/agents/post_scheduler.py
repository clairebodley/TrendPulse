from celery import shared_task
from services.buffer_service import buffer_service
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
            # Get Buffer profile for platform
            profile = buffer_service.get_profile_by_service(post.platform)
            
            if profile:
                # Schedule post via Buffer
                result = buffer_service.create_post(
                    profile_ids=[profile["id"]],
                    text=post.content,
                    scheduled_at=post.scheduled_for.isoformat()
                )
                
                if "success" in result or "id" in result:
                    post.status = "scheduled"
                    post.buffer_id = result.get("id")
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
        
        # Get Buffer profile
        profile = buffer_service.get_profile_by_service(post_data["platform"])
        
        if profile:
            # Schedule via Buffer
            result = buffer_service.create_post(
                profile_ids=[profile["id"]],
                text=post_data["content"],
                scheduled_at=post_data["scheduled_for"]
            )
            
            if "success" in result or "id" in result:
                post.status = "scheduled"
                post.buffer_id = result.get("id")
                db.commit()
                return {"status": "success", "post_id": post.id}
            else:
                post.status = "failed"
                db.commit()
                return {"status": "error", "message": "Failed to schedule via Buffer"}
        else:
            return {"status": "error", "message": f"No Buffer profile found for {post_data['platform']}"}
            
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