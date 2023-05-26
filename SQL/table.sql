/*==============================================================*/
/* DBMS name:      Microsoft SQL Server 2017                    */
/* Created on:     5/26/2023 3:16:46 PM                         */
/*==============================================================*/


if exists (select 1
from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F')
where r.fkeyid = object_id('Comment') and o.name = 'FK_COMMENT_COMMENTIN_USER')
alter table Comment
   drop constraint FK_COMMENT_COMMENTIN_USER
go

if exists (select 1
from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F')
where r.fkeyid = object_id('Comment') and o.name = 'FK_COMMENT_HAVE_POST')
alter table Comment
   drop constraint FK_COMMENT_HAVE_POST
go

if exists (select 1
from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F')
where r.fkeyid = object_id('Follow') and o.name = 'FK_FOLLOW_FOLLOWED_USER')
alter table Follow
   drop constraint FK_FOLLOW_FOLLOWED_USER
go

if exists (select 1
from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F')
where r.fkeyid = object_id('Follow') and o.name = 'FK_FOLLOW_FOLLOWING_USER')
alter table Follow
   drop constraint FK_FOLLOW_FOLLOWING_USER
go

if exists (select 1
from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F')
where r.fkeyid = object_id('Post') and o.name = 'FK_POST_CONTAIN_BOARD')
alter table Post
   drop constraint FK_POST_CONTAIN_BOARD
go

if exists (select 1
from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F')
where r.fkeyid = object_id('Post') and o.name = 'FK_POST_POSTING_USER')
alter table Post
   drop constraint FK_POST_POSTING_USER
go

if exists (select 1
from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F')
where r.fkeyid = object_id('"Post Content"') and o.name = 'FK_POST CON_CONSIST_POST')
alter table "Post Content"
   drop constraint "FK_POST CON_CONSIST_POST"
go

if exists (select 1
from sysobjects
where  id = object_id('Board')
   and type = 'U')
   drop table Board
go

if exists (select 1
from sysindexes
where  id    = object_id('Comment')
   and name  = 'Commenting_FK'
   and indid > 0
   and indid < 255)
   drop index Comment.Commenting_FK
go

if exists (select 1
from sysindexes
where  id    = object_id('Comment')
   and name  = 'Have_FK'
   and indid > 0
   and indid < 255)
   drop index Comment.Have_FK
go

if exists (select 1
from sysobjects
where  id = object_id('Comment')
   and type = 'U')
   drop table Comment
go

if exists (select 1
from sysindexes
where  id    = object_id('Follow')
   and name  = 'Followed_FK'
   and indid > 0
   and indid < 255)
   drop index Follow.Followed_FK
go

if exists (select 1
from sysindexes
where  id    = object_id('Follow')
   and name  = 'Following_FK'
   and indid > 0
   and indid < 255)
   drop index Follow.Following_FK
go

if exists (select 1
from sysobjects
where  id = object_id('Follow')
   and type = 'U')
   drop table Follow
go

if exists (select 1
from sysindexes
where  id    = object_id('Post')
   and name  = 'Contain_FK'
   and indid > 0
   and indid < 255)
   drop index Post.Contain_FK
go

if exists (select 1
from sysindexes
where  id    = object_id('Post')
   and name  = 'Posting_FK'
   and indid > 0
   and indid < 255)
   drop index Post.Posting_FK
go

if exists (select 1
from sysobjects
where  id = object_id('Post')
   and type = 'U')
   drop table Post
go

if exists (select 1
from sysindexes
where  id    = object_id('"Post Content"')
   and name  = 'Consist_FK'
   and indid > 0
   and indid < 255)
   drop index "Post Content".Consist_FK
go

if exists (select 1
from sysobjects
where  id = object_id('"Post Content"')
   and type = 'U')
   drop table "Post Content"
go

if exists (select 1
from sysobjects
where  id = object_id('"User"')
   and type = 'U')
   drop table "User"
go

/*==============================================================*/
/* Table: Board                                                 */
/*==============================================================*/
create table Board
(
   "Board ID" int not null,
   "Board Name" char(30) null,
   constraint PK_BOARD primary key ("Board ID")
)
go

