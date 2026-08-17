1、数据搜索模块
1.1 创建任务
基本信息
接口名称：创建任务1
接口地址：https://dc.datastory.com.cn/project/job/add
请求类型：HTTPS
请求方式：POST
是否需要 token 访问：是

响应格式：application/json
请求格式：application/x-www-form-urlencoded

接口描述
创建任务接口，参数默认值为空则代表无。

请求头说明
参数名称	是否必须	类型	描述	默认值
Authorization	true	string	通过【登录接口】获取 token	
Content-Type	true	string	响应格式参数，需传入值为 application/json	
请求参数说明
主要参数：

1. name：必传，任务名称
2. sheetName：非必传，建议传，文件夹名称
3. jobType：必传1
4. titTemplateId：非必传，一般不传，ETL模板id
5. searchCondition：必传，数据采集条件，含系列子参数：数据类型/站点/匹配字段/采集主回帖/情感等‘’
6. profiltersListStr：必传，分析对象配置表，含系列子参数：分析对象名称，关键词过滤词，账号id等；
7. schedule：必传，任务调度相关信息，含系列子参数：邮箱，一次性/周期性任务，采集频率，采集频率时间单位，延迟启动等；
8. ftp/es：二选一，导出地址，ftp或es地址，ftp客户内部自己提供，es联系数说管理员提供;

参数名称	子参数名称	是否必须	类型	描述	默认值
name	——	true	string	任务名字，限制如下：
1. 不可重复、不可为空
2. 最多只支持输入60个字符
3. 仅支持数字、英文、中文、中划线(英文)、下划线(英文)的文字格式	
sheetName
——	false	string	文件夹名，推荐传【API任务】，若不传，无法通过登录数说聚合可视化查看API创建的任务详情，若传输即可在数说聚合指定的文件夹下查看该任务	
jobType	——	true	string	必须传1	
titTemplateId
——	false	number	ETL的模板ID，任务执行之前会根据模版id请求ETL接口获取模版中的算子	
searchCondition	——	true	object	json字符串，构造数据采集条件，说明如下

1. 当使用关键词采集且采集source非微博、微信、小红书时，必传该source对应的site；

2. 当使用账号采集时，仅需传入对应站点的账号ID即可，需指定账号对应的source和site；

3. 关键词和账号即【keywords、uid、biz、xhsAccId、svAccId、kuaiShouAccId、biliAccId】必传其一，否则会导致任务无数据，当关键词和账号同时传入时，表示两个条件同时生效；	
searchCondition
isFast	true	string	数据采集方式（微博微信新闻论坛，推荐使用传0；其他推荐传1）

0：获取数说当前符合条件的存量数据；（新闻论坛微博微信）；

1：发起实时采集，数据入库后获取符合条件的存量数据；	
searchCondition
startTime	true	string	获取数据发表时间段的开始时间，时间戳（毫秒）	
searchCondition
endTime	true	string	获取数据发表时间段的结束时间，时间戳（毫秒）；结束时间-开始时间不能超过1年	
searchCondition
source	true	string	数据平台来源，多个来源用英文逗号隔开，例如抓微博和微信传 weibo,weixin；

weibo：微博

weixin：微信

forum：论坛

news：新闻

video：视频

blog：博客

qa：问答

ecom：电商

xiaohongshu：小红书

shortVideo：短视频

gameOfNewsForum：游戏	
searchCondition	weiboMsgType	false	string	采集内容，source包含weibo时候必填；

1 ：微博主帖

2：微博回帖

0：微博主帖+回帖	
searchCondition
forumSite	false	string	采集站点，可不传，有指定论坛站点时才必传；多个站点用英文逗号隔开；	
searchCondition
forumMsgType	false	string	采集内容，source包含forum时候必填；

1 ：论坛主帖

2：论坛回帖

0：论坛主帖+回帖	1
searchCondition
newsSite	false	string	采集站点，可不传，有指定站点时才必传；多个站点用英文逗号隔开；	
searchCondition	newsMsgType	false	string	采集内容，source包含news时必填

1：新闻主帖

2：新闻评论

0：新闻主帖+新闻评论	
searchCondition
ecomSite	false	string	采集站点，可不传，有指定站点时才必传；多个站点用英文逗号隔开；

京东: 5

天猫: 10

searchCondition
ecomMsgType	false	string	采集内容，source 包含ecom时必填

1：电商商品

2：电商评论	1
searchCondition
videoSite	false	string	采集站点，可不传，有指定站点时才必传；多个站点用英文逗号隔开；

哔哩哔哩：44

优酷：32

爱奇艺：47

腾讯视频 ：35	
searchCondition
videoMsgType	false	number	采集内容，source包含video时必填

1：视频主帖

2：视频评论

0：视频主帖+视频评论	1
searchCondition
blogSite	false	string	采集站点，可不传，有指定站点时才必传；多个站点用英文逗号隔开；	
searchCondition
qaSite	false	string	采集站点，可不传，有指定站点时才必传；多个站点用英文逗号隔开；
知乎：101944	
searchCondition
qaMsgType	false	string	采集内容，source包含qa必填

1： 问题

2：问题的回答

0：问题+问题的回答	1
searchCondition
shortVideoSite	false	string	采集站点，可不传，有指定站点时才必传；多个站点用英文逗号隔开；

抖音：1003583

快手：1334510	
searchCondition
shortVideoMsgType	false	number	采集内容，source包含shortVideo时必填

1：短视频主帖

2：短视频评论

0：短视频主帖+短视频评论	0
searchCondition
xiaohongshuMsgType	false	string	采集内容，source包含xiaohongshu时必填

1：小红书笔记

2：笔记评论

0：小红书笔记+笔记评论	0
searchCondition
appStoreMsgType	false	number	采集内容，source包含appStore时必填

1：应用商店主帖

2：应用商店评论	
searchCondition
appStoreSite	false	string	采集站点，可不传，有指定站点时才必传；多个站点用英文逗号隔开；

小米应用商店: 2345434

oppo软件商店: 2360260

vivo应用商店: 2343373

googlePlay应用商店: 2341891

三星应用商店: 2372138

苹果应用商店: 2372309	
searchCondition
crawlFetchConf	false	object	微博微信采集选用接口， json字符串；isFast为1时必填	
searchCondition
sentiments	true	string	情感，多个情感英文逗号隔开，推荐传 0,1,-1

0：中性

1：正面

-1：负面	0,1,-1
searchCondition
keywordFields	true	string	关键词和过滤词，搜索匹配的字段，多个用英文逗号隔开，推荐传内容-content、标题-title，其余参数可按站点采集需求调整 

content：内容

title：标题

audio_asr_content：音频内容识别（仅适用微博，小红书，抖音，快手）

cover_ocr_content：视频封面内容识别（仅适用新闻，论坛，微博，小红书，抖音，快手，哔哩哔哩视频）

video_highlight_content：匹配花字（仅适用微博，小红书，抖音，快手）

video_content：视频文本识别（仅适用微博，小红书，抖音，快手）

commodity_title：带货标题（仅适用抖音-视频主帖）警告：纯评论的场景会导致取到大量数据

src_content：源内容（仅适用微博）

src_cover_content：源内容封面（仅适用微博）

src_audio_content：源内容音频（仅适用微博）

src_highlight_content：源内容花字（仅适用微博）

src_video_content：源视频文本（仅适用微博）

searchCondition
zhihuPostType	false	string	questions：提问

articles：文章

pins：想法

多个选择使用英文逗号分隔 ,	
searchCondition	douyinPostType	false	string	
video#0：常规视频


video#1：广告视频



image#0：常规图文


image#1：广告图文



多个选择使用英文逗号分隔 

searchCondition	kuaishouPostType	false	string	video#0：常规视频

image#0：常规图文

多个选择使用英文逗号分隔	
searchCondition	bilibiliPostType	false	string	video：视频

dynamic：动态

article：专栏

多个选择使用英文逗号分隔 ,	
searchCondition	isAdMap	false	object	用于筛选数据是否为广告，对应输出字段【是否广告】，不填时默认不限，可按需选择需要筛选1个或多个阵地，数值为0（非广告），1（是广告）。以下是各阵地（含所有）填写示例：
 
all: 0,1（所有阵地，输入该参数时，其他阵地数值不生效）
news: 0,1（仅新闻）
forum: 0,1（仅论坛）
weibo: 0,1（仅微博）
weixin: 0,1（仅微信）
ecomCommunity: 0,1（仅电商社区）
appStore: 0,1（仅应用商店）
xiaohongshu: 0,1（仅小红书）
shortVideo: 0,1（仅短视频）
ecom: 0,1（仅电商）
video: 0,1（仅视频）
qa: 0,1（仅问答）
blog: 0,1（仅其他）	Map<阵地，数值>
searchCondition	interactionRangeMap	false	object	用于筛选数据的互动量范围，对应输出字段【互动量】，不填时默认不限，可按需选择需要筛选1个或多个阵地，数值格式为"${gte}-${lte}"。以下是各阵地（含所有）填写示例：
 
all: 1000-100000（所有阵地，输入该参数时，其他阵地数值不生效）
news: 1000-100000（仅新闻）
forum: 1000-100000（仅论坛）
weibo: 1000-100000（仅微博）
weixin: 1000-100000（仅微信）
ecomCommunity: 1000-100000（仅电商社区）
appStore: 1000-100000（仅应用商店）
xiaohongshu: 1000-100000（仅小红书）
shortVideo: 1000-100000（仅短视频）
ecom: 1000-100000（仅电商）
video: 1000-100000（仅视频）
qa: 1000-100000（仅问答）
blog: 1000-100000（仅其他）	Map<阵地，数值>

"1000-" 大于等于1000
 
"-100000" 大于等于0小于等于100000（同时过滤空值）
 
"1000-100000" 大于等于1000，小于等于100000
——	profiltersListStr	true	array[object]	分析对象，json字符串	
profiltersListStr
name	true	string	分析对象名	
profiltersListStr
keywords	true	string	关键词，使用 “+” 连接表示且关系， “|” 连接表示或关系，支持英文括号 “( )”用于组合运算。 如果要匹配+( )| 本身，可以使用“\\”进行转义，如“\\+关注”。 （API传参和产品前端界面的转义符有区别，产品前端界面转义为“\”）
完整示例：(雅诗兰黛|兰蔻)+(口红|粉底) 展开后为：雅诗兰黛+口红|雅诗兰黛+粉底|兰蔻+口红|兰蔻+粉底

