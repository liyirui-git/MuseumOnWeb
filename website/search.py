from website.search_via_sql import *

dynasty_dic = {
'旧石器':  1,
'新石器':  2,
'夏':	3,
'商'	:   4,
'周':	5,
'春秋':	6,
'战国':	7,
'秦':	8,
'汉':	9,
'三国':	10,
'晋':	11,
'南北朝':	12,
'隋':	13,
'唐':	14,
'五代十国':	15,
'宋':	16,
'元':	17,
'明':	18,
'清':	19,
'民国':	20,
'近代':	21
}

province_dic = {
'北京市':	11,
'北京':	11,
'天津市':	12,
'天津':	12,
'河北省':	13,
'河北':	13,
'山西省':	14,
'山西':	14,
'内蒙古自治区':	15,
'内蒙古':	15,
'内蒙':	15,
'辽宁省':	21,
'辽宁':	21,
'吉林省':	22,
'吉林':	22,
'黑龙江省':	23,
'黑龙江':	23,
'上海市':	31,
'上海':	31,
'江苏省':	32,
'江苏':	32,
'浙江省':	33,
'浙江':	33,
'安徽省':	34,
'安徽':	34,
'福建省':	35,
'福建':	35,
'江西省':	36,
'江西':	36,
'山东省':	37,
'山东':	37,
'河南省':	41,
'河南':	41,
'湖北省':	42,
'湖北':	42,
'湖南省':	43,
'湖南':	43,
'广东省':	44,
'广东':	44,
'广西壮族自治区':	45,
'广西':	45,
'海南省':	46,
'海南':	46,
'重庆市':	50,
'重庆':	50,
'四川省':	51,
'四川':	51,
'贵州省':	52,
'贵州':	52,
'云南省':	53,
'云南':	53,
'西藏自治区':	54,
'西藏':	54,
'陕西省':	61,
'陕西':	61,
'甘肃省':	62,
'甘肃':	62,
'青海省':	63,
'青海':	63,
'宁夏回族自治区':	64,
'宁夏':	64,
'新疆维吾尔自治区':	65,
'新疆':	65,
'台湾省':	71,
'台湾':	71,
'香港特别行政区':	81,
'香港':	81,
'澳门特别行政区':	82,
'澳门':	82
}


# 在返回的结果中，当时为了在MuseumOffline中可以方便地显示，加入了很多的空格来排版，现在来看已经不需要了。
def click_search(search, username):
    result_dic = {}
    # 目前按编号查找暂时不用分词
    if search in dynasty_dic:
        result_dic = do_search(dynasty_dic[search], 2, '', [], username)
    elif search in province_dic:
        result_dic = do_search(province_dic[search], 4, '', [], username)
    elif search.find('【搜索】') != -1:
        search = search.split('【搜索】')[1]
        result_dic = do_search(0, 1, search, [], username)
    # 在这里之前是利用编号与系统交互
    # 在这里之后是先利用分词工具，将分词结果匹配一定的规则，了解用户的查询意图以后，给予相应的反馈
    else:
        print("分词 > " + antiqueNameLA.normal(search))
        word_list = antiqueNameLA.get_word(search)
        result_dic = {}
        # 添加一些规则吧
        # 这个为了应对出土地和出土时间信息
        if search.find('出土') != -1 or search.find('发现') != -1:
            # 说明这里关注点是出土地信息
            if search.find('哪里') != -1 or search.find('地方') != -1 or search.find('出土地') != -1:
                if search.find('哪些') != -1:
                    # 在推荐列表中返回该地方的其他文物，通过文本部分返回问题的答案
                    result_dic = do_search_plus(1, search, word_list, username, dynasty_dic, province_dic)
                else:
                    # 这里说明关注的只是当前文物，所以该文物放在推荐中，然后文本返回该问题的答案。
                    result_dic = do_search_plus(2, search, word_list, username, dynasty_dic, province_dic)
            # elif search.find('时间') != -1 or search.find('时候') != -1:
            #     if search.find('哪些') != -1:
            #         result_dic = do_search_plus(3, search, word_list, username, dynasty_dic, province_dic)
            #     else:
            #         result_dic = do_search_plus(4, search, word_list, username, dynasty_dic, province_dic)
        # 此时是为了应对文物的朝代信息
        elif search.find('朝代') != -1 or search.find('年代') != -1:
            if search.find('哪些') != -1:
                # 这里说明关注点在相同朝代的其他文物
                result_dic = do_search_plus(5, search, word_list, username, dynasty_dic, province_dic)
            else:
                # 这里说明关注点在当前文物是哪一个朝代
                result_dic = do_search_plus(6, search, word_list, username, dynasty_dic, province_dic)

        else:
            # 目前通过分词实现了对文物的名字的查找
            # 在调试的时候，再打开输出分词结果
            result_dic = do_search(0, 0, '', word_list, username)

    return result_dic
