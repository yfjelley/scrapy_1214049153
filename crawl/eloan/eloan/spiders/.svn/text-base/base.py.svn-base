#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
import urllib
from eloan.items import EloanItem
import urllib2
import os
import re



class ELOANspider(CrawlSpider):
    name = 'eloan'
    allowd_domain = ['eloancn.com']
    #删除文件start
    #if (os.path.exists("content.txt")): os.remove("content.txt")
    #if (os.path.exists("content_index.txt")): os.remove("content_index.txt")
    #删除文件end

    url_list = []; #初始化url_list数组

    download_delay = 3  #访问间隔秒数

    #for循环开始：访问产品列表的10个页面
    for i in range(1,10) :
        url_js = 'http://www.eloancn.com/new/loadAllTender.action?page=' + str(i)
        #print(url_js)
        wp = urllib2.urlopen(url_js) #打开连接
        content = wp.read() #获取页面内容
        content_productid = re.findall('http://www.eloancn.com:80/loan/loandetail.action\?tenderid='r'\d{5}', content) #获取 （"productid":） 及其后6位的id
        content_url = [content_index.replace('http://www.eloancn.com:80/',
                                                     'http://www.eloancn.com/')
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
        item = EloanItem()
        sel = Selector(response)
        #item['link'] = sel.xpath('//a[@class=\"viewBtn\"]/@href').extract()
        #title2 = title1.extract().split(",")[1].split("-")[0]
        name1 = sel.xpath('//title/text()').extract()[0]
        name2 = name1.split(" ")[2]
        item['name'] = name2[0:-6]
        item['link']  = response.url
        item['amount'] = sel.xpath('//div[@class=\"ld_info fl\"]/ul/li/span[@class=\"font22 colorE6\"]/text()').extract()[0].strip()
        #item['amount'] = amount.split(" ")[0] #截取空格钱第一个字段
        #rate_text = sel.xpath('//div[@id=\"view_con_m\"]/p/text()').extract()[0]
        #num = len(rate_text.split("/")[0]) + 2 #截取/前的位数
        income_rate1 = sel.xpath('//div[@class=\"ld_info fl\"]/ul/li/span[@class=\"font22 colorE6\"]/text()').extract()[1].strip()
        income_rate2 = sel.xpath('//div[@class=\"ld_info fl\"]/ul/li[@class=\"wd300\"]/text()').extract()[1].strip()
        item['income_rate'] = income_rate1 + income_rate2
        term1 = sel.xpath('//div[@class=\"ld_info fl\"]/ul/li/span[@class=\"font22 colorE6\"]/text()').extract()[2].strip()
        term2 = sel.xpath('//div[@class=\"ld_info fl\"]/ul/li[@class=\"wd180\"]/text()').extract()[1].strip()
        item['term'] = term1 + term2
        repay_type = sel.xpath('//div[@class=\"ld_info fl\"]/ul/li[@class=\"wd180\"]/text()').extract()[2].strip()
        item['repay_type'] = repay_type[5:]
        item['area'] = sel.xpath('//div[@class=\"ld_user fl\"]/p/text()').extract()[0].strip()
        item['reward'] = ''
        item['protect_mode'] = ''
        item['description'] = sel.xpath('//div[@class=\"recordBorder clear bgFF\"]/div[@class=\"record\"]/dl/dd/text()').extract()[0].strip()
        item['transfer_claim'] = ''
        item['min_amount'] = ''
        item['process'] = sel.xpath('//div[@class=\"ld_info fl\"]/ul/li/span/em[@style=\"width:100.0%;background-color:#7cae4a;\"]/text()').extract()[0].strip()
        yield item