拆解后的关键词组不能大于200组	
profiltersListStr
filterwords	false	string	过滤词，语法规则同关键词；拆解后的关键词组不能大于200组	
profiltersListStr
uid	true	string	微博uid，source必传weibo，多个uid用英文逗号隔开	
profiltersListStr
biz	true	string	微信biz，source必传weixin，多个biz用英文逗号隔开	
profiltersListStr
xhsAccId	true	string	小红书账号id，source必传xiaohongshu，多个xhsAccId用英文逗号隔开	
profiltersListStr
biliAccId	true	string	B站账号id，source必传Video，videoSite必传44，多个biliAccId用英文逗号隔开	
profiltersListStr
zhihuAccId	true	string	知乎账号id，source必传Qa，qaSite必传101944，多个zhihuAccId用英文逗号隔开	
profiltersListStr	svAccId	true	string	抖音账号id，source必传shortVideo，shortVideoSite必传1003583，多个svAccId用英文逗号隔开	
profiltersListStr	kuaiShouAccId	true	string	快手账号id，source必传shortVideo，shortVideoSite必传1334510，多个kuaiShouAccId用英文逗号隔开	
profiltersListStr	wechatVideoUid	true	string	微信视频号账号id，source必传shortVideo，shortVideoSite必传25047925，多个wechatVideoUid用英文逗号隔开	
schedule	——	true	object	json字符串，调度相关的信息	
schedule	emails	true	string	任务完成后，联系邮箱【任务运行结果接收邮箱，可设置多个，多个邮箱请用应为英文分号分隔】	
schedule
isTemp	true	string	任务启动周期
1：一次性任务，指一次性回溯历史数据，endTime不能晚于当前时间

0：周期性任务，指定未来时间段内定期采集，endTime不能早于当前时间	
schedule
unit	true	string	采集频率时间单位，一次性任务传 d

d：每N天采集一次

M：每月N日采集一次	
schedule
interval	true	string	具体的采集时间间隔，如每1天采集一次，则传1
schedule	startTime	false	string	取用户前端输入任务启动时间和当前时间，对比两个时间大小，取大为任务启动时间（仅当schedule.isTemp为1时生效；schedule.isTemp为0时，传此参数无用）
schedule
startTimeOffset	false	number	延迟启动设置，每N天采集的任务默认0点启动，通过此参数控制每天任务启动时刻；若需每天获取微信数据时，传值18，且offsetUnit传值H，即每天18点获取昨天数据【否则漏数】，其他情况可不传	
schedule
offsetUnit	false	string	延迟启动的时间单位，若需每天获取微信数据时，传值H

H：小时

d：天	
schedule	searchUnitRange	false	number	周期设置unit单位为H，取数时间范围默认为最近48小时，取数时间最大值为48小时，默认是 interval字段值+1

周期设置unit单位为d，取数时间范围默认为最近N+1天，取数时间最大值为2N天，默认是 interval字段值+1	
schedule	emailMode	false	number	在不指定的情况下，默认为1，在指定空值的情况下，默认为-1,该配置与emails共同使用，emails指定发送邮箱

0-成功&失败通知，

1-成功通知，
2-失败通知,

其他值（如-1）-不论失败还是成功都不通知	
ftp	——	false	array[object]
ftp参数，json字符串（API调用无需提供FTP服务器参数给数说进行配置；无需使用FTP传输数据，则忽略此参数）	
ftp	account	true	string	ftp账户	
ftp
password	true	string	ftp密码	
ftp
host	true	string	ftp域名	
ftp
port	true	string	ftp端口	
ftp
filePath	true	string	文件目录	
ftp
filename	true	string	文件名	
ftp
type	true	string	ftp服务器类型，分ftp和sftp	
ftp
createNewFolder	false	boolean	是否在文件目录下创建当前日期目录	
ftp	
fileFormat

false

string

可选值为：csv，json

es	——	false	object	es参数，json字符串 （如需使用，联系数说同事提供参数）	
es	host	true	string	es集群主机，例如：dev4:9205:9305,dev5:9205:9305,dev6:9205:9305	
es
cluster	true	string	es集群名称：例如：hermes_es_cluster	
es
indexName	true	string	索引名	
es
typeName	false	string	类型名，推荐不传，不传时会自动生成一个随机值；不传该参数时，每个任务都会在ES集群生成一个新的数据源；周期任务会自动追加到同一个数据源	
matrix	matrix	false	object	导出到方舟	
matrix	projectId	true	number	方舟项目id	
matrix	dirId	false	number	方舟文件夹（选填，不填的情况下数据源创建在项目的根目录）	
matrix	datasourceName	true	string	方舟数据源名称（自己根据任务随机命名）	
matrixAppend 

——	false	object	追加导出到方舟时	
matrixAppend
matrixId	true	number	聚合系统中注册的方舟数据源关联id，将新跑的数据追加到指定的数据源	
hdfs	——	false	object	hdfs参数，json字符串，传入该参数、任务运行完成后可在聚合前端界面中下载本地文件	
hdfs	path	false	string	hdfs保存路径，以'/'开头的话，就是从hdfs的根目录开始。没有'/'开头就以/projects/datastory/titan/{path}，参数未填时默认保存在 /projects/datastory/titan/hermes	
hdfs
fileFormat	false	string	hdfs保存文件格式，非必填，值非空时校验，支持json, excel, csv，不区分大小写，默认csv	
hive	——	false	object	hive参数，json字符串	
hive	host	true	string	主机名，支持格式：[ip:port] 或 [域名:port]	
hive
database	true	string	库名，需提前创建	
hive
tableName	true	string	表名，无需提前创建，已创建会覆盖数据，未创建时会创建表并写入数据	
hive
account	false	string	账号名	
hive
password	false	string	密码	
oss	——	false	object	oss参数，json字符串	
oss	engineType	true	string	存储类型，支持：tencentcos-腾讯云，aliyunoss-阿里云	
oss	connectId	true	string	存储服务的唯一key，详见【辅助接口 - 2. 新建oss资源并获取connectId接口】	
oss	fileName	true	string	文件名	
oss	path	true	string	导出路径，以"/"开头	
oss	otherConfig	true	object	其他参数，json字符串	
oss	
fileFormat

false

string

可选值为：csv，json

otherConfig	bucketName	false	string	储存桶名称，当engineType有数值传入时必填	
返回字段说明
参数名称	类型	描述
success	boolean	接口请求是否成功
code	number	接口返回的错误编码
data	number	任务id
message	string	接口返回的提示信息
1.2 修改周期任务
基本信息
接口名称: 修改周期任务
接口地址: https://dc.datastory.com.cn/project/job/modify
请求类型: HTTPS
请求方式: POST
响应格式: JSON
是否需要 token 访问: 是

请求格式：application/x-www-form-urlencoded

接口描述
修改任务接口，id为必须，传endTime，表示修改周期任务采集数据的结束时间，周期频率不变；分析对象的修改为覆盖操作，也就是你之前传了3个分析对象，现在传2个，那么新的调度只跑这两个新的。

请求头说明
参数名称	是否必须	类型	描述	默认值
Authorization	true	string	通过【登录接口】获取 token	
请求参数说明
参数名称	子参数名称	是否必须	类型	描述	
id	id	true	number	任务id	
titTemplateId 

——	false	number	ETL的模板ID，任务执行之前会根据模版id请求ETL接口获取模版中的算子	
searchCondition 

——	true	object	json字符串，搜索条件	
searchCondition	endTime	true	string	获取数据发表时间段的结束时间，时间戳（毫秒）；PS：开始时间不可修改	
searchCondition	isFast	true	string	0：获取数说当前符合条件的存量数据；（新闻论坛微博/小红书/抖音微信传0）；

1：发起实时采集，数据入库后获取符合条件的存量数据；	
searchCondition	siteLabel
false	string	站点标签，多个用英文逗号隔开。站点标签等同于输入如下参数：数据平台来源（source，值取决于所选站点标签）、数据平台来源站点id（xxxSite，例如newsSiteId，值取决于所选站点标签）、采集内容（xxxMsgTye，例如newsMsgType，值为1，即采集主贴）、匹配字段（keywordFields，值为content,title），当显式输入上述参数时：采集内容和匹配字段以显式输入的为准，数据平台来源和数据平台来源的站点id将自动合并。	
searchCondition	source	true	string	数据平台来源，多个来源用英文逗号隔开，例如抓微博和微信传 weibo,weixin；

weibo：微博

weixin：微信

forum：论坛

news：新闻

video：视频

blog：博客

qa：问答

ecom：电商

xiaohongshu：小红书

shortVideo：短视频	
searchCondition	keywordFields
true	string	关键词和过滤词，搜索匹配的字段，多个用英文逗号隔开，推荐传内容-content、标题-title，其余参数可按站点采集需求调整 

content：内容

title：标题

audio_asr_content：音频内容识别（仅适用微博，小红书，抖音，快手）

cover_ocr_content：视频封面内容识别（仅适用新闻，论坛，微博，小红书，抖音，快手，哔哩哔哩视频）

video_highlight_content：匹配花字（仅适用微博，小红书，抖音，快手）

video_content：视频文本识别（仅适用微博，小红书，抖音，快手）

commodity_title：带货标题（仅适用抖音-视频主帖）警告：纯评论的场景会导致取到大量数据

src_content：源内容（仅适用微博）

src_cover_content：源内容封面（仅适用微博）

src_audio_content：源内容音频（仅适用微博）

src_highlight_content：源内容花字（仅适用微博）

src_video_content：源视频文本（仅适用微博）

searchCondition	forumSite	false	string	采集站点，source包含forum时候必填；多个站点用英文逗号隔开；	
searchCondition	forumMsgType	false	string	采集内容，source包含forum时候必填；

1 ：论坛主帖

2：论坛回帖

0：论坛主帖+回帖	
searchCondition	newsSite	false	string	采集站点，source包含news必填；多个站点用英文逗号隔开；	
searchCondition	ecomSite	false	string	采集站点，source 包含ecom时必填；多个站点用英文逗号隔开；	
searchCondition	ecomMsgType	false	string	采集内容，source 包含ecom时必填

1：电商商品

2：电商评论	
searchCondition	videoSite	false	string	采集站点，source包含video必填；多个站点用英文逗号隔开；	
searchCondition	videoMsgType	false	number	采集内容，source包含video时必填

1：视频主帖

2：视频评论

0：视频主帖+视频评论	
searchCondition	blogSite	false	string	采集站点，source包含blog时必填；多个站点用英文逗号隔开；	
searchCondition	qaSite	false	string	采集站点，source包含qa必填；多个站点用英文逗号隔开；	
searchCondition	qaMsgType	false	string	采集内容，source包含qa必填

1： 问题

2：问题的回答

0：问题+问题的回答	
searchCondition	shortVideoSite	false	string	采集站点，source包含shortVideo时必填；多个站点用英文逗号隔开；	
searchCondition	shortVideoMsgType	false	number	采集内容，source包含shortVideo时必填

1：短视频主帖

2：短视频评论

0：短视频主帖+短视频评论	
searchCondition	xiaohongshuMsgType	false	string	采集内容，source包含xiaohongshu时必填
1：小红书笔记

2：笔记评论

0：小红书笔记+笔记评论	
searchCondition	appStoreMsgType	false	number	采集内容，source包含appStore时必填

