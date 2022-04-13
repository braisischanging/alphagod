import scrapy


class HowraredropsSpider(scrapy.Spider):
    name = 'howrareDrops'
    allowed_domains = ['howrare.is']
    start_urls = ['http://howrare.is/drops'] 

    def parse(self, response):


        drops_date = response.xpath("//div[@class='wrap content page']/div[@class='all_collections_wrap drops']/div[@class='all_collections']")

        for drop_date in drops_date:

            project_drop_date = drop_date.xpath("normalize-space(./div[@class='all_coll_row drop_date']/text())").get()

            next_drops = drop_date.xpath("./div[@class='all_coll_row']")

            for drop in next_drops:

                project_name = drop.xpath("normalize-space(./div[@class='all_coll_col'][1]/a/span/text())").get()
                project_description = drop.xpath("normalize-space(./div[@class='all_coll_col'][6]/text())").get()
                img_url = drop.xpath("./div[@class='all_coll_col'][1]/a/img/@src").get()
                web_link = drop.xpath("./div[@class='all_coll_col drop_links'][1]/a[not(contains(@href,'twitter')) and not(contains(@href,'discord'))]/@href").get()
                twitter_link = drop.xpath("./div[@class='all_coll_col drop_links'][1]/a[contains(@href,'twitter')]/@href").get()
                discord_link = drop.xpath("./div[@class='all_coll_col drop_links'][1]/a[contains(@href,'discord')]/@href").get()
                mint_time = drop.xpath("normalize-space(./div[@class='all_coll_col'][2]/text())").get()
                project_price = drop.xpath("normalize-space(./div[@class='all_coll_col'][5]/text())").get()
                project_pieces = drop.xpath("normalize-space(./div[@class='all_coll_col'][4]/text())").get()
                

                yield{
                    'name':project_name,
                    'description':project_description,
                    'image':img_url,
                    'webLink':web_link,
                    'twitterLink':twitter_link,
                    'discordLink':discord_link,
                    'mintDate':project_drop_date,
                    'mintTime':mint_time,
                    'mintPrice':project_price,
                    'mintPieces':project_pieces
                }
