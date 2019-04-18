from website.search_via_sparql import *


# 在返回的结果中，当时为了在MuseumOffline中可以方便地显示，加入了很多的空格来排版，现在来看已经不需要了。
def click_search(search):
    result_dic = {}
    # 目前按编号查找暂时不用分词
    if search.find('【文物】') != -1:
        # 文物的查找的结果最好能返回带有类别信息的结果，比如，文物名：xxx，尺寸：xxx
        # 而且文物中缺少最重要的朝代，出土地这些信息啊
        # 查文物这种比较基本的，实在不行就再重新封装一下
        search = search.split('【文物】')[1]
        result_dic = search_antique_with_num(int(search))
    elif search.find('【朝代】') != -1:
        # 朝代的查找结果信息少到可怜，后面应该回去扩充朝代的详细数据了。
        # 同时查找朝代的结果，应当是可以得到这个朝代的文物。不过也可以在后面的分词中添加，如果有提到“xx朝”又出现“文物”的时候，列举文物。
        search = search.split('【朝代】')[1]
        result_dic = search_dynasty_with_num(int(search))
    elif search.find('【省份】') != -1:
        # 同样的，省份的结果信息也是少的可怜，也应该去扩充一下，把各个省的详细数据添加进来
        # 同时查找省份的结果，应当是可以得到省份中出土的文物。不过也可以在后面的分词中添加，如果有提到“xx省”又出现“文物”的时候，列举文物。
        search = search.split('【省份】')[1]
        result_dic = search_province_with_num(int(search))
    elif search.find('【用途】') != -1:
        search = search.split('【用途】')[1]
        result_dic = search_usage_with_num(int(search))
    elif search.find('【搜索】') != -1:
        search = search.split('【搜索】')[1]
        item_list = -1
        for list_ele in AntiqueList:
            if list_ele[1].find(search) != -1:
                item_list = int(list_ele[0])
                result_dic = search_antique_with_num(int(item_list))
    else:
        # 目前通过分词实现了对文物的名字的查找
        # 在调试的时候，再打开输出分词结果
        print("分词 > " + antiqueNameLA.normal(search))
        user_word_list = antiqueNameLA.get_word(search)
        for user_word in user_word_list:
            item_list = []
            # type_flag -> 1 antique
            # type_flag -> 2 dynasty
            # type_flag -> 3 province
            # type_flag -> 4 usage
            type_flag = 0
            for list_ele in AntiqueList:
                if list_ele[1] == user_word:
                    item_list.append(int(list_ele[0]))
                    type_flag = 1
            if type_flag == 0:
                for list_ele in DynastyList:
                    if list_ele[1] == user_word:
                        item_list.append(int(list_ele[0]))
                        type_flag = 2
            if type_flag == 0:
                for list_ele in ProvinceList:
                    if list_ele[1] == user_word:
                        item_list.append(int(list_ele[0]))
                        type_flag = 3
            if type_flag == 0:
                for list_ele in UsageList:
                    if list_ele[1] == user_word:
                        item_list.append(int(list_ele[0]))
                        type_flag = 4
            if type_flag == 0:
                 print("结果 > 对不起，不懂你的意思~")
            else:
                for item in item_list:
                    if type_flag == 1:
                        result_dic = search_antique_with_num(int(item))
                    elif type_flag == 2:
                        result_dic = search_dynasty_with_num(int(item))
                    elif type_flag == 3:
                        result_dic = search_province_with_num(int(item))
                    elif type_flag == 4:
                        result_dic = search_usage_with_num(int(item))
    # print(result_dic)
    return result_dic