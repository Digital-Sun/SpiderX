# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class BaiduNewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    key_word = scrapy.Field()
    create_time = scrapy.Field()
    title = scrapy.Field()
    source = scrapy.Field()
    time = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
