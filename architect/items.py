# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArchitectItem(scrapy.Item):
    name_arch = scrapy.Field()
    address = scrapy.Field()
    town = scrapy.Field()
    county = scrapy.Field()
    postcode = scrapy.Field()
    phone = scrapy.Field()
    email = scrapy.Field()
    webb = scrapy.Field()
    about = scrapy.Field()    
