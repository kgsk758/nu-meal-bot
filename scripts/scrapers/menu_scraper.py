from .scraper_base import ScraperBase
from config.constants import MenuSiteConfig, Shops
import copy
import time

class MenuScraper(ScraperBase):
    def set_cookie(self, url):
        return self._get(url)

    def get_menu(self, shop_idx: int):
        shop_id = Shops.IDS[shop_idx]
        
        # ユーザー様のHTMLに合わせたデータ構成
        data = {
            "shop_id": str(shop_id),
            "client_id": "15"
        }
        params = MenuSiteConfig.FORM_DATA["params"]

        # ユーザー様提供のヘッダを忠実に再現
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "ja",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "null",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "sec-ch-ua": '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
        }

        # --- ステップ1 & 2: 初回POSTとリダイレクト先GETの完遂 ---
        # requestsはデフォルトで302リダイレクトをGETで追いかけます。
        # これにより「POST -> 302 -> GET index.php」というブラウザの初回挙動を再現し、
        # セッションを確立させます。
        self.session.post(
            MenuSiteConfig.MENU_PAGE, 
            data=data, 
            params=params,
            headers=headers,
            timeout=5
        )

        # ブラウザの操作間隔を模倣
        time.sleep(0.5)

        # --- ステップ3: 本命の2回目POST ---
        # すでにセッション(PHPSESSID)が確立・有効化されているため、
        # このリクエストで 200 OK とメニュー内容が返ってくるはずです。
        res = self.session.post(
            MenuSiteConfig.MENU_PAGE, 
            data=data, 
            params=params,
            headers=headers,
            timeout=5
        )

        return res
