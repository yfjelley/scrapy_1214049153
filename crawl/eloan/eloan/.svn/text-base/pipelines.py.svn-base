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

class EloanPipeline(object):
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
        query_delete = self.dbpool.runInteraction(self.deleteData) #清空数据


    def process_item(self, item, spider):
        print spider
        # run db query in thread pool
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)
        return item

    def deleteData(self, tx):  #定义清空表函数
        tx.execute("delete from temp_subject_el")

    def _conditional_insert(self, tx, item):
        if item.get('name'):
            tx.execute(\
                "insert into temp_subject_el\
                (name,\
                 platform_id,\
                 link,\
                 amount,\
                 income_rate,\
                 term,\
                 repay_type,\
                 publish_time,\
                 area,\
                 reward,\
                 protect_mode,\
                 description,\
                 process,\
                 transfer_claim,\
                 min_amount\
                 )\
                values ( %s, '7', %s, %s, %s, %s, %s, sysdate(), %s, %s, %s, %s, %s,%s,%s)",
                (

                 item['name'],
                 item['link'],
                 item['amount'],
                 item['income_rate'],
                 item['term'],
                 item['repay_type'],
                 item['area'],
                 item['reward'],
                 item['protect_mode'],
                 item['description'],
                 item['process'],
                 item['transfer_claim'],
                 item['min_amount']



                #item['amount']
                )
                    )

    def handle_error(self, e):
        log.err(e)


        # -*- coding: utf-8 -*-

