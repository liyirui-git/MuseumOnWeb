import MySQLdb
import time
import math

weight_table = {
    'DY': 1,
    'DM': 3,
    'Province': 1,
    'Time': 1,
    'ProducePlace': 6,
    'Museum': 1,
    'Usage': 3,
    'Type': 2,
    'Subtype': 5,
    'Shape': 1,
    'Color': 1,
    'Producer': 6,
    'Kiln': 5,
    'Texture': 2,
    'Craft': 2,
    'Culture': 3,
    'Pattern': 1,
}

recommend_size = 8
weight_max = 100000
cosine_threshold = 0.35
# 我按照三天26万秒来估计的，期望三天能够冷却到之前的一半
# 先把秒降数量级，除以10万得到2.6。
# -2.6 * k = ln(1/2) 即 2.6 * k = ln(2)
# k = 0.69 / 2.6 = 0.2654
Newton_K = 0.2654
# 决定热度在整个排名打分系统中的所起的作用
Weight_K = 2
# 规定20次落选能被一次被选择抵消
Punish_K = 20
# 规定协同过滤推荐的个数
CF_NUM = 5

# # 连接文物数据，得到文物名表
db_antique = MySQLdb.connect('127.0.0.1', 'root', '123456', 'museumdb_new', charset='utf8')
cursor_antique = db_antique.cursor()
# 存放文物名的字典
antique_dic = {}
cursor_antique.execute('SELECT DISTINCT AntiName FROM antique;')
antique_name = cursor_antique.fetchall()
antique_ct = 0
for item in antique_name:
    antique_dic[item[0]] = antique_ct
    antique_ct = antique_ct + 1
db_antique.close()

# 得到实体表
entity_table = {}
entity_file = open('website/src/entity.txt', encoding='utf8')
entity_ct = 0
for line in entity_file.readlines():
    entity_table[line.split()[0]] = entity_ct
    entity_ct = entity_ct + 1


# 获取列表的第二个元素
def take_second(elem):
    return elem[1]


# 牛顿热度衰减
def heat(dt):
    return math.exp(-1 * Newton_K * dt / 100000)


# 计算余弦相似度
# 结果应该是数值越小越相似。数值的分布的范围为是[0，1]
def cosine_distance(a, b):
    if len(a) != len(b):
        return False
    numerator = 0
    denoma = 0
    denomb = 0
    for i in range(len(a)):
        numerator += a[i]*b[i]
        denoma += abs(a[i])**2
        denomb += abs(b[i])**2
    noma = (math.sqrt(denoma)*math.sqrt(denomb))
    if noma != 0:
        result = 1 - numerator / noma
    else:
        result = 1.0
    return result


# 这个是一个最初的非常朴素的一个协同过滤
def item_based_CF(infor):
    db = MySQLdb.connect('127.0.0.1', 'root', '123456', 'museum_website_v0', charset='utf8')
    cursor = db.cursor()
    recommend_list = []
    cursor.execute('SELECT DISTINCT username FROM website_recordviausername WHERE search = %s'
                   % repr(infor[1]))
    user_list = cursor.fetchall()
    for user in user_list:
        cursor.execute('SELECT DISTINCT search FROM website_recordviausername WHERE username = %s'
                       % repr(user[0]))
        view_list = cursor.fetchall()
        for item in view_list:
            if item[0] != infor[1]:
                flag = 0
                for i in recommend_list:
                    if i[0] == item[0]:
                        i[1] = i[1] + 1
                        flag = 1
                        break
                if flag == 0:
                    recommend_list.append([item[0], 1])
    db.close()
    recommend_list.sort(key=take_second, reverse=True)
    ct = 0
    # print(recommend_list)
    recommend_return = []
    for item in recommend_list:
        recommend_return.append(item[0])
        ct = ct + 1
        if ct == CF_NUM:
            break
    return recommend_return


def get_user_vector(username, cursor_website):
    # 先得到当前用户的浏览记录，生成用户向量
    # print(username)
    cursor_website.execute('SELECT search FROM website_recordviausername WHERE username = %s'
                           % repr(username))
    search_record = cursor_website.fetchall()
    vector = []
    # 先将向量数组初始化为全0
    for i in range(0, len(antique_dic)):
        vector.append(0)
    # 然后把出现的文物的位置置为1
    for one in search_record:
        if one[0] in antique_dic:
            # print(one[0] + " is " + str(antique_dic[one[0]]))
            vector[antique_dic[one[0]]] = 1
    return vector


def get_user_vector_via_proper(username, cursor_website):
    # 得到用户当前用户
    cursor_website.execute('SELECT search FROM website_recordviausername WHERE username = %s'
                           % repr(username))
    search_record = cursor_website.fetchall()
    vector = []
    # 先将向量数组初始化为全0
    for i in range(0, len(entity_table)):
        vector.append(0)
    for one in search_record:
        cursor_antique.execute('SELECT AntiDY, AntiProvince, AntiKiln, AntiType, AntiTexture, AntiMuseum, AntiUsage FROM antique WHERE AntiName = %s'
                               % repr(one[0]))
        antique_detail = cursor_antique.fetchall()
        for item in antique_detail:
            for i in item:
                if i in entity_table:
                    print(i)
                    vector[entity_table[i]] = vector[entity_table[i]] + 1
    return vector


