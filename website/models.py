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


# 这里就不认为设计主键了，让他自己设置一个id自增。
# username是用户名，inforname是查询的文物名。
class UsingRecords(models.Model):
      username = models.CharField(max_length=16)
      inforname = models.CharField(max_length=32)
