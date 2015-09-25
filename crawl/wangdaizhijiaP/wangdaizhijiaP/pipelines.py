# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from scrapy import log
from twisted.enterprise import adbapi
from scrapy.http import Request
from scrapy.exceptions import DropItem
from scrapy.contrib.pipeline.images import ImagesPipeline
import time
import MySQLdb
import MySQLdb.cursors

class WangdaizhijiaPPipeline(object):
    """docstring for MySQLstor"""
    def __init__(self):

        self.dbpool = adbapi.ConnectionPool('MySQLdb', #engine
            host = 'ddbid2015.mysql.rds.aliyuncs.com',
            db = 'ddbid_db',
            user = 'scrapy',
            passwd = 'ddbid_mysql1243',
            cursorclass = MySQLdb.cursors.DictCursor,
            charset = 'utf8',
            use_unicode = True
        )
        query_delete = self.dbpool.runInteraction(self.deleteData) #清空数据,分base的爬虫在shell脚本里清空数据


    def process_item(self, item, spider):
        print spider
        # run db query in thread pool
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)
        return item

    def deleteData(self, tx):  #定义清空表函数
        tx.execute("delete from temp_platformp_info_daily")

    def _conditional_insert(self, tx, item):
        if item.get('platform_name'):
            tx.execute(\
                "insert into temp_platformp_info_daily\
                (day_id,\
                 platform_name,\
                 inv_quantity\
                 )\
                values (%s, %s, %s)",
                (
                 item['day_id'],
                 item['platform_name'],
                 #item['amount'],
                 item['inv_quantity']
                #item['amount']
                )
                    )

    def handle_error(self, e):
        log.err(e)


        # -*- coding: utf-8 -*-

