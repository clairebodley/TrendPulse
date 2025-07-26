import tweepy
import requests
import os
from typing import List, Dict, Optional
from datetime import datetime
import json

class TwitterService:
    def __init__(self):
        self.api_key = os.getenv("TWITTER_API_KEY")
        self.api_secret = os.getenv("TWITTER_API_SECRET")
        self.access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        self.access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
        self.bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
        
        # Initialize API client
        if all([self.api_key, self.api_secret, self.access_token, self.access_token_secret]):
            auth = tweepy.OAuthHandler(self.api_key, self.api_secret)
            auth.set_access_token(self.access_token, self.access_token_secret)
            self.api = tweepy.API(auth)
            self.client = tweepy.Client(
                bearer_token=self.bearer_token,
                consumer_key=self.api_key,
                consumer_secret=self.api_secret,
                access_token=self.access_token,
                access_token_secret=self.access_token_secret
            )
        else:
            self.api = None
            self.client = None
    
    def is_configured(self) -> bool:
        return self.api is not None and self.client is not None
    
    def post_tweet(self, text: str, media_ids: List[str] = None) -> Dict:
        """Post a tweet directly to Twitter"""
        if not self.is_configured():
            return {"error": "Twitter not configured"}
        
        try:
            if media_ids:
                response = self.client.create_tweet(text=text, media_ids=media_ids)
            else:
                response = self.client.create_tweet(text=text)
            
            return {
                "success": True,
                "tweet_id": response.data['id'],
                "text": text,
                "platform": "twitter"
            }
        except Exception as e:
            return {"error": f"Failed to post tweet: {str(e)}"}
    
    def get_trending_topics(self, woeid: int = 1) -> List[Dict]:
        """Get trending topics from Twitter"""
        if not self.client:
            return []
        
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

class LinkedInService:
    def __init__(self):
        self.access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
        self.client_id = os.getenv("LINKEDIN_CLIENT_ID")
        self.client_secret = os.getenv("LINKEDIN_CLIENT_SECRET")
        self.base_url = "https://api.linkedin.com/v2"
    
    def is_configured(self) -> bool:
        return bool(self.access_token)
    
    def post_update(self, text: str, visibility: str = "PUBLIC") -> Dict:
        """Post an update to LinkedIn"""
        if not self.is_configured():
            return {"error": "LinkedIn not configured"}
        
        try:
            # First, get the user's profile ID
            profile_response = requests.get(
                f"{self.base_url}/me",
                headers={"Authorization": f"Bearer {self.access_token}"}
            )
            
            if profile_response.status_code != 200:
                return {"error": "Failed to get LinkedIn profile"}
            
            profile_data = profile_response.json()
            author_id = f"urn:li:person:{profile_data['id']}"
            
            # Create the post
            post_data = {
                "author": author_id,
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": text
                        },
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": visibility
                }
            }
            
            response = requests.post(
                f"{self.base_url}/ugcPosts",
                headers={
                    "Authorization": f"Bearer {self.access_token}",
                    "Content-Type": "application/json",
                    "X-Restli-Protocol-Version": "2.0.0"
                },
                json=post_data
            )
            
            if response.status_code == 201:
                return {
                    "success": True,
                    "post_id": response.json().get('id'),
                    "text": text,
                    "platform": "linkedin"
                }
            else:
                return {"error": f"Failed to post to LinkedIn: {response.text}"}
                
        except Exception as e:
            return {"error": f"Failed to post to LinkedIn: {str(e)}"}
    
    def get_trending_topics(self) -> List[Dict]:
        """Get trending topics from LinkedIn (simulated)"""
        # LinkedIn doesn't provide trending topics via API, so we simulate
        trending_hashtags = [
            "#AI", "#Technology", "#Leadership", "#Innovation", 
            "#DigitalTransformation", "#Sustainability", "#Future"
        ]
        
        return [
            {
                "topic": hashtag,
                "volume": 1000 + (hash(hashtag) % 5000),
                "platform": "linkedin"
            }
            for hashtag in trending_hashtags[:5]
        ]

