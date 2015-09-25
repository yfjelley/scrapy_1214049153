# -*- coding: utf-8 -*-

# Scrapy settings for yirendai project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'yirendai'

SPIDER_MODULES = ['yirendai.spiders']
NEWSPIDER_MODULE = 'yirendai.spiders'
ITEM_PIPELINES={
    'yirendai.pipelines.YirendaiPipeline':400,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'yirendai (+http://www.yourdomain.com)'
