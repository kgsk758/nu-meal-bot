from bs4 import BeautifulSoup

class ParserBase:
    def __init__(self, response):
        self.soup = BeautifulSoup(response.text, "html.parser")