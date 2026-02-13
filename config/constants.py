#schedule site
SCHEDULE_URL = "https://www.nucoop.jp/shop/"


class MenuSiteConfig:
    #URLs
    MAIN_PAGE = "https://signage.univcoop-tokai.net/smt_menu_ants2/index.php?uv=15"
    MENU_PAGE = "https://signage.univcoop-tokai.net/smt_menu_ants2/view_list.php"
    #Shop id
    HOKUBU_ID = 127
    FOREST_ID = 68
    MEIDINING_ID = 100
    SAI_ID = 103
    IGAKUBU_ID = 105
    #shop site post data
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