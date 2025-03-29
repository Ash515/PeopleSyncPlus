select * from empinfo
select * from leaverequest
insert into skillset(empid,skill,rating) values(5002,'C++',10)

insert into empinfo(empid,emppass,name,phno,seating,destination,team,manager,org,doj,officelocation) values(5001,'a@123','Ashwin Kumar R',7358228847,'PL90','Software Developer Trainer','Human Resource','5000','Zoho Corporation','15/12/2021','Chennai')

DELETE from empinfo where empid='5001'

insert into managers(empid,name,reporteescount,team) values(3246,'Sohail MI',83,'Human Resource')

update hr set manager=5001 where id=5002

insert into managers(empid,name,reporteescount,team) values(2020,'Guru Moorthi K',6,'Human Resource')
insert into hr(id,name,destination,seating,extension,manager,team,phno,org,doj,officelocation) values(3246,'Sohail M','Manager-HR','S9U8','5678','2321','Human Resource',7871386734,'Zoho Corporation','20/2/2019','Chennai')

select * from hr
select * from managers

ALTER TABLE hr
add COLUMN manager BIGINT;

insert into newhires(empid,name,team,doj) values(5004,'Mathew L','Human Resource','16/1/2023')

select * from newhires

		insert into holidays(name,date,restricted) values('Independance Day','15 Aug','Holiday')

update holidays set date='16 Jan' where date ='16/01/2023'

select * from skillset 

select * from goals
CREATE TABLE goalset(
	empid BIGINT,
   gid SERIAL,
   taskname VARCHAR,
	description VARCHAR,
	startdate VARCHAR,
	duedate VARCHAR,
	priority VARCHAR,
	status VARCHAR
);


select * from skillset
select * from empinfo
select * from goalset
insert into goalset(empid,taskname,description,startdate,duedate,priority,status) VALUES(5002,'makeentry','2/03/2023','3/3/2023','High','Open')

select * from attendancelog

select * from empinfo

delete checkin from empinfo where empid=5001

ALTER TABLE empinfo
DROP COLUMN checkin;
 
CREATE TABLE quicklinks (
    linkid text
);

select * from quicklinks;

insert into quicklinks(linkid,date,link,linkname) values(02,'April 30,2023','https://www.yahoo.com/','Yahoo Link')


DELETE from quicklinks 