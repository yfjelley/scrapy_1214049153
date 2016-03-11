#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
import urllib
from datonghang.items import DatonghangItem
import urllib2
import os
import re

class DatonghangSpider(CrawlSpider):
    name = 'datonghang'

    allowd_domain = ['www.dtcash.com']

    #删除文件start
    #if (os.path.exists("content.txt")): os.remove("content.txt")
    #if (os.path.exists("content_index.txt")): os.remove("content_index.txt")
    #删除文件end

    url_list = []; #初始化url_list数组

    download_delay = 3  #访问间隔秒数

    #for循环开始：访问产品列表的10个页面
    for i in range(1,10) :

        url_js = 'http://www.dtcash.com/product/list/' + str(i) + '-0-0.html'

        wp = urllib.urlopen(url_js) #打开连接
        content = wp.read() #获取页面内容

        content_productid = re.findall('/Product/Index/'r'\d{8}', content) #获取 （"productid":） 及其后6位的id
        content_url = [content_index.replace('/Product/Index/',
                                                     'http://www.dtcash.com/Product/Index/')
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
 

    def parse(self, response):
        item = DatonghangItem()
        sel = Selector(response)
        #item['link'] = sel.xpath('//a[@class=\"viewBtn\"]/@href').extract()
        #title1 = title[0]
        #title2 = title1.extract().split(",")[1].split("-")[0]
        item['name'] = sel.xpath('//div[@class=\"list-div-tit\"]/span[@class=\"vis-mid\"]/text()').extract()[0]
        item['link'] = response.url
        amount = sel.xpath('//div[@class=\"span6 font-flo\"]/span[@class=\"vis-mid\"]/text()').extract()[0]
        item['amount'] = amount
        item['income_rate'] = sel.xpath('//span[@class=\"vis-mid list-red\"]/text()').extract()[0]
        item['term'] = sel.xpath('//div[@class=\"span6 second\"]/span[@class=\"vis-mid\"]/text()').extract()[0]
        item['repay_type'] = sel.xpath('//p[@class=\"base-hk16 base-pay pull-left font-flo\"]/span/text()').extract()[0][5:]
        item['reward'] = ''
        item['protect_mode'] = sel.xpath('//p[@class=\"base-mB0 base-three-color6 base-three-LH40 mb-bo\"]/text()').extract()[0]
        item['area'] = sel.xpath('//div[@class=\"span6 product-three-mT15\"]/p/text()').extract()[13]
        item['description'] = sel.xpath('//div[@class=\"list-div-tit\"]/span[@class=\"vis-mid\"]/text()').extract()[0]
        item['transfer_claim'] = ''
        item['min_amount'] = '1'
        finished = sel.xpath('//strong[@class=\"pricechange\"]/text()').extract()[0][1:]
        amount1 = amount[:-1]
        total = float(amount1) * 10000
        item['process'] =  float(finished) / total * 100
        #"https://list.lufax.com/list/productDetail?productId=" + sel.xpath('//input/text()').extract()[4]
        #[0].encode('utf-8')
        #[n.encode('utf-8') for n in title]

        yield item