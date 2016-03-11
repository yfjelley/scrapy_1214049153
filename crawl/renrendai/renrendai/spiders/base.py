#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from renrendai.items import RenrendaiItem
import urllib
import urllib2
import os
import re



class RenrendaiSpider(CrawlSpider):
    name = 'renrendai'
    allowd_domain = ['renrendai.com']

    #删除文件start
    #if (os.path.exists("content.txt")): os.remove("content.txt")
    #if (os.path.exists("content_index.txt")): os.remove("content_index.txt")
    #删除文件end

    url_list = []; #初始化url_list数组

    #download_delay = 3  #访问间隔秒数

    #for循环开始：访问产品列表的10个页面
    for i in range(1,10) :
        url_js = 'http://www.we.com/lend/loanList.action#page-'+str(i)
        print "url_js is :",url_js
        wp = urllib2.urlopen(url_js) #打开连接
        content = wp.read() #获取页面内容
        content_productid = re.findall('\"loanId\":'r'\d{6}', content) #获取 （"loanId":） 及其后6位的id

        #print(content_productid)
        content_url = [content_index.replace('\"loanId\":',
                                             'http://www.we.com/lend/detailPage.action?loanId=')
                                             for content_index in content_productid]  #替换url
        print(content_url)
        #url写入文件
        #fp = open("content.txt",'a')
        #fp.write(content)
        #写入productid位置
        #fp = open("content_index.txt",'a')
        #fp.write(str(content_url) + '\n')
        url_list.extend(content_url) #将content_url里的url迭代写入url_list
        #print "url_list is :",url_list

    #for循环结束
    start_urls = set(url_list) #start_urls赋值
    print "start_urls is:",start_urls


    def parse(self, response):
        item = RenrendaiItem()
        sel = Selector(response)
        item['name'] = sel.xpath('//*[@id="loan-basic-panel"]/div/div[1]/div/em[2]/text()').extract()[0].strip()
        #item['name'] = name.extract().split("-")[0].strip() #截取地一个-前的字段，并去除空格
        item['link'] = response.url
        item['amount'] = sel.xpath('//*[@id="loan-basic-panel"]/div/div[2]/div[1]/div/dl[1]/dd/em/text()').extract()[0]
        item['min_amount'] = ''
        item['income_rate'] = sel.xpath('//*[@id="loan-basic-panel"]/div/div[2]/div[1]/div/dl[2]/dd/em[1]/text()').extract()[0]
        item['term'] = sel.xpath('//*[@id="loan-basic-panel"]/div/div[2]/div[1]/div/dl[3]/dd/em/text()').extract()[0]
        item['area'] = ''
        item['transfer_claim'] = ''
        item['repay_type'] = sel.xpath('//*[@id="loan-basic-panel"]/div/div[2]/div[1]/ul/li[2]/span[2]/text()').extract()[0]
        item['reward'] = ''
        item['protect_mode'] = sel.xpath('//*[@id="loan-basic-panel"]/div/div[2]/div[1]/ul/li[1]/span[2]/text()').extract()[0]
        item['description'] = sel.xpath('//*[@id="loan-tab-content"]/div/div[1]/div[3]/div/text()').extract()[0].strip()
        process = sel.xpath('//*[@id="loan-basic-panel"]/div/div[2]/div[1]/ul/li[3]/span[2]/span[2]/em/text()').extract()[0].strip()
        if process:
            item['process'] = process[0]
        else:
            item['process'] = '100%'
        #[0].encode('utf-8')
        #[n.encode('utf-8') for n in title]

        yield item
