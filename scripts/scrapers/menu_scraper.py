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
        url = "https://signage.univcoop-tokai.net/smt_menu_ants2/view_list.php?uv=15&current_day=0&current_page=no_page"
        # ユーザー様のHTMLに合わせたPOSTデータ形式
        data = f"shop_id={shop_id}&client_id=15"
        
        # 1. セッションの完全な初期化
        self.session.cookies.clear()
        self.session.headers.clear()
        
        # ブラウザの全ヘッダーをセッションに固定
        # requestsのデフォルトヘッダーによるボット判定を避けます
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "ja",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Connection": "keep-alive",
            "Origin": "null",
            "Content-Type": "application/x-www-form-urlencoded",
            "Upgrade-Insecure-Requests": "1",
            "sec-ch-ua": '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-User": "?1",
        })

        # 人間らしく見せるためのダミークッキー (Google Analytics)
        # ユーザー様の成功ログに含まれていたものを模倣します
        self.session.cookies.set("_ga", "GA1.1.1763706508.1774526162", domain="signage.univcoop-tokai.net")
        self.session.cookies.set("_gid", "GA1.2.1748237429.1774526162", domain="signage.univcoop-tokai.net")

        # 2. 最初のアクセス（空打ち）
        # 自動リダイレクトを有効にし、POST -> 302 -> GET index.php までを一気に終わらせます。
        # これにより、セッションが確立され、かつ「メインページを訪問済み」の状態になります。
        self.session.post(url, data=data, timeout=5)
        
        # サーバー側のセッション書き込み時間を考慮して待機
        time.sleep(1.0)

        # 3. 本命のアクセス（再びアクセス）
        # すでにクッキーを保持した状態での再アクセスなので、今度は 200 OK が期待できます。
        res = self.session.post(url, data=data, timeout=5)

        return res
