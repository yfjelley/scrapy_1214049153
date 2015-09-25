
/*
name		    :平台每日数据
script file	    :platform_info_daily.sql
author		    :daniel
created		    :2014-12-24
modified		:2014-12-24
desc		    :
*/

#指定数据库名称
use ddbid_db;

replace into t_platform_info_daily(day_id, platform_id, amount, inv_quantity)
select         t.day_id,                
               t1.id,
                         round(replace(t.amount, '万元', '') * 10000, 0) amount,
                         replace(replace(t.inv_quantity, ',', ''), '人', '') inv_quantity
        from temp_platform_info_daily t
 inner join t_platform t1 on t1.name = case when t.platform_name = '翼龙贷网' then '翼龙贷' else t.platform_name end
