# 推荐算法：
# 推荐算法采用统计相同朝代(1)、省份(1)、用途(1)、以及详细朝代(2)的文物，括号中是各自的权重
# 每次从相关文物中选取权重最高的五个推荐给用户。
# 推荐列表结构：
# |文物名|目前的分|
# | xxx |  xxx  |

# 这里通过加载的文件岂不是有点慢，直接连数据库访问数据库呗
# 暑假的时候，为了实现文物或者其他实体的编号与实体名字之间的对应关系，是通过读取资源文件存到列表里，然后在列表中搜索实现的。
# 随着数据量的增长，这种方法一是占用内存，还有列表的搜索太慢。
# 为什么要拿名字再回去找序号呢？因为我现在还没解决SPARQL不支持中文的问题，后面会继续尝试直接解决，但在现在暂时改为数据库查询实现。

import MySQLdb
from website.lexical_analyzer import *
from website.recommend import weight_recommend, item_based_CF_new

# 通过自己定义的用户词典，启动一个封装好的针对当前文物的THULAC
# 除了subtype表，其他表中的名字都被我加进去了。
antiqueNameLA = myLA("website/src/userName_new.txt")


def do_search(num, mode, name, word_list, username):
    db = MySQLdb.connect('localhost', 'root', '123456', 'museumdb_new', charset='utf8')
    cursor = db.cursor()
    # mode
    result_dic = {}
    # mode-> 0：通过分词结果查找
    # 这里就可以添加一些自然语言的规则
    if mode == 0:
        for user_word in word_list:
            # 这里暂时先处理出现了文物名的情况
            # 对于出现文物名的情况，还要处理文物的推荐结果
            cursor.execute('SELECT * FROM antique WHERE AntiName = %s'
                           % repr(user_word))
            result = cursor.fetchall()
            if len(result) > 0 and len(result[0][0]) > 0:
                ##########
                # antique 的结构
                # 0: AntiNum
                # 1: AntiName
                # 2: AntiDY
                # 3: AntiDM
                # 4: AntiDS
                # 5: AntiProvince
                # 6: AntiDetailPlace
                # 7: AntiTime
                # 8: AntiProducePlace
                # 9: AntiMuseum
                # 10: AntiUsage
                # 11: AntiType
                # 12: AntiSubType
                # 13: AntiSize
                # 14: AntiShape
                # 15: AntiColor
                # 16: AntiWeight
                # 17: AntiProducer
                # 18: AntiKiln
                # 19: AntiTexture
                # 20: AntiCraft
                # 21: AntiCulture
                # 22: AntiPattern
                # 23: AntiStory
                # 24: AntiSimple
                # 25: AntiDetail
                ###########
                result_dic['number'] = result[0][0]
                result_dic['name'] = result[0][1]
                result_dic['dynasty'] = result[0][2]
                result_dic['dynasty_detail'] = result[0][3]
                result_dic['province'] = result[0][5]
                result_dic['place_detail'] = result[0][6]
                result_dic['time'] = result[0][7]
                result_dic['produceplace'] = result[0][8]
                result_dic['museum'] = result[0][9]
                result_dic['usage'] = result[0][10]
                result_dic['type'] = result[0][11]
                result_dic['subtype'] = result[0][12]
                result_dic['size'] = result[0][13]
                result_dic['shape'] = result[0][14]
                result_dic['color'] = result[0][15]
                result_dic['weight'] = result[0][16]
                result_dic['producer'] = result[0][17]
                result_dic['kiln'] = result[0][18]
                result_dic['texture'] = result[0][19]
                result_dic['craft'] = result[0][20]
                result_dic['culture'] = result[0][21]
                result_dic['pattern'] = result[0][22]
                result_dic['story'] = result[0][23]
                result_dic['simple'] = result[0][24]
                result_dic['introduction'] = result[0][25]
                # 添加推荐文物
                result_dic['relevant'] = weight_recommend(result[0])

                result_dic['item_CF'] = item_based_CF_new(result[0], username)
    # mode-> 1：通过输入文物名中的片段来模糊查找
    # 将得到的结果作为推荐文物返回给使用者
    elif mode == 1:
        cursor.execute('SELECT AntiName FROM antique WHERE AntiName LIKE %s'
                       % repr('%' + name + '%'))
        result = cursor.fetchall()
        recommend_list = []
        for item in result:
            recommend_list.append(item[0])
        result_dic['relevant'] = recommend_list
    # mode-> 2： 说明输入是朝代序号
    # 鉴于朝代的一些信息可能不方便直接以图的形式展示，这里以后可以新建一个key：text，以备想要用文字展示。
    # 朝代利用返回字典的 key：relevant 来传递相关的文物， 而这里 relevant 对应的是一个列表
    elif mode == 2:
        cursor.execute('SELECT AntiName FROM antique WHERE AntiDYNum = %d'
                       % num)
        result = cursor.fetchall()
        recommend_list = []
        for item in result:
            recommend_list.append(item[0])
        result_dic['relevant'] = recommend_list
    # mode-> 4：说明输入是省份序号
    # 同样将得到的结果作为推荐返回给使用者
    elif mode == 4:
        cursor.execute('SELECT AntiName FROM antique WHERE AntiProvinceNum = %d'
                       % num)
        result = cursor.fetchall()
        recommend_list = []
        for item in result:
            recommend_list.append(item[0])
        result_dic['relevant'] = recommend_list

    db.commit()
    db.close()
    return result_dic


