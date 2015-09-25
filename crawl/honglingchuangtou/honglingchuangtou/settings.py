# -*- coding: utf-8 -*-

# Scrapy settings for lujinsuo project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'honglingchuangtou'

SPIDER_MODULES = ['honglingchuangtou.spiders']
NEWSPIDER_MODULE = 'honglingchuangtou.spiders'
ITEM_PIPELINES={
    'honglingchuangtou.pipelines.HonglingchuangtouPipeline':400,
}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tianyan (+http://www.yourdomain.com)'
