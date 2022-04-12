import scrapy


class HowraredropsSpider(scrapy.Spider):
    name = 'howrareDrops'
    allowed_domains = ['howrare.is']
    start_urls = ['http://howrare.is/']

    def parse(self, response):
        pass
