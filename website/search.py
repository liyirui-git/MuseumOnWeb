from website.search_via_sql import *


# 在返回的结果中，当时为了在MuseumOffline中可以方便地显示，加入了很多的空格来排版，现在来看已经不需要了。
def click_search(search, username):
    result_dic = {}
    # 目前按编号查找暂时不用分词

    if search.find('【朝代】') != -1:
        # 朝代的查找结果信息少到可怜，后面应该回去扩充朝代的详细数据了。
        # 同时查找朝代的结果，应当是可以得到这个朝代的文物。不过也可以在后面的分词中添加，如果有提到“xx朝”又出现“文物”的时候，列举文物。
        search = search.split('【朝代】')[1]
        result_dic = do_search(int(search), 2, '', [], username)
    elif search.find('【省份】') != -1:
        # 同样的，省份的结果信息也是少的可怜，也应该去扩充一下，把各个省的详细数据添加进来
        # 同时查找省份的结果，应当是可以得到省份中出土的文物。不过也可以在后面的分词中添加，如果有提到“xx省”又出现“文物”的时候，列举文物。
        search = search.split('【省份】')[1]
        result_dic = do_search(int(search), 4, '', [], username)
    elif search.find('【搜索】') != -1:
        search = search.split('【搜索】')[1]
        result_dic = do_search(0, 1, search, [], username)
    # 在这里之前是利用编号与系统交互
    # 在这里之后是先利用分词工具，将分词结果匹配一定的规则，了解用户的查询意图以后，给予相应的反馈
    else:
        # 目前通过分词实现了对文物的名字的查找
        # 在调试的时候，再打开输出分词结果
        print("分词 > " + antiqueNameLA.normal(search))
        word_list = antiqueNameLA.get_word(search)
        result_dic = do_search(0, 0, '', word_list, username)

    return result_dic
