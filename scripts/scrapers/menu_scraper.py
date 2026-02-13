from .scraper_base import ScraperBase
from config.constants import MenuSiteConfig
import copy

class MenuScraper(ScraperBase):
    def set_cookie(self, URL):
        res = self._get(URL)
        return res
    def get_menu(self, shop_id):
        form_data = copy.deepcopy(MenuSiteConfig.FORM_DATA)
        form_data["data"]["shop_id"] = shop_id
        params = form_data["params"]
        data = form_data["data"]
        main_page_res = self.set_cookie(MenuSiteConfig.MAIN_PAGE)
        if main_page_res:
            menu_page_res = self._post(
                url=MenuSiteConfig.MENU_PAGE,
                data=data,
                params=params
            )
            return menu_page_res
        
        else: return None





