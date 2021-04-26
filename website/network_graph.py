from pyecharts import Graph
import MySQLdb
# 国风颜色
# 燕脂
yanzhi = 'rgb(159, 53, 58)'
# 翠绿
cuilv = 'rgb(32, 161, 98)'
# 铜绿
tonglv = 'rgb(43,174,133)'
# 羽扇豆蓝
yushandoulan = 'rgb(97, 154, 195)'
# 虹蓝
honglan = 'rgb(33, 119, 184)'
# 这个是当前查询的文物的边的value值，有别于推荐的文物的边的值。
main_link_value = 1000
# 在关系图中显示推荐文物的最大数量
recommend_max = 4
# result_dic 的结构
'''
result_dic = {
    'number':
    'name':
    'dynasty':
    'dynasty_detail':
    'province':
    'place_detail':
    'time':
    'produceplace':
    'museum':
    'usage':
    'type':
    'subtype':
    'size':
    'shape':
    'color':
    'weight':
    'producer':
    'kiln':
    'texture':
    'craft':
    'culture':
    'pattern':
    'story':
    'simple':
    'introduction':
    'relevant':
}
'''

# 第一个值是属性值在关系图中的节点名，同时也是其在result_dic中的Key值
# 第二个值是这个属性的权值
# 第三个值是这个属性在数据库中的列号
weight_map = (
    ('dynasty', 1, 2,),
    ('dynasty_detail', 3, 3,),
    ('province', 1, 5,),
    ('time', 1, 7,),
    ('produceplace', 6, 8,),
    ('museum', 1, 9,),
    ('usage', 3, 10,),
    ('type', 2, 11,),
    ('subtype', 5, 12,),
    ('shape', 1, 14,),
    ('color', 1, 15,),
    ('producer', 6, 17,),
    ('kiln', 5, 18,),
    ('texture', 2, 19,),
    ('craft', 2, 20,),
    ('culture', 3, 21,),
    ('pattern', 1, 22,),
)


