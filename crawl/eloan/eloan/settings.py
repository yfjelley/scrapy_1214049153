# -*- coding: utf-8 -*-

# Scrapy settings for eloan project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'eloan'

SPIDER_MODULES = ['eloan.spiders']
NEWSPIDER_MODULE = 'eloan.spiders'
ITEM_PIPELINES={
    'eloan.pipelines.EloanPipeline':400,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'eloan (+http://www.yourdomain.com)'
