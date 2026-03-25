from .scraper_base import ScraperBase
from config.constants import MenuSiteConfig, Shops

import copy

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

        self.set_cookie(MenuSiteConfig.MAIN_PAGE)

        headers = {
            "Referer": MenuSiteConfig.MAIN_PAGE,
            "Origin": "https://signage.univcoop-tokai.net",
        }

        menu_page_res = self.session.post(
            url=MenuSiteConfig.MENU_PAGE,
            data=data,
            params=params,
            headers=headers,
            timeout=5
        )

        if "index.php" in menu_page_res.url:
            menu_page_res = self.session.post(
                url=MenuSiteConfig.MENU_PAGE,
                data=data,
                params=params,
                headers=headers,
                timeout=5
            )

        return menu_page_res




