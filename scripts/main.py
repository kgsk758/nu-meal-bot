import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

from scrapers.menu_scraper import MenuScraper
from scrapers.schedule_scraper import ScheduleScraper
from config import constants
from scripts.parsers.schedule_parser import ScheduleParser

print("\nstart main.py\n")

menu_scraper = MenuScraper()
schedule_scraper = ScheduleScraper()

menu_res = menu_scraper.get_menu(constants.MenuSiteConfig.FOREST_ID)
schedule_res = schedule_scraper.get_schedule()

if menu_res is None or schedule_res is None:
    raise RuntimeError("failed to get menu or schedule response")

shop_status = None
try:
    menu_parser = ScheduleParser(schedule_res)
    shop_status = menu_parser.get_shop_state_today(constants.ShopIndex.DINING, "25")
except RuntimeError as e:
    print(f"failed to get schedule:{e}")

print(shop_status)
