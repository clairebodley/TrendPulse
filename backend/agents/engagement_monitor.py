from celery import shared_task
from services.buffer_service import buffer_service
from database import SessionLocal
from models import Post, Metrics, AgentLog
from datetime import datetime

@shared_task
def check_engagement():
    """Monitor engagement metrics for posted content"""
    db = SessionLocal()
    try:
        # Get recently posted content
        posted_posts = db.query(Post).filter(
            Post.status == "posted",
            Post.buffer_id.isnot(None)
        ).all()
        
        metrics_updated = 0
        
        for post in posted_posts:
            # Get post stats from Buffer
            stats = buffer_service.get_post_stats(post.buffer_id)
            
            if stats and "statistics" in stats:
                post_stats = stats["statistics"]
                
                # Calculate engagement rate
                total_engagement = (
                    post_stats.get("likes", 0) +
                    post_stats.get("shares", 0) +
                    post_stats.get("comments", 0)
                )
                
                # Create or update metrics
                metrics = Metrics(
                    post_id=post.id,
                    platform=post.platform,
                    likes=post_stats.get("likes", 0),
                    shares=post_stats.get("shares", 0),
                    comments=post_stats.get("comments", 0),
                    clicks=post_stats.get("clicks", 0),
                    engagement_rate=total_engagement / max(post_stats.get("reach", 1), 1) * 100
                )
                
                db.add(metrics)
                metrics_updated += 1
        
        db.commit()
        
        # Log agent activity
        log = AgentLog(
            agent_name="engagement_monitor",
            action="check_engagement",
            data={"metrics_updated": metrics_updated},
            success=True
        )
        db.add(log)
        db.commit()
        
        return {"status": "success", "metrics_updated": metrics_updated}
        
    except Exception as e:
        db.rollback()
        log = AgentLog(
            agent_name="engagement_monitor",
            action="check_engagement",
            data={"error": str(e)},
            success=False
        )
        db.add(log)
        db.commit()
        return {"status": "error", "message": str(e)}
    finally:
        db.close()

def get_engagement_metrics():
    """Get engagement metrics for dashboard"""
    db = SessionLocal()
    try:
        metrics = db.query(Metrics).order_by(Metrics.measured_at.desc()).limit(50).all()
        
        # Calculate summary stats
        total_posts = len(set(m.post_id for m in metrics))
        avg_engagement = sum(m.engagement_rate for m in metrics) / len(metrics) if metrics else 0
        total_likes = sum(m.likes for m in metrics)
        total_shares = sum(m.shares for m in metrics)
        
        return {
            "summary": {
                "totalPosts": total_posts,
                "avgEngagement": round(avg_engagement, 2),
                "totalLikes": total_likes,
                "totalShares": total_shares,
                "engagementLift": 32  # Simulated baseline comparison
            },
            "metrics": [
                {
                    "id": metric.id,
                    "postId": metric.post_id,
                    "platform": metric.platform,
                    "likes": metric.likes,
                    "shares": metric.shares,
                    "comments": metric.comments,
                    "clicks": metric.clicks,
                    "engagementRate": metric.engagement_rate,
                    "measuredAt": metric.measured_at.isoformat()
                }
                for metric in metrics
            ]
        }
    finally:
        db.close()