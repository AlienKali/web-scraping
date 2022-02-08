from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup

class Noticia(Item):
    tirutla=Field()
    descripcion = Field()

class ElUniversospider(Spider):
    name = "MiSegundoSpider"
    custom_dettings ={
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
    Chrome/80.0.3987.149 Safari/537.36"
    }

    start_urls = ["https://www.eluniverso.com/deportes/"]


def parse(self,response):
    soup = BeautifulSoup(response.body)
    contenedor_noticias=soup.find_all('ul',class_='feed | divide-y relative   ')

    for contenedor in contenedor_noticias:
        noticias = contenedor.find_all('li',class_='relative')
        for noticia in noticias:
            item = ItemLoader(Noticia(),response.body)
            titular = noticia.find('h2').text
            descripcion = noticia.find('p')
            if (descripcion != None):
                descripcion =descripcion.text
            else:
                descripcion='N/A'

            item.add_value('titular', titular)
            item.add_value('descripcion',descripcion)

            yield item.load_item()

''' #Scarpy
    def parse(self,response):
        sel = Selector(response)
        noticias = sel.xpath('//ul[@class="feed | divide-y relative   "]/li[@class="relative"]')
        for noticia in noticias:
            item = ItemLoader(Noticia(),noticia)
            item.add_xpath('titular','.//h2/a/text()')
            item.add_xpath('descripcion','.//p/text()')

            yield item.load_item()
'''

