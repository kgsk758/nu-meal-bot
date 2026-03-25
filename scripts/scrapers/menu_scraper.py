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

        print(f"\n--- Debug: Fetching menu for shop {shop_id} ---")

        # 1. Initial GET to get the base cookie
        res1 = self.session.get(MenuSiteConfig.MAIN_PAGE)
        print(f"Step 1: Initial GET. URL: {res1.url}, Cookies: {len(self.session.cookies)}")

        # 2. First POST attempt
        res2 = self.session.post(
            url=MenuSiteConfig.MENU_PAGE,
            data=data,
            params=params,
            timeout=5
        )
        print(f"Step 2: Warm-up POST. Final URL: {res2.url}, Cookies: {len(self.session.cookies)}")

        # 3. Short wait
        time.sleep(0.5)

        # 4. Second POST attempt
        menu_page_res = self.session.post(
            url=MenuSiteConfig.MENU_PAGE,
            data=data,
            params=params,
            timeout=5
        )
        print(f"Step 3: Final POST. Final URL: {menu_page_res.url}, Cookies: {len(self.session.cookies)}")
        print(f"   Response snippet: {menu_page_res.text[:100].strip()}")

        return menu_page_res


