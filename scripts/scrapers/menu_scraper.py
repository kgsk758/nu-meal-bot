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
        
        # ユーザー様のブラウザ情報を正確に反映（Refererなし）
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

        # 1. 最初のPOST（allow_redirects=False）でPHPSESSIDを取得
        # ユーザー様の実験結果（初回は302リダイレクトされる）をシミュレート
        self.session.post(
            MenuSiteConfig.MENU_PAGE, 
            data=form_data["data"], 
            params=form_data["params"],
            headers=headers,
            allow_redirects=False,
            timeout=5
        )

        # 2. 本番のPOST
        # 取得したPHPSESSIDを用いて、200 OKのレスポンスを期待します
        res = self.session.post(
            MenuSiteConfig.MENU_PAGE, 
            data=form_data["data"], 
            params=form_data["params"],
            headers=headers,
            timeout=5
        )
        
        # 念のためのリトライ処理
        if "index.php" in res.url:
            time.sleep(0.5)
            res = self.session.post(
                MenuSiteConfig.MENU_PAGE, 
                data=form_data["data"], 
                params=form_data["params"],
                headers=headers,
                timeout=5
            )

        return res
