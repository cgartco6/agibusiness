import tweepy
from linkedin_api import Linkedin
import instabot
from .base_agent import BaseAgent
from datetime import datetime
import time

class SocialPosterAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_id="social_poster_v3",
            capabilities=["cross_posting", "scheduling", "analytics"]
        )
        self.platforms = {
            'twitter': self._init_twitter(),
            'linkedin': Linkedin(
                os.getenv('LINKEDIN_EMAIL'),
                os.getenv('LINKEDIN_PASSWORD')
            ),
            'instagram': instabot.Bot()
        }
    
    def _init_twitter(self):
        return tweepy.Client(
            consumer_key=os.getenv('TWITTER_API_KEY'),
            consumer_secret=os.getenv('TWITTER_API_SECRET'),
            access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
            access_token_secret=os.getenv('TWITTER_ACCESS_SECRET')
        )
    
    def post_to_all(self, content, platforms=None, schedule_time=None):
        """Post content to multiple platforms"""
        results = {}
        platforms = platforms or self.platforms.keys()
        
        for platform in platforms:
            try:
                if schedule_time:
                    self._schedule_post(platform, content, schedule_time)
                    results[platform] = "scheduled"
                else:
                    results[platform] = self._post_now(platform, content)
            except Exception as e:
                results[platform] = f"error: {str(e)}"
                self.log_error(f"{platform} post failed: {str(e)}")
        
        return results
    
    def _post_now(self, platform, content):
        """Immediate posting logic"""
        if platform == 'twitter':
            return self.platforms['twitter'].create_tweet(text=content['text'])
        elif platform == 'linkedin':
            return self.platforms['linkedin'].post_article(content['title'], content['text'])
        elif platform == 'instagram':
            return self.platforms['instagram'].upload_photo(content['image_path'], caption=content['text'])
    
    def _schedule_post(self, platform, content, schedule_time):
        """Queue post for future time"""
        # In production: Would integrate with Celery or similar
        delay = (schedule_time - datetime.now()).total_seconds()
        if delay > 0:
            time.sleep(delay)
            return self._post_now(platform, content)
        raise ValueError("Schedule time must be in the future")
