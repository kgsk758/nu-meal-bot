from .scraper_base import ScraperBase
from config.constants import ScheduleSiteConfig

class ScheduleScraper(ScraperBase):
    def get_schedule(self):
        schedule_res = self._get(ScheduleSiteConfig.MAIN_PAGE)
        return schedule_res