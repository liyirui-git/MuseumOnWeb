from django.shortcuts import render
from .user_database import add_to_db, log_in, add_to_record
from .search import click_search
from .connect_d2rq import *
from .network_graph import graph
import time
# Create your views here.


def register(request):
    # print(request.META)
    # 从注册页准备注册，就开启D2RQ线程
    thread_d2rq = D2RQ()
    thread_d2rq.start()
    return render(request, "register.html")


def index_redirect(request):
    path = request.get_full_path()
    print(path)
    new_path = {}
    if request.method == 'POST':
        # 注册
        if 'register' in request.POST:
            username = request.POST.get("username", None)
            password = request.POST.get('password', None)
            add_to_db(username, password, 2)
            new_path['new_url'] = path + "=" + username + '/'
            return render(request, "temp.html", new_path)
        # 登录
        elif 'login' in request.POST:
            username = request.POST.get("username", None)
            password = request.POST.get("password", None)
            retu = log_in(username, password)
            new_path['new_url'] = path + "=" + username + '/'
            if retu == 1:
                return render(request, "temp.html", new_path)
            elif retu == -2:
                return render(request, "error_602.html")
            else:
                return render(request, "error_603.html")
        # 游客登录用时间戳来实现用户名
        elif 'tourist' in request.POST:
            username = 'u'+str(int(time.time()))
            password = 'u'+str(int(time.time()))
            add_to_db(username, password, 1)
            new_path['new_url'] = path + "=" + username + '/'
            return render(request, "temp.html", new_path)

'''
def index(request):
    # print(request.META)
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
            result_dic = click_search(search_content)
            # result_return['return_result'] = result[0]
            result_return['network_graph'] = graph(result_dic)
            if 'relevant' in result_dic and len(result_dic['relevant']) > 1:
                recommend_list = result_dic['relevant']
                result_return['recommend'] = recommend_list
                return render(request, "index.html", result_return)
            else:
                return render(request, "index.html", result_return)
        else:
            return render(request, "index.html")
    else:
        return render(request, "error_601.html")
    # 这一句else是防止直接从index进入系统，为了必须先注册再登录，但现在遇到一点问题，所以先注释掉
    # else:
        # return render(request, "error_601.html")

'''


def index_addition(request, info):
    result_return = {}
    antique_name = info.split('=')[0]
    # 这个user_name就是用户名了。
    user_name = info.split('=')[1]
    if request.method == 'POST' and 'search_submit' in request.POST:
        search_content = request.POST.get("search_content", None)
        result_dic = click_search(search_content)
        if 'name' in result_dic:
            add_to_record(user_name, result_dic['name'])
        result_return['network_graph'] = graph(result_dic)
        result_return['username'] = user_name
        if 'museum' in result_dic:
            if result_dic['museum'] == '中国国家博物馆':
                result_return['image_path'] = '/images/chn_pic/' + result_dic['number'][1:] + '.jpg'
            elif result_dic['museum'] == '故宫博物院':
                result_return['image_path'] = '/images/dpm_pic/' + result_dic['number'][1:] + '.jpg'
        if 'relevant' in result_dic and len(result_dic['relevant']) >= 1:
            recommend_list = result_dic['relevant']
            result_return['recommend'] = recommend_list
            return render(request, "index.html", result_return)
        else:
            return render(request, "index.html", result_return)
    else:
        result_dic = click_search(antique_name)
        result_return['network_graph'] = graph(result_dic)
        result_return['username'] = user_name
        if 'museum' in result_dic:
            if result_dic['museum'] == '中国国家博物馆':
                result_return['image_path'] = '/images/chn_pic/' + result_dic['number'][1:] + '.jpg'
            elif result_dic['museum'] == '故宫博物院':
                result_return['image_path'] = '/images/dpm_pic/' + result_dic['number'][1:] + '.jpg'
        if 'name' in result_dic:
            add_to_record(user_name, result_dic['name'])
        if 'relevant' in result_dic and len(result_dic['relevant']) >= 1:
            recommend_list = result_dic['relevant']
            result_return['recommend'] = recommend_list
            return render(request, "index.html", result_return)
        else:
            return render(request, "index.html", result_return)