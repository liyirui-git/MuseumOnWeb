from website.models import UserData, RecordViaUsername, ButtonClick, RecommendRecord, SearchRecord


# 返回1表示账号密码正确，返回-1表示账号存在密码错误，返回-2表示账号不存在。
def log_in(name, pw):
    try:
        result = UserData.objects.get(username=name)
        if result.password == pw:
            return 1
        else:
            return -1
    except:
        return -2


# 向用户数据库中添加一个项
def add_to_db(name, pw, lim):
    user = UserData(username=name, password=pw, limits=lim)
    user.save()


# 向用户使用记录表添加一个项
def add_to_record(name, search):
    record = RecordViaUsername(username=name, search=search)
    record.save()


# 向点击跳转记录表添加一次点击跳转
def add_to_click(name1, name2, time):
    click = ButtonClick(antique1=name1, antique2=name2, time=time)
    click.save()


def add_to_recommend_record(ma, re, time, a1, a2, a3, a4, a5, a6, a7):
    r_record = RecommendRecord(MainAntique=ma, recommend=re, time=time, antique1=a1, antique2=a2, antique3=a3,
                               antique4=a4, antique5=a5, antique6=a6, antique7=a7)
    r_record.save()


def add_to_search_record(username, search, time, valid):
    s_record = SearchRecord(username=username, search=search, time=time, valid=valid)
    s_record.save()