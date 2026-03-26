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
        form_data["data"]["shop_id"] = str(shop_id)
        
        data = form_data["data"]
        params = form_data["params"]

        # ブラウザにより近いヘッダを設定
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "ja,en;q=0.9",
            "Origin": "null",
            "Content-Type": "application/x-www-form-urlencoded",
            "Upgrade-Insecure-Requests": "1",
        }

        print(f"\n--- Debug Start: shop_id {shop_id} ---")

        # 1. まずはメインページをGETしてクッキーを初期化 (通常の訪問パターン)
        self.session.get(MenuSiteConfig.MAIN_PAGE, headers=headers)
        print(f"[Step 1] GET to MAIN_PAGE: Cookies={self.session.cookies.get_dict()}")

        # 2. 本番POST
        res = self.session.post(
            MenuSiteConfig.MENU_PAGE, 
            data=data, 
            params=params,
            headers=headers,
            timeout=5
        )
        
        print(f"[Step 2] POST to MENU_PAGE: Final URL={res.url}")

        # 3. もしリダイレクトされていたら「一度リダイレクト先を踏んでから再試行」
        if "index.php" in res.url:
            print(f" - Still redirected. Trying 'visit redirect destination' strategy.")
            time.sleep(0.5)
            # リダイレクト先を一度GETして訪問履歴を作る
            self.session.get(res.url, headers=headers)
            # 再度POST
            res = self.session.post(
                MenuSiteConfig.MENU_PAGE, 
                data=data, 
                params=params,
                headers=headers,
                timeout=5
            )
            print(f"[Step 3] Retry POST: Final URL={res.url}")

        print(f"--- Debug End ---\n")

        return res
