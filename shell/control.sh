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
CONFIG_PATH=/usr/scrapy/config
SHELL_PATH=/usr/scrapy/shell
LOG_PATH=/usr/scrapy/log
###########################
#         程序开始        #
###########################
#判断前一次程序是否完成
num=`ps -ef|grep run_sql.sh|grep -v grep|wc -l`
if [ $num -ne 0 ]; then
for pid in `ps -ef|grep run_sql.sh|grep -v grep|awk '{print $2}'`
do
kill -9 $pid  #kill掉还在运行的进程
done
for pid1 in `ps -ef|grep 'scrapy crawl'|grep -v grep|awk '{print $2}'`
do
kill -9 $pid1  #kill掉还在运行的进程
done
fi
sleep 30
mysql=`ps -ef|grep 'mysql -hddbid2015'|grep -v grep|wc -l`  #手动修改mysql的host和usr
while [ $mysql -ne 0 ]
do
sleep 10
mysql=`ps -ef|grep 'mysql -hddbid2015'|grep -v grep|wc -l`
done
#-----------------------------------------------------------------------------------------------------------
ST_TIME=`date +'%Y-%m-%d %H:%M:%S'`
#删除临时表数据
for table_name in `cat $CONFIG_PATH/list.table`
do
mysql -h$MYSQLHOST -u$USER -p$PASSWORD -e"
use ddbid_db;
delete from ddbid_db.temp_subject_$table_name;
quit"
done
#-------------------------------------------------------------------------------------------------------------
#爬虫开始抓数
echo "INFO: $ST_TIME-------本批次抓取开始-------------"
LOG_TIME=`date +"%Y%m%d%H%M%S"`
while read line
do
spider_doc=`echo $line|awk '{print $1}'`
spider_name=`echo $line|awk '{print $2}'`
START_TIME=`date +'%Y-%m-%d %H:%M:%S'`
echo "INFO: $START_TIME 调起SPIDER-->$spider_name"
sh $SHELL_PATH/run_sql.sh $spider_doc $spider_name > $LOG_PATH/$LOG_TIME$spider_name.log 2>&1 & 
RUNNING_COUNT=`ps -ef|grep 'run_sql.sh'|grep -v grep|wc -l`
while [ $RUNNING_COUNT -ge 30 ] #控制并发数量
do
sleep 20
RUNNING_COUNT=`ps -ef|grep 'run_sql.sh'|grep -v grep|wc -l`
echo "已经有$RUNNING_COUNT个程序在工作，请稍后........."
done
continue
done<$CONFIG_PATH/list.spider
IS_FINISHED=`ps -ef|grep 'run_sql.sh'|grep -v grep|wc -l` #判断所有程序是否运行完成
while [ $IS_FINISHED -ne 0 ]
do
sleep 20
IS_FINISHED=`ps -ef|grep 'run_sql.sh'|grep -v grep|wc -l`
echo "还有$IS_FINISHED个程序在工作中，请稍后........."
done
END_TIME=`date +'%Y-%m-%d %H:%M:%S'`
echo "INFO: $END_TIME-------本批次抓取结束-------------"
#----------------------------------------------------------------------------------------------------------------
#对抓取后的数据做逻辑处理
LJ_STIME=`date +'%Y-%m-%d %H:%M:%S'`
echo "$LJ_STIME:开始逻辑处理进入正式表-------------------------------------------"
for SQLSCRIPT in `cat $CONFIG_PATH/list.table`
do
count_sql=`mysql -h$MYSQLHOST -u$USER -p$PASSWORD -e"
select count(*) from ddbid_db.temp_subject_$SQLSCRIPT;
quit"`
count=`echo $count_sql|awk '{print $2}'`
if [ $count -ne 0 ]; then
echo "temp_subject_$SQLSCRIPT抓取$count条数据"
mysql -h$MYSQLHOST -u$USER -p$PASSWORD < $SQL_PATH/$SQLSCRIPT.sql
else
echo "temp_subject_$SQLSCRIPT没有抓取到数据，Erro"
fi
continue
done
`mysql -h$MYSQLHOST -u$USER -p$PASSWORD -e"
use ddbid_db;
update t_subject
set month_rate=income_rate/12,
    ten_thousand_revenue=income_rate/12*term/100*10000,
    finish_amount=amount*process/100,
    allow_amount=amount-(amount*process/100),
    random_rank=rand()*100000000000,
    term_name = case when term < 1 then round(term * 30) else term end ,
    term_unit = case when term < 1 then '天' else '个月' end ;
quit"`
LJ_ETIME=`date +'%Y-%m-%d %H:%M:%S'`
echo "$LJ_ETIME:逻辑处理结束---------------------------------------"
