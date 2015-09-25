#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
import urllib
from wsloan.items import WsloanItem
import urllib2
import os
import re



class WSLOANspider(CrawlSpider):
    name = 'wsloan'
    allowd_domain = ['www.wsloan.com']
    download_delay = 3  #访问间隔秒数
    start_urls = ['http://www.wsloan.com/invest.aspx?page='+str(x) for x in range(1,10)]
    #['http://www.p2peye.com/hangqing/frtsgp'+str(x)+'.html' for x in range(2,100)]+['http://www.p2peye.com/hangqing/']

    rules = (
        Rule(SgmlLinkExtractor(allow=('/jkxq.aspx\?id='r'\d{4}', )),
             callback='parse_page', follow=True),
    )
    def parse_page(self, response):
        item = WsloanItem()
        sel = Selector(response)
        item['name'] = sel.xpath('//span[@class=\"red\"]/text()').extract()[0]
        link = response.url
        item['link']  = link
        amount = sel.xpath('//span[@class=\"m fs\"]/text()').extract()[0]
        item['amount'] = amount[1:]
        item['income_rate'] = sel.xpath('//span[@class=\"l2 fs\"]/text()').extract()[0]
        item['term'] = sel.xpath('//span[@class=\"l2 fs\"]/text()').extract()[1]
        item['repay_type'] = sel.xpath('//div[@class=\"row-l\"]/text()').extract()[2][12:]
        item['area'] = ''
        item['reward'] = sel.xpath('//span[@class=\"l2 fs\"]/text()').extract()[2]
        item['protect_mode'] = ''
        item['description'] = sel.xpath('//span[@class=\"red\"]/text()').extract()[0]
        item['process'] =  sel.xpath('//div[@class=\"row-l\"]/span/text()').extract()[4]
        item['transfer_claim'] = ''
        item['min_amount'] = sel.xpath('//div[@class=\"row-l\"]/span/text()').extract()[6][1:]
        yield item


