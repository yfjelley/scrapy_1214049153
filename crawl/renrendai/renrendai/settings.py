# -*- coding: utf-8 -*-

# Scrapy settings for renrendai project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'renrendai'

SPIDER_MODULES = ['renrendai.spiders']
NEWSPIDER_MODULE = 'renrendai.spiders'
ITEM_PIPELINES={
    'renrendai.pipelines.RenrendaiPipeline':400,
}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tianyan (+http://www.yourdomain.com)'
