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
        item['name'] = sel.xpath('//*[@id="main"]/div[2]/div/div[1]/h3/text()').extract()[0]
        link = response.url
        item['link']  = link

        item['amount'] = sel.xpath('//*[@id="main"]/div[2]/div/div[1]/ul/li[1]/i/text()').extract()[0]
        item['income_rate'] = sel.xpath('//*[@id="main"]/div[2]/div/div[1]/ul/li[3]/label/i/text()').extract()[0]
        item['term'] = sel.xpath('//*[@id="main"]/div[2]/div/div[1]/ul/li[2]/label/i/text()').extract()[0]
        item['repay_type'] = sel.xpath('//tr[2]/td[1]/span/text()').extract()[0]
        item['area'] = ''
        try:
            item['reward'] = sel.xpath('//span[@class=\"l2 fs\"]/text()').extract()[2]
        except:
            item['reward'] = ''
        item['protect_mode'] = ''
        try:
            item['description'] =  sel.xpath('//tr[2]/td/p/text()').extract()[0]
        except:
            item['description'] = ''

        try:
        	  item['process'] = sel.xpath('//li[@class=\"invrate\"]/font/text()').extract()[0]
            #item['process'] = sel.xpath('//tr[6]/td/text()').extract()[0]
        except:
            item['process'] = ''
        item['transfer_claim'] = ''
        try:
            item['min_amount'] = sel.xpath('//tr[7]/td/text()').extract()[0]
        except:
            item['min_amount'] = ''
        yield item