1：应用商店主帖

2：应用商店评论	
searchCondition	appStoreSite	false	string	采集站点，可不传，有指定站点时才必传；多个站点用英文逗号隔开；

小米应用商店: 2345434

oppo软件商店: 2360260

vivo应用商店: 2343373

googlePlay应用商店: 2341891

三星应用商店: 2372138

苹果应用商店: 2372309	
searchCondition  	gameOfNewsForumMsgType	false	number	采集内容，source包含gameOfNewsForum时必填

2：游戏评论	
searchCondition	gameOfNewsForumSite	false	string	采集站点，可不传，有指定站点时才必传；多个站点用英文逗号隔开；

TapTap：1003678

哔哩哔哩游戏：2372392

好游快爆：25472383	
profiltersListStr

——	true	array[object]	分析对象，json字符串	
profiltersListStr	name	true	string	分析对象名	
profiltersListStr	keywords	true		关键词，使用 “+” 连接表示且关系， “|” 连接表示或关系，支持英文括号 “( )”用于组合运算。 如果要匹配+( )| 本身，可以使用“\”进行转义，如“\+关注”。 完整示例：(雅诗兰黛|兰蔻)+(口红|粉底) 展开后为：雅诗兰黛+口红|雅诗兰黛+粉底|兰蔻+口红|兰蔻+粉底

拆解后的关键词组不能大于200组	
profiltersListStr	filterwords	true		过滤词，语法规则同关键词；拆解后的关键词组不能大于200组	
profiltersListStr	uid	true		微博uid，source必传weibo，多个uid用英文逗号隔开	
profiltersListStr	biz	true		微信biz，source必传weixin，多个biz用英文逗号隔开	
profiltersListStr	xhsAccId	true		小红书账号id，source必传xiaohongshu，多个xhsAccId用英文逗号隔开	
profiltersListStr	biliAccId	true		B站账号id，source必传Video，videoSite必传44，多个biliAccId用英文逗号隔开	
profiltersListStr	svAccId	true		抖音账号id，source必传shortVideo，shortVideoSite必传1003583，多个svAccId用英文逗号隔开	
profiltersListStr	kuaiShouAccId	true		快手账号id，source必传shortVideo，shortVideoSite必传1334510，多个kuaiShouAccId用英文逗号隔开	
schedule	——	false	object
json字符串，调度相关的信息	
schedule	emailMode	false	number	在不指定的情况下，默认为1，在指定空值的情况下，默认为-1,该配置与emails共同使用，emails指定发送邮箱

0-成功&失败通知，
1-成功通知，
2-失败通知,

其他值（如-1）-不论失败还是成功都不通知	
schedule	emails	false	string	任务完成后，联系邮箱【任务运行结果接收邮箱，可设置多个，多个邮箱请用应为英文分号分隔】	
返回字段说明
参数名称	类型	描述
success	boolean	接口请求是否成功
code	number	接口返回的错误编码
data	object	
message	string	接口返回的提示信息


2、数据超市模块
2.1 创建任务
基本信息
接口名称：创建任务

接口地址：https://dc.datastory.com.cn/application/market/job/v1/run

请求类型：HTTPS
请求方式：POST

是否需要 token 访问：是

响应格式：application/json
请求格式：application/json

接口描述
创建任务接口，参数默认值为空则代表无。

请求头说明
参数名称	是否必须	类型	描述	默认值
Authorization	true	string	通过【登录接口】获取 token	
Content-Type	true	string	响应格式参数，需传入值为 application/json	
请求参数说明
父参数名称	参数名称	是否必须	类型	描述	示例值	默认值
jobName

——	true	string	任务名字，限制如下：
1. 不可重复、不可为空
2. 最多只支持输入60个字符
3. 仅支持数字、英文、中文、中划线(英文)、下划线(英文)的文字格式	

sheetId 

——	false	number	文件夹id，若不传，无法通过登录数说聚合可视化查看API创建的任务详情，若传输即可在数说聚合指定的文件夹下查看该任务		
appId 

——	true	number	传值详见【2.3 数据超市支持的采集列表】

appId不可为空	

scopeId 

——	true	number	传值详见【2.3 数据超市支持的采集列表】

scopeId不可为空	

titTemplateId 

——	false	number	ETL工作流模板id	

sourceConfig

——	true	object	采集输入输出配置	

sourceConfig	input	true	string	参数值：keyword-条件是关键词，uid-条件是用户uid，topic-快手话题；

url参数分为两种情况：url或surl （由于不同站点的url存在差异性，有的站点的url需要解析转换才能命中数据，因此url分为surl和url两种，用户可通过以下映射选择参数，参数如果错误可能会导致任务创建失败，或者任务取数为0.）；

surl：支持的站点见【2.3 数据超市支持的采集列表】；

url：支持的站点见【2.3 数据超市支持的采集列表】；

uid：支持的站点见【2.3 数据超市支持的采集列表】

topic：快手,lofter

field_tag：微博，快手，B站视频

forum_name:百度贴吧
forum_names:NGA论坛（由于该站点内主贴与板块存在一对多的关系，因此该条件字段名带“s”）

car_series:汽车之家，太平洋汽车网，易车网，爱卡汽车网，车质网


sourceConfig	matchType	false	array	input选择keyword时该参数有意义，指关键词匹配的文本，标准参数值：content-内容，title-标题；

特殊匹配字段，只对于特定站点有效（在使用特殊字段的情况下，请谨慎核对字段是否对站点有效，否则可能导致大量误取数）；
微博：src_content-源内容；cover_ocr_content-视频封面内容；audio_asr_content-音频内容识别；video_highlight_content-视频花字识别，video_content-视频文本识别，src_cover_content-源内容封面，src_audio_content-源内容音频，src_highlight_content-源内容花字，src_video_content-源视频文本；

b站：video_labels-视频标签，cover_ocr_content-视频封面内容识别

小红书：cover_ocr_content-视频封面内容；audio_asr_content-音频内容识别；video_highlight_content-视频花字识别；cooperation_brand_labels-合作品牌，video_content-视频文本识别；

快手：audio_asr_content-音频内容识别，cover_ocr_content-视频封面内容识别，video_highlight_content-视频花字识别，video_content-视频文本识别；

微信视频号：cover_ocr_content-视频封面内容识别。

百度贴吧：forum_name-匹配贴吧名称	["content","title"]表示关键词匹配内容和标题	["content","title"]
sourceConfig	output	true	array	采集输出的内容，主要为主帖/评论/更新互动量/账号信息等，参数值存在多种，且和输入input有对应关系，详见下表中【2.3 数据超市支持的采集列表】	["POST","COMMENT","INTERACTION"]表示输出主贴/评论/更新互动量	
sourceConfig	isAd	false	string	用于筛选数据是否为广告，对应输出字段【是否广告】，不填时默认不限，可按需选择需要筛选，数值为0（非广告），1（是广告）。		
sourceConfig	interactionRange	false	string	用于筛选数据的互动量范围，对应输出字段【互动量】，不填时默认不限，可按需选择需要筛选，数值格式为"${gte}-${lte}"	"1000-" 大于等于1000
 
"-100000" 小于等于100000（同时过滤空值）
 
"1000-100000" 大于等于1000，小于等于100000	
sourceConfig

crawlDatasourceIdMap 

false

object

在线取数选定（针对特殊站点，目前暂时只针对小红书在线更新互动量任务）

key值参照output
value值为固定值，可选值如下：
14-小红书内容详情（标题/内容字段）+互动量
15-小红书仅更新互动量（不含标题/内容字段）

举例：小红书发酵互动量时希望同时更新互动量和内容详情：

{"INTERACTION":14}

sourceConfig	condition	true	array	输入条件	

condition
name	true	string	分析对象名，condition中多个元素的name字段不能重复


condition
keywords	false	string	input值为keyword时必填，输出结果会匹配符合该关键词的文本

input值为uid时可选，sourceConfig中的matchType必选，请参考sourceConfig对象matchType，输出结果会匹配符合该关键词的文本


condition
filterwords	false	string	input值为keyword时可填，输出结果会过滤该关键词的文本

input值为uid时可选，sourceConfig中的matchType必选，请参考sourceConfig对象matchType，输出结果会过滤该关键词的文本


condition	uid	false	string	input值为uid时必填，多个uid以","隔开，输出结果为该uid下的内容		
condition
url	false	string	input值为url时，多个url以","隔开，输出结果为该url下的内容，url的输入需符合各站点正则匹配，各站点正则见附录	

condition	biz	true	string	采集站点为微信，且input值为url时必填，多个biz以","隔开，与url组合输出数据		
condition	topic	false	string	input值为topic时必填,多个话题以","隔开，例如：王牌竞速,王牌竞速卤卤		
condition	content_mode	false	string	input值为field_tag时选填，内容类型，取值有PGC/UGC/UKN，多种类型逗号隔开	""	
condition	interaction_cnt_range	false	string	input值为field_tag时选填，互动量范围，格式"${gte}-${lte}"	"300-" 大于等于300

"-1000" 小于等于1000

"300-1000" 大于等于300，小于等于1000	
condition	
keywords

false	string	input值为field_tag时选填，提及关键词，和match_type共同作用，输出结果会匹配符合该关键词的文本		
condition	match_type	false	string	input值为field_tag时选填，提及关键词，和keywords共同作用，指keywords匹配的文本，参数值：content-内容，title-标题

特殊匹配字段，只对于特定站点有效（在使用特殊字段的情况下，请谨慎核对字段是否对站点有效，否则可能导致大量误取数）

微博：src_content-源内容，无title字段

b站：video_labels-视频标签

快手：audio_asr_content-音频内容识别，cover_ocr_content-视频封面内容识别，video_highlight_content-匹配花字		
condition	exists_field	false	string	input值为field_tag时选填，音图识别，仅快手有效，取值为 cover_ocr_content-视频封面内容识别非空，audio_asr_content-音频内容识别非空，多个取值逗号隔开	"cover_ocr_conten,audio_asr_content"	
condition	car_series	false	string	input值为car_series时必填,多个车系以","隔开，例如：宝马X5,保时捷	指定车系	
condition	forum_name	false	string	input值为forum_name时必填,多个板块名称以","隔开，例如：宝马,保时捷	指定板块	
condition	forum_names	false	string	input值为forum_names时必填,多个板块名称以","隔开，例如：宝马,保时捷	由于该站点内主贴与板块存在一对多的关系，因此该条件字段名带“s”	
scheduleConfig	——	true	object	任务运行时间配置	

scheduleConfig	type	true	string	调度类型，参数值：TEMP-临时，SIMPLE-周期	

scheduleConfig	startDataTime	true	string	获取数据发表时间段的开始时间，时间戳（毫秒）	

scheduleConfig	endDataTime	true	string	获取数据发表时间段的结束时间，时间戳（毫秒）	

