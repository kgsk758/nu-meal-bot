from .scraper_base import ScraperBase
from config.constants import MenuSiteConfig, Shops
import copy
import time

class MenuScraper(ScraperBase):
    def set_cookie(self, url):
        return self._get(url)

    def get_menu(self, shop_idx: int):
        shop_id = Shops.IDS[shop_idx]
        
        # config/constants.py から取得したデータを使用
        form_data = copy.deepcopy(MenuSiteConfig.FORM_DATA)
        form_data["data"]["shop_id"] = str(shop_id)
        
        data = form_data["data"]
        params = form_data["params"]

        print(f"\n--- Debug Start: shop_id {shop_id} ---")

        # 1. 空打ちPOST (PHPSESSID取得用)
        initial_headers = {
            "Origin": "null",
            "Content-Type": "application/x-www-form-urlencoded",
            "Upgrade-Insecure-Requests": "1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        }
        
        res1 = self.session.post(
            MenuSiteConfig.MENU_PAGE, 
            data=data, 
            params=params,
            headers=initial_headers,
            allow_redirects=False,
            timeout=5
        )
        
        print(f"[Step 1] POST to MENU_PAGE")
        print(f" - Status: {res1.status_code}")
        print(f" - Cookies in response: {res1.cookies.get_dict()}")
        print(f" - Location: {res1.headers.get('Location')}")

        # 2. 本番POST
        res2 = self.session.post(
            MenuSiteConfig.MENU_PAGE, 
            data=data, 
            params=params,
            headers=initial_headers,
            timeout=5
        )
        
        print(f"[Step 2] POST to MENU_PAGE (following redirects)")
        print(f" - Final URL: {res2.url}")
        print(f" - Cookies in session: {self.session.cookies.get_dict()}")
        print(f" - Request Headers Sent: {res2.request.headers}")
        print(f"--- Debug End ---\n")

        return res2
