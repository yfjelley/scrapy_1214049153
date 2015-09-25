#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from niwodai.items import NiwodaiItem
import urllib
import urllib2
import os
import re
import httplib

class NiwodaiSpider(CrawlSpider):
    name = 'niwodai'
    allowd_domain = ['member.niwodai.com']
    url_list = []; #初始化url_list数组
    download_delay = 3  #访问间隔秒数

    #for循环开始：访问产品列表的10个页面
    for i in range(1,10) :
        url_js = 'https://member.niwodai.com/loan/loan.do?totalCount=388&pageNo=' + str(i)

        wp = urllib2.urlopen(url_js) #打开连接
        content = wp.read() #获取页面内容
        content_productid = re.findall('_blank\" href=\"/xiangmu/v'r'[\S]*', content) #获取 （"productid":） 及其后6位的id
        content_url = [content_index.replace('_blank\" href=\"/xiangmu/v',
                                                     'https://member.niwodai.com/xiangmu/v')
                                                    for content_index in content_productid]  #替换url
        content_url2 = [content_index2.replace('\"',
                                                 '')
                                                for content_index2 in content_url]  #替换链接最后一个“
        url_list.extend(content_url2) #将content_url里的url迭代写入url_list
    #for循环结束

    start_urls = set(url_list) #start_urls赋值,并去重
    print url_list
    def parse(self, response):
        item = NiwodaiItem()
        sel = Selector(response)
        item['name'] = sel.xpath('//div[@class=\"title\"]/a/text()').extract()[0]
        item['link'] = response.url
        item['amount'] = sel.xpath('//div[@class=\"b\"]/span/text()').extract()[0].strip()
        item['min_amount'] = ''
        item['income_rate'] = sel.xpath('//div[@class=\"b fc_orange\"]/span/text()').extract()[0]

        term1 = sel.xpath('//div[@class=\"b\"]/span[@class=\"fs_32\"]/text()').extract()[1]
        term2 = sel.xpath('//div[@class=\"b\"]/span[@class=\"fs_18\"]/text()').extract()[1]
        item['term'] = term1 + term2

        item['area'] = ''
        item['transfer_claim'] = ''
        item['repay_type'] = sel.xpath('//ul[@class=\"clearfix line2 b_border\"]/li/span/text()').extract()[0]
        item['reward'] = ''

        item['protect_mode'] = ''
        item['description'] = sel.xpath('//p[@class=\"fc_6 text\"]/text()').extract()[0]
        item['process'] = sel.xpath('//ul[@class=\"clearfix line2\"]/li/text()').extract()[1]

        yield item

    #def parse_page2(self, response):



