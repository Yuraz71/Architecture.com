import scrapy
import architect.items as items
from scrapy.spiders import CrawlSpider
import re

class ArchSpider(CrawlSpider):
    name = 'arch'

    allowed_domains = ['find-an-architect.architecture.com']
    start_urls = ['https://find-an-architect.architecture.com/FAAPractices.aspx?page=1', ]

    def parse(self, response):
        # Organize cycle for items
        # Each item in block starting with 'article'
        for sel in response.css('article'):
            architect = items.ArchitectItem()
            architect['name_arch'] = sel.css('a::text').extract_first().strip()

            try:
                address = re.sub('\n+'," ", sel.css("div.pageMeta-item.icon.address::text").extract_first()).strip()
            except:
                address = ''
            architect['address'] = address

            architect['phone'] = re.sub('\n+'," ", sel.css("div.pageMeta-item.icon::text").extract()[1]).strip()
            architect['webb'] = sel.css("a.tagList.exLink::text").extract_first()

            try:
                about = sel.css("div.pageMeta-item.icon p::text").extract_first().strip()
            except:
                about = ''
            about = (re.sub('\n+', " ", about))
            about = (re.sub('\r+', "", about))
            architect['about'] = about

            yield architect

        # goto next page
        try:
            next_page = response.xpath("//span[@class='sys_navigationnext']/a/@href").extract()[0]
            next_page = 'https://find-an-architect.architecture.com' + next_page
            print("page = ", next_page)
        except:
            print("Done")
            return

        yield scrapy.Request(next_page, callback=self.parse)
