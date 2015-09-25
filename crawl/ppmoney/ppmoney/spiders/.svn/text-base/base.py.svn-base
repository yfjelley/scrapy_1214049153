#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
import urllib
from ppmoney.items import PPmoneyItem
import urllib2
import os
import re



class PPMONEYspider(CrawlSpider):
    name = 'ppmoney'
    allowd_domain = ['ppmoney.com']
    download_delay = 3  #访问间隔秒数
    #url1 = ['http://www.ppmoney.com/anwenying?page='+str(x) for x in range(1,10)] #安稳盈--债券转让
    url1 = ['http://www.ppmoney.com/xiaodaibao?page='+str(x) for x in range(1,10)] #小贷宝
    url2 = ['http://www.ppmoney.com/zhitoubao?page='+str(x) for x in range(1,10)] #直投保
    #把url2追加进url1中
    url1.extend(url2)

    start_urls = url1
    #print start_urls

    rules = (
        Rule(SgmlLinkExtractor(allow=('/Project/LoanDetail/.*', )),
             callback='parse_page', follow=True), #小贷宝
        Rule(SgmlLinkExtractor(allow=('/Project/Detail/.*', )),
             callback='parse_page', follow=True), #直投保
    )

    def parse_page(self, response):
        item = PPmoneyItem()
        sel = Selector(response)
        #item['link'] = sel.xpath('//a[@class=\"viewBtn\"]/@href').extract()
        #title1 = title[0]
        #title2 = title1.extract().split(",")[1].split("-")[0]
        item['name'] = sel.xpath('//div[@class=\"l-proj\"]/h1/text()').extract()[0]
        link = response.url
        item['link'] = link
        amount1 = sel.xpath('//div[@class=\"l-proj\"]/div[@class=\"l-proj-c\"]/ul[@class=\"cf\"]/li/span/text()').extract()[1].strip()
        amount2 = sel.xpath('//div[@class=\"l-proj\"]/div[@class=\"l-proj-c\"]/ul[@class=\"cf\"]/li/span/text()').extract()[2].strip()
        item['amount'] = amount1 + amount2
        #item['amount'] = amount.split(" ")[0] #截取空格钱第一个字段
        #rate_text = sel.xpath('//div[@id=\"view_con_m\"]/p/text()').extract()[0]
        #num = len(rate_text.split("/")[0]) + 2 #截取/前的位数
        item['income_rate'] = sel.xpath('//div[@class=\"l-proj\"]/div[@class=\"l-proj-c\"]/ul[@class=\"cf\"]/li/span[@class=\"value red\"]/text()').extract()[0].strip()
        term1 = sel.xpath('//div[@class=\"l-proj\"]/div[@class=\"l-proj-c\"]/ul[@class=\"cf\"]/li/span/text()').extract()[9].strip()
        term2 = sel.xpath('//div[@class=\"l-proj\"]/div[@class=\"l-proj-c\"]/ul[@class=\"cf\"]/li/span/text()').extract()[10].strip()
        term3 = sel.xpath('//div[@class=\"l-proj\"]/div[@class=\"l-proj-c\"]/ul[@class=\"cf\"]/li[@class=\"w-100\"]/text()').extract()
        if len(term3) > 3:
            item['term'] = term1 + term3[2].strip()
        else:
            item['term'] = term1 + term2
        text1 = sel.xpath('//div[@class=\"l-proj\"]/div[@class=\"l-proj-c\"]/ul[@class=\"cf\"]/li/span/text()').extract()
        text2 =sel.xpath('//div[@class=\"l-proj\"]/div[@class=\"l-proj-c\"]/ul[@class=\"cf\"]/li/text()').extract()
        description = sel.xpath('//div[@id=\"intro\"]/div/p/text()').extract()
        description1 = sel.xpath('//div[@id=\"intro\"]/div/p/span/text()').extract()
        description2 = sel.xpath('//div[@id=\"intro\"]/div/text()').extract()
        if  len(text1)== 23:
            item['repay_type'] = text1[-8].strip()
            item['area'] =''
            item['reward'] = ''
            item['protect_mode'] = ''
        else:
            item['repay_type'] = text2[-1].strip()
            item['area'] =''
            item['reward'] = ''
            item['protect_mode'] = ''
        if len(description) == 2:
            item['description'] = description[1]
        elif len(description) == 1:
            item['description'] = description[0]
        else:
            if description1:
                item['description'] = description1[0]
            else:
                item['description'] = description2[0]
        item['transfer_claim'] = ''
        item['min_amount'] = '100.00'
        product_id = link[-4:]
        process_link = 'http://www.ppmoney.com/project/AsyncLoadPrjStatus/' + str(product_id)
        pl = urllib2.urlopen(process_link) #打开连接
        rate_text = pl.read() #获取页面内容
        process = rate_text.split(":")[2].split(",")[0].replace('\"','')
        #if process and process <> '100.00':
        item['process'] = process
        #else:
        #    item['process'] = ''
        yield item


