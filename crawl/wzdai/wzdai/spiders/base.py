#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
import urllib
from wzdai.items import WzdaiItem
import urllib2
import os
import re
import json


class WZDAIspider(CrawlSpider):
    name = 'wzdai'
    allowd_domain = ['www.wzdai.com']

    url_list = []; #初始化url_list数组

    download_delay = 3  #访问间隔秒数

    #for循环开始：访问产品列表的10个页面
    for i in range(1,2):
        url_js = 'http://finance.wzdai.com/list.shtml'
        print(url_js)
        wp = urllib.urlopen(url_js) #打开连接
        content = wp.read() #获取页面内容
        content_productid = re.findall('detail_'r'\d{6}', content) #获取 （"productid":） 及其后6位的id
        content_url = [content_index.replace('detail_',
                                                     'https://www.wzdai.com/invest/ajaxDetail.html?callback=jQuery1111019497463972268458_1418355470547&id=')
                                                    for content_index in content_productid]  #替换url

        #url写入文件
        #fp = open("content.txt",'a')
        #fp.write(content)
        #写入productid位置
        #fp = open("content_index.txt",'a')
        #fp.write(str(content_index_new) + '\n')
        url_list.extend(set(content_url)) #将content_url里的url迭代写入url_list
    #for循环结束

    start_urls = url_list #start_urls赋值
    #print(start_urls)

    def parse(self, response):
        item = WzdaiItem()
        sel = Selector(response)
        link = response.url
        link1 = link.replace('https://www.wzdai.com/invest/ajaxDetail.html?callback=jQuery1111019497463972268458_1418355470547&id=','http://invest.wzdai.com/pagers/invest/dpbdetail_')
        item['link'] = link1 + '.html'
    #json字典数据规范
        text = urllib.urlopen(link).read()
        text1 = text.replace('jQuery1111019497463972268458_1418355470547(','')
        text2 = text1.replace('})','}')
        text_all = json.loads(text2)  #打开连接
    #--------------------------------------------------------------------------------------
        item['name'] = text_all['borrow']['name']
        amount = text_all['borrow']['account']
        amount_yes = text_all['borrow']['account_yes']
        item['amount'] = amount
        item['income_rate'] = text_all['borrow']['apr']
        is_day = text_all['borrow']['is_day']
        if is_day == '1':
            term = text_all['borrow']['time_limit_day']
            item['term'] = term + 'day'
        else:
            term = text_all['borrow']['time_limit']
            item['term'] = term + 'month'
        item['repay_type'] = text_all['borrow']['style'] #0:按月分期还款 1：每月还息到期还本 2：一次性还款
        item['area'] = ''
        item['reward'] = ''
        item['protect_mode'] = ''
        #item['description'] = text_all['borrow']['content']
        item['description'] = text_all['borrow']['name']
        item['process'] = float(amount_yes)/float(amount) * 100
        item['transfer_claim'] = ''
        item['min_amount'] = ''
        yield item


