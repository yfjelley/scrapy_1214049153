# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class WsloanItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    platform_name = Field()
    link = Field()
    name = Field()
    amount = Field()
    income_rate = Field()
    term = Field()
    type = Field()
    area = Field()
    repay_type = Field()
    reward = Field()
    protect_mode = Field()
    description = Field()
    process = Field()
    transfer_claim= Field()
    min_amount = Field()