def graph(result_dic):
    # 节点
    # print(result_dic)
    if 'name' not in result_dic:
        return None
    nodes = []
    links = []
    '''
    links 中的 symbolSize 在指定带箭头的边以后，显示的是箭头的大小
    '''
    if 'dynasty' in result_dic and len(result_dic['dynasty']) > 0:
        nodes.append({"name": result_dic['dynasty'],
                      "symbolSize": 30,
                      "itemStyle": {"color": yanzhi}})
        links.append({'source': '【' + result_dic['name'] + '】',
                      'target': result_dic['dynasty'],
                      'symbolSize': 8,
                      'value': main_link_value,
                      "lineStyle": {"color": cuilv},
                      "label": {'show': True,
                                'formatter': '朝代为',
                                'color': 'black'}})
    if 'dynasty_detail' in result_dic and len(result_dic['dynasty_detail']) > 0:
        nodes.append({"name": result_dic['dynasty_detail'],
                      "symbolSize": 30,
                      "itemStyle": {"color": yanzhi}})
        links.append({'source': '【' + result_dic['name'] + '】',
                      'target': result_dic['dynasty_detail'],
                      'symbolSize': 8,
                      'value': main_link_value,
                      "lineStyle": {"color": cuilv},
                      "label": {'show': True,
                                'formatter': '详细朝代为',
                                'color': 'black'}})
    if 'province' in result_dic and len(result_dic['province']) > 0:
        nodes.append({"name": result_dic['province'],
                      "symbolSize": 30,
                      "itemStyle": {"color": yanzhi}})
        links.append({'source': '【' + result_dic['name'] + '】',
                      'target': result_dic['province'],
                      'symbolSize': 8,
                      'value': main_link_value,
                      "lineStyle": {"color": cuilv},
                      "label": {'show': True,
                                'formatter': '出土省份',
                                'color': 'black'}})
    if 'place_detail' in result_dic and len(result_dic['place_detail']) > 0:
        nodes.append({"name": result_dic['place_detail'],
                      "symbolSize": 30,
                      "itemStyle": {"color": yanzhi}})
        links.append({'source': '【' + result_dic['name'] + '】',
                      'target': result_dic['place_detail'],
                      'symbolSize': 8,
                      'value': main_link_value,
                      "lineStyle": {"color": cuilv},
                      "label": {'show': True,
                                'formatter': '出土详细地址',
                                'color': 'black'}})
    if 'time' in result_dic and len(result_dic['time']) > 0:
        nodes.append({"name": result_dic['time'] + '年',
                      "symbolSize": 30,
                      "itemStyle": {"color": yanzhi}})
        links.append({'source': '【' + result_dic['name'] + '】',
                      'target': result_dic['time'] + '年',
                      'symbolSize': 8,
                      'value': main_link_value,
                      "lineStyle": {"color": cuilv},
                      "label": {'show': True,
                                'formatter': '出土年份',
                                'color': 'black'}})
    if 'produceplace' in result_dic and len(result_dic['produceplace']) > 0:
        nodes.append({"name": result_dic['produceplace'],
                      "symbolSize": 30,
                      "itemStyle": {"color": yanzhi}})
        links.append({'source': '【' + result_dic['name'] + '】',
                      'target': result_dic['produceplace'],
                      'symbolSize': 8,
                      'value': main_link_value,
                      "lineStyle": {"color": cuilv},
                      "label": {'show': True,
                                'formatter': '产地',
                                'color': 'black'}})
    if 'museum' in result_dic and len(result_dic['museum']) > 0:
        nodes.append({"name": result_dic['museum'],
                      "symbolSize": 30,
                      "itemStyle": {"color": yanzhi}})
        links.append({'source': '【' + result_dic['name'] + '】',
                      'target': result_dic['museum'],
                      'symbolSize': 8,
                      'value': main_link_value,
                      "lineStyle": {"color": cuilv},
                      "label": {'show': True,
                                'formatter': '馆藏于',
                                'color': 'black'}})
    if 'usage' in result_dic and len(result_dic['usage']) > 0:
        nodes.append({"name": result_dic['usage'],
                      "symbolSize": 30,
                      "itemStyle": {"color": yanzhi}})
        links.append({'source': '【' + result_dic['name'] + '】',
                      'target': result_dic['usage'],
                      'symbolSize': 8,
                      'value': main_link_value,
                      "lineStyle": {"color": cuilv},
                      "label": {'show': True,
                                'formatter': '用途是',
                                'color': 'black'}})
    if 'type' in result_dic and len(result_dic['type']) > 0:
        nodes.append({"name": result_dic['type'],
                      "symbolSize": 30,
                      "itemStyle": {"color": yanzhi}})
        links.append({'source': '【' + result_dic['name'] + '】',
                      'target': result_dic['type'],
                      'symbolSize': 8,
                      'value': main_link_value,
                      "lineStyle": {"color": cuilv},
                      "label": {'show': True,
                                'formatter': '所属种类',
                                'color': 'black'}})
    if 'subtype' in result_dic and len(result_dic['subtype']) > 0:
        nodes.append({"name": result_dic['subtype'],
                      "symbolSize": 30,
                      "itemStyle": {"color": yanzhi}})
        links.append({'source': '【' + result_dic['name'] + '】',
                      'target': result_dic['subtype'],
                      'symbolSize': 8,
                      'value': main_link_value,
                      "lineStyle": {"color": cuilv},
                      "label": {'show': True,
                                'formatter': '所属子类别',
                                'color': 'black'}})
    if 'size' in result_dic and len(result_dic['size']) > 0:
        nodes.append({"name": result_dic['size'],
                      "symbolSize": 30,
                      "itemStyle": {"color": yanzhi}})
        links.append({'source': '【' + result_dic['name'] + '】',
                      'target': result_dic['size'],
                      'symbolSize': 8,
                      'value': main_link_value,
                      "lineStyle": {"color": cuilv},
                      "label": {'show': True,
                                'formatter': '尺寸为',
                                'color': 'black'}})
    if 'shape' in result_dic and len(result_dic['shape']) > 0:
        nodes.append({"name": result_dic['shape'],
                      "symbolSize": 30,
                      "itemStyle": {"color": yanzhi}})
        links.append({'source': '【' + result_dic['name'] + '】',
                      'target': result_dic['shape'],
                      'symbolSize': 8,
                      'value': main_link_value,
                      "lineStyle": {"color": cuilv},
                      "label": {'show': True,
                                'formatter': '形状为',
                                'color': 'black'}})
    if 'color' in result_dic and len(result_dic['color']) > 0:
        nodes.append({"name": result_dic['color'],
                      "symbolSize": 30,
                      "itemStyle": {"color": yanzhi}})
        links.append({'source': '【' + result_dic['name'] + '】',
                      'target': result_dic['color'],
                      'symbolSize': 8,
                      'value': main_link_value,
                      "lineStyle": {"color": cuilv},
                      "label": {'show': True,
                                'formatter': '颜色为',
                                'color': 'black'}})
    if 'weight' in result_dic and len(result_dic['weight']) > 0:
        nodes.append({"name": result_dic['weight'],
                      "symbolSize": 30,
                      "itemStyle": {"color": yanzhi}})
        links.append({'source': '【' + result_dic['name'] + '】',
                      'target': result_dic['weight'],
                      'symbolSize': 8,
                      'value': main_link_value,
                      "lineStyle": {"color": cuilv},
                      "label": {'show': True,
                                'formatter': '重量为',
                                'color': 'black'}})
    if 'producer' in result_dic and len(result_dic['producer']) > 0:
        nodes.append({"name": result_dic['producer'],
                      "symbolSize": 30,
                      "itemStyle": {"color": yanzhi}})
        links.append({'source': '【' + result_dic['name'] + '】',
                      'target': result_dic['producer'],
                      'symbolSize': 8,
                      'value': main_link_value,
                      "lineStyle": {"color": cuilv},
                      "label": {'show': True,
                                'formatter': '作者',
                                'color': 'black'}})
    if 'kiln' in result_dic and len(result_dic['kiln']) > 0:
        nodes.append({"name": result_dic['kiln'],
                      "symbolSize": 30,
                      "itemStyle": {"color": yanzhi}})
        links.append({'source': '【' + result_dic['name'] + '】',
                      'target': result_dic['kiln'],
                      'symbolSize': 8,
                      'value': main_link_value,
                      "lineStyle": {"color": cuilv},
                      "label": {'show': True,
                                'formatter': '窑口',
                                'color': 'black'}})
    if 'texture' in result_dic and len(result_dic['texture']) > 0:
        nodes.append({"name": result_dic['texture'],
                      "symbolSize": 30,
                      "itemStyle": {"color": yanzhi}})
        links.append({'source': '【' + result_dic['name'] + '】',
                      'target': result_dic['texture'],
                      'symbolSize': 8,
                      'value': main_link_value,
                      "lineStyle": {"color": cuilv},
                      "label": {'show': True,
                                'formatter': '材质为',
                                'color': 'black'}})
    if 'craft' in result_dic and len(result_dic['craft']) > 0:
        nodes.append({"name": result_dic['craft'],
                      "symbolSize": 30,
                      "itemStyle": {"color": yanzhi}})
        links.append({'source': '【' + result_dic['name'] + '】',
                      'target': result_dic['craft'],
                      'symbolSize': 8,
                      'value': main_link_value,
                      "lineStyle": {"color": cuilv},
                      "label": {'show': True,
                                'formatter': '制作工艺为',
                                'color': 'black'}})
    if 'culture' in result_dic and len(result_dic['culture']) > 0:
        nodes.append({"name": result_dic['culture'],
                      "symbolSize": 30,
                      "itemStyle": {"color": yanzhi}})
        links.append({'source': '【' + result_dic['name'] + '】',
                      'target': result_dic['culture'],
                      'symbolSize': 8,
                      'value': main_link_value,
                      "lineStyle": {"color": cuilv},
                      "label": {'show': True,
                                'formatter': '所属文化类型为',
                                'color': 'black'}})
    if 'pattern' in result_dic and len(result_dic['pattern']) > 0:
        nodes.append({"name": result_dic['pattern'],
                      "symbolSize": 30,
                      "itemStyle": {"color": yanzhi}})
        links.append({'source': '【' + result_dic['name'] + '】',
                      'target': result_dic['pattern'],
                      'symbolSize': 8,
                      'value': main_link_value,
                      "lineStyle": {"color": cuilv},
                      "label": {'show': True,
                                'formatter': '纹饰图案为',
                                'color': 'black'}})
    if 'story' in result_dic and len(result_dic['story']) > 0:
        nodes.append({"name": result_dic['time'],
                      "symbolSize": 30,
                      "itemStyle": {"color": yanzhi}})
        links.append({'source': '【' + result_dic['name'] + '】',
                      'target': result_dic['story'],
                      'symbolSize': 8,
                      'value': main_link_value,
                      "lineStyle": {"color": cuilv},
                      "label": {'show': True,
                                'formatter': '相关故事传说',
                                'color': 'black'}})
    if 'simple' in result_dic and len(result_dic['simple']) > 0:
        nodes.append({"name": result_dic['simple'],
                      "symbolSize": 30,
                      "itemStyle": {"color": yanzhi}})
        links.append({'source': '【' + result_dic['name'] + '】',
                      'target': result_dic['simple'],
                      'symbolSize': 8,
                      'value': main_link_value,
                      "lineStyle": {"color": cuilv},
                      "label": {'show': True,
                                'formatter': '象征意义',
                                'color': 'black'}})

    # 后面考虑把relevant也加进来。

    db = MySQLdb.connect('127.0.0.1', 'root', '123456', 'museumdb_new', charset='utf8')
    cursor = db.cursor()
    if 'relevant' in result_dic:
        i = 0
        for item in result_dic['relevant']:
            cursor.execute('SELECT * FROM antique WHERE AntiName = %s'
                           % repr(item))
            result = cursor.fetchall()
            # 给这些相关文物也添加一个结点
            nodes.append({"name": '【' + result[0][1] + '】',
                          "symbolSize": 45,
                          "itemStyle": {"color": yushandoulan},
                          "label": {"color": 'black',
                                    'position': 'inside',
                                    'fontWeight': 'bold'}})
            # 然后给对应的属性添加边
            for w in weight_map:
                key_name = w[0]
                weight = w[1]
                col_num = w[2]
                if len(result[0][col_num]) > 0 and result[0][col_num] == result_dic[key_name]:
                    links.append({'source': '【' + result[0][1] + '】',
                                  'target': result_dic[key_name],
                                  'symbolSize': 8,
                                  'value': 100,
                                  "lineStyle": {"color": honglan}})
            i = i + 1
            if i == recommend_max:
                break
    db.close()

    g = Graph("文物信息")

    # 将文物名包在中括号里面是遇到了文物名与文物的某个属性值冲突比如文物“鼎”与子类别“鼎”，这样的情况无法生成关系图
    nodes.append({"name": '【' + result_dic['name'] + '】',
                  "symbolSize": 80,
                  "itemStyle": {"color": tonglv},
                  "label": {"color": 'black',
                            'fontSize': 16,
                            'position': 'inside',
                            'fontWeight': 'bold'}})

    g.add("", nodes, links,
          is_label_show=True,
          graph_layout='force',
          label_text_color=True,
          graph_edge_length=[100, 200],
          graph_repulsion=1000,
          graph_gravity=0.5,
          graph_edge_symbol=['', 'arrow'],)

    # 此处如果打开会生成一个render.html
    # g.render()
    return g.render_embed()
