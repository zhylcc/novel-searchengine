#### 项目描述
> 本项目实现了《元尊》的关键词检索和特定信息提取系统
+ novelspider
	> 爬虫模块
	+ 将爬取的小说内容以本地txt文件的形式保存在`/novelspider/novelspiderout/`下
		> 非必要
	+ 在本地mongodb数据库表`coursework2_db.novel_origin`中写入各章节 __序号、标题、内容、内容长度和索引标志__ 字段信息
		> 索引模块需要，索引构建后可删除
	+ 数据库文件已导出：`/novelspider/yuanzun.json`
+ indexrequest
	> 索引模块
	+ 根据写入的数据库内容建立索引并提供信息查询和提取方法
	+ 索引字段与数据库字段一致，索引文件保存在`/indexrequest/index/`下
		> 必要
	+ 查询结果按 __序号__ 字段升序排列，突出关键词
	+ 提取信息包括 __关键词、修饰、地点、年龄、时间和出现频次__
+ searchengine
	> 引擎模块
	+ 交互界面，调用索引模块的方法获取数据并显示在网页上
	+ 包含 __主页、检索结果页、信息提取页__

#### 运行环境要求
1. Python版本：`Python3.8`
2. 安装依赖三方包：`requests.txt`

#### 运行方式
1. 直接使用
	+ 运行`/searchengine/runserver.py`
	+ 浏览器窗口进入**127.0.0.1:8000**
	> 注意：仅支持在主页进行检索，即每次检索后需手动返回主页
2. 完整运行
	+ 删除已保存的本地相关文件
		+ 小说章节内容文件夹（若有）：`/novelspider/novelspiderout/`
		+ 本地数据库表（若有）：`coursework2_db.novel_origin`
		+ 索引文件夹（必有）：`/indexrequest/index/`
	+ 运行爬虫模块启动文件：`/novelspider/startspider.py`
	+ 运行索引模块构建文件：`/indexrequest/indexbuilder.py`
		> 需要等待爬虫完成
	+ 运行引擎模块启动文件：`/searchengine/runserver.py`
		> 需要等待索引完成，启动后保持运行，退出时手动关闭