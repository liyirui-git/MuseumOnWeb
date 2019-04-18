# 此处建了一个SPARQL的类
from SPARQLWrapper import SPARQLWrapper, JSON
from website.lexical_analyzer import *
sparql_head = '''PREFIX : <http://www.kgdemo.com#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX vocab: <http://localhost:2020/resource/vocab/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX map: <http://localhost:2020/resource/#>
PREFIX db: <http://localhost:2020/resource/>'''


class SPARQL:
    @staticmethod
    def run(search, mode):
        # mode -> 1表示返回的是文物的查询结果
        sparql = SPARQLWrapper("http://localhost:2020/sparql")
        sparql.setQuery(search)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        return_dic = {}

        # 说明是文物，还需添加一些附加信息
        if mode == 1:
            for result in results["results"]["bindings"]:
                if result["hasValue"]["type"] == 'literal':
                    print(result)
                    if result["property"]["value"].find("AntiName") != -1:
                        return_dic['name'] = result["hasValue"]["value"]
                    elif result["property"]["value"].find("AntiSize") != -1:
                        return_dic['size'] = result["hasValue"]["value"]
                    elif result["property"]["value"].find("#label") != -1:
                        return_dic['number'] = result["hasValue"]["value"].split("#")[1]
            for result in results["results"]["bindings"]:
                if result["hasValue"]["type"] == 'uri':
                    if result["hasValue"]["value"].find("resource") != -1:
                        second_info = result["hasValue"]["value"].split("resource")[1]
                        if second_info.find("/dynasty") != -1:
                            dynasty_num = second_info.split("dynasty/")[1]
                            for item in DynastyList:
                                if item[0] == dynasty_num:
                                    dynasty_name = item[1]
                            return_dic['dynasty'] = dynasty_name
                            # 此处准备向推荐列表中添加朝代相关文物的内容：
                            add_recommend_list(dynasty_num, 1)
                        elif second_info.find("antique_dynasty") != -1:
                            dynasty_d_num = second_info.split("antique_dynasty/")[1]
                            for item in DynastyDetailList:
                                if item[0] == dynasty_d_num:
                                    dynasty_d_name = item[1]
                            return_dic['dynasty_detail'] = dynasty_d_name
                            # ！！！！ 注意  ！！！！
                            # 此处应补充完推荐算法
                            #
                        elif second_info.find("province") != -1:
                            province_num = second_info.split("province/")[1]
                            for item in ProvinceList:
                                if item[0] == province_num:
                                    province_name = item[1]
                            return_dic['province'] = province_name
                            # 此处准备向推荐列表中添加省份的相关文物的内容：
                            add_recommend_list(province_num, 2)
                        elif second_info.find("antique_usage") != -1:
                            usage_num = second_info.split("antique_usage/")[1]
                            for item in UsageList:
                                if item[0] == usage_num:
                                    usage_name = item[1]
                            return_dic['usage'] = usage_name
                            # 此处准备向推荐列表中添加用途相关文物的内容：
                            add_recommend_list(usage_num, 1)
            relevant = []
            for item in select_recommend_list(4):
                relevant.append(item)
            return_dic['relevant'] = relevant
        else:
            relevant = []
            for result in results["results"]["bindings"]:
                try:
                    if result["isValueOf"]["type"] == 'uri':
                        if result["isValueOf"]["value"].find("antique/") != -1:
                            antique_num = result["isValueOf"]["value"].split("antique/")[1]
                            for item in AntiqueList:
                                if item[0] == antique_num:
                                    antique_name = item[1]
                                    relevant.append(antique_name)
                except:
                    print("The value of \"isValueOf\" is None!")
            return_dic['relevant'] = relevant
        # print(relevant)
        return return_dic


def search_antique_with_num(num):
    search = '''SELECT DISTINCT ?property ?hasValue
            WHERE {
              { <http://localhost:2020/resource/antique/''' + str(num) + '''> ?property ?hasValue }
            }
            ORDER BY (!BOUND(?hasValue)) ?property ?hasValue'''
    return sparql.run(sparql_head + search, 1)


