from django.db import models

# Create your models here.

from django.db import models


# 这里设置用户名为这个用户数据表的主键
# limits表示用户的权限，这里规定admin的权限为5，普通用户的权限为2，游客的权限为1。
# 设置权限也是为了后面对某一类用户的数据进行清理。
class UserData(models.Model):
    username = models.CharField(max_length=16, primary_key=True)
    password = models.CharField(max_length=16)
    limits = models.IntegerField()


# 这个是记录用户搜索浏览记录数据，让其自己加一个自增的主键就好
class RecordViaUsername(models.Model):
    username = models.CharField(max_length=16)
    search = models.CharField(max_length=64)


# 这是记录用户点击记录数据
class ButtonClick(models.Model):
    # 展示页的文物
    antique1 = models.CharField(max_length=64)
    # 感性趣点击的文物
    antique2 = models.CharField(max_length=64)
    # 点击发生时的时间
    time = models.IntegerField()


# 记录用户推荐过程的数据
class RecommendRecord(models.Model):
    MainAntique = models.CharField(max_length=64)
    recommend = models.CharField(max_length=64)
    antique1 = models.CharField(max_length=64)
    antique2 = models.CharField(max_length=64)
    antique3 = models.CharField(max_length=64)
    antique4 = models.CharField(max_length=64)
    antique5 = models.CharField(max_length=64)
    antique6 = models.CharField(max_length=64)
    antique7 = models.CharField(max_length=64)
    time = models.IntegerField()
