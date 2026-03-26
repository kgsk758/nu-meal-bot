from .scraper_base import ScraperBase
from config.constants import MenuSiteConfig, Shops
import copy
import time

class MenuScraper(ScraperBase):
    def set_cookie(self, url):
        return self._get(url)

    def log_request(self, label, response):
        """リクエストとレスポンスの全容を詳細に記録する"""
        req = response.request
        print(f"\n{'='*20} {label} {'='*20}")
        print(f"[Request]")
        print(f"  URL:    {req.url}")
        print(f"  Method: {req.method}")
        print(f"  Headers:")
        for k, v in req.headers.items():
            print(f"    {k}: {v}")
        if req.body:
            print(f"  Body:   {req.body}")
        
        print(f"\n[Response]")
        print(f"  Status: {response.status_code}")
        print(f"  URL:    {response.url}")
        print(f"  Cookies in Response: {response.cookies.get_dict()}")
        if "Location" in response.headers:
            print(f"  Location: {response.headers['Location']}")
        print(f"{'='*50}\n")

    def get_menu(self, shop_idx: int):
        shop_id = Shops.IDS[shop_idx]
        
        # パラメータとデータの構築
        params = MenuSiteConfig.FORM_DATA["params"]
        data = {"shop_id": str(shop_id), "client_id": "15"}
        
        # ユーザー様提供のヘッダー
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

        # 1. 最初のPOST (302リダイレクトを期待して手動制御)
        res1 = self.session.post(
            MenuSiteConfig.MENU_PAGE, 
            data=data, 
            params=params, 
            headers=headers,
            allow_redirects=False,
            timeout=5
        )
        self.log_request("STEP 1: INITIAL POST", res1)

        # 2. リダイレクト先 (index.php) をGETで訪問
        if res1.status_code == 302:
            location = res1.headers.get("Location")
            if location:
                if location.startswith("/"):
                    location = "https://signage.univcoop-tokai.net" + location
                
                # GET用のヘッダー調整
                get_headers = headers.copy()
                get_headers.pop("Content-Type", None)
                get_headers.pop("Origin", None)
                
                res2 = self.session.get(location, headers=get_headers, timeout=5)
                self.log_request("STEP 2: REDIRECT GET", res2)
                time.sleep(0.5)

        # 3. 本命の2回目POST
        res3 = self.session.post(
            MenuSiteConfig.MENU_PAGE, 
            data=data, 
            params=params, 
            headers=headers,
            timeout=5
        )
        self.log_request("STEP 3: FINAL POST", res3)

        return res3
