# 智慧博物馆网站版
## 一、文件结构
```
-- MuseumOnWeb_v0
------ \_\_init__.py: Django自动生成的，存在的意义是使得Pycharm认为这是一个项目
------ settings.py: 相关的配置
------ urls.py: 控制从url到views.py中函数或者说到html网页的映射
------ wsgi.py: 网络连接相关的
-- static: 用来存放一些静态网页的资源
-- templates: 用来存放网页模板
-- venv: Pycharm自动生成的Python37的环境。为保证程序的可移植性，最好把虚拟环境创建在每个项目里面
-- website
------ \_\_init__.py: Django自动生成的，存在的意义是使得Pycharm认为这是一个项目
------ admin.py:
------ apps.py:
------ connect_d2rq.py: 这个是从我之前暑假的项目MuseumOffine里面直接移植过来的，主要负责开启D2RQ的服务
------ lexical_qnalyzer.py: 这个也是从我之前暑假的项目MuseumOffline里面直接移植过来的，主要是调用了THULAC的分词库，实现分词。
------ models.py: Django的模型文件，负责在MySQL中创建一个表，我这里让其创建的是用户登录信息表。
------ network_graph.py: 使用pyecharts的库，生成关系图。
------ search_old.py: 只有一个函数，就是click_search，这个是也是从暑假的项目移过来以后稍微做了一些修改，从之前将数据传给GUI的控件改为了返回一个字符串。它负责处理网页搜索框中用户输入的文本。
------ search.py: 之前的通过SPARQL进行交互的程序留在了search_old.py里面，这里从新构造了一个配合search_via_sql.py完成交互的查询。
------ search_via_sparql.py: 这个也是从我暑假的项目里面移植过来的，负责通过SPARQL语言在localhost:2020端口与D2RQ进行交互。
------ search_via_sql.py: 这个是新建的一个通过SQL语句与MySQL进行直接的交互，
------ user_database.py 负责与MySQL进行交互
------ views.py 负责控制视图，和应对网页的中被触发的请求，是urls与html之间的桥梁。
-- db.sqlite3: sqlite3是Django自带的一个小型的数据，可能是与其有关
-- error_list: 报错信息对照表
-- manage.py: Django自动生成的文件。
```
## 二、有关外部包
主要用到的外部的包有：
- pyecharts==0.5.11（这里主要原因是pyecharts 1.0版本不再向下兼容，安装方法为“pip install pyecharts==0.5.11”）
【补充说明】在重新安装配置pyecharts的过程中，本人遇到了contextvar.py文件报错：找不到模块“_contextvar.py”。但是发现在pycharm中ctrl加左键点击能够打开文件“_contextvar.py”
于是找到_contextvar.py文件所处的位置，将该文件移动到contextvar.py所处的文件夹下即可。
- thulac
- mysqlclient
- django

## 三、写给自己
##### 1.在Terminal中启动
输入命令 
'''
C:\ProgramFiles\Anaconda3\python manage.py runserver 0.0.0.0:8080
'''

##### 2.在docker中运行
在docker容器中运行的话，需要先激活 `(museum)` conda环境，然后去到 `/home/MuseumOnWeb` 文件夹下，运行命令：
```
PYTHONIOENCODING=utf8 python manage.py runserver 0.0.0.0:8080
```

