# -*- coding: utf-8 -*-

# Scrapy settings for lujinsuo project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'niwodai'

SPIDER_MODULES = ['niwodai.spiders']
NEWSPIDER_MODULE = 'niwodai.spiders'
ITEM_PIPELINES={
    'niwodai.pipelines.NiwodaiPipeline':400,
}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tianyan (+http://www.yourdomain.com)'
