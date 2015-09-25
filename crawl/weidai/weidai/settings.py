# -*- coding: utf-8 -*-

# Scrapy settings for weidai project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'weidai'

SPIDER_MODULES = ['weidai.spiders']
NEWSPIDER_MODULE = 'weidai.spiders'
ITEM_PIPELINES={
    'weidai.pipelines.WeidaiPipeline':400,
}

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
    'weidai.middlewares.ProxyMiddleware': 100,
}

#DOWNLOAD_MIDDLEWARES = {
 #   #'weidai.UserAgent.RotateUserAgentMiddleware':100,
  #  'weidai.middlewares.ProxyMiddleware':100,
   # 'scrapy.contrib.downloadermidffleware.httpproxy.HttpProxyMiddleware':110,
#}
#COOKIES_ENABLES=False
#download_delay = 5
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'weidai (+http://www.yourdomain.com)'

#LOG_ENABLED = True
#LOG_ENCODING = 'utf-8'
#LOG_LEVEL = 'DEBUG'
#LOG_STDOUT = False