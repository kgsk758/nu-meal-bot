from bs4 import BeautifulSoup
from .parser_base import ParserBase

class MenuParser(ParserBase):
    def __init__(self, response):
        super().__init__(response)
        self.img_elems = self.soup.select("img")
    
    def get_img_links(self):
        image_links = []
        for img_elem in self.img_elems:
            src = img_elem.get("src")

            if not src:
                continue

            if not src.startswith(('http://', 'https://')):
                print(f"Skipping relative or invalid image src: {src}")
                continue

            if src.endswith('s.png'):
                src = src[0:-5] + 'l.png'  # 's'を'l'に置き換える:高解像度画像を取得
                image_links.append(src)
            else:
                print(f"image link not end with 's.png': {src}")
                continue
        
        return image_links