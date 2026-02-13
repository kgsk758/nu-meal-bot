import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

from scrapers.menu_scraper import MenuScraper
from scrapers.schedule_scraper import ScheduleScraper
from config import constants

print("\nstart main.py\n")

menu_scraper = MenuScraper()
menu_res = menu_scraper.get_menu(constants.MenuSiteConfig.FOREST_ID)
schedule_scraper = ScheduleScraper()
schedule_res = schedule_scraper.get_schedule()
print(schedule_res)
