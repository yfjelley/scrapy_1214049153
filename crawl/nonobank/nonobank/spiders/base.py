#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from nonobank.items import NonobankItem
import urllib
import urllib2
import os
import re

class NonobankSpider(CrawlSpider):
    name = 'nonobank'
    allowd_domain = ['www.nonobank.com/']

    #删除文件start
    #if (os.path.exists("content.txt")): os.remove("content.txt")
    #if (os.path.exists("content_index.txt")): os.remove("content_index.txt")
    #删除文件end

    url_list = []; #初始化url_list数组

    #download_delay = 3  #访问间隔秒数

    #for循环开始：访问产品列表的10个页面
    for i in range(0,10) :
        url_js = 'http://www.nonobank.com/Lend/GetLendList/8/' + str(i)\
                 + '?bo_expect=bo_expect&bo_expect_sort=00&bo_finish_rate=bo_finish_rate&bo_finish_rate_sort=00&'\
                 + 'bo_price=bo_price&bo_price_sort=00&bo_rate=bo_rate&bo_rate_sort=00&borrow_type=0&exTime=0'
                 #nnb js调用的页面链接，str(i)是翻页数

        wp = urllib2.urlopen(url_js) #打开连接
        content = wp.read() #获取页面内容
        content_productid = re.findall('\"bo_id\":\"'r'\S{6}', content) #获取 （"productid":） 及其后6位的id
        content_url = [content_index.replace('\"bo_id\":\"',
                                                     'https://www.nonobank.com/Lend/View/')
                                                    for content_index in content_productid]  #替换url
        content_url2 = [content_index2.replace('\"',
                                                 '')
                                                for content_index2 in content_url]  #替换链接最后一个“
        #url写入文件
        #fp = open("content.txt",'a')
        #fp.write(content)
        #写入productid位置
        #fp = open("content_index.txt",'a')
        #fp.write(str(content_index_new) + '\n')
        url_list.extend(content_url2) #将content_url里的url迭代写入url_list
    #for循环结束

    start_urls = set(url_list) #start_urls赋值,并去重
    print content_productid
    print content_url2

    def parse(self, response):
        item = NonobankItem()
        sel = Selector(response)
        try:
            item['name'] = sel.xpath('//*[@id="lenddetail"]/div[2]/div[1]/text()').extract()[0]
            #item['name'] = sel.xpath('//div[@class=\"info_list\"]/div/text()').extract()[0]
        except:
            item['name'] = ''
        item['link'] = response.url
        try:
            item['amount'] = sel.xpath('//*[@id="lenddetail"]/div[2]/div[2]/div[1]/ul/li[1]/p/span/text()').extract()[0]
            #item['amount'] = sel.xpath('//div[@class=\"info_list_right\"]/ul/li/text()').extract()[0]
        except:
            item['amount'] = ''
        item['min_amount'] = ''
        try:
            item['income_rate'] = sel.xpath('//*[@id="lenddetail"]/div[2]/div[2]/div[1]/ul/li[2]/p/span/text()').extract()[0]
            #item['income_rate'] = sel.xpath('//div[@class=\"info_list_left\"]/ul/li/text()').extract()[0]
        except:
            item['income_rate']=''
        try:
            item['term'] = sel.xpath('//*[@id="lenddetail"]/div[2]/div[2]/div[1]/ul/li[3]/p/span/text()').extract()[0]
        except:
            item['term'] =''
        item['area'] = ''
        item['transfer_claim'] = ''
        try:
            item['repay_type'] = sel.xpath('//*[@id="lenddetail"]/div[2]/div[2]/div[2]/ul[1]/li[2]/text()').extract()[0].split(u'：')[1]
        except:
            item['repay_type']=''
        item['reward'] = ''
        try:
            item['protect_mode'] = sel.xpath('//div[@class=\"info_list_right\"]/ul/li/a/text()').extract()[0]
        except:
            item['protect_mode']=''
        try:
            item['description'] = sel.xpath('//*[@id="lenddetail"]/div[4]/div[1]/div[3]/div/dl/dd/text()').extract()[0].split(u':')[1]
        except:
            item['description']=''
        try:
            item['process'] = sel.xpath('//div[@class="list_01"]/ul/li/text()').extract()[4]
        except:
            item['process']=''
        #[0].encode('utf-8')
        #[n.encode('utf-8') for n in title]

        yield item
