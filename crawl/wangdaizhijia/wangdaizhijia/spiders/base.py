#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
import urllib
from wangdaizhijia.items import WangdaizhijiaItem
import urllib2
import os
import re
import json
import datetime



class WangdaizhijiaImage(CrawlSpider):
    name='wangdaizhijia'
    allowed_domain=["wangdaizhijia.com"]
    download_delay = 2  #访问间隔秒数

    #lastDate = datetime.date.today() - datetime.timedelta(days=1)
    start_urls = ['http://www.p2peye.com/platdata.html']

    def parse(self,response):
        sel = Selector(response)
        items = []
        #day_id = sel.xpath('//div[@id=\"widgetField\"]/span/text()').extract()
        platform_name = sel.xpath('//td[@class=\"name\"]/a/text()').extract()
        #platform_name = sel.xpath('//tbody/tr/td/a/span/text()').extract()
        amount = sel.xpath('//td[@class=\"total\"]/text()').extract()
        #amount = sel.xpath('//td[@class=\"ts col_AA1C20 td0\"]/text()').extract()
        inv_quantity = sel.xpath('//td[@class=\"pnum\"]/text()').extract()
        for i in range(0, len(platform_name)):
            item = WangdaizhijiaItem()
            item['day_id'] = datetime.date.today() - datetime.timedelta(days=1)
            item['platform_name'] = platform_name[i]
            item['amount'] = amount[i]
            item['inv_quantity'] = inv_quantity[i]
            items.append(item)
        return items
