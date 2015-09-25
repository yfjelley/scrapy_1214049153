
/*
name		    :陆金所
script file	:ljs.sql
author		  :daniel
created		  :2014-12-9
modified		:2014-12-11
desc		    :
*/

#指定数据库名称
use mysql;

#没有抓取到的数据自动结标,进入历史变更表
insert into t_subject_change_his(subject_id,process_before,process_after,change_time)
select t1.id,
			 t1.process process_before,
			 100 process_after,
			 sysdate()
	from t_subject t1
 where t1.platform_id = 1
	 and not exists(select 1 from temp_subject_ljs t where t.link = t1.link)
;

#没有抓取到的数据自动结标,更新为100%
update t_subject t1 
	 set t1.process = 100
 where t1.platform_id = 1
	 and not exists(select 1 from temp_subject_ljs t where t.link = t1.link)
;

/*2014-12-25更新*/
#历史表已经存在100%的标的无需进数
delete from temp_subject_ljs 
 where process = 100 
	 and exists(select 1 from t_subject_his t1 where t1.link = temp_subject_ljs.link )
;

#更新change_his表中进度大于抓取标的进度的数据
update t_subject_change_his t1
	 set t1.valid_status = 0
 where exists(select 1 from temp_subject_ljs t, t_subject t2
											where t2.link = t.link
											  and t2.id = t1.subject_id
												and t1.process_after > replace(t.process, '%', '') ) #注意此处process逻辑要修改
;

#记录进度变更历史，process取数逻辑要修改
insert into t_subject_change_his(subject_id,process_before,process_after,change_time)
select t1.id,
			 t1.process process_before,
			 t.process process_after,
			 sysdate()
	from temp_subject_ljs t
 inner join t_subject t1 on t1.link = t.link and t1.process <> replace(t.process, '%', '')  #注意此处process逻辑要修改
;

#记录进度变更历史，process取数逻辑要修改，处理temp表进度不是100，而his表进度是100的问题
insert into t_subject_change_his(subject_id,process_before,process_after,change_time)
select t1.id,
			 t1.process process_before,
			 t.process process_after,
			 sysdate()
	from temp_subject_ljs t
 inner join t_subject_his t1 on t1.link = t.link and t1.process <> replace(t.process, '%', '')  #注意此处process逻辑要修改
;

#插入进度由100变为小于100的数据
insert into t_subject(id,platform_id,link,name,amount,min_amount,income_rate,term,type,area,transfer_claim,repay_type,publish_time,end_time,reward,protect_mode,description,process)
select t1.id,
			 t.platform_id,
			 t.link,
			 t.name,
			 replace(t.amount, ',', ''),
			 case t.min_amount when '' then null else replace(t.min_amount, ',', '') end min_amount,
			 replace(t.income_rate, '%', '') income_rate,
			 case when t.term like '%月%' then replace(t.term, '个月', '') else t.term end as term,
			 '平台产品' type,
			 t.area,
			 case t.transfer_claim when null then 'N' when '' then 'N' else 'Y' end transfer_claim,
			 t.repay_type,
			 t.publish_time,
			 case when replace(t.process, '%', '') = '100' then sysdate() else null end end_time,
			 t.reward,
			 t.protect_mode,
			 t.description,
			 replace(t.process, '%', '') process
	from temp_subject_ljs t
 inner join t_subject_his t1 on t1.link = t.link
;

#删除历史表中进度为100%，但抓取的进度小于100%的标的
delete from t_subject_his
 where exists(select 1 from temp_subject_ljs t1 where t1.link = t_subject_his.link and t1.process <> 100)
;
/*2014-12-25更新结束*/

replace into t_subject(id,platform_id,link,name,amount,min_amount,income_rate,term,type,area,transfer_claim,repay_type,publish_time,end_time,reward,protect_mode,description,process,create_time)
select t1.id,
			 t.platform_id,
			 t.link,
			 t.name,
			 replace(t.amount, ',', ''),
			 case t.min_amount when '' then null else replace(t.min_amount, ',', '') end min_amount,
			 replace(t.income_rate, '%', '') income_rate,
			 case when t.term like '%月%' then replace(t.term, '个月', '') else t.term end as term,
			 '平台产品' type,
			 t.area,
			 case t.transfer_claim when null then 'N' when '' then 'N' else 'Y' end transfer_claim,
			 t.repay_type,
			 t.publish_time,
			 case when replace(t.process, '%', '') = '100' then sysdate() else null end end_time,
			 t.reward,
			 t.protect_mode,
			 t.description,
			 replace(t.process, '%', '') process,
			 t1.create_time
	from temp_subject_ljs t
	left join t_subject t1 on t1.link = t.link
;


#新标的写入进度变更历史
insert into t_subject_change_his(subject_id,process_before,process_after,change_time)
select t1.id,
			 null,
			 t1.process process_after,
			 sysdate()
	from t_subject t1
 where not exists(select 1 from t_subject_change_his t2 where t2.subject_id = t1.id) 
	 and t1.platform_id = 1
;

#100%标的进入历史表
insert into t_subject_his(id,platform_id,link,name,amount,min_amount,income_rate,term,type,area,transfer_claim,repay_type,publish_time,end_time,reward,protect_mode,description,process)
select id,platform_id,link,name,amount,min_amount,income_rate,term,type,area,transfer_claim,repay_type,publish_time,end_time,reward,protect_mode,description,process
	from t_subject t1
 where t1.platform_id = 1
	 and t1.process = 100
;

#删除主表中100%的标的
delete from t_subject
 where platform_id = 1
	 and process = 100
;
