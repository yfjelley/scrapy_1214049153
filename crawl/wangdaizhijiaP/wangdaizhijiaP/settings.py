# -*- coding: utf-8 -*-

# Scrapy settings for wangdaizhijiaP project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'wangdaizhijiaP'

SPIDER_MODULES = ['wangdaizhijiaP.spiders']
NEWSPIDER_MODULE = 'wangdaizhijiaP.spiders'
ITEM_PIPELINES={
    'wangdaizhijiaP.pipelines.WangdaizhijiaPPipeline':400,
    }
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'wangdaizhijiaP (+http://www.yourdomain.com)'
