#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from itouzi.items import ItouziItem
import urllib
import urllib2
import os
import re
import httplib
import sys
import json


#爱投资对于已完成还款的标的，将不公示其信息
class ItouziSpider(CrawlSpider):
    #  to solve the problem:'ascii' codec can't decode byte 0xe5 in position 0: ordinal not in range(128)
    #reload(sys)
    #sys.setdefaultencoding('utf8')
    #/
    name = 'itouzi'
    allowd_domain = ['www.itouzi.com']
    url_list = []; #初始化url_list数组
    download_delay = 3  #访问间隔秒数

    #for循环开始：访问产品列表的10个页面
    for x in range(1,2) :
        url_js = 'http://www.itouzi.com/dinvest/ajax/list?page='+str(x)+'&type=2'

        wp = urllib2.urlopen(url_js) #打开连接
        content = wp.read() #获取页面内容
        content_productid = re.findall('id='r'\S{46}', content) #获取 （"productid":） 及其后6位的id
        #content_url = [content_index.replace('http://www.anxin.com/invest/',
         #                                            'https://member.niwodai.com/xiangmu/v')
          #                                          for content_index in content_productid]  #替换url
        content_url1 = [content_index1.replace('id=',
                                                 'http://www.itouzi.com/dinvest/invest/detail?id=')
                                                for content_index1 in content_productid]  #替换链接最后一个“
        url_list.extend(content_url1) #将content_url里的url迭代写入url_list
    for x in range(1,2) :
        url_js = 'http://www.itouzi.com/dinvest/ajax/list?page='+str(x)+'&type=6'

        wp = urllib2.urlopen(url_js) #打开连接
        content = wp.read() #获取页面内容
        content_productid2 = re.findall('id='r'\S{46}', content) #获取 （"productid":） 及其后6位的id
        #content_url = [content_index.replace('http://www.anxin.com/invest/',
         #                                            'https://member.niwodai.com/xiangmu/v')
          #                                          for content_index in content_productid]  #替换url
        content_url2 = [content_index2.replace('id=',
                                                 'http://www.itouzi.com/dinvest/factoring/detail?id=')
                                                for content_index2 in content_productid2]  #替换链接最后一个“
        url_list.extend(content_url2) #将content_url里的url迭代写入url_list
    for x in range(1,2) :
        url_js = 'http://www.itouzi.com/dinvest/ajax/list?page='+str(x)+'&type=5'
        print url_js
        wp = urllib2.urlopen(url_js) #打开连接
        content = wp.read() #获取页面内容
        content_productid3 = re.findall('id='r'\S{46}', content) #获取 （"productid":） 及其后6位的id
        #content_url = [content_index.replace('http://www.anxin.com/invest/',
         #                                            'https://member.niwodai.com/xiangmu/v')
          #                                          for content_index in content_productid]  #替换url
        content_url3 = [content_index3.replace('id=',
                                                 'http://www.itouzi.com/dinvest/lease/detail?id=')
                                                for content_index3 in content_productid3]  #替换链接最后一个“
        url_list.extend(content_url3) #将content_url里的url迭代写入url_list
    for x in range(1,2) :
        url_js = 'http://www.itouzi.com/dinvest/ajax/list?page='+str(x)+'&type=7'

        wp = urllib2.urlopen(url_js) #打开连接
        content = wp.read() #获取页面内容
        content_productid4 = re.findall('id='r'\S{46}', content) #获取 （"productid":） 及其后6位的id
        #content_url = [content_index.replace('http://www.anxin.com/invest/',
         #                                            'https://member.niwodai.com/xiangmu/v')
          #                                          for content_index in content_productid]  #替换url
        content_url4 = [content_index4.replace('id=',
                                                 'http://www.itouzi.com/dinvest/art/detail?id=')
                                                for content_index4 in content_productid4]  #替换链接最后一个“
        url_list.extend(content_url4) #将content_url里的url迭代写入url_list
    #for循环结束

    start_urls = set(url_list) #start_urls赋值,并去重

    #def parse_page(self, response):
    def parse(self, response):
        item = ItouziItem()
        sel = Selector(response)
        #item['link'] = sel.xpath('//a[@class=\"viewBtn\"]/@href').extract()
        #title1 = title[0]
        #title2 = title1.extract().split(",")[1].split("-")[0]
        name = sel.xpath('//title/text()').extract()[0]
        num = len(name) - 24
        item['name'] = name[0:num]
        print item['name']
        item['link'] = response.url
        print item['link']

        amount1 = sel.xpath('//div[@class=\"i-p-i-c-condition clearfix\"]/dl/dd/strong/text()').extract()
        amount2 = sel.xpath('//div[@class=\"i-p-i-c-condition clearfix\"]/dl/dd/span/text()').extract()
        if amount1 and amount2:
            item['amount'] = amount1[1] + amount2[1]
        else:
            item['amount'] = ''

        item['min_amount'] = ''
        try:
            item['income_rate'] = sel.xpath('//em[@class=\"fs-xl strong\"]/text()').extract()[0]
        except:
            item['income_rate'] = ''
        term1 = sel.xpath('//div[@class=\"i-p-i-c-condition clearfix\"]/dl/dd/strong/text()').extract()[0]
        term2 = sel.xpath('//div[@class=\"i-p-i-c-condition clearfix\"]/dl/dd/span/text()').extract()[0]
        item['term'] = term1 + term2

        item['area'] = ''
        item['transfer_claim'] = ''
        item['repay_type'] = sel.xpath('//ul[@class=\"i-p-i-guarantee mgt\"]/li/text()').extract()[0]
        item['reward'] = ''

        item['protect_mode'] = sel.xpath('//a[@class=\"tips fl\"]/@title').extract()[0]

        description = sel.xpath('//div[@id=\"projectDesc\"]/div/div[@class=\"allDesc\"]/p/text()').extract()
        if description:
            item['description'] = description[0].strip()
        else:
            item['description'] = ''

        process = sel.xpath('//div[@class=\"clearfix\"]/span/text()').extract()
        if process:
            item['process'] = process[1].strip()
        else:
            item['process'] = ''
        #[0].encode('utf-8')
        #[n.encode('utf-8') for n in title]

        yield item

