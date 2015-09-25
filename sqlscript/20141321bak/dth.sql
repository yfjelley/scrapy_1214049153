
/*
name		    :大同行
script file	    :dth.sql
author		    :roger
created		    :2014-12-17
modified		:2014-12-17,  2014-12-25 by daniel
desc		    :
*/

#指定数据库名称
use mysql;

#记录未抽取到得已结标的进度为100%的标的
insert into t_subject_change_his(subject_id,process_before,process_after,change_time)
select t1.id,
			 t1.process process_before,
			 100 process_after,
			 sysdate()
	from t_subject t1
where not exists(select 1 from temp_subject_dth t where t.link = t1.link)
 and t1.platform_id = 15
;

#更新未抽取到的已经结标的进度为100%
update t_subject
set process = 100
where not exists(select 1 from temp_subject_dth t1 where t1.link = t_subject.link)
 and t_subject.platform_id = 15
;

/*2014-12-25更新*/
#历史表已经存在100%的标的无需进数
delete from temp_subject_dth 
 where process = 100 
	 and exists(select 1 from t_subject_his t1 where t1.link = temp_subject_dth.link )
;

#更新change_his表中进度大于抓取标的进度的数据
update t_subject_change_his t1
	 set t1.valid_status = 0
 where exists(select 1 from temp_subject_dth t, t_subject t2
											where t2.link = t.link
											  and t2.id = t1.subject_id
												and t1.process_after > round(t.process,2) ) #注意此处process逻辑要修改
;

#记录进度变更历史，process取数逻辑要修改
insert into t_subject_change_his(subject_id,process_before,process_after,change_time)
select t1.id,
			 t1.process process_before,
			 t.process process_after,
			 sysdate()
	from temp_subject_dth t
 inner join t_subject t1 on t1.link = t.link and t1.process <> round(t.process,2)  #注意此处process逻辑要修改
;

#记录进度变更历史，process取数逻辑要修改，处理temp表进度不是100，而his表进度是100的问题
insert into t_subject_change_his(subject_id,process_before,process_after,change_time)
select t1.id,
			 t1.process process_before,
			 t.process process_after,
			 sysdate()
	from temp_subject_dth t
 inner join t_subject_his t1 on t1.link = t.link and t1.process <> round(t.process,2)  #注意此处process逻辑要修改
;

#插入进度由100变为小于100的数据
insert into t_subject(id,platform_id,link,name,amount,min_amount,income_rate,term,type,area,transfer_claim,repay_type,publish_time,end_time,reward,protect_mode,description,process)
select t1.id,
			 t.platform_id,
			 t.link,
			 t.name,
			 case when t.amount like '%万%' then replace(t.amount,'万','') * 10000
			      when t.amount like '%千%' then replace(t.amount,'千','') * 1000
			 end amount,
			 case when t.min_amount is null then 0 else t.min_amount end min_amount,
			 replace(t.income_rate, '%', ''),
			 case when t.term like '%月%' then replace(t.term,'个月','')
			      when t.term like '%天%' then replace(t.term,'天','') / 30
			 end term,
			 case when t.name like '%企业%' or t.name like '%厂%' or t.name like '%公司%' then '企业贷'
				  when t.name like '%房产%' and t.name like '%抵%' then '房贷'
			      else '个人资产抵押' end type,
			 t.area,
			 case t.transfer_claim when null then 'N' when '' then 'N' else 'Y' end transfer_claim,
			 t.repay_type ,
			 t.publish_time,
			 case when replace(t.process, '%', '') = 100 then sysdate() else null end end_time,
			 t.reward,
			 case when t.protect_mode is not null then '公司担保' else '' end protect_mode,
			 t.description,
		   round(t.process,2) process
	from temp_subject_dth t
 inner join t_subject_his t1 on t1.link = t.link
;

#删除历史表中进度为100%，但抓取的进度小于100%的标的
delete from t_subject_his
 where exists(select 1 from temp_subject_dth t1 where t1.link = t_subject_his.link and t1.process <> 100)
;
/*2014-12-25更新结束*/

#温州贷
replace into t_subject(id,platform_id,link,name,amount,min_amount,income_rate,term,type,area,transfer_claim,repay_type,publish_time,end_time,reward,protect_mode,description,process,create_time)
select t1.id,
			 t.platform_id,
			 t.link,
			 t.name,
			 case when t.amount like '%万%' then replace(t.amount,'万','') * 10000
			      when t.amount like '%千%' then replace(t.amount,'千','') * 1000
			 end amount,
			 case when t.min_amount is null then 0 else t.min_amount end min_amount,
			 replace(t.income_rate, '%', ''),
			 case when t.term like '%月%' then replace(t.term,'个月','')
			      when t.term like '%天%' then replace(t.term,'天','') / 30
			 end term,
			 case when t.name like '%企业%' or t.name like '%厂%' or t.name like '%公司%' then '企业贷' 
				  when t.name like '%房产%' and t.name like '%抵%' then '房贷' 		
			      else '个人资产抵押' end type,
			 t.area,
			 case t.transfer_claim when null then 'N' when '' then 'N' else 'Y' end transfer_claim,
			 t.repay_type ,
			 t.publish_time,
			 case when replace(t.process, '%', '') = 100 then sysdate() else null end end_time,
			 t.reward,
			 case when t.protect_mode is not null then '公司担保' else '' end protect_mode,
			 t.description,
		   round(t.process,2) process,
		   t1.create_time
	from temp_subject_dth t
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
	 and t1.platform_id = 15
;

#100%标的进入历史表
insert into t_subject_his(id,platform_id,link,name,amount,min_amount,income_rate,term,type,area,transfer_claim,repay_type,publish_time,end_time,reward,protect_mode,description,process)
select id,platform_id,link,name,amount,min_amount,income_rate,term,type,area,transfer_claim,repay_type,publish_time,end_time,reward,protect_mode,description,process
	from t_subject t1
 where t1.platform_id = 15
	 and t1.process = 100
;

#删除主表中100%的标的
delete from t_subject
 where platform_id = 15
	 and process = 100
;