#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from youli.items import YouliItem
import urllib
import urllib2
import os
import re
import httplib

class TianyanSpider(CrawlSpider):
    name = 'youli'
    allowd_domain = ['yooli.com']
    download_delay = 3  #访问间隔秒数
    url1 = ['http://www.yooli.com/dingcunbao/page/'+str(x)+'.html' for x in range(1,10)]
    url2 = ['http://www.yooli.com/yuexitong/page/'+str(x)+'.html' for x in range(1,10)]
    url1.extend(url2)

    start_urls = url1
    print start_urls

    rules = (
        Rule(SgmlLinkExtractor(allow=('/dingcunbao/detail.*\.html', )),
             callback='parse_page', follow=True),
        Rule(SgmlLinkExtractor(allow=('/dingcunbaoV/detail.*\.html', )),
             callback='parse_page', follow=True),
        Rule(SgmlLinkExtractor(allow=('/yuexitong/detail.*\.html', )),
             callback='parse_page2', follow=True),
    )



    def parse_page(self, response):
        item = YouliItem()
        sel = Selector(response)
        #item['link'] = sel.xpath('//a[@class=\"viewBtn\"]/@href').extract()
        #title1 = title[0]
        #title2 = title1.extract().split(",")[1].split("-")[0]
        item['name'] = sel.xpath('//div[@class=\"head\"]/h2/text()').extract()[0]
        item['link'] = response.url
        item['amount'] = sel.xpath('//dl[@class=\"f\"]/dd/em/text()').extract()[0]
        item['min_amount'] = ''

        income_rate1 = sel.xpath('//div[@class=\"profit\"]/dl/dd/em/text()').extract()[1]
        income_rate2 = sel.xpath('//span[@class=\"flot\"]/text()').extract()[0]
        item['income_rate'] = income_rate1 + income_rate2

        term1 = sel.xpath('//div[@class=\"profit\"]/dl/dd/em/text()').extract()[2].strip()
        term2 = sel.xpath('//div[@class=\"profit\"]/dl/dd/text()').extract()[3].strip()
        item['term'] = term1 + term2

        item['area'] = ''
        item['transfer_claim'] = ''
        item['repay_type'] = ''
        item['reward'] = ''

        item['protect_mode'] = sel.xpath('//span[@class=\"vouch\"]/text()').extract()[0]
        item['description'] = sel.xpath('//div[@class=\"table-plan\"]/table/tr/td/text()').extract()[3].strip()
        item['process'] = sel.xpath('//div[@class=\"per\"]/@data-rel').extract()[0]

        #[0].encode('utf-8')
        #[n.encode('utf-8') for n in title]

        yield item

    def parse_page2(self, response):
        item = YouliItem()
        sel = Selector(response)
        item['name'] = sel.xpath('//div[@class=\"head\"]/h2/text()').extract()[0].strip()
        item['link'] = response.url
        item['amount'] = sel.xpath('//dl[@class=\"f\"]/dd/em/text()').extract()[0]
        item['min_amount'] = ''

        income_rate1 = sel.xpath('//div[@class=\"profit\"]/dl/dd/em/text()').extract()[1]
        income_rate2 = sel.xpath('//span[@class=\"flot\"]/text()').extract()[0]
        item['income_rate'] = income_rate1 + income_rate2

        term1 = sel.xpath('//div[@class=\"profit\"]/dl/dd/em/text()').extract()[2].strip()
        term2 = sel.xpath('//div[@class=\"profit\"]/dl/dd/text()').extract()[3].strip()
        item['term'] = term1 + term2

        item['area'] = ''
        item['transfer_claim'] = ''
        item['repay_type'] = ''
        item['reward'] = ''

        item['protect_mode'] = sel.xpath('//span[@class=\"vouch\"]/text()').extract()[0]
        item['description'] = sel.xpath('//div[@class=\"explain\"]/text()').extract()[1].strip()
        item['process'] = sel.xpath('//div[@class=\"per\"]/@data-rel').extract()[0]

        #[0].encode('utf-8')
        #[n.encode('utf-8') for n in title]

        yield item