scheduleConfig	schedStartTime
false	string	任务开始运行时间，时间戳（毫秒）（仅当scheduleConfig.type为TEMP时生效；scheduleConfig.type为SIMPLE时，传此参数无用；）
scheduleConfig	commentDelay	false	number	评论更新时间，单位小时，当output包含COMMENT时必填

1.当input为url，且scheduleConfig.type为SIMPLE时，该字段表示每隔多少小时更新一次评论；

2.其余情况，该字段表示主贴开始采集多久后更新一次评论。	

scheduleConfig	commentDelayList	false	array	1. 评论更新时间，单位小时，当output包含COMMENT且不是url的时候必填（该值是多选，如果填充此值，commentDelay可不填）

2. 单个数值中最多可传7个数值参数，传参示例："commentDelayList":[0,24,48,72,96,120,144]

3.其余情况，该字段表示主贴开始采集多久后更新一次评论
根据权限控制的参数，默认不支持使用，详情请咨询聚合管理员
scheduleConfig	commentDelayUnit	false	string	评论更新时间间隔单位，不传时默认为H（小时），数值包括：d,H（日，小时，仅支持传入其中一个值）	H	
scheduleConfig	interactionDelay	false	number	互动量更新时间，单位小时，当output包含INTERACTION时必填

1.当input为url，且scheduleConfig.type为SIMPLE时，该字段表示每隔多少小时更新一次互动量；

2.其余情况，该字段表示主贴开始采集多久后更新一次互动量。	

scheduleConfig	interactionDelayList	false	array	1. 互动量更新时间，单位天（2024年1月11日调整），当output包含INTERACTION且不是url必填（该值是多选，如果填充此值，interactionDelay可不填）

2.单个数值中最多可传7个数值参数，传参示例："interactionDelayList":[0,1,2,3,4,5,6]

3.其余情况，该字段表示主贴开始采集多久后更新一次互动量
根据权限控制的参数，默认不支持使用，详情请咨询聚合管理员
scheduleConfig	interactionDelayUnit	false	string	互动量更新时间间隔单位，不传时默认为d（日），数值包括：d（日，仅支持传入其中一个值）	d	
scheduleConfig	useInteractionDefaultDelay	false	boolean	互动量更新时使用默认更新，false-不使用默认更新，true-使用默认更新。与scheduleConfig.interactionDelay参数二选一。

1.目前支持：微博/微信/知乎/哔哩哔哩站点；

2.不支持：input为url，且scheduleConfig.type为SIMPLE。	

scheduleConfig	interval	false	number	任务运行周期，scheduleConfig.type为SIMPLE时，该参数必填	interval=1，unit=d，表示1天运行一次任务	
scheduleConfig	unit	false	string	任务运行周期单位，scheduleConfig.type为SIMPLE时，该参数必填，参数值：d-日，M-月	

scheduleConfig	searchStartTime	false	number	取数时间间隔，参数值：d-日,H-小时，非必填，默认和interval相同
searchUnit为H，取数时间间隔最大值为48小时

searchUnit为d，取数时间间隔最大值为2N天	
scheduleConfig	searchUnit	false	string	取数时间间隔单位，非必填，默认和unit相同
exportConfig	——	true	object	数据导出配置	

exportConfig	ftp	false	object	导出到ftp时填写该参数	

ftp	filePath	true	string	文件路径	

ftp	filename	true	string	文件名	

ftp	
fileFormat

false 

string 

可选值为：csv，json

ftp	id	true	number	ftp地址id	

exportConfig	es	false	object	导出到es时填写该参数，es，es-append两个参数只能输入一个参数	

es	cluster	true	string	集群	

es	host	true	string	地址名	

es	indexName	true	string	索引名	

es	typeName	true	string
类型名	

exportConfig	esAppend	false	object	追加导出到es时填写该参数，es，es-append两个参数只能输入一个参数	

esAppend
jobId
true	number	聚合任务id，把新跑的数据追加到任务上	

exportConfig	matrix
false	object
导出到方舟时填写该参数，es，esAppend，matrix，matrixAppend四个参数只能输入一个参数	

matrix	projectId	true	number
方舟项目id	

matrix	dirId	false	number	方舟文件夹（选填，不填的情况下数据源创建在项目的根目录）	

matrix	datasourceName	true	string
方舟数据源名称（自己根据任务随机命名）	

exportConfig	matrixAppend
false	object
追加导出到方舟时填写该参数，es，esAppend，matrix，matrixAppend四个参数只能输入一个参数	

matrixAppend	matrixId
true	number	聚合系统中注册的方舟数据源关联id，将新跑的数据追加到指定的数据源	

exportConfig	local	false	object	导出到本地时填写该参数	

exportConfig	tencentcos	false	object	导出腾讯云cos时填写该参数		
tencentcos	connectId	true	string	存储服务的唯一key，详见【辅助接口 - 2. 新建oss资源并获取connectId接口】		
tencentcos	fileName	true	string	文件名		
tencentcos	path	true	string	导出路径，以“/”开头		
tencentcos	otherConfig	true	string	其他参数，json字符串

"otherConfig": "{\"bucketName\": \"sme-wpptech\"}"
tencentcos

fileFormat

false	
string

可选值为：csv，json

otherConfig	bucketName	true	string	储存桶名称，当engineType为tencentcos时必填		
exportConfig	aliyunoss	false	object	导出阿里有oss时填写该参数		
aliyunoss	connectId	true	string	存储服务的唯一key，详见【辅助接口 - 2. 新建oss资源并获取connectId接口】		
aliyunoss	fileName	true	string	文件名		
aliyunoss	path	true	string	导出路径，以“/”开头		
aliyunoss	otherConfig	true	string	储存桶名称，当engineType为aliyunoss时必填 示例：

"otherConfig": "{\"bucketName\": \"sme-wpptech\"}"
aliyunoss 

fileFormat

false

string 

可选值为：csv，json

otherConfig	bucketName	true	string	储存桶名称，当engineType为aliyunoss时必填		
globalConfig	——	true	object	通用配置	

globalConfig	email	true	string	任务结束时通知的邮件	

globalConfig	emailMode	true	number	邮件通知的模式，参数值：0-成功&失败通知，1-成功通知，2-失败通知	

globalConfig	isRealTime	true	object	参数值：0-快速取数，直接全量库取存量数据，1-在线取数，先爬虫入库，再取全量库数据，

示例："isRealTime": {"POST": 1,"COMMENT": 1}

示例含义：主贴在线取数，评论在线取数	

globalConfig	isKeepTrend	output为USER时，true；其他-false	boolean	是否保留趋势，参数值：true-保留，false-不保留，scheduleConfig.type为SIMPLE时该参数有效	
false
附录
url的正则匹配公式

b站：
https://www.bilibili.com/video/(av\d+|BV[0-9a-z]+)


豆瓣小组：
https://www.douban.com/group/topic/\d+


豆瓣电影
https://movie.douban.com/subject/\d+

豆瓣电视剧
https://movie.douban.com/subject/\d+


微博
https?://weibo\.com/\d+


微信
https://mp.weixin.qq.com/s.*(biz=.+|mid=.+|idx=.+|sn=.+){4}


    小红书
https://www.xiaohongshu.com/discovery/item/\w+


知乎
https://(zhuanlan.zhihu.com/p/\d+|www.zhihu.com/question/\d+)


苹果应用商店
https?://apps.apple.com/cn/app/id\\d+
 
 
电商商品URL
天猫：^https?://detail(\\.m)?\\.tmall\\.com\\/item\\.html?\\?.*id=\\d+
淘宝：^https?://(item.taobao.com/item.html?\\?id=\\d+|a.m.taobao.com/i\\d+.html?)
京东：^https?://.*item.jd.[^\\/]+/.*\\d+.html?
苏宁：^https?://product.suning.com/\\d+/\\d+.html?
网易考拉：^https?://\\w+.kaola.com(.\\w+)?/product/\\d+(\\.html)?
唯品会：^https?://detail.vip.com/detail-\\d+-\\d+.html?<br/>
 
 
电商店铺URL
天猫：
^https?://(?!chaoshi)\w+(\.m)?\.tmall\..+
^https?://shop\d+.m.tmall.com
^https?://shop\d+.m.taobao.com
淘宝：^https?://shop\d+.m.taobao.com
京东：^https?:\/\/mall\.jd\..+?\/(index-\d+|view_search[\d-]+)\.html?
苏宁：^https?://.+.suning.com
网易考拉：^https?:\/\/k?mall\.kaola\.com(/(pc|app))?/\d+
唯品会：^https?://list.vip.com/brand.html?\?sn=\d+<br/>


2.2 修改周期任务
基本信息
接口名称：修改周期任务

接口地址：https://dc.datastory.com.cn/application/market/job/reset

请求类型：HTTPS
请求方式：POST

是否需要 token 访问：是
响应类型：application/json

请求类型：application/json

接口描述
创建任务接口，参数默认值为空则代表无。

请求头说明
参数名称	是否必须	类型	描述	默认值
Authorization	true	string	通过【登录接口】获取 token
请求参数说明
参数名称	子参数名称	是否必须	类型	描述	示例值	默认值
id	——	true	number	修改的周期任务任务id	

titTemplateId 

——	false	number	ETL工作流模板id		
updateModule 

——	true	object	更新任务配置模块的标识		
updateModule	updateProfiler	false	boolean	是否更新采集输入	
false
updateModule	updateSchedule	false	boolean	是否更新采集周期	
false
updateModule	updateFermentation	false	boolean	是否更新发酵配置	
false
updateModule	updateEmail	false	boolean	是否更新通知配置	
false
sourceConfig	——	true	object	采集输入输出配置

*当updateProfiler为true时该对象及其属性必填	

sourceConfig	input	true	string	输入类型，值与原任务保持不变

参数值：keyword-条件是关键词，uid-条件是用户uid，topic-快手话题，field_tag-内容标签，topic_url-话题url，url-单帖url

站点限制：
topic：快手
url：哔哩哔哩游戏，TapTap
field_tag：微博，快手，B站视频

修改任务不支持以下参数input：
surl，shop_url，crowd_attributes	

sourceConfig	matchType	false	array	input选择keyword时该参数有意义，指关键词匹配的文本，参数值：content-内容，title-标题

特殊匹配字段，只对于特定站点有效（在使用特殊字段的情况下，请谨慎核对字段是否对站点有效，否则可能导致大量误取数）

b站：video_labels-视频标签

快手：audio_asr_content-音频内容识别，cover_ocr_content-视频封面内容识别，video_highlight_content：匹配花字	["content","title"]表示关键词匹配内容和标题	["content","title"]
sourceConfig	output	true	array	采集输出的内容，主要为主帖/评论/更新互动量/账号信息等，参数值存在多种，且和输入input有对应关系，详见下表中【2.3 数据超市支持的采集列表】	["POST","COMMENT","INTERACTION"]表示输出主贴评论和更新互动量	
sourceConfig	condition	true	array	输入条件，当updateProfiler为true时该对象及其属性必填	

