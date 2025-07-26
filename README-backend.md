# TrendPulse Multi-Agent Backend

A sophisticated multi-agent architecture for social media trend spotting and content optimization.

## 🏗️ Architecture

### 5 Core Agents:
- **TrendWatcherAgent**: Monitors Twitter, LinkedIn, Instagram for trending topics
- **ContentCrafterAgent**: Generates AI-powered content using GPT-4
- **PostSchedulerAgent**: Schedules posts via Buffer API
- **EngagementMonitorAgent**: Tracks performance metrics
- **StrategyOptimizerAgent**: A/B tests and optimizes content

### Technology Stack:
- **FastAPI** - High-performance API framework
- **Celery** - Distributed task queue for background agents
- **Redis** - Message broker and caching
- **PostgreSQL** - Persistent data storage
- **Docker** - Containerized deployment

## 🚀 Quick Start

1. **Clone and setup environment:**
```bash
cp backend/.env.example backend/.env
# Edit .env with your API keys
```

2. **Start with Docker:**
```bash
docker-compose up -d
```

3. **API will be available at:**
- FastAPI: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 🔑 Required API Keys

### Buffer (Multi-platform posting)
1. Go to https://buffer.com/developers
2. Create app and get access token
3. Connect your social accounts

### OpenAI (Content generation)
1. Get API key from https://platform.openai.com
2. Add to OPENAI_API_KEY in .env

### Twitter (Trend monitoring)
1. Create developer account at https://developer.twitter.com
2. Get Bearer Token for API v2
3. Add to TWITTER_BEARER_TOKEN in .env

## 📊 API Endpoints

- `GET /api/trends` - Current trending topics
- `GET /api/drafts` - Generated content drafts
- `GET /api/posts` - Scheduled posts
- `GET /api/metrics` - Engagement analytics
- `GET /api/agents/status` - Agent health status
- `POST /api/generate-content` - Generate content for topic
- `POST /api/schedule-post` - Schedule a new post

## 🔄 Agent Workflow

1. **TrendWatcher** fetches trending topics every 5 minutes
2. **ContentCrafter** generates posts for trending topics
3. **PostScheduler** queues posts via Buffer at optimal times
4. **EngagementMonitor** tracks performance every 3 minutes
5. **StrategyOptimizer** analyzes and improves strategy every 10 minutes

## 🐳 Docker Services

- `backend` - FastAPI application
- `celery-worker` - Background task processor
- `celery-beat` - Task scheduler
- `redis` - Message broker
- `postgres` - Database

## 📈 Monitoring

View logs and agent activity:
```bash
docker-compose logs -f backend
docker-compose logs -f celery-worker
```

## 🔧 Development

Run without Docker:
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
celery -A main.celery worker --loglevel=info
celery -A main.celery beat --loglevel=info
```