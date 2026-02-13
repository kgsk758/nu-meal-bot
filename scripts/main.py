import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

from scrapers.menu_scraper import MenuScraper
from config import constants

print("start main.py")

menu_scraper = MenuScraper()
menu_res = menu_scraper.get_menu(constants.MenuSiteConfig.FOREST_ID)
print(menu_res.text)
