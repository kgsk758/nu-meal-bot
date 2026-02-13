import tweepy
class TwitterClient:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.client = tweepy.Client(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
            )
        self.auth = tweepy.OAuth1UserHandler(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
            )
        self.api = tweepy.API(self.auth)
    
    def post(self, text, file=None):
        try:
            media_ids = None
            if file:
                media = self.api.media_upload(filename="image.png", file=file)
                media_ids = [media.media_id]
            self.client.create_tweet(text=text, media_ids=media_ids)
            print("ツイートに成功")
        except tweepy.TweepyException as e:
            print(f"ツイートに失敗:{e}")