condition	name	true	string	分析对象名，condition中多个元素的name字段不能重复	

condition	keywords	false	string	input值为keyword时必填，输出结果会匹配符合该关键词的文本

input值为uid时可选，sourceConfig中的matchType必选，请参考sourceConfig对象matchType，输出结果会匹配符合该关键词的文本	

condition	uid	false	string	input值为uid时必填，多个uid以","隔开，输出结果为该uid下的内容	

condition	filterwords	false	string	input值为keyword时可填，输出结果会过滤该关键词的文本

input值为uid时可选，sourceConfig中的matchType必选，请参考sourceConfig对象matchType，输出结果会过滤该关键词的文本	

condition	topic	false	string	input值为topic时必填,多个话题以","隔开，例如：王牌竞速,王牌竞速卤卤	

scheduleConfig	——	true	object	任务运行时间配置

*当updateSchedule为true时该对象及其属性必填	

scheduleConfig	type	true	string	调度类型，参数值：SIMPLE-周期

*TEMP类型任务不支持修改	

scheduleConfig	endDataTime	true	string	获取数据发表时间段的结束时间，时间戳（毫秒）

*当updateSchedule为true时必填，可延长结束时间	

scheduleConfig	commentDelay	false	number	评论更新时间，单位小时，该字段表示主贴开始采集多久后更新一次评论

*当updateFermentation为true，且当output包含COMMENT时必填	

scheduleConfig	interactionDelay	false	number	互动量更新时间，单位小时，该字段表示主贴开始采集多久后更新一次互动量

*当updateFermentation为true，且当output包含INTERACTION时必填	

scheduleConfig	useInteractionDefaultDelay	false	boolean	互动量更新时使用默认更新，false-不使用默认更新，true-使用默认更新。

1.目前支持：微博/微信/知乎/哔哩哔哩站点；

*当updateFermentation为true，且当output包含INTERACTION时，与scheduleConfig.interactionDelay参数二选一	

globalConfig 

——	true	object	通用配置，修改任务过程中该参数必填

*当updateEmail为true时该对象及其属性生效	

globalConfig	email	true	string	任务结束时通知的邮件	

globalConfig	emailMode	true	number	邮件通知的模式，参数值：0-成功&失败通知，1-成功通知，2-失败通知




2.3 数据超市支持的采集列表
常用的输入方式：关键词，账号，单帖url

站点	采集区域	appid	scopeId	关键词/过滤词：keyword	账号：uid	单帖url：surl
微博	微博	6	4	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	账号信息：USER
主帖（非账号信息时必填）：POST
互动量：INTERACTION
评论：COMMENT	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
转发：REPOST
点赞列表：LIKE
微信	微信公众号	7	10	主帖（必填）：POST
互动量：INTERACTION	主帖（必填）：POST
互动量：INTERACTION	主帖（必填）：POST
互动量（必填）：INTERACTION
小红书	小红书	13	11	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	账号信息：USER
主帖（非账号信息时必填）：POST
互动量：INTERACTION
评论：COMMENT	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
抖音	短视频	8	7	以下POST类型至少传其一，建议传常规图文和常规视频：
常规图文：POST-image#0
常规视频：POST-video#0
广告图文：POST-image#1
广告视频：POST-video#1

互动量：INTERACTION
评论：COMMENT	账号信息：USER
非账号信息时，POST类型至少传其一，建议传常规图文和常规视频：
常规图文：POST-image#0

常规视频：POST-video#0

广告图文：POST-image#1

广告视频：POST-video#1



互动量：INTERACTION
评论：COMMENT	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
快手	快手	12	6	
以下POST类型至少传其一：



常规图文：POST-image#0

常规视频：POST-video#0



互动量：INTERACTION

评论：COMMENT

账号信息：USER

非账号信息时，POST类型至少传其一：

常规图文：POST-image#0

常规视频：POST-video#0



互动量：INTERACTION
评论：COMMENT

主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT

微信视频号	微信视频号	70	50	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	账号信息：USER
主帖（非账号信息时必填）：POST
互动量：INTERACTION
评论：COMMENT	无
哔哩哔哩	视频	14	9	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT-0
弹幕：COMMENT-1	账号信息：USER
主帖（非账号信息时必填）：POST
互动量：INTERACTION
评论：COMMENT	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT-0
弹幕：COMMENT-1

当传入含评论更新时间（commentDelay）参数时，COMMENT-0表示主帖的评论；
当没有传评论更新时间（commentDelay）参数时，COMMENT-0表示仅评论
哔哩哔哩	动态	14	56	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT-0	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT-0	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT-0
仅评论：COMMENT

当传入含评论更新时间（commentDelay）参数时，COMMENT-0表示主帖的评论；
当没有传评论更新时间（commentDelay）参数时，COMMENT表示仅评论
哔哩哔哩	专栏	14	69	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT

当传入含评论更新时间（commentDelay）参数时，COMMENT表示主帖的评论；
当没有传评论更新时间（commentDelay）参数时，COMMENT表示仅评论
知乎	知乎	10	8	以下POST类型至少传其一：
回答：POST_answers
问题：POST_questions
文章：POST_articles
想法：POST_pins
视频：POST_zvideo

互动量：INTERACTION
评论：COMMENT	账号信息：USER
非账号信息时，以下POST类型至少传其一：
回答：POST_answers
问题：POST_questions
文章：POST_articles
想法：POST_pins
视频：POST_zvideo

互动量：INTERACTION
评论：COMMENT	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
懂车帝	口碑	53	38	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
懂车帝	论坛	53	43	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
懂车帝	新闻	53	54	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
汽车之家	口碑	15	12	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
汽车之家	论坛	15	39	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
汽车之家	新闻	15	51	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
太平洋汽车网	点评	16	13	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	主帖（必填）：POST
互动量：INTERACTION	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
太平洋汽车网	论坛	16	41	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
太平洋汽车网	新闻	16	55	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
易车网	点评	17	14	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
易车网	论坛	17	40	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
易车网	新闻	17	52	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
爱卡汽车网	论坛	18	42	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
爱卡汽车网	新闻	18	53	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
爱卡汽车网	口碑	18	15	主帖（必填）：POST
互动量：INTERACTION	无	主帖（必填）：POST
评论：COMMENT
今日头条	今日头条	11	5	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	账号信息：USER
主帖（非账号信息时必填）：POST
互动量：INTERACTION
评论：COMMENT	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
网易新闻	网易新闻	54	33	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	无	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
新浪新闻	新浪新闻	55	36	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	无	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
搜狐新闻	搜狐新闻	56	35	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	无	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
腾讯新闻	腾讯新闻	57	34	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	无	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
百家号	百家号	58	37	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	无	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
车质网	投诉	72	58	主帖（必填）：POST	无	无
酷安	酷安	74	61	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	账号信息：USER
主帖（非账号信息时必填）：POST
互动量：INTERACTION
评论：COMMENT	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
晋江文学城	晋江闲情	76	63	主帖（必填）：POST
评论：COMMENT	无	无
百度贴吧	百度贴吧	77	64	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT

当传入含评论更新时间（commentDelay）参数时，COMMENT表示主帖的评论；
当没有传评论更新时间（commentDelay）参数时，COMMENT表示仅评论	无	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
taptap	论坛	45	66	主帖（必填）：POST
评论：COMMENT

当传入含评论更新时间（commentDelay）参数时，COMMENT表示主帖的评论；
当没有传评论更新时间（commentDelay）参数时，COMMENT表示仅评论	无	无
NGA	NGA	78	65	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT

当传入含评论更新时间（commentDelay）参数时，COMMENT表示主帖的评论；
当没有传评论更新时间（commentDelay）参数时，COMMENT表示仅评论	无	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
虎扑	虎扑	83	67	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	无	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
Lofter	Lofter	84	68	主帖（必填）：POST
评论：COMMENT	无	无
黑猫投诉	黑猫投诉	92	76	主帖（必填）：POST	无	无
凤凰网	凤凰网	98	79	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	无	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
一点资讯	一点资讯	110	94	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	无	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
新华网	新华网	99	80	主帖（必填）：POST
互动量：INTERACTION	无	主帖（必填）：POST
互动量：INTERACTION
库街区	库街区	101	83	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	无	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
懂球帝	懂球帝	102	84	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	无	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
新出行	点评	103	85	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
新出行	新闻	103	86	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	无	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
新出行	论坛	103	87	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	无	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
旅法师营地	旅法师营地	104	88	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT

当传入含评论更新时间（commentDelay）参数时，COMMENT表示主帖的评论；
当没有传评论更新时间（commentDelay）参数时，COMMENT表示仅评论	无	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
凯恩之角	凯恩之角	105	89	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT

当传入含评论更新时间（commentDelay）参数时，COMMENT表示主帖的评论；
当没有传评论更新时间（commentDelay）参数时，COMMENT表示仅评论	无	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
搜狐视频	搜狐视频	143	128	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT

当传入含评论更新时间（commentDelay）参数时，COMMENT表示主帖的评论；
当没有传评论更新时间（commentDelay）参数时，COMMENT表示仅评论	无	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
腾讯视频	腾讯视频	142	127	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT	无	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
爱奇艺	爱奇艺	116	100	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT		主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
汽车头条	汽车头条	144	129	主帖（必填）：POST
互动量：INTERACTION	无	主帖（必填）：POST
互动量：INTERACTION
百度知道	百度知道	145	130	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT

当传入含评论更新时间（commentDelay）参数时，COMMENT表示主帖的评论；
当没有传评论更新时间（commentDelay）参数时，COMMENT表示仅评论	无	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
界面新闻	界面新闻	148	131	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT

当传入含评论更新时间（commentDelay）参数时，COMMENT表示主帖的评论；
当没有传评论更新时间（commentDelay）参数时，COMMENT表示仅评论	无	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
360快讯	360快讯	149	132	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT

当传入含评论更新时间（commentDelay）参数时，COMMENT表示主帖的评论；
当没有传评论更新时间（commentDelay）参数时，COMMENT表示仅评论	无	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
Zaker新闻	Zaker新闻	151	133	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT

当传入含评论更新时间（commentDelay）参数时，COMMENT表示主帖的评论；
当没有传评论更新时间（commentDelay）参数时，COMMENT表示仅评论	无	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
新浪汽车	新闻	152  	134	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT

当传入含评论更新时间（commentDelay）参数时，COMMENT表示主帖的评论；
当没有传评论更新时间（commentDelay）参数时，COMMENT表示仅评论	无	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT


其他输入方式：

站点	采集区域	采集输入	appid	scopeId	input参数	output参数
抖音	短视频	话题URL	8	7	topic_url	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
抖音	短视频	用户URL	8	7	user_url	账号信息：USER
非账号信息时，以下POST类型至少传其一，建议传常规图文和常规视频：
常规图文：POST-image#0
常规视频：POST-video#0
广告图文：POST-image#1
广告视频：POST-video#1

