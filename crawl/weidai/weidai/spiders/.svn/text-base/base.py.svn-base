#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
import urllib
from weidai.items import WeidaiItem
import urllib2
import os
import re
import json


class WEIDAIspider(CrawlSpider):
    name = 'weidai'
    allowd_domain = ['weidai.com.cn']
    #删除文件start
    if (os.path.exists("content.txt")): os.remove("content.txt")
    if (os.path.exists("content_index.txt")): os.remove("content_index.txt")
    #删除文件end

    url_list = []; #初始化url_list数组

    #download_delay = 5   #访问间隔秒数

    #for循环开始：访问产品列表的10个页面
    for i in range(1,10) :
        url_js = 'https://www.weidai.com.cn/?m=Biao&t=today&pageIndex=' + str(i) + '&pageSize=8&sortField=b.verify_time&sortOrder=desc&data=null'
        #print(url_js)
        wp = urllib2.urlopen(url_js) #打开连接
        content = wp.read() #获取页面内容
        content_productid = re.findall('"bid":"'r'\d{5}', content) #获取 （"productid":） 及其后6位的id
        content_url = [content_index.replace('\"bid\":"',
                                                     'https://www.weidai.com.cn/?m=Test&s=view&bid=')
                                                    for content_index in content_productid]  #替换url
        #url写入文件
        #fp = open("content.txt",'a')
        #fp.write(content)
        #写入productid位置
        #fp = open("content_index.txt",'a')
        #fp.write(str(content_url) + '\n')
        url_list.extend(content_url) #将content_url里的url迭代写入url_list
    #for循环结束

    start_urls = set(url_list) #start_urls赋值
    #print(start_urls)

    def parse(self, response):
        item = WeidaiItem()
        sel = Selector(response)
        link = response.url
        #text_all = urllib2.urlopen(link).read() #打开连接
        text_all = json.loads(urllib2.urlopen(link).read())  #打开连接
        print text_all.keys()
        #print text_all.values()
        item['name'] = text_all['binfo']['name']
        link1 = text_all['binfo']['bid']
        link2 = 'https://www.weidai.com.cn/ind/bidinfo.html?id=' + link1
        item['link']  = link2
        item['amount'] = text_all['binfo']['account']
        item['income_rate'] = text_all['binfo']['borrow_apr']
        term = text_all['binfo']['borrow_period']
        term_type = text_all['binfo']['days']
        item['term'] = term
        #item['term_type'] = term_type
        term_type1 = 'day'
        term_type2 = 'month'
        if int(term_type) > 29:   #天
            item['term'] = str(term) + term_type1
        else:  #月
            item['term'] = str(term) + term_type2
        item['repay_type'] =text_all['binfo']['borrow_style'] #(1:月还息到期还本;2:等额本息还款)
        item['area'] = text_all['user']['v_area']
        item['reward'] = ''
        item['protect_mode'] = ''
        item['description'] = text_all['binfo']['name']
        item['transfer_claim'] = ''
        item['min_amount'] = text_all['binfo']['tender_account_min']
        item['process'] = text_all['binfo']['borrow_account_scale']

        yield item