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

        # 1. First GET to trigger the 302 and receive PHPSESSID
        self.session.get(MenuSiteConfig.MAIN_PAGE, allow_redirects=True)

        # 2. Second GET to confirm session with a 200 OK, mimicking the browser's redirect follow
        self.session.get(MenuSiteConfig.MAIN_PAGE)

        # Browser-like headers for the POST request
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "ja,en;q=0.9",
            "Origin": "https://signage.univcoop-tokai.net",
            "Referer": MenuSiteConfig.MAIN_PAGE,
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0",
        }

        # 3. First POST attempt
        menu_page_res = self.session.post(
            url=MenuSiteConfig.MENU_PAGE,
            data=data,
            params=params,
            headers=headers,
            allow_redirects=True,
            timeout=5
        )

        # 4. If still redirected to index.php, wait and try once more with the updated session
        if "index.php" in menu_page_res.url:
            time.sleep(0.5)
            menu_page_res = self.session.post(
                url=MenuSiteConfig.MENU_PAGE,
                data=data,
                params=params,
                headers=headers,
                allow_redirects=True,
                timeout=5
            )

        return menu_page_res
