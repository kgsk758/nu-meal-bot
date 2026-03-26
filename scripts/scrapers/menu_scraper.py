from .scraper_base import ScraperBase
from config.constants import MenuSiteConfig, Shops
import copy
import time

class MenuScraper(ScraperBase):
    def set_cookie(self, url):
        return self._get(url)

    def log_request(self, label, response):
        req = response.request
        print(f"\n{'='*20} {label} {'='*20}")
        print(f"[Request] {req.method} {req.url}")
        print(f"  Cookie: {req.headers.get('Cookie')}")
        print(f"  Body:   {req.body}")
        print(f"[Response] Status: {response.status_code}")
        print(f"  Location: {response.headers.get('Location')}")
        print(f"  Final URL: {response.url}")
        print(f"{'='*50}\n")

    def get_menu(self, shop_idx: int):
        shop_id = Shops.IDS[shop_idx]
        
        # パラメータを含むフルURL (URLエンコード済みの形式で固定)
        full_url = "https://signage.univcoop-tokai.net/smt_menu_ants2/view_list.php?uv=15&current_day=0&current_page=no_page"
        # ユーザー様のHTMLに合わせたデータ
        post_data = f"shop_id={shop_id}&client_id=15"
        
        # ヘッダーをブラウザと完全に一致させる
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

        # 1. 最初のPOST (302リダイレクトを誘発)
        # allow_redirects=False を指定して、勝手にGETへ遷移させない
        res1 = self.session.post(full_url, data=post_data, headers=headers, allow_redirects=False, timeout=5)
        self.log_request("STEP 1: INITIAL POST", res1)

        # 2. リダイレクト先 (index.php) をGETで訪問
        location = res1.headers.get("Location")
        if location:
            if location.startswith("/"):
                location = "https://signage.univcoop-tokai.net" + location
            
            # GETリクエストを実行
            res2 = self.session.get(location, headers=headers, timeout=5)
            self.log_request("STEP 2: REDIRECT GET (index.php)", res2)
            time.sleep(0.5)

        # 3. 本命の2回目POST
        # ここもあえて allow_redirects=False にして挙動を直接確認
        res3 = self.session.post(full_url, data=post_data, headers=headers, allow_redirects=False, timeout=5)
        self.log_request("STEP 3: FINAL POST", res3)

        # もしSTEP 3が200なら成功。もし302ならまだ何かが足りない。
        if res3.status_code == 200:
            return res3
        
        # 302の場合は、一応リダイレクトを追いかけた結果を返して、Parserに任せる
        return self.session.post(full_url, data=post_data, headers=headers, timeout=5)
