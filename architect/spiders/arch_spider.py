import scrapy
import architect.items as itt
import re

class ArchSpider(scrapy.Spider):
    name = "arch"
    start_urls = ['https://find-an-architect.architecture.com/FAAPractices.aspx?page=1' ]

    def parse(self, response):
        page = response.url.split("page=")[-1]
        print ("page = ", page)
        for sel in response.css('article'):
            architect = itt.ArchitectItem()
            try:
                architect['name_arch'] = sel.css('a::text').extract_first().strip()
            except:
                architect['name_arch'] = ''

            addr1 = re.sub('\n+'," ", sel.css("div.pageMeta-item.icon.address::text").extract_first())
            addr = re.split(',', addr1)
            postcode = addr[len(addr)-1].strip()
            county = addr[len(addr)-2]
            if  county.strip() in 'LONDON|London|Bristol|BRISTOL|Manchester|MANCHESTER|Edinburgh|EDINBURGH|Bath|BATH|Glasgow|GLASGOW':
                county = ''
                town = addr[len(addr)-2].strip()
                address1 = addr[len(addr)-3].strip()
            else:
                town = addr[len(addr)-3].strip()
                i=0
                address1 = ''
                while (i<len(addr)-3):
                    address1 = address1+addr[i]
                    i=i+1
            
            architect['address'] = address1
            architect['town'] = town
            architect['county'] = county
            architect['postcode'] = postcode
            
            try:
                phone = sel.css("div.pageMeta-item.icon::text").extract()[1].strip()
            except:
                phone = ''
            if 'Tel:' in phone:
                phone = phone[5:]
            architect['phone'] = phone
            
            try:
                email = sel.css("a.tagList.faaemail::text").extract().strip()
            except:
                email = ''
            architect['email'] = email
            
            architect['webb'] = sel.css("a.tagList.exLink::text").extract_first()
            
            footer = sel.css("div.listingItem-extra")
            if not footer:
                about = " "
                housing_exp = ' '
                comm_exp = ' '
            else:
                try:
                    about_ar = footer.css("div.pageMeta-item.icon p::text").extract_first().strip()
                except:
                    about_ar = ''
                about_ar = (re.sub('\n+'," ", about_ar))
                about_ar = (re.sub('\r+',"", about_ar))
                
            architect['about'] = about_ar
            yield architect
        
        next_page = 'https://find-an-architect.architecture.com/FAAPractices.aspx?page='+str(int(page)+1)
        if int(page)+1 < 10:
            yield scrapy.Request(next_page, callback=self.parse)
 