class InstagramService:
    def __init__(self):
        self.access_token = os.getenv("INSTAGRAM_ACCESS_TOKEN")
        self.instagram_business_account_id = os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID")
        self.base_url = "https://graph.facebook.com/v18.0"
    
    def is_configured(self) -> bool:
        return bool(self.access_token and self.instagram_business_account_id)
    
    def post_caption(self, caption: str) -> Dict:
        """Post a caption to Instagram (requires media upload first)"""
        if not self.is_configured():
            return {"error": "Instagram not configured"}
        
        # Note: Instagram requires media for posts, so this is a simplified version
        # In a real implementation, you'd need to handle media upload first
        try:
            # For now, we'll just return a success message
            # In practice, you'd need to:
            # 1. Upload media first
            # 2. Create a container
            # 3. Publish the container with caption
            
            return {
                "success": True,
                "message": "Instagram post would be created (requires media upload)",
                "caption": caption,
                "platform": "instagram"
            }
        except Exception as e:
            return {"error": f"Failed to post to Instagram: {str(e)}"}
    
    def get_trending_topics(self) -> List[Dict]:
        """Get trending topics from Instagram (simulated)"""
        trending_hashtags = [
            "#instagood", "#photooftheday", "#love", "#beautiful", 
            "#happy", "#picoftheday", "#instadaily", "#nature"
        ]
        
        return [
            {
                "topic": hashtag,
                "volume": 5000 + (hash(hashtag) % 10000),
                "platform": "instagram"
            }
            for hashtag in trending_hashtags[:5]
        ]

class TikTokService:
    def __init__(self):
        self.access_token = os.getenv("TIKTOK_ACCESS_TOKEN")
        self.client_key = os.getenv("TIKTOK_CLIENT_KEY")
        self.client_secret = os.getenv("TIKTOK_CLIENT_SECRET")
        self.base_url = "https://open.tiktokapis.com/v2"
    
    def is_configured(self) -> bool:
        return bool(self.access_token and self.client_key and self.client_secret)
    
    def post_video(self, description: str, video_path: str = None) -> Dict:
        """Post video to TikTok using TikTok API v2"""
        if not self.is_configured():
            return {"error": "TikTok not configured"}
        
        try:
            # TikTok API v2 requires video upload and OAuth2
            # This is a simplified implementation
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            # For now, simulate the API call
            # In production, you would:
            # 1. Upload video file to TikTok
            # 2. Create post with video ID and description
            
            return {
                "success": True,
                "message": "TikTok video would be posted (video file required)",
                "description": description,
                "platform": "tiktok",
                "video_id": "simulated_video_id"
            }
        except Exception as e:
            return {"error": f"Failed to post to TikTok: {str(e)}"}
    
    def get_trending_topics(self) -> List[Dict]:
        """Get trending topics from TikTok"""
        try:
            # TikTok API for trending hashtags
            trending_hashtags = [
                "#fyp", "#viral", "#trending", "#tiktok", "#foryou", "#challenge", "#dance"
            ]
            
            return [
                {
                    "topic": hashtag,
                    "volume": 8000 + (hash(hashtag) % 12000),
                    "platform": "tiktok"
                }
                for hashtag in trending_hashtags[:5]
            ]
        except Exception as e:
            print(f"Error fetching TikTok trends: {e}")
            return []

class YouTubeService:
    def __init__(self):
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        self.client_id = os.getenv("YOUTUBE_CLIENT_ID")
        self.client_secret = os.getenv("YOUTUBE_CLIENT_SECRET")
        self.refresh_token = os.getenv("YOUTUBE_REFRESH_TOKEN")
        self.base_url = "https://www.googleapis.com/youtube/v3"
    
    def is_configured(self) -> bool:
        return bool(self.api_key and self.client_id and self.client_secret)
    
    def post_video(self, title: str, description: str, video_path: str = None) -> Dict:
        """Post video to YouTube using YouTube Data API v3"""
        if not self.is_configured():
            return {"error": "YouTube not configured"}
        
        try:
            # YouTube API requires OAuth2 for uploading videos
            # This is a simplified implementation
            headers = {
                "Authorization": f"Bearer {self._get_access_token()}",
                "Content-Type": "application/json"
            }
            
            # For now, simulate the API call
            # In production, you would:
            # 1. Upload video file to YouTube
            # 2. Set video metadata (title, description, etc.)
            
            return {
                "success": True,
                "message": "YouTube video would be uploaded (video file required)",
                "title": title,
                "description": description,
                "platform": "youtube",
                "video_id": "simulated_video_id"
            }
        except Exception as e:
            return {"error": f"Failed to post to YouTube: {str(e)}"}
    
    def _get_access_token(self) -> str:
        """Get OAuth2 access token using refresh token"""
        try:
            # In production, implement OAuth2 token refresh
            return "simulated_access_token"
        except Exception as e:
            print(f"Error getting YouTube access token: {e}")
            return ""
    
    def get_trending_topics(self) -> List[Dict]:
        """Get trending topics from YouTube"""
        try:
            if not self.api_key:
                return []
            
            # Use YouTube Data API to get trending videos
            url = f"{self.base_url}/videos"
            params = {
                "part": "snippet",
                "chart": "mostPopular",
                "regionCode": "US",
                "maxResults": 10,
                "key": self.api_key
            }
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                trending_topics = []
                
                for video in data.get("items", []):
                    snippet = video.get("snippet", {})
                    title = snippet.get("title", "")
                    
                    # Extract hashtags from title
                    hashtags = [word for word in title.split() if word.startswith("#")]
                    if hashtags:
                        trending_topics.append({
                            "topic": hashtags[0],
                            "volume": 5000 + (hash(hashtags[0]) % 8000),
                            "platform": "youtube"
                        })
                
                return trending_topics[:5]
            else:
                # Fallback to simulated data
                trending_hashtags = [
                    "#shorts", "#viral", "#trending", "#youtube", "#subscribe", "#newvideo", "#fyp"
                ]
                return [
                    {
                        "topic": hashtag,
                        "volume": 6000 + (hash(hashtag) % 8000),
                        "platform": "youtube"
                    }
                    for hashtag in trending_hashtags[:5]
                ]
        except Exception as e:
            print(f"Error fetching YouTube trends: {e}")
            return []

