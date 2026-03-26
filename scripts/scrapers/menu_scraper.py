from .scraper_base import ScraperBase
from config.constants import MenuSiteConfig, Shops
import copy
import time

class MenuScraper(ScraperBase):
    def set_cookie(self, url):
        return self._get(url)

    def get_menu(self, shop_idx: int):
        shop_id = Shops.IDS[shop_idx]
        
        # URLの定義
        url = "https://signage.univcoop-tokai.net/smt_menu_ants2/view_list.php?uv=15&current_day=0&current_page=no_page"
        index_url = "https://signage.univcoop-tokai.net/smt_menu_ants2/index.php?uv=15"
        
        # requestsにエンコードとContent-Type付与を任せるため、辞書型で定義
        data = {
            "shop_id": shop_id,
            "client_id": 15
        }
        
        # 1. セッションの完全な初期化
        self.session.cookies.clear()
        self.session.headers.clear()
        
        # GETリクエストでも不自然にならない、標準的なヘッダーのみをセッションに固定
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "ja",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        })

        # 2. メインページ(index.php)へのGETアクセス
        # これにより、302リダイレクトを発生させずに安全にPHPSESSIDを取得します
        self.session.get(index_url, timeout=5)
        
        # サーバー側のセッション書き込み時間を考慮して待機
        time.sleep(1.0)

        # 3. 本命のアクセス（POST）
        # POST特有のヘッダー（Origin, Referer）をここでだけ付与して正規の画面遷移に見せます
        post_headers = {
            "Origin": "https://signage.univcoop-tokai.net",
            "Referer": index_url
        }
        res = self.session.post(url, data=data, headers=post_headers, timeout=5)

        return res