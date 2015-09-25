#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from lujinsuo.items import LujinsuoItem
import urllib
import urllib2
import os
import re

class LujinsuoSpider(CrawlSpider):
    name = 'lujinsuo'
    allowd_domain = ['list.lufax.com']

    #删除文件start
    #if (os.path.exists("content.txt")): os.remove("content.txt")
    #if (os.path.exists("content_index.txt")): os.remove("content_index.txt")
    #删除文件end

    url_list = []; #初始化url_list数组

    download_delay = 3  #访问间隔秒数

    #for循环开始：访问产品列表的10个页面
    for i in range(1,10) :
        url_js = 'https://list.lufax.com/list/service/product/listing/' + str(i) \
                + '?' +'minAmount=0&maxAmount=100000000&minInstalments=1&maxInstalments=240' \
                + '&collectionMode=&productName=&column=publishedAt&order=asc&isDefault=true&' \
                + 'isPromotion=0&pageLimit=10'  #陆金所js调用的页面链接，str(i)是翻页数

        wp = urllib2.urlopen(url_js) #打开连接
        content = wp.read() #获取页面内容
        content_productid = re.findall('\"productId\":'r'\d{6}', content) #获取 （"productid":） 及其后6位的id
        content_url = [content_index.replace('\"productId\":',
                                                     'https://list.lufax.com/list/productDetail?productId=')
                                                    for content_index in content_productid]  #替换url

        #url写入文件
        #fp = open("content.txt",'a')
        #fp.write(content)
        #写入productid位置
        #fp = open("content_index.txt",'a')
        #fp.write(str(content_index_new) + '\n')
        url_list.extend(content_url) #将content_url里的url迭代写入url_list
    #for循环结束

    start_urls = set(url_list) #start_urls赋值,并去重


    def parse(self, response):
        item = LujinsuoItem()
        sel = Selector(response)
        #item['link'] = sel.xpath('//a[@class=\"viewBtn\"]/@href').extract()
        #title1 = title[0]
        #title2 = title1.extract().split(",")[1].split("-")[0]
        item['name'] = sel.xpath('//title/text()').extract()[0][0:-10]
        item['link'] = response.url
        amount = sel.xpath('//ul[@class=\"clearfix detail-info-list\"]/li/p/strong/text()').extract()[0]
        item['amount'] = amount.split(" ")[0] #截取空格钱第一个字段
        item['min_amount'] = ''
        item['income_rate'] = sel.xpath('//strong[@class=\"tips-title\"]/text()').extract()[0]
        item['term'] = sel.xpath('//ul[@class=\"clearfix detail-info-list\"]/li/p/strong/text()').extract()[2]
        item['area'] = ''
        item['transfer_claim'] = ''
        item['repay_type'] = sel.xpath('//span[@class=\"tips-title\"]/text()').extract()[0]
        item['reward'] = sel.xpath('//span[@class=\"description\"]/text()').extract()[0].strip()
        item['protect_mode'] = sel.xpath('//span[@class=\"tips-title\"]/text()').extract()[1]
        item['description'] = sel.xpath('//table[@class=\"product-description\"]/tr/td/text()').extract()[5]
        item['process'] = sel.xpath('//span[@class=\"progressTxt\"]/text()').extract()[0]

        #[0].encode('utf-8')
        #[n.encode('utf-8') for n in title]

        yield item
