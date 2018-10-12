import csv
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ArchitectPipeline(object):
    def open_spider(self, ArchSpider):
        self.csvfile = open("./files/architect2.csv", 'wt', encoding="UTF-8")
        self.writer = csv.writer(self.csvfile)
        
    def close_spider(self, ArchSpider):
        self.csvfile.close()
        
    def process_item(self, architect, ArchSpider):
        self.writer.writerow((architect['name_arch'], architect['address'], architect['town'], architect['county'], architect['postcode'], architect['phone'], architect['email'], architect['webb'], architect['about']))
        architect['name_arch']=architect['address']=architect['town']=architect['county']=architect['postcode']=architect['phone']=architect['email']=architect['webb']=architect['about']=''
        return architect
