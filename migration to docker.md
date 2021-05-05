## docker中MySQL的配置

在这里使用的是ubuntu:18.04+mysql5.7。

我的项目适配mysql8.0+似乎存在一些问题。

#### 环境搭建

需要先在docker中安装mysql，相关教程比较多而且步骤也比较简单，可以参考链接：[Ubuntu下配置MySQL](https://liyirui-git.github.io/tech/%E6%8A%98%E8%85%BE/MySQL_in_Ubuntu.html)  就不在这里赘述了。

或者可以直接下载我搭建好的docker环境：

```
$ docker pull li1rui/mysql-5.7-ubuntu-18.04:0.2
```

在docker里面需要通过命令，启动mysql服务

```
$ service mysql start
```

#### Debug

此时遇到**问题**：

```
MySQLdb._exceptions.OperationalError: (2002, "Can't connect to local MySQL server through socket '/tmp/mysql.sock' (2)")
```

解决方法，将代码中调用MySQLdb的地方，ip从"localhost"改为"127.0.0.1"：

```python
# db_antique = MySQLdb.connect('localhost', 'root', '123456', 'museumdb_new', charset='utf8')
db_antique = MySQLdb.connect('127.0.0.1', 'root', '123456', 'museumdb_new', charset='utf8')
```

之后便遇到了访问被拒绝的**问题**：

```
MySQLdb._exceptions.OperationalError: (1698, "Access denied for user 'root'@'localhost'")
```

进入到mysql中，可以看到如下结果：

```sql
mysql> USE mysql;
mysql> SELECT User, Host, plugin FROM mysql.user;
+------------------+-----------+-----------------------+
| User             | Host      | plugin                |
+------------------+-----------+-----------------------+
| root             | localhost | auth_socket           |
| mysql.session    | localhost | mysql_native_password |
| mysql.sys        | localhost | mysql_native_password |
| debian-sys-maint | localhost | mysql_native_password |
+------------------+-----------+-----------------------+
```

可以看到，the `root` user is using the `auth_socket` plugin，解决方法：

```sql
mysql> USE mysql;
mysql> UPDATE user SET plugin='mysql_native_password' WHERE User='root';
mysql> SELECT User, Host, plugin FROM mysql.user;
+------------------+-----------+-----------------------+
| User             | Host      | plugin                |
+------------------+-----------+-----------------------+
| root             | localhost | mysql_native_password |
| mysql.session    | localhost | mysql_native_password |
| mysql.sys        | localhost | mysql_native_password |
| debian-sys-maint | localhost | mysql_native_password |
+------------------+-----------+-----------------------+
```

现在看已经修改了，继续执行后面几步：

```
mysql> FLUSH PRIVILEGES;
mysql> exit;

$ sudo service mysql restart
```

此时遇到问题：

```
MySQLdb._exceptions.OperationalError: (1045, "Access denied for user 'root'@'localhost' (using password: YES)")
```

此时用命令：`mysql -u root -p` 也不能成功登录，报错信息也是：

```
ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: YES)
```

大概是root的密码出了问题，解决方法如下：

先停止MySQL的服务：

```
$ /etc/init.d/mysql stop
```

执行下面的命令，以不检查密码的方式登录

```
$ mysqld_safe --user=mysql --skip-grant-tables --skip-networking &
```

使用root登录mysql数据库

```
mysql -u root mysql
```

更新root的密码为 123456，需要注意版本问题：

mysql5.7以下版本

```
mysql> UPDATE mysql.user SET Password=PASSWORD('123456') where USER='root';
```

mysql5.7版本：

```
mysql> UPDATE mysql.user SET authentication_string=PASSWORD('123456') where USER='root';
```

刷新权限：

```
mysql> flush privileges;
```

退出

```
mysql> exit
```

重新登录

```
mysql> mysql -uroot -p
```

发现问题已经解决，同时manage.py的报错变成了找不到数据库，所以问题解决，后续便是创建数据库。



#### 创建数据库

将之前备份下来的sql文件导入到MySQL数据库中

我这里备份下来两个sql文件，分别对应之前的两个数据库

```
museumdb_new.sql
museum_website_v0.sql
```

具体的导入方法也可以参考：[Ubuntu下配置MySQL](https://liyirui-git.github.io/tech/%E6%8A%98%E8%85%BE/MySQL_in_Ubuntu.html)



## 项目运行

项目运行所需要的命令：

```
PYTHONIOENCODING=utf8 python manage.py runserver 0.0.0.0:8080
```

