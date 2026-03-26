from .scraper_base import ScraperBase
from config.constants import MenuSiteConfig, Shops
import time

class MenuScraper(ScraperBase):
    def set_cookie(self, url):
        return self._get(url)

    def get_menu(self, shop_idx: int):
        shop_id = Shops.IDS[shop_idx]
        
        # ユーザー様のHTMLに合わせたフルURLとPOSTデータ
        url = "https://signage.univcoop-tokai.net/smt_menu_ants2/view_list.php?uv=15&current_day=0&current_page=no_page"
        data = {"shop_id": str(shop_id), "client_id": "15"}
        
        # 1. セッションのクッキーを一旦クリア（常に初回訪問からシミュレートするため）
        self.session.cookies.clear()
        
        # 2. 最初のアクセス（空打ち）
        # requestsのデフォルト挙動(allow_redirects=True)を利用して、
        # POST -> 302 -> GET index.php の一連の流れを完遂させ、セッションを確立させます。
        self.session.post(url, data=data, timeout=5)
        
        # ブラウザの操作間隔を模倣し、サーバー側の処理を待ちます
        time.sleep(1.5)
        
        # 3. 本命のアクセス
        # すでにクッキーを保持し、メインページ訪問済みの状態での再POSTです。
        # ブラウザで「もう一度送信した」状態を再現します。
        res = self.session.post(url, data=data, timeout=5)
        
        # もしこれでも index.php に飛ばされている場合は、念のためもう一回だけ試行
        if "index.php" in res.url:
            time.sleep(1.0)
            res = self.session.post(url, data=data, timeout=5)
            
        return res
