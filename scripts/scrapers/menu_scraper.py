from .scraper_base import ScraperBase
from config.constants import MenuSiteConfig, Shops
import copy
import time

class MenuScraper(ScraperBase):
    def set_cookie(self, url):
        return self._get(url)

    def get_menu(self, shop_idx: int):
        shop_id = Shops.IDS[shop_idx]
        form_data = copy.deepcopy(MenuSiteConfig.FORM_DATA)
        form_data["data"]["shop_id"] = shop_id
        
        # 1. Initialize session and get cookies
        self.set_cookie(MenuSiteConfig.MAIN_PAGE)

        # 2. POST to get the menu (with a retry if redirected back to index)
        headers = {"Referer": MenuSiteConfig.MAIN_PAGE}
        res = self.session.post(
            MenuSiteConfig.MENU_PAGE, 
            data=form_data["data"], 
            params=form_data["params"], 
            headers=headers
        )
        
        if "index.php" in res.url:
            time.sleep(0.5)
            res = self.session.post(
                MenuSiteConfig.MENU_PAGE, 
                data=form_data["data"], 
                params=form_data["params"], 
                headers=headers
            )

        return res
