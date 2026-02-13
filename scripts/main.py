import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

from scrapers.menu_scraper import MenuScraper
from scrapers.schedule_scraper import ScheduleScraper
from config import constants
from scripts.parsers.schedule_parser import ScheduleParser
from scripts.parsers.menu_parser import MenuParser

print("\nstart main.py\n")

menu_scraper = MenuScraper()
schedule_scraper = ScheduleScraper()

menu_res = menu_scraper.get_menu(constants.MenuSiteConfig.FOREST_ID)
schedule_res = schedule_scraper.get_schedule()

if menu_res is None or schedule_res is None:
    raise RuntimeError("failed to get menu or schedule response")

shop_status = None

schedule_parser = ScheduleParser(schedule_res)
shop_status = schedule_parser.get_shop_state_today(constants.ShopIndex.DINING, "25")
print(shop_status)
shop_status = schedule_parser.get_shop_state_today(constants.ShopIndex.HOKUBU, "16")
print(shop_status)

menu_parser = MenuParser(menu_res)
img_links = menu_parser.get_img_links()
print(img_links)