from .scraper_base import ScraperBase
from config.constants import MenuSiteConfig, Shops
import copy
import time

class MenuScraper(ScraperBase):
    def set_cookie(self, url):
        return self._get(url)

    def get_menu(self, shop_idx: int):
        shop_id = Shops.IDS[shop_idx]
        
        # クエリパラメータを含むフルURL
        full_url = "https://signage.univcoop-tokai.net/smt_menu_ants2/view_list.php?uv=15&current_day=0&current_page=no_page"
        # ユーザー様のHTMLに合わせたPOSTデータ
        post_data = f"shop_id={shop_id}&client_id=15"
        
        # ユーザー様のブラウザ情報を完全に再現
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "ja",
            "Accept-Encoding": "gzip, deflate, br, zstd",
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

        # セッションヘッダーを一旦クリアして固定
        self.session.headers.clear()

        # 1. 最初のPOST（302リダイレクトを誘発させてクッキーを確保）
        res1 = self.session.post(full_url, data=post_data, headers=headers, allow_redirects=False, timeout=5)

        # 2. リダイレクト先 (index.php) をGETで訪問
        # これによりサーバー側でセッションが「有効な人間」としてマークされることを狙います
        location = res1.headers.get("Location")
        if location:
            if location.startswith("/"):
                location = "https://signage.univcoop-tokai.net" + location
            
            get_headers = headers.copy()
            get_headers.pop("Content-Type", None)
            get_headers.pop("Origin", None)
            
            self.session.get(location, headers=get_headers, timeout=5)
            # ブラウザの人間的な操作間隔を長めに模倣
            time.sleep(2.0)

        # 3. 本命の2回目POST
        # Refererをindex.phpに設定して「ページ内からの遷移」を装う
        final_headers = headers.copy()
        final_headers["Referer"] = "https://signage.univcoop-tokai.net/smt_menu_ants2/index.php?uv=15"
        
        res = self.session.post(full_url, data=post_data, headers=final_headers, timeout=5)

        return res