互动量：INTERACTION
评论：COMMENT
今日头条	今日头条	用户URL	11	5	user_url	账号信息：USER
主帖（非账号信息时必填）：POST
互动量：INTERACTION
评论：COMMENT
微博	微博	用户URL	6	4	user_url	账号信息：USER
主帖（非账号信息时必填）：POST
互动量：INTERACTION
评论：COMMENT
知乎	知乎	话题	10	8	topic	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
快手	快手	话题	12	6	topic	以下POST类型至少传其一，建议传常规图文和常规视频：
常规图文：POST-image#0
常规视频：POST-video#0

互动量：INTERACTION
评论：COMMENT
小红书	小红书	用户URL	13	11	user_url	账号信息：USER
主帖（非账号信息时必填）：POST
互动量：INTERACTION
评论：COMMENT
哔哩哔哩	视频	话题	14	9	topic_keyword	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT-0
弹幕：COMMENT-1
哔哩哔哩	游戏	游戏url	14	32	url	主帖（必填）：POST
互动量：INTERACTION
评论（游戏评价）：COMMENT

当传入含评论更新时间（commentDelay）参数时，COMMENT表示主帖的评论；
当没有传评论更新时间（commentDelay）参数时，COMMENT表示仅游戏评价
哔哩哔哩	动态	话题	14	56	topic_keyword	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT-0
哔哩哔哩	番剧	番剧url	14	70	surl
以下为单选：
长短评：COMMENT
剧集评论：BANGUMI_COMMENT
哔哩哔哩	番剧	剧集url	14	70	bangumi_url
剧集评论：BANGUMI_COMMENT

汽车之家	新闻	用户URL	15	51	user_url	账号信息：USER
主帖（非账号信息时必填）：POST
互动量：INTERACTION
评论：COMMENT
汽车之家	口碑	车系	15	12	car_series	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
汽车之家	口碑	用户URL	15	12	user_url	账号信息：USER
主帖（非账号信息时必填）：POST
互动量：INTERACTION
评论：COMMENT
汽车之家	论坛	板块名称	15	39	forum_name	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
汽车之家	论坛	板块ID	15	39	forum_id	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
汽车之家	论坛	用户URL	15	39	user_url	账号信息：USER
主帖（非账号信息时必填）：POST
互动量：INTERACTION
评论：COMMENT
太平洋汽车网	点评	车系	16	13	car_series	主帖（必填）：POST
互动量：INTERACTION
太平洋汽车网	论坛	板块名称	16	41	forum_name	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
太平洋汽车网	论坛	板块ID	16	41	forum_id	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
易车网	点评	车系	17	14	car_series	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
易车网	论坛	板块名称	17	40	forum_name	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
易车网	论坛	板块ID	17	40	forum_id	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
爱卡汽车网	口碑	车系	18	15	car_series	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
爱卡汽车网	论坛	板块名称	18	42	forum_name	主帖（必填）：POST
互动量：INTERACTION
爱卡汽车网	论坛	板块ID	18	42	forum_id	主帖：POST
taptap	游戏	游戏url	45	31	url	主帖：POST
互动量：INTERACTION
评论（游戏评价）：COMMENT

当传入含评论更新时间（commentDelay）参数时，COMMENT表示主帖的评论；
当没有传评论更新时间（commentDelay）参数时，COMMENT表示仅游戏评价
taptap	论坛	板块名称	45	66	forum_name	主帖：POST
互动量：INTERACTION
评论：COMMENT

当传入含评论更新时间（commentDelay）参数时，COMMENT表示主帖的评论；
当没有传评论更新时间（commentDelay）参数时，COMMENT表示仅评论
懂车帝	新闻	用户URL	53	54	user_url	账号信息：USER
主帖（非账号信息时必填）：POST
互动量：INTERACTION
评论：COMMENT
懂车帝	口碑	车系	53	38	car_series	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
懂车帝	口碑	用户URL	53	38	user_url	账号信息：USER
主帖（非账号信息时必填）：POST
互动量：INTERACTION
评论：COMMENT
懂车帝	论坛	板块名称	53	43	forum_name	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
懂车帝	论坛	板块ID	53	43	forum_id	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
懂车帝	论坛	用户URL	53	43	user_url	账号信息：USER
主帖（非账号信息时必填）：POST
互动量：INTERACTION
评论：COMMENT
新浪汽车	新闻	板块名称	152	134	forum_name	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
百度贴吧	百度贴吧	板块名称	77	64	forum_name	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
NGA	NGA	板块名称	78	65	forum_names	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
Lofter	Lofter	话题	84	68	topic	主帖（必填）：POST
评论：COMMENT
好游快爆	游戏	游戏url	85	71	surl	主帖：POST
互动量：INTERACTION
评论（游戏评价）：COMMENT

当传入含评论更新时间（commentDelay）参数时，COMMENT表示主帖的评论；
当没有传评论更新时间（commentDelay）参数时，COMMENT表示仅游戏评价
好游快爆	论坛	板块名称	85	82	forum_name	主帖：POST
互动量：INTERACTION
评论：COMMENT

当传入含评论更新时间（commentDelay）参数时，COMMENT表示主帖的评论；
当没有传评论更新时间（commentDelay）参数时，COMMENT表示仅评论
小黑盒	游戏	游戏url	106	126	surl	主帖：POST
互动量：INTERACTION
评论（游戏评价）：COMMENT

当传入含评论更新时间（commentDelay）参数时，COMMENT表示主帖的评论；
当没有传评论更新时间（commentDelay）参数时，COMMENT表示仅游戏评价
小黑盒	论坛	板块名称	106	90	fourum_names	主帖：POST
互动量：INTERACTION
评论：COMMENT

当传入含评论更新时间（commentDelay）参数时，COMMENT表示主帖的评论；
当没有传评论更新时间（commentDelay）参数时，COMMENT表示仅评论
库街区	库街区	板块名称	101	83	forum_name	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
新出行	点评	车系	103	85	car_series	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
新出行	论坛	板块名称	103	87	forum_name	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
旅法师营地	旅法师营地	板块名称	104	88	forum_names	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT
凯恩之角	凯恩之角	板块名称	105	89	forum_names	主帖（必填）：POST
互动量：INTERACTION
评论：COMMENT


3、通用模块
3.1 停止任务（周期任务专用，但不适用于周期子任务）
基本信息
接口名称：停止任务
接口地址：https://dc.datastory.com.cn/job/stop
请求类型：HTTPS
请求方式：GET
响应格式：JSON
是否需要 token 访问：是

接口描述
停止正在运行的任务

请求头说明
参数名称	是否必须	类型	描述	默认值
Authorization	true	string	通过【登录接口】获取 token	
请求参数说明
参数名称	是否必须	类型	描述	默认值
id	true	number	聚合任务id	
返回字段说明
参数名称	类型	描述
success	boolean	接口请求是否成功
code	number	接口返回的错误编码
data	object	
message	string	接口返回的提示信息


3.2 重启任务（周期任务专用，但不适用于周期子任务）
基本信息
接口名称：启动任务

接口地址：https://dc.datastory.com.cn/job/restart

请求类型：HTTPS
请求方式：GET

响应格式：JSON

是否需要 token 访问：是

接口描述
启动已停止的任务

请求头说明
参数名称	是否必须	类型	描述	默认值
Authorization	true	string	通过【登录接口】获取 token	
请求参数说明
参数名称	是否必须	类型	描述	默认值
id	true	number	聚合任务id	
返回字段说明
参数名称	类型	描述
success	boolean	接口请求是否成功
code	number	接口返回的错误编码
data	object	
message	string	接口返回的提示信息


3.3 重跑任务（一次性或周期子任务专用）
基本信息
接口名称：重跑任务

接口地址：https://dc.datastory.com.cn/job/schedule/rerun

请求类型：HTTPS
请求方式：POST

请求格式：application/x-www-form-urlencoded
响应格式：JSON

是否需要 token 访问：是

接口描述
启动已停止的任务

请求头说明
参数名称	是否必须	类型	描述	默认值
Authorization	true	string	通过【登录接口】获取 token	
请求参数说明
参数名称	是否必须	类型	描述	默认值
id	true	number	任务实例id（注意任务id与任务实例id不同,可参见4.2查询任务及子任务状态）	
返回字段说明
参数名称	类型	描述
success	boolean	接口请求是否成功
code	number	接口返回的错误编码
data	object	
message	string	接口返回的提示信息, 比如：

任务不存在
余额不足，请联系管理员充值
任务处于'等待运行'或'运行中'，需终止方可重跑
调度不存在


3.4 终止任务（一次性或周期子任务专用）
基本信息
接口名称：终止任务

接口地址：https://dc.datastory.com.cn/job/schedule/kill

请求类型：HTTPS
请求方式：GET

响应格式：JSON

是否需要 token 访问：是

接口描述
终止运行中的任务

请求头说明
参数名称	是否必须	类型	描述	默认值
Authorization	true	string	通过【登录接口】获取 token	
请求参数说明
参数名称	是否必须	类型	描述	默认值
id	true	number	
任务实例id（注意任务id与任务实例id不同,可参见4.2查询任务及子任务状态）

返回字段说明
参数名称	类型	描述
success	boolean	接口请求是否成功
code	number	接口返回的错误编码
data	object	
message	string	接口返回的提示信息,举例：

调度服务器异常
停止调度任务失败




4、示例合集
4.1 数据搜索-创建任务请求示例
微博+快手-关键词
【任务条件】
关键词：(瑞幸|星巴克)+(美式|拿铁)；过滤词：抽奖
关键词匹配方式：内容，音频，花字
时间范围：2025-06-01 000000-2025-6-2 235959
数据源：微博，短视频
站点：微博，快手
主回帖类型：微博主回帖，快手主帖
抖音主帖类型：常规视频，常规图文
任务类型：快速取数，一次性任务
导出方式：导出到本地


【curl】

curl --location 'https://dc.datastory.com.cn/project/job/add' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--header 'Authorization: 替换成登录接口返回的token' \
--data-urlencode 'name=微博快手' \
--data-urlencode 'jobType=1' \
--data-urlencode 'sheetName=API任务' \
--data-urlencode 'searchCondition={"isFast":0,"startTime":1748707200000,"endTime":1748793600000,"sentiments":"1,0,-1","keywordFields":"content,audio_asr_content,video_highlight_content","source":"weibo,shortVideo","weiboMsgType":0,"shortVideoSite":"1334510","shortVideoMsgType":1,"kuaishouPostType":"video#0,image#0"}' \
--data-urlencode 'profiltersListStr=[{"name":"咖啡","keywords":"(瑞幸|星巴克)+(美式|拿铁)","filterwords":"抽奖"}]' \
--data-urlencode 'schedule={"emails":"your-email@example.com","isTemp":1,"unit":"d","interval":1}' \
--data-urlencode 'hdfs={"path":"/projects/datastory/titan/hermes","fileFormat":"csv"}'


