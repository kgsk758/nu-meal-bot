from bs4 import BeautifulSoup
from .parser_base import ParserBase

from config.constants import ScheduleSiteConfig

class ScheduleParser(ParserBase):
    def get_shop_state_today(self, shop_idx, date:str):
        shop_name = ScheduleSiteConfig.SHOP_NAMES[shop_idx]

        shop_tables = self.get_shop_tables()

        #get table
        table = None
        for shop_table in shop_tables:
            if shop_table[1] == shop_name:
                table = shop_table[0]
        if table is None:
            raise RuntimeError("could not find schedule table")
        
        symbol_means = self.get_symbol_means(table)
        date_symbols = self.get_date_symbols(table)
        
        if not date in date_symbols:
            raise RuntimeError("date not on the schedule")
        return symbol_means[date_symbols[date]]
        
    def get_symbol_means(self, table:BeautifulSoup):
        state_dict = {}
        state_rows = table.find_all('dl')
        for state_row in state_rows:
            state_dict[state_row.dt.string] = state_row.dd.string
        if state_dict == {}:
            raise RuntimeError("could not get symbol means")

        return state_dict

    def get_date_symbols(self, table:BeautifulSoup):
        date_symbols = {}
        tds = table.find_all('td')
        for td in tds:
            span_element = td.find('span')
            if not span_element:
                continue
            text = td.get_text(strip=True)
            span_text = span_element.get_text(strip=True)
            only_symbol = text.replace(span_text, '')
            
            date_symbols[span_element.string] = only_symbol
        
        if date_symbols == {}:
            raise RuntimeError("failed to get date symbols")
        
        return date_symbols

    def get_shop_tables(self):
        shops = self.soup.find_all('h3', class_="h3_title01 mb10")
        shop_tables = []
        for shop in shops:
            if shop.string in ScheduleSiteConfig.SHOP_NAMES:
                shop_tables.append((shop.parent, shop.string))
        if shop_tables == []:
            raise RuntimeError("could not get shop tables")
        
        return shop_tables


