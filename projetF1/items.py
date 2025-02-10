# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class MonprojetItem(scrapy.Item):
    position = scrapy.Field()
    driver = scrapy.Field()
    team = scrapy.Field()
    time = scrapy.Field()
    #nom des variables que l'on veut scrapper sur le site
    pass
