from config.constants import TweetTemplate
from datetime import date

class TweetBuilder:
    def get_open_tweet_text(date: date, shop_name: str, shop_state: str)->str:
        full_date = f"{date.year}/{date.month}/{date.day}"
        return TweetTemplate.OPEN_TWEET(full_date, shop_name, shop_state)
    def get_closed_tweet_text(date: date, shop_names:list[str])->str:
        full_date = f"{date.year}/{date.month}/{date.day}"
        closed_shops_str = ', '.join(shop_names)
        return TweetTemplate.CLOSED_TWEET(full_date, closed_shops_str)