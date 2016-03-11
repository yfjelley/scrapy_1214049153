#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from yiqihao.items import YiqihaoItem
import urllib
import urllib2
import os
import re
import requests

class YiqihaoSpider(CrawlSpider):
    name = 'yiqihao'
    allowd_domain = ['www.yiqihao.com']

    url_list = []; #初始化url_list数组

    download_delay = 3  #访问间隔秒数

    #for循环开始：访问产品列表的10个页面,
    #‘一起好’页面需要模拟点击才能读取页面数据，不能简单的通过传参读取
    for i in range(1,10) :
        url = 'https://www.yiqihao.com/loan/list'
        headers = {
            'User-Agent': 'User-Agent:Mozilla/5.0',
            'Origin': 'https://www.yiqihao.com',
            'Host': 'www.yiqihao.com',
            'Referer': 'https://www.yiqihao.com/loan/list',
            }
        s = requests.Session()  #需要improt requests
        post_data = {'size': 7, 'p': i} #页面循环
        r = s.post(url, post_data, headers=headers)
        content = r.content
        #print r.content

        content_productid = re.findall('\"lid\":\"'r'\S{7}', content) #获取 （"lid":） 及其后7位的id
        content_url = [content_index.replace('\"lid\":\"',
                                             'https://www.yiqihao.com/loan/detail/')
                                             for content_index in content_productid]  #替换url
        content_url2 = [content_index2.replace('\"',
                                               '')
                                               for content_index2 in content_url]  #替换链接最后一个“
        url_list.extend(content_url2) #将content_url里的url迭代写入url_list
    #for循环结束

    start_urls = set(url_list) #start_urls赋值,并去重
    #print start_urls


    def parse(self, response):
        item = YiqihaoItem()
        sel = Selector(response)
        #item['link'] = sel.xpath('//a[@class=\"viewBtn\"]/@href').extract()
        #title1 = title[0]
        #title2 = title1.extract().split(",")[1].split("-")[0]
        item['name'] = sel.xpath('//h5[@class=\"loaninfo-title\"]/text()').extract()[0]
        item['link'] = response.url
        item['amount'] = sel.xpath('//span[@class=\"darkred\"]/text()').extract()[2]
        item['min_amount'] = ''
        item['income_rate'] = sel.xpath('//span[@class=\"darkred\"]/text()').extract()[0]
        item['term'] = sel.xpath('//span[@class=\"darkred\"]/text()').extract()[1]
        item['area'] = ''
        item['transfer_claim'] = ''
        item['repay_type'] = sel.xpath('//span[@style=\"width:57%;float:right\"]/text()').extract()[0]
        item['reward'] = ''
        item['protect_mode'] = ''
        item['description'] = sel.xpath('//div[@id=\"des\"]/text()').extract()[0].strip()

        process1 = int(sel.xpath('//span[@class=\"bold\"]/text()').extract()[1][:-1])
        process2 = int(sel.xpath('//span[@class=\"bold\"]/text()').extract()[2][:-1])
        if process2 == 0:
            item['process'] = '100%'
        else:
            item['process'] = str(round((float(process1)/(process1+process2)),2))+'%'


        #[0].encode('utf-8')
        #[n.encode('utf-8') for n in title]

        yield item
