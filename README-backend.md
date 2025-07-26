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

### Twitter (Direct posting)
1. Go to https://developer.twitter.com
2. Create a developer account and app
3. Get your API Key, API Secret, Access Token, and Access Token Secret
4. Get your Bearer Token for API v2

### LinkedIn (Direct posting)
1. Go to https://www.linkedin.com/developers/
2. Create a new app
3. Get your Client ID and Client Secret
4. Generate an access token with posting permissions

### Instagram (Direct posting)
1. Go to https://developers.facebook.com
2. Create a Facebook app
3. Add Instagram Basic Display or Instagram Graph API
4. Get your access token and business account ID

### OpenAI (Content generation)
1. Get API key from https://platform.openai.com
2. Add to OPENAI_API_KEY in .env

## 🔐 Social Media API Setup

The application now uses direct social media APIs instead of Buffer. Here's how to set up each platform:

### Environment Variables

Add these to your `.env` file:

```bash
# Twitter API (for posting and trend monitoring)
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
TWITTER_BEARER_TOKEN=your_twitter_bearer_token

# LinkedIn API
LINKEDIN_ACCESS_TOKEN=your_linkedin_access_token
LINKEDIN_CLIENT_ID=your_linkedin_client_id
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret

# Instagram API
INSTAGRAM_ACCESS_TOKEN=your_instagram_access_token
INSTAGRAM_BUSINESS_ACCOUNT_ID=your_instagram_business_account_id
```

## 📊 API Endpoints

- `GET /api/trends` - Current trending topics
- `GET /api/drafts` - Generated content drafts
- `GET /api/posts` - Scheduled posts
- `GET /api/metrics` - Engagement analytics
- `GET /api/agents/status` - Agent health status
- `POST /api/generate-content` - Generate content for topic
- `POST /api/schedule-post` - Schedule a new post
- `GET /api/social/status` - Check social media platform configuration
- `POST /api/social/post` - Post content to social media platforms
- `GET /api/social/trends` - Get trending topics from all platforms

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