# -*- coding: utf-8 -*-

# Scrapy settings for itouzi project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'itouzi'

SPIDER_MODULES = ['itouzi.spiders']
NEWSPIDER_MODULE = 'itouzi.spiders'
ITEM_PIPELINES={
    'itouzi.pipelines.ItouziPipeline':400,
}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tianyan (+http://www.yourdomain.com)'
#which spider should use WEBKIT
WEBKIT_DOWNLOADER=['ccb']

DOWNLOADER_MIDDLEWARES = {
    'itouzi.downloader.WebkitDownloader': 543,
}

import os
os.environ["DISPLAY"] = ":0"
