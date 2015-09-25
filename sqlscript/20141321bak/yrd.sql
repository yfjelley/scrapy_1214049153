
/*
name		    :宜人贷
script file	    :yrd.sql
author		    :roger
created		    :2014-12-16
modified		:2014-12-16
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
where not exists(select 1 from temp_subject_yrd t where t.link = t1.link)
and t1.platform_id = 16
;

#更新未抽取到的已经结标的进度为100%
update t_subject
set process = 100
where not exists(select 1 from temp_subject_yrd t1 where t1.link = t_subject.link)
and t_subject.platform_id = 16
;

/*2014-12-25更新*/
#历史表已经存在100%的标的无需进数
delete from temp_subject_yrd 
 where process = 100 
	 and exists(select 1 from t_subject_his t1 where t1.link = temp_subject_yrd.link )
;

#更新change_his表中进度大于抓取标的进度的数据
update t_subject_change_his t1
	 set t1.valid_status = 0
 where exists(select 1 from temp_subject_yrd t, t_subject t2
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
	from temp_subject_yrd t
 inner join t_subject t1 on t1.link = t.link and t1.process <> replace(t.process, '%', '')  #注意此处process逻辑要修改
;

#记录进度变更历史，process取数逻辑要修改，处理temp表进度不是100，而his表进度是100的问题
insert into t_subject_change_his(subject_id,process_before,process_after,change_time)
select t1.id,
			 t1.process process_before,
			 t.process process_after,
			 sysdate()
	from temp_subject_yrd t
 inner join t_subject_his t1 on t1.link = t.link and t1.process <> replace(t.process, '%', '')  #注意此处process逻辑要修改
;

#插入进度由100变为小于100的数据
insert into t_subject(id,platform_id,link,name,amount,min_amount,income_rate,term,type,area,transfer_claim,repay_type,publish_time,end_time,reward,protect_mode,description,process)
select t1.id,
			 t.platform_id,
			 t.link,
			 t.name,
			 replace(t.amount,',','') amount,
			 case when t.min_amount is null then 0 else t.min_amount end min_amount,
			 replace(t.income_rate, '%', ''),
			 t.term,
			 case when t.name like '%车%' and t.name like '%周转%' then '车贷'
						when t.name like '%房产%' and t.name like '%抵%' then '房贷'
						when t.name like '%企业%' then '企业贷'
						else '个人信用贷' end type,
			 t.area,
			 case t.transfer_claim when null then 'N' when '' then 'N' else 'Y' end transfer_claim,
			 t.repay_type ,
			 t.publish_time,
			 case when replace(t.process, '%', '') = 100 then sysdate() else null end end_time,
			 t.reward,
			 case when t.protect_mode like '%本息担保%' then '第三方担保' else t.protect_mode end protect_mode,
			 case when t.description like '%企业%' then '企业贷' else '个人信用贷' end description,
		   replace(t.process, '%', '')
	from temp_subject_yrd t
 inner join t_subject_his t1 on t1.link = t.link
;

#删除历史表中进度为100%，但抓取的进度小于100%的标的
delete from t_subject_his
 where exists(select 1 from temp_subject_yrd t1 where t1.link = t_subject_his.link and t1.process <> 100)
;
/*2014-12-25更新结束*/

#宜人贷
replace into t_subject(id,platform_id,link,name,amount,min_amount,income_rate,term,type,area,transfer_claim,repay_type,publish_time,end_time,reward,protect_mode,description,process,create_time)
select t1.id,
			 t.platform_id,
			 t.link,
			 t.name,
			 replace(t.amount,',','') amount,
			 case when t.min_amount is null then 0 else t.min_amount end min_amount,
			 replace(t.income_rate, '%', ''),
			 t.term,
			 case when t.name like '%车%' and t.name like '%周转%' then '车贷' 
						when t.name like '%房产%' and t.name like '%抵%' then '房贷' 
						when t.name like '%企业%' then '企业贷' 
						else '个人信用贷' end type,
			 t.area,
			 case t.transfer_claim when null then 'N' when '' then 'N' else 'Y' end transfer_claim,
			 t.repay_type ,
			 t.publish_time,
			 case when replace(t.process, '%', '') = 100 then sysdate() else null end end_time,
			 t.reward,
			 case when t.protect_mode like '%本息担保%' then '第三方担保' else t.protect_mode end protect_mode,
			 case when t.description like '%企业%' then '企业贷' else '个人信用贷' end description,
		   replace(t.process, '%', ''),
		   t1.create_time
	from temp_subject_yrd t
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
	 and t1.platform_id = 16
;

#100%标的进入历史表
insert into t_subject_his(id,platform_id,link,name,amount,min_amount,income_rate,term,type,area,transfer_claim,repay_type,publish_time,end_time,reward,protect_mode,description,process)
select id,platform_id,link,name,amount,min_amount,income_rate,term,type,area,transfer_claim,repay_type,publish_time,end_time,reward,protect_mode,description,process
	from t_subject t1
 where t1.platform_id = 16
	 and t1.process = 100
;

#删除主表中100%的标的
delete from t_subject
 where platform_id = 16
	 and process = 100
;