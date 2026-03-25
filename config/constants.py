class ShopIndex:
    IGAKUBU = 0
    HOKUBU = 1
    FOREST = 2
    DINING = 3
    SAI = 4
class Shops:
    NAMES = (
        "医学部食堂(FOOD SQUARE)",
        "北部食堂",
        "ダイニングフォレスト",
        "南部食堂1階 Mei-dining",
        "南部食堂2階 彩〜Sai〜"
    )
    IDS = (
        105,
        127,
        68,
        100,
        103
    )

class ScheduleSiteConfig:
    MAIN_PAGE = "https://www.nucoop.jp/shop/"

class MenuSiteConfig:
    #URLs
    MAIN_PAGE = "https://signage.univcoop-tokai.net/smt_menu_ants2/index.php?uv=15"
    MENU_PAGE = "https://signage.univcoop-tokai.net/smt_menu_ants2/view_list.php"
    
    #menu site post data
    FORM_DATA = {
        "params" : {
            "uv": "15",
            "current_day": "0",
            "current_page": "no_page"
        },
        "data" : {
            "shop_id": None, #Shop id
            "client_id": "15",
        },
    }

#http request config
class ScraperConfig:
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
    TIMEOUT = 5

class TweetTemplate:
    def OPEN_TWEET(full_date: str, shop_name: str, shop_state: str) -> str:
        return f"今日({full_date})の{shop_name}のメニューです。\n営業時間:{shop_state}"
    def CLOSED_TWEET(full_date: str, closed_shops: str) -> str:
            return f"今日({full_date})の{closed_shops}は休業です。"
