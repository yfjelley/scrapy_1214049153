# -*- coding: utf-8 -*-

# Scrapy settings for itouzi project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'paipaidai'

SPIDER_MODULES = ['paipaidai.spiders']
NEWSPIDER_MODULE = 'paipaidai.spiders'
ITEM_PIPELINES={
    'paipaidai.pipelines.PaipaidaiPipeline':400,
}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tianyan (+http://www.yourdomain.com)'
