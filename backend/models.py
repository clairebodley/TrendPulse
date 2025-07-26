from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Text, JSON
from sqlalchemy.sql import func
from database import Base

class Trend(Base):
    __tablename__ = "trends"
    
    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, index=True)
    platform = Column(String)
    volume = Column(Integer)
    sentiment = Column(String)
    growth = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String)
    content = Column(Text)
    platform = Column(String)
    status = Column(String, default="draft")
    scheduled_for = Column(DateTime(timezone=True))
    posted_at = Column(DateTime(timezone=True))
    buffer_id = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Metrics(Base):
    __tablename__ = "metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer)
    platform = Column(String)
    likes = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    engagement_rate = Column(Float, default=0.0)
    measured_at = Column(DateTime(timezone=True), server_default=func.now())

class AgentLog(Base):
    __tablename__ = "agent_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    agent_name = Column(String)
    action = Column(String)
    data = Column(JSON)
    success = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())