def search_dynasty_with_num(num):
    search = '''SELECT DISTINCT ?property ?isValueOf
            WHERE {
              { <http://localhost:2020/resource/dynasty/''' + str(num) + '''> ?property ?hasValue }
            UNION
            { ?isValueOf ?property <http://localhost:2020/resource/dynasty/''' + str(num) + '''> }
            }
            ORDER BY (!BOUND(?hasValue)) ?property ?hasValue'''
    return sparql.run(sparql_head + search, 0)


def search_province_with_num(num):
    search = '''SELECT DISTINCT ?property ?isValueOf
        WHERE {
          { <http://localhost:2020/resource/province/''' + str(num) + '''> ?property ?hasValue }
        UNION
        { ?isValueOf ?property <http://localhost:2020/resource/province/''' + str(num) + '''> }
        }
        ORDER BY (!BOUND(?hasValue)) ?property ?hasValue'''
    return sparql.run(sparql_head + search, 0)


def search_usage_with_num(num):
    search = '''SELECT DISTINCT ?property ?isValueOf
        WHERE {
          { <http://localhost:2020/resource/antique_usage/''' + str(num) + '''> ?property ?hasValue }
        UNION
        { ?isValueOf ?property <http://localhost:2020/resource/antique_usage/''' + str(num) + '''> }
        }
        ORDER BY (!BOUND(?hasValue)) ?property ?hasValue'''
    return sparql.run(sparql_head + search, 0)


def add_recommend_list(key_num, mode):
    # mode -> 1, Dynasty
    # mode -> 2, Province
    # mode -> 3, Usage
    # mode -> 4, Dynasty Detail
    # 注意，mode 4 目前没有启用
    if mode == 1:
        antique_dic = search_dynasty_with_num(key_num)
    elif mode == 2:
        antique_dic = search_province_with_num(key_num)
    elif mode == 3:
        antique_dic = search_usage_with_num(key_num)

    antique_list = antique_dic['relevant']
    for antique in antique_list:
        exist = 0
        for re in recommend_list:
            if antique == re[0]:
                if mode != 4:
                    re[1] = str(int(re[1]) + 1)
                else:
                    re[1] = str(int(re[1]) + 2)
                exist = 1
        if exist == 0:
            recommend = []
            recommend.append(antique)
            recommend.append('1')
            recommend_list.append(recommend)


def select_recommend_list(times):
    # times 推荐的个数
    best_list = []
    num = 0
    for i in range(0, times):
        for recommend in recommend_list:
            if int(recommend[1]) > num:
                num = int(recommend[1])
                recommend[1] = str(0)
                best_list.append(recommend[0])
    del recommend_list[:]
    return best_list

# 推荐算法：
# 推荐算法采用统计相同朝代(1)、省份(1)、用途(1)、以及详细朝代(2)的文物，括号中是各自的权重
# 每次从相关文物中选取权重最高的五个推荐给用户。
# 推荐列表结构：
# |文物名|目前的分|
# | xxx |  xxx  |
recommend_list = []
# 启动通过文物名，变成一个文物名分词
antiqueNameLA = myLA("website/src/userName.txt")
# 用一个列表来存储文物的编号与文物名，在用户输入文物名的时候，在列表中查找相应文物名一栏来确定文物的编号
# 其实在这里用列表存储不是一个很好的数据结构。但由于是从值来得到关键码，所以用字典更麻烦，目前数据量较小，在这里就不再优化。
DynastyList = load_dict_from_file("website/src/DynastyNumName.txt")
DynastyDetailList = load_dict_from_file("website/src/DynastyDetail.txt")
ProvinceList = load_dict_from_file("website/src/ProvinceNumName.txt")
UsageList = load_dict_from_file("website/src/UsageNumName.txt")
AntiqueList = load_dict_from_file("website/src/AntiqueNumName.txt")
sparql = SPARQL()