【Python】

import requests
import json

# API配置
URL = 'https://dc.datastory.com.cn/project/job/add/'
HEADERS = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': (
        '替换成登录接口返回的token'
        )
    }

    data = {
        "name": "微博主回帖快手主帖",
        "jobType": 1,
        "sheetName": "API任务",
        "searchCondition": """{
        "isFast": 0,
        "startTime": 1748707200000,
        "endTime": 1748793600000,
        "source": "weibo,shortVideo",
        "weiboMsgType": 0,
        "shortVideoSite": "1334510",
        "shortVideoMsgType": 1,
        "sentiments": "0,1,-1",
        "keywordFields": "content,audio_asr_content,video_highlight_content",
        "kuaishouPostType": "video#0,image#0"
    }""",

    "profiltersListStr": """[
    {
        "name": "咖啡",
        "keywords": "(瑞幸|星巴克)+(美式|拿铁)",
        "filterwords": "抽奖"
    }
    ]""",

    "schedule": """{
        "emails": "your-email@example.com",
        "emailMode": 2,
        "isTemp": 1,
        "unit": "d",
        "interval": 1,
        "startTime": 1762310806000
    }""",

    "hdfs": """{
        "path": "/projects/datastory/titan/hermes",
        "fileFormat": "csv"
    }"""
    }



    # 发送请求
try:
    response = requests.post(URL, data=data, headers=HEADERS)
    response.raise_for_status()  # 检查请求是否成功

    # 打印响应结果
    print('Status Code:', response.status_code)
    print('Response:', response.text)

except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")


指定账号周期采集
【任务条件】

微博账号：1809745371
B站账号：352063206
时间范围：2025-10-01 000000-2025-10-31 235959
数据源：微博，视频
站点：微博，B站
主回帖类型：微博主帖，B站主帖
任务类型：快速取数，一次性任务
导出方式：导出到本地


curl --location 'https://dc.datastory.com.cn/project/job/add' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--header 'Authorization: 替换成登录接口返回的token' \
--header 'Cookie: dc-login-iden=.datastory.com.cn#c28b65da-3d29-4cba-9dd5-341da1124ff6; SESSION=47c71fb0-276a-4019-9e62-bf1d5f328656' \
--data-urlencode 'name=微博B站账号' \
--data-urlencode 'jobType=1' \
--data-urlencode 'sheetName=API任务' \
--data-urlencode 'searchCondition={"isFast":0,"startTime":1759248000000,"endTime":1761926399000,"sentiments":"1,0,-1","weiboFields":"content","weiboMsgType":1,"videoFields":"content,title","videoMsgType":1,"videoSite":"44","bilibiliPostType":"video","source":"weibo,video"}' \
--data-urlencode 'profiltersListStr=[{"name":"分析对象1","uid":"1809745371","biliAccId":"352063206"}]' \
--data-urlencode 'schedule={"emails":"your-email@example.com","emailMode":2,"isTemp":1,"unit":"d","interval":1,"startTime":1762312769000}' \
--data-urlencode 'hdfs={"path":"/projects/datastory/titan/hermes","fileFormat":"csv"}'


【python】



import requests
import json

# API配置
URL = 'https://dc.datastory.com.cn/project/job/add/'
HEADERS = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': (
        '替换成登录接口返回的token'
        )
    }

    data = {
        "name": "微博B站账号",
        "jobType": 1,
        "sheetName": "API任务",
        "searchCondition": """{
        "isFast": 0,
        "startTime": 1759248000000,
        "endTime": 1761926399000,
        "sentiments": "1,0,-1",
        "weiboMsgType": 1,
        "videoMsgType": 1,
        "videoSite": "44",
        "bilibiliPostType": "video",
        "source": "weibo,video"
    }""",
    "profiltersListStr": """[{
        "name": "分析对象1",
        "uid": "1809745371",
        "biliAccId": "352063206"
    }]""",
    "schedule": """{
        "emails": "your-email@example.com",
        "emailMode": 2,
        "isTemp": 1,
        "unit": "d",
        "interval": 1,
        "startTime": 1762310806000
    }""",
    "hdfs": """{
        "path": "/projects/datastory/titan/hermes",
        "fileFormat": "csv"
    }"""
    }


    # 发送请求
try:
    response = requests.post(URL, data=data, headers=HEADERS)
    response.raise_for_status()  # 检查请求是否成功

    # 打印响应结果
    print('Status Code:', response.status_code)
    print('Response:', response.text)

except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")


4.2 数据搜索-导出配置示例
数据搜索导出方式

# 如有ftp访问限制的，请联系管理员并提供数说ip设为白名单

# 在任务中传ftp参数
"ftp" :{

        "account":"xxx",#ftp账户
        "password":"xxx", #ftp密码
        "port":"21", # 开主动模式21
        "host": "120.31.140.156",  # FTP服务器地址
        "filename": "xxx",  # 文件名
        "filePath": "/cloud/data3/vsftp/dc", # 文件路径
        "fileFormat": "csv" # 文件格式
        "type": "ftp" # ftp服务器类型，分ftp和sftp
    }



    #导出到es
"es": {
        "cluster": "xxxx", # 集群名称
        "host": "xxx", # 集群地址
        "indexName": "xxx" # 索引名称
        "typeName": "xxx" # 索引类型,可不填

    }


    #导出到方舟新建数据源

    "matrix": {
        "projectId": "999999", #方舟项目id
        "dirId": "99999", #方舟文件夹id
        "datasourceName": "自定义数据源名称" #方舟数据源名称
    }



    # 导出到阿里云OSS- 需通过辅助接口获取connectId

"oss": {
        "engineType": "aliyunoss",
        "connectId": "xxx",  # 存储服务的唯一key，通过辅助接口获取
        "otherConfig": "{\"bucketName\":\"hg-bigdata-etl\"}", #存储桶名称
        "fileName": "xx", # 文件名称
        "path": "/xx/xx", #导出路径，以“/”开头
        "fileFormat": "csv" # 文件格式,csv或json

    }


    # 导出到腾讯云COS- 需通过辅助接口获取connectId

"oss": {
        "engineType": "tencentcos",
        "connectId": "xxx", #  存储服务的唯一key，通过辅助接口获取
        "otherConfig": "{\"bucketName\":\"xx\"}", #存储桶名称
        "fileName": "douyin", # 文件名称
        "path": "/xx", #导出路径，以“/”开头
        "fileFormat": "csv" # 文件格式,csv或json
    }

    # 导出到本地，任务运行完成后聚合前端页面下载
"hdfs": {
        "path":{}
    }


4.3 数据搜索-创建任务返回示例


{
    "message": null,
    "success": true,
    "code": 0,
    "data": 123456
}
data即为任务id

4.4 数据搜索-修改周期任务返回示例
只修改周期和抓取的结束时间
curl --location --request POST 'http://localhost:8080/project/job/modify' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'id=5186' \
--data-urlencode 'searchCondition={"isFast":"0","endTime":1601488800000}'


参数例子
id:5186
searchCondition:{"endTime":1601488800000}


    修改分析对象


curl --location --request POST 'http://localhost:8080/project/job/modify' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'id=5186' \
--data-urlencode 'searchCondition={"isFast":"0","qaSite":"101944","source":"qa,weibo","xiaohongshuMsgType":0}' \
--data-urlencode 'profiltersListStr=[{"filterwords":"招聘|何鸿燊|网络|赌博|杀猪|赌王|曾荫权|孙小果|捕鱼|足球盘口|下了一场秋雨|nba投注|网投|网络赌博|赌博网址|德州扑克|十三水|二八杠|抢庄牌九|血战麻将|抢庄大战|买球网址|足球投注|足球竞技|老虎机|冰球突破|现金网|8N球|我王赢别|谦虚镶边|网上娱乐平台|总站网址|下载网址|唯一官网|30情定水舞间","keywords":"澳门 银河|澳門 銀河|Galaxy Macau|澳门 Galaxy|银河 Macau|Broadway Macau|澳门 百老汇|StarWorld macau|澳门 星际酒店|ChaBei Galaxy|茶杯 银河|澳门 利兹卡尔顿|澳门 丽思卡尔顿|Macau Ritz-Carlton|澳门 悦榕庄|Macau Banyan Tree|路氹泉悦套房|澳门 万豪|Macau JW Marriott|Macau Hotel Okura|澳门 大仓|UA银河影院|UA Galaxy Cinemas|UA銀河影院|UA影院|银河UA|澳门 红伶|澳門 紅伶|China Rouge Macau|Grand Resort Deck|天浪淘园|天浪淘園|Promenade Shops|澳门 时尚汇|银河时尚汇|澳门 怡世宝水疗|澳门 JW儿童乐园|银娱优越会|澳门 悦涛廊|澳门 丽轩|Macau Laiheen|澳门 蒙特卡洛巴黎咖啡馆|澳门 DEAN&DELUCA|澳门 钻石大堂|银河 钻石表演|运财巨钻","name":"对象名称"}]'


参数例子
id:5186
searchCondition:{"qaSite":"101944","source":"qa,weibo","xiaohongshuMsgType":0}
    profiltersListStr:[{"filterwords":"招聘|何鸿燊|网络|赌博|杀猪|赌王|曾荫权|孙小果|捕鱼|足球盘口|下了一场秋雨|nba投注|网投|网络赌博|赌博网址|德州扑克|十三水|二八杠|抢庄牌九|血战麻将|抢庄大战|买球网址|足球投注|足球竞技|老虎机|冰球突破|现金网|8N球|我王赢别|谦虚镶边|网上娱乐平台|总站网址|下载网址|唯一官网|30情定水舞间","keywords":"澳门 银河|澳門 銀河|Galaxy Macau|澳门 Galaxy|银河 Macau|Broadway Macau|澳门 百老汇|StarWorld macau|澳门 星际酒店|ChaBei Galaxy|茶杯 银河|澳门 利兹卡尔顿|澳门 丽思卡尔顿|Macau Ritz-Carlton|澳门 悦榕庄|Macau Banyan Tree|路氹泉悦套房|澳门 万豪|Macau JW Marriott|Macau Hotel Okura|澳门 大仓|UA银河影院|UA Galaxy Cinemas|UA銀河影院|UA影院|银河UA|澳门 红伶|澳門 紅伶|China Rouge Macau|Grand Resort Deck|天浪淘园|天浪淘園|Promenade Shops|澳门 时尚汇|银河时尚汇|澳门 怡世宝水疗|澳门 JW儿童乐园|银娱优越会|澳门 悦涛廊|澳门 丽轩|Macau Laiheen|澳门 蒙特卡洛巴黎咖啡馆|澳门 DEAN&DELUCA|澳门 钻石大堂|银河 钻石表演|运财巨钻","name":"对象名称"}]


