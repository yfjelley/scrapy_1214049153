#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from paipaidai.items import PaipaidaiItem
import urllib
import urllib2
import os
import re
import httplib
import sys


#爱投资对于已完成还款的标的，将不公示其信息
class PaipaidaiSpider(CrawlSpider):
    #  to solve the problem:'ascii' codec can't decode byte 0xe5 in position 0: ordinal not in range(128)
    reload(sys)
    sys.setdefaultencoding('utf8')
    #/
    name = 'paipaidai'
    allowd_domain = ['www.paipaidai.com']
    download_delay = 2  #访问间隔秒数
    #['https://www.itouzi.com/dinvest/invest/detail?id=44335555475675434642733d']
    url1 = ['http://www.ppdai.com/lend/12_s0_p'+str(x) for x in range(1,3)] #热投区
    url2 = ['http://www.ppdai.com/lend/13_s0_p'+str(x) for x in range(1,3)] #安全标专区
    url3 = ['http://www.ppdai.com/lend/14_s0_p'+str(x) for x in range(1,3)] #逾期就赔
    url4 = ['http://www.ppdai.com/lend/8_s0_p'+str(x) for x in range(1,3)]  #网商专区
    url5 = ['http://www.ppdai.com/lend/3_s0_p'+str(x) for x in range(1,3)]  #二次借款
    url6 = ['http://www.ppdai.com/lend/15_s0_p'+str(x) for x in range(1,3)] #合作机构专区
    url7 = ['http://www.ppdai.com/lend/16_s0_p'+str(x) for x in range(1,3)] #新手福利标
    url1.extend(url2)
    url1.extend(url3)
    url1.extend(url4)
    url1.extend(url5)
    url1.extend(url6)
    url1.extend(url7)

    start_urls = url1
    #print start_urls

    rules = (
        Rule(SgmlLinkExtractor(allow=('/list/.*', )),
             callback='parse_page', follow=True),

    )



    #def parse_page(self, response):
    def parse_page(self, response):
        item = PaipaidaiItem()
        sel = Selector(response)
        item['name'] = sel.xpath('//span[@class=\"\"]/text()').extract()[0]
        print item['name']
        item['link'] = response.url
        item['amount'] = sel.xpath('/html/body/div[3]/div[2]/div[1]/div[1]/div[2]/dl[1]/dd/text()').extract()[0].strip()
        item['min_amount'] = ''
        item['income_rate'] = sel.xpath('/html/body/div[3]/div[2]/div[1]/div[1]/div[2]/dl[2]/dd/text()').extract()[0].strip()

        item['term'] =  sel.xpath('/html/body/div[3]/div[2]/div[1]/div[1]/div[2]/dl[3]/dd/text()').extract()[0].strip()


        item['area'] = ''
        item['transfer_claim'] = ''
        item['repay_type'] = sel.xpath('/html/body/div[3]/div[2]/div[1]/div[1]/div[3]/div[1]/div[1]/text()').extract()[0].strip().split(":")[1]

        item['reward'] = ''
        item['protect_mode'] = ''
        try:
            item['description'] = sel.xpath('/html/body/div[3]/div[3]/div/p/text()').extract()[0].strip()
        except:
            item['description']=''
        item['process'] = sel.xpath('/html/body/div[3]/div[2]/div[1]/div[1]/div[3]/div[2]/div[1]/text()').extract()[1].strip()


        #[0].encode('utf-8')
        #[n.encode('utf-8') for n in title]

        yield item
