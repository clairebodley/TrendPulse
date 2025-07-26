import openai
import os
from typing import Dict, List

class OpenAIService:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
    def generate_post_content(self, topic: str, platform: str, tone: str = "engaging") -> str:
        """Generate platform-specific content for a topic"""
        
        platform_prompts = {
            "twitter": f"Write a witty, engaging tweet about '{topic}'. Keep it under 280 characters. Include relevant hashtags. Tone: {tone}",
            "linkedin": f"Write a professional LinkedIn post about '{topic}'. Make it insightful and engaging. Include a call-to-action. Tone: {tone}",
            "instagram": f"Write an Instagram caption about '{topic}'. Make it visually engaging with emojis and 3-5 hashtags. Tone: {tone}"
        }
        
        prompt = platform_prompts.get(platform, platform_prompts["twitter"])
        
        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a social media expert creating engaging content."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error generating content: {str(e)}"
    
    def generate_content_variants(self, topic: str, platform: str, count: int = 2) -> List[str]:
        """Generate multiple content variants for A/B testing"""
        variants = []
        for i in range(count):
            tone = ["engaging", "professional", "witty", "informative"][i % 4]
            content = self.generate_post_content(topic, platform, tone)
            variants.append(content)
        return variants
    
    def optimize_content(self, original_content: str, performance_data: Dict) -> str:
        """Optimize content based on performance data"""
        prompt = f"""
        Original post: "{original_content}"
        Performance: {performance_data.get('engagement_rate', 0)}% engagement rate
        
        Rewrite this post to improve engagement. Focus on:
        - Better hook/opening
        - More compelling call-to-action
        - Better hashtag selection
        - More engaging tone
        """
        
        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a social media optimization expert."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.8
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return original_content

openai_service = OpenAIService()