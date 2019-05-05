from django.shortcuts import render
from .user_database import add_to_db, log_in, add_to_record, add_to_recommend_record, add_to_search_record
from .search import click_search
from .connect_d2rq import *
from .network_graph import graph
import time
# Create your views here.

defult_recommend = ['后母戊鼎',
                    '张择端清明上河图卷',
                    '【搜索】兰亭序',
                    '红地描金囍字碗',
                    '掐丝珐琅缠枝莲纹梅瓶',
                    '窑变釉梅瓶',
                    '孝端皇后凤冠',
                    '紫檀嵌珐琅重檐楼阁更钟']


def register(request):
    # print(request.META)
    # 从注册页准备注册，就开启D2RQ线程
    # thread_d2rq = D2RQ()
    # thread_d2rq.start()
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
            new_path['new_url'] = path + "=" + username + '=/'
            return render(request, "temp.html", new_path)
        # 登录
        elif 'login' in request.POST:
            username = request.POST.get("username", None)
            password = request.POST.get("password", None)
            retu = log_in(username, password)
            new_path['new_url'] = path + "=" + username + '=/'
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
            new_path['new_url'] = path + "=" + username + '=/'
            return render(request, "temp.html", new_path)


def index_addition(request, info):
    result_return = {}
    antique_name = info.split('=')[0]
    # 这个user_name就是用户名了。
    user_name = info.split('=')[1]
    # 这个 is_button_jump 表示
    old_antique_name = info.split('=')[2]
    if len(old_antique_name) >= 1 and len(antique_name) >= 1 and \
            request.method == 'POST' and 'recommend_button' in request.POST:
        the_list = request.POST.get("hidden_list", None).split()
        i = 0
        antique1 = ''
        antique2 = ''
        antique3 = ''
        antique4 = ''
        antique5 = ''
        antique6 = ''
        antique7 = ''
        if the_list[i] != antique_name:
            antique1 = the_list[i]
            i = i + 1
        else:
            i = i + 1
            antique1 = the_list[i]
        if the_list[i] != antique_name:
            antique2 = the_list[i]
            i = i + 1
        else:
            i = i + 1
            antique2 = the_list[i]
        if the_list[i] != antique_name:
            antique3 = the_list[i]
            i = i + 1
        else:
            i = i + 1
            antique3 = the_list[i]
        if the_list[i] != antique_name:
            antique4 = the_list[i]
            i = i + 1
        else:
            i = i + 1
            antique4 = the_list[i]
        if the_list[i] != antique_name:
            antique5 = the_list[i]
            i = i + 1
        else:
            i = i + 1
            antique5 = the_list[i]
        if the_list[i] != antique_name:
            antique6 = the_list[i]
            i = i + 1
        else:
            i = i + 1
            antique6 = the_list[i]
        if the_list[i] != antique_name:
            antique7 = the_list[i]
        else:
            i = i + 1
            antique7 = the_list[i]
        add_to_recommend_record(old_antique_name, antique_name, int(time.time()),
                                antique1, antique2, antique3, antique4, antique5, antique6, antique7)
    if request.method == 'POST' and 'search_submit' in request.POST:
        search_content = request.POST.get("search_content", None)
        result_dic = click_search(search_content, user_name)
        if 'name' in result_dic:
            add_to_record(user_name, result_dic['name'])
            add_to_search_record(user_name, result_dic['name'], int(time.time()), 1)
        else:
            add_to_search_record(user_name, result_dic['name'], int(time.time()), 0)
        # 生成关系图
        result_return['old_antiname'] = result_dic['name']
        result_return['network_graph'] = graph(result_dic)
        result_return['username'] = user_name
        if 'museum' in result_dic:
            if result_dic['museum'] == '中国国家博物馆':
                result_return['image_path'] = '/images/chn_pic/' + result_dic['number'][1:] + '.jpg'
            elif result_dic['museum'] == '故宫博物院':
                result_return['image_path'] = '/images/dpm_pic/' + result_dic['number'][1:] + '.jpg'
        if 'introduction' in result_dic:
            result_return['introduction'] = result_dic['introduction']
        if 'item_CF' in result_dic:
            result_return['item_CF'] = result_dic['item_CF']
        if 'relevant' in result_dic and len(result_dic['relevant']) >= 1:
            recommend_list = result_dic['relevant']
            result_return['recommend'] = recommend_list
            recommend_return = ''
            for one in recommend_list:
                recommend_return = recommend_return + one + ' '
            result_return['recommend_return'] = recommend_return
            return render(request, "index.html", result_return)
        else:
            result_return['recommend'] = defult_recommend
            return render(request, "index.html", result_return)
    else:
        result_dic = click_search(antique_name, user_name)
        # 生成关系图
        result_return['old_antiname'] = antique_name
        result_return['network_graph'] = graph(result_dic)
        result_return['username'] = user_name
        if 'museum' in result_dic:
            if result_dic['museum'] == '中国国家博物馆':
                result_return['image_path'] = '/images/chn_pic/' + result_dic['number'][1:] + '.jpg'
            elif result_dic['museum'] == '故宫博物院':
                result_return['image_path'] = '/images/dpm_pic/' + result_dic['number'][1:] + '.jpg'
        if 'introduction' in result_dic:
            result_return['introduction'] = result_dic['introduction']
        if 'name' in result_dic:
            add_to_record(user_name, result_dic['name'])
        if 'item_CF' in result_dic:
            result_return['item_CF'] = result_dic['item_CF']
        if 'relevant' in result_dic and len(result_dic['relevant']) >= 1:
            recommend_list = result_dic['relevant']
            result_return['recommend'] = recommend_list
            recommend_return = ''
            for one in recommend_list:
                recommend_return = recommend_return + one + ' '
            result_return['recommend_return'] = recommend_return
            return render(request, "index.html", result_return)
        else:
            result_return['recommend'] = defult_recommend
            return render(request, "index.html", result_return)