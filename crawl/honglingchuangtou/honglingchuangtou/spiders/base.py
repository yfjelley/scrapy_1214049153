#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from honglingchuangtou.items import HonglingchuangtouItem
import urllib
import urllib2
import os
import re

class HonglingchuangtouSpider(CrawlSpider):
    name = 'honglingchuangtou'
    allowd_domain = ['my089.com']

    #删除文件start
    #if (os.path.exists("content.txt")): os.remove("content.txt")
    #if (os.path.exists("content_index.txt")): os.remove("content_index.txt")
    #删除文件end

    url_list = []; #初始化url_list数组

    download_delay = 3  #访问间隔秒数

    #for循环开始：访问产品列表的10个页面
    for i in range(1,10) :
        url_js = 'https://www.my089.com/Loan/default.aspx?pid=' + str(i)  #页面链接，str(i)是翻页数
        wp = urllib2.urlopen(url_js) #打开连接
        content = wp.read() #获取页面内容
        content_productid = re.findall('Detail.aspx'r'[\S]*', content) #获取 （"productid":） 及其后6位的id
        content_url = [content_index.replace('Detail.aspx',
                                                     'https://www.my089.com/Loan/Detail.aspx')
                                                    for content_index in content_productid]  #替换url
        content_url2 = [content_index2.replace('\"',
                                                 '')
                                                for content_index2 in content_url]  #替换链接最后一个“

        #url写入文件
        #fp = open("content.txt",'a')
        #fp.write(content)
        #写入productid位置
        #fp = open("content_index.txt",'a')
        #fp.write(str(content_url2) + '\n')
        url_list.extend(content_url2) #将content_url里的url迭代写入url_list
    #for循环结束

    start_urls = set(url_list) #start_urls赋值,并去重


    def parse(self, response):
        item = HonglingchuangtouItem()
        sel = Selector(response)
        #item['link'] = sel.xpath('//a[@class=\"viewBtn\"]/@href').extract()
        #title1 = title[0]
        #title2 = title1.extract().split(",")[1].split("-")[0]
        item['name'] = sel.xpath('//span[@class=\"bt_txt\"]/text()').extract()[0]
        item['link'] = response.url
        item['amount'] = sel.xpath('//li[@class=\"jine\"]/span/b/text()').extract()[0][1:]
        item['min_amount'] = sel.xpath('//div[@class=\"biao_info\"]/ul/li/span/b/text()').extract()[4].split('~')[0]
        #item['amount'] = amount.split(" ")[0] #截取空格钱第一个字段
        item['income_rate'] = sel.xpath('//div[@class=\"biao_info\"]/ul/li/span/b[@class=\"number\"]/text()').extract()[0]
        item['term'] = sel.xpath('//div[@class=\"biao_info\"]/ul/li/span/b[@class=\"number\"]/text()').extract()[1]
        item['area'] = ''
        item['transfer_claim'] = ''
        item['repay_type'] = sel.xpath('//div[@class=\"biao_info\"]/ul/li/span/text()').extract()[4]
        item['reward'] = sel.xpath('//div[@class=\"Bid_Reward\"]/div/text()').extract()[0].strip()
        item['protect_mode'] = ''
        item['description'] = sel.xpath('//div[@class=\"textbox\"]/text()').extract()[0].strip()
        item['process'] = sel.xpath('//div[@class=\"Loading\"]/span[@class=\"lf\"]/text()').extract()[0]

        #[0].encode('utf-8')
        #[n.encode('utf-8') for n in title]

        yield item