4.5 数据搜索-停止任务返回示例
{
    "message": null,
    "success": true,
    "code": 0,
    "data": true
}
4.6 数据搜索-重启任务返回示例
{
    "message": null,
    "success": true,
    "code": 0,
    "data": true
}
4.7 数据搜索-重跑任务返回示例
{
    "message": null,
    "success": true,
    "code": 0,
    "data": null
}
4.8 数据超市-创建任务请求示例
示例：微博，根据单帖url周期性采集主贴和评论
【任务条件】

站点：微博

时间范围：2025年10月1日0点0分0秒-2025年11月7日23时59分59秒

采集内容：主帖，互动量评论

周期：互动量每天1次，评论每天1次



【curl】

curl --location 'https://dc.datastory.com.cn/application/market/job/v1/run' \
--header 'Content-Type: application/json' \
--header 'Authorization: 替换成登录接口返回的token' \

--data-raw '{

        "jobName": "单帖URL连续更新互动量和评论",
        "sheetId": 3463,
        "appId": 6,
        "scopeId": 4,
        "globalConfig": {
        "email": "your-email@example.com",
        "emailMode": 2,
        "isRealTime": {
        "COMMENT": 0,
        "INTERACTION": 0,
        "POST": 0
    }
    },
        "scheduleConfig": {
        "commentDelay": 1,
        "commentDelayUnit": "d",
        "startDataTime": 1759248000000,
        "endDataTime": 1762531199000,
        "interactionDelay": 1,
        "interactionDelayUnit": "d",
        "interval": 1,
        "type": "SIMPLE",
        "unit": "d"
    },
        "sourceConfig": {
        "condition": [
    {
        "url": "https://weibo.com/1809745371/Q9z044Ara,https://weibo.com/1809745371/Q8itRsmdp",
        "name": "分析对象1"
    }
        ],
        "input": "surl",
        "output": [
        "POST",
        "INTERACTION",
        "COMMENT"
        ]
    },
        "exportConfig": {
        "local": {}
    }
    }'


【python】




import requests
import json

url = 'https://dc.datastory.com.cn/application/market/job/v1/run'
headers = {'Content-Type': 'application/json','Authorization':'替换成登录接口返回的token'}

    # 构建请求体数据
requestData = {
    # 基础信息-任务名称，站点信息
    "jobName": "单帖URL连续更新互动量和评论",
    "appId": 6,  #站点标识
    "scopeId":4, #站点区域标识
    "sheetId": "51364", #文件夹id，对应聚合任务链接的jobsId

    "scheduleConfig": {
    "startDataTime":1759248000000, # 数据开始时间
    "endDataTime": 1762531199000, # 数据结束时间
    "type": "SIMPLE", # 任务调度类型，TEMP-一次性任务，SIMPLE-周期任务
    "unit": "d", # 任务运行单位，天
    "interval": 1, # 周期运行周期，表示1天运行1次任务
    "commentDelayUnit": "d",  # 评论任务的单位
    "commentDelay":1, # 评论任务每天1次
    "interactionDelayUnit": "d", # 互动量任务的运行单位，按天
    "interactionDelay": 1  # 互动量任务每天1次

},

    # 分析对象设置
    "sourceConfig": {
    "condition":
    #分析对象列表
    [
{
    "name": "分析对象1",
    "url": "https://weibo.com/1809745371/Q9z044Ara,https://weibo.com/1809745371/Q8itRsmdp",
}

    ],

    "input": "surl",  # 输入类型，单帖URL

    # 采集内容，主帖（区分主帖类型），互动量+评论
    "output": [
    "POST",
    "INTERACTION",
    "COMMENT"
    ]

},

    # 快速或在线取数，邮件配置
    "globalConfig": {
    "email": "your-email@example.com",
    "emailMode": 2,
    "isKeepTrend": False,
    "isRealTime": {
    "COMMENT": 1,
    "INTERACTION": 1,
    "POST": 1
}
},
    # 导出方式
    "exportConfig": {
    "local": {}

}
}


    # 发送POST请求
response = requests.post(url, data=json.dumps(requestData), headers=headers)

# 输出响应数据
print(response.text)


示例：快手-关键词-每天1次-主帖+互动量+评论
【任务条件】

站点：快手

时间范围：2025年12月1日0点0分0秒-12月31日23点59分59秒

2组关键词：分析对象1：vivo+手机；分析对象2：oppo+手机

采集内容：主帖（常规视频+常规图文），互动量，评论

周期频率：主帖每天1次，评论T+1天，互动量T+1天

取数范围：关键词每天获取近2天的主帖（为了补充部分晚入库的主帖）





【curl】

curl --location 'https://dc.datastory.com.cn/application/market/job/v1/run' \
--header 'Content-Type: application/json' \
--header 'Authorization: 替换成登录接口返回的token' \

--data-raw '{

        "jobName": "快手关键词主帖互动量评论周期",
        "sheetId": 3463,
        "appId": 12,
        "scopeId": 6,

        "globalConfig": {
        "email": "your-email@example.com",
        "emailMode": 2,
        "isRealTime": {
        "COMMENT": 0,
        "INTERACTION": 0,
        "POST": 0
    }
    },


        "scheduleConfig": {
        "commentDelay": 1,
        "commentDelayUnit": "d",
        "endDataTime": 1767196799000,
        "interactionDelay": 1,
        "interactionDelayUnit": "d",
        "interval": 1,
        "schedStartTime": 1764604800000,
        "searchStartTime": 2,
        "searchUnit": "d",
        "startDataTime": 1764518400000,
        "type": "SIMPLE",
        "unit": "d"
    },

        "sourceConfig": {
        "condition": [
    {
        "filterwords": "",
        "keywords": "vivo+手机",
        "name": "分析对象1"
    },
    {
        "filterwords": "",
        "keywords": "oppo+手机",
        "name": "分析对象2"
    }
        ],

        "input": "keyword",
        "matchType": [
        "content",
        "title"
        ],
        "output": [
        "POST-video#0",
        "POST-image#0",
        "INTERACTION",
        "COMMENT"
        ]
    },
        "exportConfig": {
        "local": {}
    }
    }'


【python】

import requests
import json

url = 'https://dc.datastory.com.cn/application/market/job/v1/run'
headers = {'Content-Type': 'application/json','Authorization':'替换成登录接口返回的token'}

    # 构建请求体数据
requestData = {

        "jobName": "快手关键词主帖互动量评论周期",
        "appId": 12,  #站点标识
        "scopeId": 6, #站点区域标识
        "sheetId": "3463", #文件夹id，对应聚合任务链接的jobsId
        
　# 任务调度配置
        "scheduleConfig": {
        "startDataTime": 1764518400000, # 数据开始时间
        "endDataTime": 1767196799000, # 数据结束时间
        "type": "SIMPLE", # 任务调度类型，TEMP-一次性任务，SIMPLE-周期任务
        "unit": "d", # 任务运行单位，d-日,H-小时
        "interval": 1, # 周期运行周期，表示1天运行1次任务
        "commentDelayUnit": "d",  # 评论任务的单位
        "commentDelay":1, # 评论任务T+1
        "interactionDelayUnit": "d", # 互动量任务的运行单位，按天
        "interactionDelay": 1,  # 互动量任务每T+1天
        "searchUnit": "d", # 取数时间间隔的单位，最近1天或最近2天
        "searchStartTime": 2 # 取数时间间隔的数值，最近1天或最近2天

    },

        # 分析对象设置
        "sourceConfig": {
        "condition":
        #分析对象列表
        [
    {
        "name": "分析对象1",
        "keywords": "vivo+手机",
        "filterwords": ""
    },
    {
        "name": "分析对象2",
        "keywords": "oppo+手机",
        "filterwords": ""
    }
        ],

        "input": "keyword",  # 输入类型关键词
        # 关键词匹配方式
        "matchType": [
        "content",
        "title"
        ],
        # 采集内容，主帖（区分主帖类型），互动量+评论
        "output": [
        "POST-video#0",
        "POST-image#0",
        "INTERACTION",
        "COMMENT"
        ]

    },

        # 快速或在线取数，邮件配置
        "globalConfig": {
        "email": "your-email@example.com",
        "emailMode": 2,
        "isKeepTrend": False,
        "isRealTime": {
        "COMMENT": 0,
        "INTERACTION": 0,
        "POST": 0
    }
    },
        # 导出方式
        "exportConfig": {
        "local": {}

    }
    }


    # 发送POST请求
response = requests.post(url, data=json.dumps(requestData), headers=headers)

# 输出响应数据
print(response.text)

4.9 数据超市-导出配置示例

# 导出到ES- 配置信息咨询管理员

"exportConfig": {
    "es": {
    "cluster": "xxxx", # 集群名称
    "host": "xxx", # 集群地址
    "indexName": "xxx" # 索引名称
    "typeName": "xxx" # 索引类型,可不填
}
}


    #导出到方舟新建数据源

"exportConfig": {
    "matrix": {
    "projectId": "999999", #方舟项目id
    "dirId": "99999", #方舟文件夹id
    "datasourceName": "自定义数据源名称" #方舟数据源名称
}
}
    <br/>
# 如有FTP访问限制的，请联系管理员并提供数说ip设为白名单
# 导出到FTP-先通过辅助接口注册ftp获取id,创建任务时传入id

"exportConfig":{
    "ftp": {
    "filePath": "/xxx", #文件路径
    "filename": "xxx", #文件名称
    "id": "xx",  #通过辅助接口获取
    "fileFormat": "csv" #文件格式,csv或json
}
}


    # 导出到阿里云OSS- 需通过辅助接口获取connectId

"exportConfig": {
    "aliyunoss": {
    "name": "aliyunoss",
    "connectId": "xxx",  # 存储服务的唯一key，通过辅助接口获取
    "otherConfig": "{\"bucketName\":\"hg-bigdata-etl\"}", #存储桶名称
    "fileName": "xx", # 文件名称
    "path": "/xx/xx", #导出路径，以“/”开头
    "fileFormat": "csv" # 文件格式,csv或json

}
}

    # 导出到腾讯云COS- 需通过辅助接口获取connectId

"exportConfig": {
    "tencentcos": {
    "name": "tencentcos",
    "connectId": "xxx", #  存储服务的唯一key，通过辅助接口获取
    "otherConfig": "{\"bucketName\":\"xx\"}", #存储桶名称
    "fileName": "douyin", # 文件名称
    "path": "/xx", #导出路径，以“/”开头
    "fileFormat": "csv" # 文件格式,csv或json
}
}
<br/>
    # 导出到本地
   "exportConfig":<span style="font-family: &quot;Helvetica Neue&quot;, Helvetica, &quot;PingFang SC&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, SimSun, sans-serif, Arial;"> {</span>
        "local": {}
        }
    