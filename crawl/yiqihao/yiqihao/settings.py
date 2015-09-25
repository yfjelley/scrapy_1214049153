# -*- coding: utf-8 -*-

# Scrapy settings for nonobank project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'yiqihao'

SPIDER_MODULES = ['yiqihao.spiders']
NEWSPIDER_MODULE = 'yiqihao.spiders'
ITEM_PIPELINES={
    'yiqihao.pipelines.YiqihaoPipeline':400,
}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tianyan (+http://www.yourdomain.com)'
