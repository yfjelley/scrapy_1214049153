#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
import urllib
from rongjinsuo.items import RongjinsuoItem
import urllib2
import os
import re



class RONGJINSUOspider(CrawlSpider):
    name = 'rongjinsuo'
    allowd_domain = ['rongjinsuo.com']
    #删除文件start
    #if (os.path.exists("content.txt")): os.remove("content.txt")
    #if (os.path.exists("content_index.txt")): os.remove("content_index.txt")
    #删除文件end

    url_list = []; #初始化url_list数组

    download_delay = 3  #访问间隔秒数

    #for循环开始：访问产品列表的10个页面
    for i in range(1,10) :
        url_js = 'http://www.rongjinsuo.com/invest/index/sort/asc/p/' + str(i) + '.html'
        #print(url_js)
        wp = urllib.urlopen(url_js) #打开连接
        content = wp.read() #获取页面内容
        content_productid = re.findall('div class=\"okay_lf\"><a href=\"/invest/'r'\d{4}''.html', content) #获取 （"productid":） 及其后6位的id
        content_url = [content_index.replace('div class=\"okay_lf\"><a href=\"',
                                                     'http://www.rongjinsuo.com')
                                                    for content_index in content_productid]  #替换url

        #url写入文件
        #fp = open("content.txt",'a')
        #fp.write(content)
        #写入productid位置
        #fp = open("content_index.txt",'a')
        #fp.write(str(content_url) + '\n')
        url_list.extend(content_url) #将content_url里的url迭代写入url_list
    #for循环结束

    start_urls = url_list #start_urls赋值
    #print(start_urls)

    def parse(self, response):
        item = RongjinsuoItem()
        sel = Selector(response)
        #item['link'] = sel.xpath('//a[@class=\"viewBtn\"]/@href').extract()
        #title1 = title[0]
        #title2 = title1.extract().split(",")[1].split("-")[0]
        name = sel.xpath('//title/text()').extract()[0]
        item['name'] = name.split("|")[1]
        item['link'] = response.url
        item['amount'] = sel.xpath('//div[@class=\"sbcr_con\"]/ul/li/samp/text()').extract()[0]
        #item['amount'] = amount.split(" ")[0] #截取空格钱第一个字段
        rate_text = sel.xpath('//div[@id=\"view_con_m\"]/p/text()').extract()[0]
        num = len(rate_text.split("/")[0]) + 2 #截取/前的位数
        item['income_rate'] = rate_text[6:num]
        term = sel.xpath('//div[@id=\"view_con_m\"]/p/text()').extract()[2]
        term_num = len(term)
        item['term'] = term[5:term_num]
        repay_type = sel.xpath('//div[@id=\"view_con_m\"]/p/text()').extract()[3]
        repay_num = len(repay_type)
        item['repay_type'] = repay_type[5:repay_num]
        area = sel.xpath('//div[@id=\"view_con_m\"]/p/text()').extract()[7]
        area_num = len(area)
        item['area'] = area[5:area_num]
        item['reward'] = ''
        item['protect_mode'] = ''
        item['description'] = sel.xpath('//meta[@name=\"description\"]/@content').extract()[0]
        process = sel.xpath('//p[@class=\"noheight\"]/text()').extract()
        #"https://list.lufax.com/list/productDetail?productId=" + sel.xpath('//input/text()').extract()[4]
        #[0].encode('utf-8')
        #[n.encode('utf-8') for n in title]
        #if process and process[0] <> '100.00%':
        item['process'] = process[0]
        #else:
        #   item['process'] = ''
        yield item