/*==============================================================*/
/* Table: Comment                                               */
/*==============================================================*/
create table Comment
(
   "User ID" numeric(15) null,
   "Post ID" numeric(10) null,
   "Coment ID" int null,
   "Comment Time" datetime null
      constraint "CKC_COMMENT TIME_COMMENT" check ("Comment Time" is null or ("Comment Time" between '2000-1-1 0:0:0' and '2099-12-31 11:59:59')),
   Comment_Content text null
)
go

/*==============================================================*/
/* Index: Have_FK                                               */
/*==============================================================*/




create nonclustered index Have_FK on Comment ("Post ID" ASC)
go

/*==============================================================*/
/* Index: Commenting_FK                                         */
/*==============================================================*/




create nonclustered index Commenting_FK on Comment ("User ID" ASC)
go

/*==============================================================*/
/* Table: Follow                                                */
/*==============================================================*/
create table Follow
(
   "Followed ID" numeric(15) null,
   "Following ID" numeric(15) null,
   "Following Time" datetime null
)
go

/*==============================================================*/
/* Index: Following_FK                                          */
/*==============================================================*/




create nonclustered index Following_FK on Follow ("Following ID" ASC)
go

/*==============================================================*/
/* Index: Followed_FK                                           */
/*==============================================================*/




create nonclustered index Followed_FK on Follow ("Followed ID" ASC)
go

/*==============================================================*/
/* Table: Post                                                  */
/*==============================================================*/
create table Post
(
   "Post ID" numeric(10) not null,
   "User ID" numeric(15) null,
   "Board ID" int null,
   PostTitle text null,
   "Post time" datetime null
      constraint "CKC_POST TIME_POST" check ("Post time" is null or ("Post time" between '2000-1-1 0:0:0' and '2099-12-31 11:59:59')),
   constraint PK_POST primary key ("Post ID")
)
go

/*==============================================================*/
/* Index: Posting_FK                                            */
/*==============================================================*/




create nonclustered index Posting_FK on Post ("User ID" ASC)
go

/*==============================================================*/
/* Index: Contain_FK                                            */
/*==============================================================*/




create nonclustered index Contain_FK on Post ("Board ID" ASC)
go

/*==============================================================*/
/* Table: "Post Content"                                        */
/*==============================================================*/
create table "Post Content"
(
   "Post ID" numeric(10) null,
   "Index" int null,
   Content text null
)
go

/*==============================================================*/
/* Index: Consist_FK                                            */
/*==============================================================*/




create nonclustered index Consist_FK on "Post Content" ("Post ID" ASC)
go

/*==============================================================*/
/* Table: "User"                                                */
/*==============================================================*/
create table "User"
(
   "User ID" numeric(15) not null,
   "User Name" char(30) null,
   "User Email" char(50) null,
   Address char(50) null,
   Telphone numeric(11) null,
   Description text null,
   Password char(20) null,
   "Creating Time" datetime null
      constraint "CKC_CREATING TIME_USER" check ("Creating Time" is null or ("Creating Time" between '2000-1-1 0:0:0' and '2099-12-31 11:59:59')),
   constraint PK_USER primary key ("User ID")
)
go

alter table Comment
   add constraint FK_COMMENT_COMMENTIN_USER foreign key ("User ID")
      references "User" ("User ID")
go

alter table Comment
   add constraint FK_COMMENT_HAVE_POST foreign key ("Post ID")
      references Post ("Post ID")
go

alter table Follow
   add constraint FK_FOLLOW_FOLLOWED_USER foreign key ("Followed ID")
      references "User" ("User ID")
go

alter table Follow
   add constraint FK_FOLLOW_FOLLOWING_USER foreign key ("Following ID")
      references "User" ("User ID")
go

alter table Post
   add constraint FK_POST_CONTAIN_BOARD foreign key ("Board ID")
      references Board ("Board ID")
go

alter table Post
   add constraint FK_POST_POSTING_USER foreign key ("User ID")
      references "User" ("User ID")
go

alter table "Post Content"
   add constraint "FK_POST CON_CONSIST_POST" foreign key ("Post ID")
      references Post ("Post ID")
go

