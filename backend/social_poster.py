import tweepy
from linkedin_api import Linkedin
import instabot
import threading

class SocialMediaAGI:
    def __init__(self):
        self.platforms = {
            'linkedin': Linkedin('api_key'),
            'twitter': tweepy.Client(
                consumer_key="YOUR_KEY",
                consumer_secret="YOUR_SECRET",
                access_token="TOKEN",
                access_token_secret="TOKEN_SECRET"
            ),
            'instagram': instabot.Bot()
        }
        self.post_queue = []

    def queue_post(self, content):
        """Thread-safe content buffering"""
        with threading.Lock():
            self.post_queue.append(content)

    def process_queue(self):
        """Autonomous posting engine"""
        while True:
            if self.post_queue:
                content = self.post_queue.pop(0)
                self.distribute(content)
            time.sleep(60)

    def distribute(self, content):
        """Multi-platform adaptive posting"""
        try:
            # LinkedIn
            if content['type'] == 'article':
                self.platforms['linkedin'].post_article(
                    title=content['title'],
                    text=content['body']
                )

            # Twitter
            elif len(content['text']) <= 280:
                self.platforms['twitter'].create_tweet(text=content['text'])

            # Instagram
            if 'image_path' in content:
                self.platforms['instagram'].upload_photo(
                    content['image_path'],
                    caption=content['text'][:2200]
                )
        except Exception as e:
            self.repair_connection()

if __name__ == "__main__":
    agi = SocialMediaAGI()
    agi.process_queue()
