from celery import shared_task
from services.openai_service import openai_service
from database import SessionLocal
from models import Post, Metrics, AgentLog
from datetime import datetime, timedelta

@shared_task
def optimize_strategy():
    """Analyze performance and optimize strategy"""
    db = SessionLocal()
    try:
        # Get recent posts with poor performance
        cutoff_time = datetime.utcnow() - timedelta(hours=24)
        
        # Find underperforming posts (engagement rate < 2%)
        underperforming_query = db.query(Post, Metrics).join(
            Metrics, Post.id == Metrics.post_id
        ).filter(
            Post.posted_at >= cutoff_time,
            Metrics.engagement_rate < 2.0
        ).all()
        
        optimizations_made = 0
        
        for post, metrics in underperforming_query:
            # Generate optimized content
            performance_data = {
                "engagement_rate": metrics.engagement_rate,
                "likes": metrics.likes,
                "shares": metrics.shares,
                "comments": metrics.comments
            }
            
            optimized_content = openai_service.optimize_content(
                post.content,
                performance_data
            )
            
            # Create new optimized post
            new_post = Post(
                topic=post.topic + " (Optimized)",
                content=optimized_content,
                platform=post.platform,
                status="draft",
                scheduled_for=datetime.utcnow() + timedelta(hours=2)
            )
            
            db.add(new_post)
            optimizations_made += 1
        
        # Analyze successful patterns
        successful_posts = db.query(Post, Metrics).join(
            Metrics, Post.id == Metrics.post_id
        ).filter(
            Post.posted_at >= cutoff_time,
            Metrics.engagement_rate >= 5.0
        ).limit(10).all()
        
        strategies_identified = []
        
        for post, metrics in successful_posts:
            strategy = {
                "platform": post.platform,
                "topic": post.topic,
                "engagement_rate": metrics.engagement_rate,
                "content_length": len(post.content),
                "hashtag_count": post.content.count("#")
            }
            strategies_identified.append(strategy)
        
        db.commit()
        
        # Log agent activity
        log = AgentLog(
            agent_name="strategy_optimizer",
            action="optimize_strategy",
            data={
                "optimizations_made": optimizations_made,
                "successful_patterns": len(strategies_identified)
            },
            success=True
        )
        db.add(log)
        db.commit()
        
        return {
            "status": "success",
            "optimizations_made": optimizations_made,
            "successful_patterns": len(strategies_identified)
        }
        
    except Exception as e:
        db.rollback()
        log = AgentLog(
            agent_name="strategy_optimizer",
            action="optimize_strategy",
            data={"error": str(e)},
            success=False
        )
        db.add(log)
        db.commit()
        return {"status": "error", "message": str(e)}
    finally:
        db.close()

def get_optimization_insights():
    """Get strategy optimization insights"""
    db = SessionLocal()
    try:
        # Get recent optimizations
        recent_logs = db.query(AgentLog).filter(
            AgentLog.agent_name == "strategy_optimizer",
            AgentLog.created_at >= datetime.utcnow() - timedelta(days=7)
        ).order_by(AgentLog.created_at.desc()).limit(10).all()
        
        return {
            "recent_optimizations": [
                {
                    "action": log.action,
                    "data": log.data,
                    "success": log.success,
                    "created_at": log.created_at.isoformat()
                }
                for log in recent_logs
            ]
        }
    finally:
        db.close()