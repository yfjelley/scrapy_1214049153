#! /bin/bash
###########################
#    导入必须环境变量     #
###########################
. /root/.bash_profile
###########################
#        参数赋值         #
###########################
MYSQLHOST=ddbid2015.mysql.rds.aliyuncs.com
USER=scrapy
PASSWORD=ddbid_mysql1243
CRAWL_PATH=/usr/scrapy/crawl
SQL_PATH=/usr/scrapy/sqlscript
SPIDER_DOC=wangdaizhijia
SPIDER_NAME=wangdaizhijia
SQLSCRIPT=platform_info_daily
###########################
#         程序开始        #
###########################
START_TIME=`date +'%Y-%m-%d %H:%M:%S'`
echo "$START_TIME 开始运行爬虫----------$SPIDER_NAME---------------------------------------"
cd $CRAWL_PATH/$SPIDER_DOC
scrapy crawl $SPIDER_NAME
sleep 10
count_sql=`mysql -h$MYSQLHOST -u$USER -p$PASSWORD -e"
select count(*) from ddbid_db.temp_platform_info_daily;
quit"`
count=`echo $count_sql|awk '{print $2}'`
echo "temp_subject_$SQLSCRIPT抓取$count条数据"
END_TIME=`date +'%Y-%m-%d %H:%M:%S'`
echo "$END_TIME 爬取结束-------------$SPIDER_NAME---------------------------------------"
mysql -h$MYSQLHOST -u$USER -p$PASSWORD < $SQL_PATH/$SQLSCRIPT.sql