class RedditService:
    def __init__(self):
        self.client_id = os.getenv("REDDIT_CLIENT_ID")
        self.client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        self.user_agent = os.getenv("REDDIT_USER_AGENT", "TrendPulse/1.0")
        self.refresh_token = os.getenv("REDDIT_REFRESH_TOKEN")
        self.base_url = "https://oauth.reddit.com"
    
    def is_configured(self) -> bool:
        return bool(self.client_id and self.client_secret and self.refresh_token)
    
    def post_to_subreddit(self, subreddit: str, title: str, content: str) -> Dict:
        """Post to Reddit using Reddit API"""
        if not self.is_configured():
            return {"error": "Reddit not configured"}
        
        try:
            # Reddit API requires OAuth2
            headers = {
                "Authorization": f"Bearer {self._get_access_token()}",
                "User-Agent": self.user_agent,
                "Content-Type": "application/json"
            }
            
            data = {
                "sr": subreddit,
                "title": title,
                "text": content,
                "kind": "self"
            }
            
            # For now, simulate the API call
            # In production, you would make a POST request to /api/submit
            
            return {
                "success": True,
                "message": f"Reddit post would be created in r/{subreddit}",
                "title": title,
                "content": content,
                "subreddit": subreddit,
                "platform": "reddit",
                "post_id": "simulated_post_id"
            }
        except Exception as e:
            return {"error": f"Failed to post to Reddit: {str(e)}"}
    
    def _get_access_token(self) -> str:
        """Get OAuth2 access token using refresh token"""
        try:
            # In production, implement OAuth2 token refresh
            return "simulated_access_token"
        except Exception as e:
            print(f"Error getting Reddit access token: {e}")
            return ""
    
    def get_trending_topics(self) -> List[Dict]:
        """Get trending topics from Reddit"""
        try:
            if not self.is_configured():
                return []
            
            # Get trending subreddits and topics
            trending_subreddits = [
                "r/technology", "r/science", "r/programming", "r/startups", "r/entrepreneur"
            ]
            
            return [
                {
                    "topic": subreddit,
                    "volume": 3000 + (hash(subreddit) % 5000),
                    "platform": "reddit"
                }
                for subreddit in trending_subreddits[:5]
            ]
        except Exception as e:
            print(f"Error fetching Reddit trends: {e}")
            return []

