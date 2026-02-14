import sys
from pathlib import Path
from datetime import date
import os
from dotenv import load_dotenv

root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

from scrapers import MenuScraper, ScheduleScraper
from parsers import ScheduleParser, MenuParser
from config import constants
from image_merger import ImageMerger
from tweet_builder import TweetBuilder
from twitter_client import TwitterClient

print("\nstart main.py\n")

today = date.today()

env_path = root_dir / 'config' / '.env'
load_dotenv(dotenv_path=env_path)
ck=os.getenv("ck")
cs=os.getenv("cs")
at=os.getenv("at")
ats=os.getenv("ats")
twitter_client = TwitterClient(
    consumer_key=ck,
    consumer_secret=cs,
    access_token=at,
    access_token_secret=ats
)

menu_scraper = MenuScraper()
schedule_scraper = ScheduleScraper()

schedule_res = schedule_scraper.get_schedule()

#if img_links:
#    merged_img = ImageMerger.merge_from_urls(urls=img_links, session=menu_scraper.session)
#    with open("merged.png", "wb") as f:
#        f.write(merged_img.getbuffer())

shop_idx_list = [
    constants.ShopIndex.IGAKUBU,
    constants.ShopIndex.FOREST,
    constants.ShopIndex.HOKUBU,
    constants.ShopIndex.DINING,
    constants.ShopIndex.SAI,
]

closed_list = []

for shop_idx in shop_idx_list:
    shop_names = constants.Shops.NAMES

    shop_state = None

    schedule_parser = ScheduleParser(schedule_res)
    
    shop_state = schedule_parser.get_shop_state_today(shop_idx, today.day)

    if '休業' in shop_state:
        closed_list.append(shop_names[shop_idx])
        continue
    
    menu_res = menu_scraper.get_menu(shop_idx)

    if menu_res is None:
        raise RuntimeError("failed to get menu_res")
    
    menu_parser = MenuParser(menu_res)
    img_links = menu_parser.get_img_links()

    merged_img = None
    if img_links:
        merged_img = ImageMerger.merge_from_urls(urls=img_links, session=menu_scraper.session)
    else:
        raise RuntimeError("couldn't get any image links")
    
    tweet = TweetBuilder.get_open_tweet_text(today,shop_names[shop_idx],shop_state)
    print(tweet)

if closed_list:
    tweet = TweetBuilder.get_closed_tweet_text(today, closed_list)
    print(tweet)