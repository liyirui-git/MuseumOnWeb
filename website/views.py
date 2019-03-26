from django.shortcuts import render
from .user_database import add_to_db, log_in
from .search import click_search
from .connect_d2rq import *
import time
# Create your views here.


def register(request):
    # 从注册页准备注册，就开启D2RQ线程
    thread_d2rq = D2RQ()
    thread_d2rq.start()
    return render(request, "register.html")


def index(request):
    if request.method == 'POST':
        # 注册
        if 'register' in request.POST:
            username = request.POST.get("username", None)
            password = request.POST.get('password', None)
            add_to_db(username, password, 2)
            return render(request, "index.html")
        # 登录
        elif 'login' in request.POST:
            username = request.POST.get("username", None)
            password = request.POST.get("password", None)
            retu = log_in(username, password)
            if retu == 1:
                return render(request, "index.html")
            elif retu == -2:
                return render(request, "error_602.html")
            else:
                return render(request, "error_603.html")
        # 游客登录用时间戳来实现用户名
        elif 'tourist' in request.POST:
            username = 'u'+str(int(time.time()))
            password = 'u'+str(int(time.time()))
            add_to_db(username, password, 1)
            return render(request, "index.html")
        elif 'search_submit' in request.POST:
            # 这个地方通过一个函数，把search_content传到后端，然后接收后端传过来的结果返回给网页。
            result_return = {}
            search_content = request.POST.get("search_content", None)
            result = click_search(search_content).split("【相关文物】：\n")
            result_return['return_result'] = result[0]
            if len(result) > 1:
                recommend_list = result[1].split('\n')
                # 因为由于格式的原因，划分完以后，最后一个元素是个空
                recommend_list.pop()
                result_return['recommend'] = recommend_list
                return render(request, "index.html", result_return)
            else:
                return render(request, "index.html")
        else:
            return render(request, "index.html")
    else:
        return render(request, "error_601.html")
    # 这一句else是防止直接从index进入系统，为了必须先注册再登录，但现在遇到一点问题，所以先注释掉
    # else:
        # return render(request, "error_601.html")


def index_addition(request, antique_name):
    result_return = {}
    search_content = antique_name
    result = click_search(search_content).split("【相关文物】：\n")
    result_return['return_result'] = result[0]
    recommend_list = result[1].split('\n')
    # 因为由于格式的原因，划分完以后，最后一个元素是个空
    recommend_list.pop()
    result_return['recommend'] = recommend_list
    return render(request, "index.html", result_return)