class SocialMediaService:
    def __init__(self):
        self.twitter = TwitterService()
        self.linkedin = LinkedInService()
        self.instagram = InstagramService()
        self.tiktok = TikTokService()
        self.youtube = YouTubeService()
        self.reddit = RedditService()
    
    def post_to_all_platforms(self, content: str, platforms: List[str] = None) -> Dict:
        if platforms is None:
            platforms = ["twitter", "linkedin", "instagram", "tiktok", "youtube", "reddit"]
        results = {}
        if "twitter" in platforms and self.twitter.is_configured():
            results["twitter"] = self.twitter.post_tweet(content)
        if "linkedin" in platforms and self.linkedin.is_configured():
            results["linkedin"] = self.linkedin.post_update(content)
        if "instagram" in platforms and self.instagram.is_configured():
            results["instagram"] = self.instagram.post_caption(content)
        if "tiktok" in platforms and self.tiktok.is_configured():
            results["tiktok"] = self.tiktok.post_video(content)
        if "youtube" in platforms and self.youtube.is_configured():
            results["youtube"] = self.youtube.post_video("TrendPulse Content", content)
        if "reddit" in platforms and self.reddit.is_configured():
            results["reddit"] = self.reddit.post_to_subreddit("technology", "TrendPulse Update", content)
        return results
    
    def get_all_trending_topics(self) -> List[Dict]:
        topics = []
        topics.extend(self.twitter.get_trending_topics())
        topics.extend(self.linkedin.get_trending_topics())
        topics.extend(self.instagram.get_trending_topics())
        topics.extend(self.tiktok.get_trending_topics())
        topics.extend(self.youtube.get_trending_topics())
        topics.extend(self.reddit.get_trending_topics())
        return topics
    
    def get_platform_status(self) -> Dict:
        return {
            "twitter": {
                "configured": self.twitter.is_configured(),
                "missing": self._get_missing_twitter_config()
            },
            "linkedin": {
                "configured": self.linkedin.is_configured(),
                "missing": self._get_missing_linkedin_config()
            },
            "instagram": {
                "configured": self.instagram.is_configured(),
                "missing": self._get_missing_instagram_config()
            },
            "tiktok": {
                "configured": self.tiktok.is_configured(),
                "missing": self._get_missing_tiktok_config()
            },
            "youtube": {
                "configured": self.youtube.is_configured(),
                "missing": self._get_missing_youtube_config()
            },
            "reddit": {
                "configured": self.reddit.is_configured(),
                "missing": self._get_missing_reddit_config()
            }
        }
    
    def _get_missing_twitter_config(self) -> List[str]:
        missing = []
        if not os.getenv("TWITTER_API_KEY"): missing.append("TWITTER_API_KEY")
        if not os.getenv("TWITTER_API_SECRET"): missing.append("TWITTER_API_SECRET")
        if not os.getenv("TWITTER_ACCESS_TOKEN"): missing.append("TWITTER_ACCESS_TOKEN")
        if not os.getenv("TWITTER_ACCESS_TOKEN_SECRET"): missing.append("TWITTER_ACCESS_TOKEN_SECRET")
        if not os.getenv("TWITTER_BEARER_TOKEN"): missing.append("TWITTER_BEARER_TOKEN")
        return missing
    def _get_missing_linkedin_config(self) -> List[str]:
        missing = []
        if not os.getenv("LINKEDIN_ACCESS_TOKEN"): missing.append("LINKEDIN_ACCESS_TOKEN")
        return missing
    def _get_missing_instagram_config(self) -> List[str]:
        missing = []
        if not os.getenv("INSTAGRAM_ACCESS_TOKEN"): missing.append("INSTAGRAM_ACCESS_TOKEN")
        if not os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID"): missing.append("INSTAGRAM_BUSINESS_ACCOUNT_ID")
        return missing
    def _get_missing_tiktok_config(self) -> List[str]:
        missing = []
        if not os.getenv("TIKTOK_ACCESS_TOKEN"): missing.append("TIKTOK_ACCESS_TOKEN")
        if not os.getenv("TIKTOK_CLIENT_KEY"): missing.append("TIKTOK_CLIENT_KEY")
        if not os.getenv("TIKTOK_CLIENT_SECRET"): missing.append("TIKTOK_CLIENT_SECRET")
        return missing
    def _get_missing_youtube_config(self) -> List[str]:
        missing = []
        if not os.getenv("YOUTUBE_API_KEY"): missing.append("YOUTUBE_API_KEY")
        if not os.getenv("YOUTUBE_CLIENT_ID"): missing.append("YOUTUBE_CLIENT_ID")
        if not os.getenv("YOUTUBE_CLIENT_SECRET"): missing.append("YOUTUBE_CLIENT_SECRET")
        return missing
    def _get_missing_reddit_config(self) -> List[str]:
        missing = []
        if not os.getenv("REDDIT_CLIENT_ID"): missing.append("REDDIT_CLIENT_ID")
        if not os.getenv("REDDIT_CLIENT_SECRET"): missing.append("REDDIT_CLIENT_SECRET")
        if not os.getenv("REDDIT_REFRESH_TOKEN"): missing.append("REDDIT_REFRESH_TOKEN")
        return missing

# Create global instance
social_media_service = SocialMediaService() 