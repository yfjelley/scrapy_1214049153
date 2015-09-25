#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
import urllib
from yirendai.items import YirendaiItem
import urllib2
import os
import re



class YIRENDAIspider(CrawlSpider):
    name = 'yirendai'
    allowd_domain = ['www.yirendai.com']
    download_delay = 3  #访问间隔秒数
    start_urls = ['http://www.yirendai.com/loan/list/'+str(x) for x in range(1,10)]
    #['http://www.p2peye.com/hangqing/frtsgp'+str(x)+'.html' for x in range(2,100)]+['http://www.p2peye.com/hangqing/']

    rules = (
        Rule(SgmlLinkExtractor(allow=('/loan/view/'r'\d{6}', )),
             callback='parse_page', follow=True),
    )
    def parse_page(self, response):
        item = YirendaiItem()
        sel = Selector(response)
        num = len(sel.xpath('//table[@class=\"elite_table\"]/tbody/tr/td/text()').extract())
        print num
        name = sel.xpath('//title/text()').extract()[0]
        item['name'] = name.split("_")[0]
        item['link'] = response.url
        amount1 = sel.xpath('//td/strong/text()').extract()[0]
        amount2 = sel.xpath('//td/strong/span/text()').extract()[0]
        item['amount'] = amount1 + amount2
        item['income_rate'] = sel.xpath('//td/strong/text()').extract()[1]
        item['term'] = sel.xpath('//td/strong/text()').extract()[2]
        item['area'] = sel.xpath('//ul[@class=\"clearfix\"]/li/text()').extract()[2][4:]
        item['reward'] = ''
        item['description'] = sel.xpath('//div[@class=\"elite_left l\"]/p/text()').extract()[0].strip('\n').strip()
        item['process'] =  sel.xpath('//strong[@class=\"l tender_completed\"]/text()').extract()[0][4:]
        item['transfer_claim'] = ''
        item['min_amount'] = ''
        if num == 6:
            item['repay_type'] = sel.xpath('//table[@class=\"elite_table\"]/tbody/tr/td/text()').extract()[4][5:]
            item['protect_mode'] = sel.xpath('//table[@class=\"elite_table\"]/tbody/tr/td/text()').extract()[5][5:]
        else:
            item['repay_type'] = sel.xpath('//table[@class=\"elite_table\"]/tbody/tr/td/text()').extract()[5][5:]
            item['protect_mode'] = sel.xpath('//table[@class=\"elite_table\"]/tbody/tr/td/text()').extract()[6][5:]

        yield item


