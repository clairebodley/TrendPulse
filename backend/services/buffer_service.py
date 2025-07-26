import requests
import os
from typing import List, Dict

class BufferService:
    def __init__(self):
        self.access_token = os.getenv("BUFFER_ACCESS_TOKEN")
        self.base_url = "https://api.bufferapp.com/1"
        
    def get_profiles(self) -> List[Dict]:
        """Get all connected social media profiles"""
        response = requests.get(
            f"{self.base_url}/profiles.json",
            params={"access_token": self.access_token}
        )
        return response.json() if response.status_code == 200 else []
    
    def create_post(self, profile_ids: List[str], text: str, scheduled_at: str = None, media: Dict = None) -> Dict:
        """Create a new post"""
        data = {
            "access_token": self.access_token,
            "text": text,
            "profile_ids[]": profile_ids,
            "now": scheduled_at is None
        }
        
        if scheduled_at:
            data["scheduled_at"] = scheduled_at
            
        if media:
            data.update(media)
            
        response = requests.post(
            f"{self.base_url}/updates/create.json",
            data=data
        )
        return response.json() if response.status_code == 200 else {"error": "Failed to create post"}
    
    def get_post_stats(self, update_id: str) -> Dict:
        """Get engagement stats for a post"""
        response = requests.get(
            f"{self.base_url}/updates/{update_id}.json",
            params={"access_token": self.access_token}
        )
        return response.json() if response.status_code == 200 else {}
    
    def get_profile_by_service(self, service: str) -> Dict:
        """Get profile ID for a specific service (twitter, linkedin, instagram)"""
        profiles = self.get_profiles()
        for profile in profiles:
            if profile.get("service") == service:
                return profile
        return {}

buffer_service = BufferService()