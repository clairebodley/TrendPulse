import tweepy
import requests
import os
from typing import List, Dict

class TwitterService:
    def __init__(self):
        self.bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
        self.client = tweepy.Client(bearer_token=self.bearer_token)
    
    def get_trending_topics(self, woeid: int = 1) -> List[Dict]:
        """Get trending topics from Twitter"""
        try:
            trends = self.client.get_place_trends(woeid)
            return [
                {
                    "topic": trend.name,
                    "volume": trend.tweet_volume or 0,
                    "platform": "twitter"
                }
                for trend in trends[0].trends[:10]
            ]
        except Exception as e:
            print(f"Error fetching Twitter trends: {e}")
            return []
    
    def search_recent_tweets(self, query: str, max_results: int = 10) -> List[Dict]:
        """Search recent tweets for sentiment analysis"""
        try:
            tweets = self.client.search_recent_tweets(
                query=query,
                max_results=max_results,
                tweet_fields=['public_metrics', 'created_at']
            )
            return [
                {
                    "text": tweet.text,
                    "metrics": tweet.public_metrics,
                    "created_at": tweet.created_at
                }
                for tweet in tweets.data or []
            ]
        except Exception as e:
            print(f"Error searching tweets: {e}")
            return []

class LinkedInService:
    def __init__(self):
        # LinkedIn trending is not available via API
        # We'll simulate by tracking popular business hashtags
        self.trending_hashtags = [
            "#AI", "#Technology", "#Leadership", "#Innovation", 
            "#DigitalTransformation", "#Sustainability", "#Future"
        ]
    
    def get_trending_topics(self) -> List[Dict]:
        """Simulate LinkedIn trending topics"""
        return [
            {
                "topic": hashtag,
                "volume": 1000 + (hash(hashtag) % 5000),
                "platform": "linkedin"
            }
            for hashtag in self.trending_hashtags[:5]
        ]

class InstagramService:
    def __init__(self):
        # Instagram trending via hashtag popularity
        self.trending_hashtags = [
            "#instagood", "#photooftheday", "#love", "#beautiful", 
            "#happy", "#picoftheday", "#instadaily", "#nature"
        ]
    
    def get_trending_topics(self) -> List[Dict]:
        """Simulate Instagram trending topics"""
        return [
            {
                "topic": hashtag,
                "volume": 5000 + (hash(hashtag) % 10000),
                "platform": "instagram"
            }
            for hashtag in self.trending_hashtags[:5]
        ]

# Service instances
twitter_service = TwitterService()
linkedin_service = LinkedInService()
instagram_service = InstagramService()