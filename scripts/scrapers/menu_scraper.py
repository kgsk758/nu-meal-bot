from .scraper_base import ScraperBase
from config.constants import MenuSiteConfig, Shops

import copy

import time

class MenuScraper(ScraperBase):
    def set_cookie(self, URL):
        res = self._get(URL)
        return res
    def get_menu(self, shop_idx: int):
        shop_id = Shops.IDS[shop_idx]
        form_data = copy.deepcopy(MenuSiteConfig.FORM_DATA)
        form_data["data"]["shop_id"] = shop_id
        params = form_data["params"]
        data = form_data["data"]

        # Set browser-like headers for the entire session
        self.session.headers.update({
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "ja,en;q=0.9",
            "Origin": "https://signage.univcoop-tokai.net",
            "Referer": MenuSiteConfig.MAIN_PAGE,
        })

        # 1. Initial GET to get the base cookie
        self.session.get(MenuSiteConfig.MAIN_PAGE)

        # 2. First POST attempt (often redirects/fails to establish session properly)
        self.session.post(
            url=MenuSiteConfig.MENU_PAGE,
            data=data,
            params=params,
            timeout=5
        )

        # 3. Short wait to mimic human behavior/server processing
        time.sleep(0.5)

        # 4. Second POST attempt (the real one)
        menu_page_res = self.session.post(
            url=MenuSiteConfig.MENU_PAGE,
            data=data,
            params=params,
            timeout=5
        )

        return menu_page_res



