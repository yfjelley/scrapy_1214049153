#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from anxin.items import AnxinItem
import urllib
import urllib2
import os
import re
import httplib

class AnxinSpider(CrawlSpider):
    name = 'anxin'
    allowd_domain = ['anxin.com']
    url_list = []; #初始化url_list数组
    download_delay = 3  #访问间隔秒数

    #for循环开始：访问产品列表的10个页面
    for i in range(1,10) :
        url_js = 'http://www.anxin.com/ajax/ajax_borrow.ashx?cmd=getfilterlist&key=r0%2Ck0%2Cp0%2Cu0%2Ca0%2Cv0%2C'\
                 + '&pageindex=' + str(i) + '&pagesize=10' \
        
        #print url_js
        wp = urllib2.urlopen(url_js) #打开连接
        content = wp.read() #获取页面内容
        content_productid = re.findall('http://www.anxin.com/invest/'r'[\S]*', content) #获取 （"productid":） 及其后6位的id
        #content_url = [content_index.replace('http://www.anxin.com/invest/',
        #                                            'https://member.niwodai.com/xiangmu/v')
        #                                          for content_index in content_productid]  #替换url
        
        #print content_productid
        content_url2 = [content_index2.replace('\'',
                                                 '')
                                                for content_index2 in content_productid]  #替换链接最后一个“
        #print content_url2 
        url_list.extend(content_url2) #将content_url里的url迭代写入url_list
        #for循环结束

    start_urls = set(url_list) #start_urls赋值,并去重
    #print(url_list)
    def parse(self, response):
        item = AnxinItem()
        sel = Selector(response)
        item['name'] = sel.xpath('//title/text()').extract()[0]
        item['link'] = response.url
        item['amount'] = sel.xpath('//div[@class=\"content\"]/p/text()').extract()[0]
        item['min_amount'] = sel.xpath('//div[@class=\"inputN\"]/span/i/text()').extract()[0]
        item['income_rate'] = sel.xpath('//div[@class=\"content\"]/p/text()').extract()[1]
        item['term'] = sel.xpath('//div[@class=\"content\"]/span/text()').extract()[1]
        item['area'] = ''
        item['transfer_claim'] = ''
        item['repay_type'] = sel.xpath('//div[@class=\"content\"]/span/text()').extract()[1]
        item['reward'] = ''

        item['protect_mode'] = ''
        item['description'] = ''
        item['process'] = sel.xpath('//div[@class=\"over\"]/span/text()').extract()[0]

        yield item

    #def parse_page2(self, response):



