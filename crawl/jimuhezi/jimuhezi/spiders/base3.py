#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from jimuhezi.items import JimuheziItem
import urllib
import urllib2
import os
import re

class JimuheziSpider(CrawlSpider):
    name = 'jimuhezi3'
    allowd_domain = ['jimubox.com']

    #删除文件start
    if (os.path.exists("content.txt")): os.remove("content.txt")
    if (os.path.exists("content_index.txt")): os.remove("content_index.txt")
    #删除文件end

    url_list = []; #初始化url_list数组
    url_list2 = [];
    download_delay = 1  #访问间隔秒数

    #for循环开始：访问产品列表的10个页面
    for i in range(5,7) :
        url_js = 'https://www.jimubox.com/Project/List?rate=&guarantee=&range=&page=' + str(i) \
                + '&category=&status='   #积木盒子调用的页面链接，str(i)是翻页数
        wp = urllib2.urlopen(url_js) #打开连接
        content = wp.read() #获取页面内容
        content_productid = re.findall('/Project/Index/'r'\d{5}', content) #获取 （"productid":） 及其后5位的id
        content_url = [content_index.replace('/Project/Index/',
                                                     'https://www.jimubox.com/Project/Index/')
                                                    for content_index in content_productid]  #替换url
        url_list.extend(content_url) #将content_url里的url迭代写入url_list

        ###积木盒子的列表页跳转至详细页时，会有不同的链接，并且该链接再挖掘就能回到第一种链接，以下为第二种链接###
        content_productid2 = re.findall('<a href=\"/Project/ProjectSet/'r'[\S]*', content) #匹配href下的链接信息
        content_url2 = [content_index2.replace('<a href="/Project/ProjectSet/',
                                                     'https://www.jimubox.com/Project/ProjectSet/')
                                                    for content_index2 in content_productid2]  #替换url
        content_url2_1 = [content_index2_1.replace('\"',
                                                 '')
                                                for content_index2_1 in content_url2]  #替换链接最后一个“
        #for循环开始
        for j in range(0, len(content_url2_1)):
            wp2 = urllib2.urlopen(content_url2_1[j])
            content2 = wp2.read()
            content_productid2_2 = re.findall('/Project/Index/'r'\d{5}', content2)
            content_url2_2 = [content_index2_2.replace('/Project/Index/',
                                                        'https://www.jimubox.com/Project/Index/')
                                                        for content_index2_2 in content_productid2_2]
            url_list.extend(content_url2_2) #迭代添加url_list元素
    #url写入文件
    #fp = open("content.txt",'a')
    #fp.write(url_list)
    #写入productid位置
    #fp = open("content_index.txt",'a')
    #fp.write(str(url_list2) + '\n')

        #for 循环结束

    #for循环结束

    start_urls = set(url_list) #start_urls赋值,并去重

    #print url_list
    #print url_list2


    def parse(self, response):
        item = JimuheziItem()
        sel = Selector(response)
        #item['link'] = sel.xpath('//a[@class=\"viewBtn\"]/@href').extract()
        #title1 = title[0]
        #title2 = title1.extract().split(",")[1].split("-")[0]
        #item['name'] = sel.xpath('//title/text()').extract()[0].split("-")[0]
        name1 = sel.xpath('//div[@class=\"project-title\"]/h2/span/text()').extract()[0]
        name2 = sel.xpath('//div[@class=\"project-title\"]/h2/text()').extract()[1].strip()
        item['name'] = name1 + name2
        item['link'] = response.url
        amount = sel.xpath('//ul[@class=\"inline\"]/li/text()').extract()[7].strip()
        unit_amount = sel.xpath('//span[@class=\"unit\"]/text()').extract()[2]
        item['amount'] = amount + unit_amount
        item['min_amount'] = ''
        item['income_rate'] = sel.xpath('//span[@class=\"data-tips\"]/span/text()').extract()[0].strip()
        term = sel.xpath('//ul[@class=\"inline\"]/li/span/text()').extract()[-4].strip()
        unit_term = sel.xpath('//span[@class=\"unit\"]/text()').extract()[1]
        item['term'] = term + unit_term
        item['area'] = sel.xpath('//div[@class=\"span6\"]/dl/dd/text()').extract()[-7].strip()
        transfer_claim = \
            sel.xpath('//div[@class=\"row-fluid\"]/div[@class=\"span10\"]/dl[@class=\"dl-horizontal\"]/dd/text()').extract()
        if transfer_claim:
            item['transfer_claim'] = transfer_claim[0].strip()
        else:
            item['transfer_claim'] = ''
        item['repay_type'] = sel.xpath('//p[@class=\"project-attribute\"]/span/text()').extract()[2].strip()
        item['reward'] = ''
        protect_mode = sel.xpath(u'//a[@title=\"点击查看担保公司信息\"]/text()').extract()
        if protect_mode:
            item['protect_mode'] = protect_mode[0]
        else:
            item['protect_mode'] = ''#
        item['description'] = sel.xpath('//p[@class=\"project-description\"]/text()').extract()[0].strip()
        process = sel.xpath('//div[@class=\"status-container\"]/div/span/text()').extract()
        if process:
            item['process'] = process[0]
        else:
            item['process'] = '100'# 100% 会显示为空，并有一个满的图标
        #[0].encode('utf-8')
        #[n.encode('utf-8') for n in title]

        yield item
