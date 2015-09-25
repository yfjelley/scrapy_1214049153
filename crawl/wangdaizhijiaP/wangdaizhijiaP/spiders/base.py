#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
import urllib
from wangdaizhijiaP.items import WangdaizhijiaPItem
import urllib2
import os
import re
import json
import datetime



class WangdaizhijiaImage(CrawlSpider):
    name='wangdaizhijiaP'
    allowed_domain=["wangdaizhijia.com"]
    download_delay = 2  #访问间隔秒数

    lastDate = datetime.date.today() - datetime.timedelta(days=1)
    start_urls = ['http://shuju.wangdaizhijia.com/platdata-2.html?startTime='\
                  + str(lastDate) + '&endTime=' + str(lastDate)]

    def parse(self,response):
        sel = Selector(response)
        items = []
        #day_id = sel.xpath('//div[@id=\"widgetField\"]/span/text()').extract()
        #platform_name = sel.xpath('//td[@class=\"tl pl10\"]/a[@class=\"pl10\"]/text()').extract()
        platform_name = sel.xpath('//tbody/tr/td/a/span/text()').extract()
        inv_quantity = sel.xpath('//tbody/tr/td/text()').extract()
        #amount = sel.xpath('//td[@class=\"ts col_AA1C20 td0\"]/text()').extract()
        #inv_quantity = sel.xpath('//td[@class=\"ts td1\"]/text()').extract()
        for i in range(0, len(platform_name)):
            item = WangdaizhijiaPItem()
            item['day_id'] = datetime.date.today() - datetime.timedelta(days=1)
            item['platform_name'] = platform_name[i]
            item['inv_quantity'] = inv_quantity[i+(i*4)-1*i]
            print item['inv_quantity']
            #item['inv_quantity'] = inv_quantity[i]
            items.append(item)
        return items