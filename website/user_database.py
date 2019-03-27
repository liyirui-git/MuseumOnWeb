from website.models import UserData, RecordViaUsername


# 向用户数据库中添加一个项
def add_to_db(name, pw, lim):
    user = UserData(username=name, password=pw, limits=lim)
    user.save()


# 返回1表示账号密码正确，返回-1表示账号存在密码错误，返回-2表示账号不存在。
def log_in(name, pw):
    result = UserData.objects.get(username=name)
    if result is not None:
        if result.password == pw:
            return 1
        else:
            return -1
    else:
        return -2


def add_to_record(name, search):
    record = RecordViaUsername(username=name, search=search)
    record.save()
