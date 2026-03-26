from .scraper_base import ScraperBase
from config.constants import MenuSiteConfig, Shops
import copy
import time

class MenuScraper(ScraperBase):
    def set_cookie(self, url):
        """互換性のために残していますが、現在はget_menu内のPOSTでクッキーを取得します"""
        return self._get(url)

    def get_menu(self, shop_idx: int):
        shop_id = Shops.IDS[shop_idx]
        form_data = copy.deepcopy(MenuSiteConfig.FORM_DATA)
        form_data["data"]["shop_id"] = shop_id
        
        # ユーザー様の調査結果に基づき、2段階のPOSTでアクセスします。
        
        # 1. クッキー取得のための「空打ち」POST
        # allow_redirects=False にすることで、302リダイレクトを追わずに
        # レスポンスヘッダの Set-Cookie をセッションに格納させます。
        self.session.post(
            MenuSiteConfig.MENU_PAGE, 
            data=form_data["data"], 
            params=form_data["params"],
            allow_redirects=False,
            timeout=5
        )

        # 2. 本番のPOST
        # すでにPHPSESSIDを保持しているため、200 OK でメニュー内容が返ってきます。
        res = self.session.post(
            MenuSiteConfig.MENU_PAGE, 
            data=form_data["data"], 
            params=form_data["params"],
            timeout=5
        )
        
        # 万が一まだ index.php にリダイレクトされている場合は、少し待って再試行します。
        if "index.php" in res.url:
            time.sleep(0.5)
            res = self.session.post(
                MenuSiteConfig.MENU_PAGE, 
                data=form_data["data"], 
                params=form_data["params"],
                timeout=5
            )

        return res