# 这个是利用余弦距离计算用户相似度来对协同过滤做的改进
def item_based_CF_new(infor, username):
    db_website = MySQLdb.connect('127.0.0.1', 'root', '123456', 'museum_website_v0', charset='utf8')
    cursor_website = db_website.cursor()
    a = get_user_vector(username, cursor_website)
    cursor_website.execute('SELECT DISTINCT username FROM website_recordviausername')
    user_list = cursor_website.fetchall()
    similar_list = []
    for user in user_list:
        if user[0] != username:
            b = get_user_vector(user[0], cursor_website)
            cosine_dis = cosine_distance(a, b)
            # print('<cosine_dis>:' + str(cosine_dis))
            if cosine_dis < cosine_threshold:
                similar_list.append(user[0])
    antique_list = []
    for person in similar_list:
        cursor_website.execute('SELECT DISTINCT search, valid FROM website_searchrecord WHERE username = %s'
                               % repr(person))
        antique_get = cursor_website.fetchall()
        for item in antique_get:
            flag = 0
            if item[1] == 0 or item[0] == infor[1]:
                continue
            for one in antique_list:
                if one[0] == item:
                    one[1] = one[1] + 1
                    flag = 1
            if flag == 0:
                antique_list.append([item[0], 1])
    antique_list.sort(key=take_second, reverse=True)
    recommend_return = []
    ct = 0
    for item in antique_list:
        recommend_return.append(item[0])
        ct = ct + 1
        if ct == 5:
            break
    db_website.close()
    return recommend_return


def heat_recommend(infor):
    # heat_list 的结构是一个(文物名，热度值)的一个数组
    heat_list = []
    db = MySQLdb.connect('127.0.0.1', 'root', '123456', 'museum_website_v0', charset='utf8')
    cursor = db.cursor()
    # 从数据库里把该文物的所有推荐记录读出来
    cursor.execute('SELECT * FROM website_recommendrecord WHERE MainAntique = %s'
                          % repr(infor[1]))
    recommend_list = cursor.fetchall()
    # time.time() 返回的是1970年以后的秒数的浮点数
    #
    current_time = int(time.time())
    for item in recommend_list:
        t0 = item[10]
        h = heat(current_time - t0)
        good_one = item[2]
        flag = 0
        for one in heat_list:
            if one[0] == good_one:
                one[1] = one[1] + h
                flag = 1
        if flag == 0:
            heat_list.append([good_one, h])
        for i in range(3, 10):
            bad_one = item[i]
            h_b = -1 * h / Punish_K
            flag = 0
            for one in heat_list:
                if one[0] == bad_one:
                    one[1] = one[1] + h_b
                    flag = 1
            if flag == 0:
                heat_list.append([bad_one, h_b])
    db.close()
    return heat_list


def weight_recommend(infor):
    db = MySQLdb.connect('127.0.0.1', 'root', '123456', 'museumdb_new', charset='utf8')
    cursor = db.cursor()

    recommend_list = []
    weight_list = []
    # 如何实现权值的推荐？
    # 建立一个权值表， 遍历数据库中的其他文物，如果某一属性的属性值与其相同，则增加相应的权值
    cursor.execute('SELECT * FROM antique')
    antique_list = cursor.fetchall()

    # 通过这个heat_list把所有热度值不为0的文物和其热度值返回
    heat_list = heat_recommend(infor)

    for item in antique_list:
        weight = 0
        if item[0] == infor[0]:
            continue

        # 把点击热度在计算权重的过程中也算是一个因素
        for one in heat_list:
            if one[0] == item[1]:
                weight = weight + Weight_K * one[1]

        weight_heat = weight

        if item[2] == infor[2]:
            weight = weight + weight_table['DY']
        if item[3] == infor[3]:
            weight = weight + weight_table['DM']
        if item[5] == infor[5]:
            weight = weight + weight_table['Province']
        if item[7] == infor[7]:
            weight = weight + weight_table['Time']
        if item[8] == infor[8]:
            weight = weight + weight_table['ProducePlace']
        if item[9] == infor[9]:
            weight = weight + weight_table['Museum']
        if item[10] == infor[10]:
            weight = weight + weight_table['Usage']
        if item[11] == infor[11]:
            weight = weight + weight_table['Type']
        if item[12] == infor[12]:
            weight = weight + weight_table['Subtype']
        if item[14] == infor[14]:
            weight = weight + weight_table['Shape']
        if item[15] == infor[15]:
            weight = weight + weight_table['Color']
        if item[17] == infor[17]:
            weight = weight + weight_table['Producer']
        if item[18] == infor[18]:
            weight = weight + weight_table['Kiln']
        if item[19] == infor[19]:
            weight = weight + weight_table['Texture']
        if item[20] == infor[20]:
            weight = weight + weight_table['Craft']
        if item[21] == infor[21]:
            weight = weight + weight_table['Culture']
        if item[22] == infor[22]:
            weight = weight + weight_table['Pattern']

        if len(weight_list) < recommend_size:
            item_list = [item[1], weight, weight_heat]
            weight_list.append(item_list)
        else:
            # 找到列表中权重的最小值
            min = weight_max
            for one in weight_list:
                if min > one[1]:
                    min = one[1]
            # 如果待插入的比最小的还小，就不用插入了
            if min < weight:
                for one in weight_list:
                    if one[1] == min:
                        weight_list.remove(one)
                        break
                item_list = [item[1], weight, weight_heat]
                weight_list.append(item_list)

    # 这里利用的是先乱序插入最后排序。
    # 也可一开始就按序插入，这样当空间满了以后，只需要跟最后一个比较。
    # 如果比最后一个权值大，删掉最后一个，再按序插入。
    weight_list.sort(key=take_second, reverse=True)
    # print(weight_list)
    for one in weight_list:
        recommend_list.append(one[0])
    db.close()
    return recommend_list
