import sys
from pathlib import Path
from datetime import date

root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

from scrapers import MenuScraper, ScheduleScraper
from parsers import ScheduleParser, MenuParser
from config import constants
from image_merger import ImageMerger
from tweet_builder import TweetBuilder



print("\nstart main.py\n")

today = date.today()
menu_scraper = MenuScraper()
schedule_scraper = ScheduleScraper()

menu_res = menu_scraper.get_menu(constants.MenuSiteConfig.HOKUBU_ID)
schedule_res = schedule_scraper.get_schedule()

if menu_res is None or schedule_res is None:
    raise RuntimeError("failed to get menu or schedule response")

shop_state = None

schedule_parser = ScheduleParser(schedule_res)
shop_state = schedule_parser.get_shop_state_today(constants.ShopIndex.DINING, today.day)
print(shop_state)

menu_parser = MenuParser(menu_res)
img_links = menu_parser.get_img_links()
print(img_links)

if img_links:
    merged_img = ImageMerger.merge_from_urls(urls=img_links, session=menu_scraper.session)
    with open("merged.png", "wb") as f:
        f.write(merged_img.getbuffer())

tweet = TweetBuilder.get_open_tweet_text(today,constants.ScheduleSiteConfig.SHOP_NAMES[constants.ShopIndex.DINING],shop_state)
print(tweet)