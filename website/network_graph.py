from pyecharts import Graph
# 国风颜色
# 燕脂
yanzhi = 'rgb(159, 53, 58)'
# 砺茶
licha = 'rgb(152, 95, 42)'
# 沈香茶
shenxiangcha = 'rgb(79, 114, 108)'
#
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


def graph(result_dic):
    # 节点
    if 'name' not in result_dic:
        return None
    nodes = [{"name": result_dic['name'],
              "symbolSize": 80,
              "value": 50,
              "itemStyle": {"color": shenxiangcha},
              "label": {"color": 'black',
                        'position': 'inside',
                        'fontWeight': 'bold'}}]
    links = []
    '''
    links 中的 symbolSize 在指定带箭头的边以后，显示的是箭头的大小
    '''
    if 'dynasty' in result_dic and len(result_dic['dynasty']) > 0:
        nodes.append({"name": result_dic['dynasty'],
                      "symbolSize": 30,
                      "itemStyle": {"color": yanzhi}})
        links.append({'source': result_dic['name'],
                      'target': result_dic['dynasty'],
                      'symbolSize': 8,
                      "lineStyle": {"color": licha},
                      "label": {'show': True,
                                'formatter': '朝代为',
                                'color': 'black'}})
    if 'dynasty_detail' in result_dic and len(result_dic['dynasty_detail']) > 0:
        nodes.append({"name": result_dic['dynasty_detail'],
                      "symbolSize": 30,
                      "itemStyle": {"color": yanzhi}})
        links.append({'source': result_dic['name'],
                      'target': result_dic['dynasty_detail'],
                      'symbolSize': 8,
                      "lineStyle": {"color": licha},
                      "label": {'show': True,
                                'formatter': '详细朝代为',
                                'color': 'black'}})
    if 'province' in result_dic and len(result_dic['province']) > 0:
        nodes.append({"name": result_dic['province'],
                      "symbolSize": 30,
                      "itemStyle": {"color": yanzhi}})
        links.append({'source': result_dic['name'],
                      'target': result_dic['province'],
                      'symbolSize': 8,
                      "lineStyle": {"color": licha},
                      "label": {'show': True,
                                'formatter': '出土省份',
                                'color': 'black'}})
    if 'place_detail' in result_dic and len(result_dic['place_detail']) > 0:
        nodes.append({"name": result_dic['place_detail'],
                      "symbolSize": 30,
                      "itemStyle": {"color": yanzhi}})
        links.append({'source': result_dic['name'],
                      'target': result_dic['place_detail'],
                      'symbolSize': 8,
                      "lineStyle": {"color": licha},
                      "label": {'show': True,
                                'formatter': '出土详细地址',
                                'color': 'black'}})
    if 'time' in result_dic and len(result_dic['time']) > 0:
        nodes.append({"name": result_dic['time'] + '年',
                      "symbolSize": 30,
                      "itemStyle": {"color": yanzhi}})
        links.append({'source': result_dic['name'],
                      'target': result_dic['time'] + '年',
                      'symbolSize': 8,
                      "lineStyle": {"color": licha},
                      "label": {'show': True,
                                'formatter': '出土年份',
                                'color': 'black'}})
    if 'produceplace' in result_dic and len(result_dic['produceplace']) > 0:
        nodes.append({"name": result_dic['produceplace'],
                      "symbolSize": 30,
                      "itemStyle": {"color": yanzhi}})
        links.append({'source': result_dic['name'],
                      'target': result_dic['produceplace'],
                      'symbolSize': 8,
                      "lineStyle": {"color": licha},
                      "label": {'show': True,
                                'formatter': '产地',
                                'color': 'black'}})
    if 'museum' in result_dic and len(result_dic['museum']) > 0:
        nodes.append({"name": result_dic['museum'],
                      "symbolSize": 30,
                      "itemStyle": {"color": yanzhi}})
        links.append({'source': result_dic['name'],
                      'target': result_dic['museum'],
                      'symbolSize': 8,
                      "lineStyle": {"color": licha},
                      "label": {'show': True,
                                'formatter': '馆藏于',
                                'color': 'black'}})
    if 'usage' in result_dic and len(result_dic['usage']) > 0:
        nodes.append({"name": result_dic['usage'],
                      "symbolSize": 30,
                      "itemStyle": {"color": yanzhi}})
        links.append({'source': result_dic['name'],
                      'target': result_dic['usage'],
                      'symbolSize': 8,
                      "lineStyle": {"color": licha},
                      "label": {'show': True,
                                'formatter': '用途是',
                                'color': 'black'}})
    if 'type' in result_dic and len(result_dic['type']) > 0:
        nodes.append({"name": result_dic['type'],
                      "symbolSize": 30,
                      "itemStyle": {"color": yanzhi}})
        links.append({'source': result_dic['name'],
                      'target': result_dic['type'],
                      'symbolSize': 8,
                      "lineStyle": {"color": licha},
                      "label": {'show': True,
                                'formatter': '所属种类',
                                'color': 'black'}})
    if 'subtype' in result_dic and len(result_dic['subtype']) > 0:
        nodes.append({"name": result_dic['subtype'],
                      "symbolSize": 30,
                      "itemStyle": {"color": yanzhi}})
        links.append({'source': result_dic['name'],
                      'target': result_dic['subtype'],
                      'symbolSize': 8,
                      "lineStyle": {"color": licha},
                      "label": {'show': True,
                                'formatter': '所属子类别',
                                'color': 'black'}})
    if 'size' in result_dic and len(result_dic['size']) > 0:
        nodes.append({"name": result_dic['size'],
                      "symbolSize": 30,
                      "itemStyle": {"color": yanzhi}})
        links.append({'source': result_dic['name'],
                      'target': result_dic['size'],
                      'symbolSize': 8,
                      "lineStyle": {"color": licha},
                      "label": {'show': True,
                                'formatter': '尺寸为',
                                'color': 'black'}})
    if 'shape' in result_dic and len(result_dic['shape']) > 0:
        nodes.append({"name": result_dic['shape'],
                      "symbolSize": 30,
                      "itemStyle": {"color": yanzhi}})
        links.append({'source': result_dic['name'],
                      'target': result_dic['shape'],
                      'symbolSize': 8,
                      "lineStyle": {"color": licha},
                      "label": {'show': True,
                                'formatter': '形状为',
                                'color': 'black'}})
    if 'color' in result_dic and len(result_dic['color']) > 0:
        nodes.append({"name": result_dic['color'],
                      "symbolSize": 30,
                      "itemStyle": {"color": yanzhi}})
        links.append({'source': result_dic['name'],
                      'target': result_dic['color'],
                      'symbolSize': 8,
                      "lineStyle": {"color": licha},
                      "label": {'show': True,
                                'formatter': '颜色为',
                                'color': 'black'}})
    if 'weight' in result_dic and len(result_dic['weight']) > 0:
        nodes.append({"name": result_dic['weight'],
                      "symbolSize": 30,
                      "itemStyle": {"color": yanzhi}})
        links.append({'source': result_dic['name'],
                      'target': result_dic['weight'],
                      'symbolSize': 8,
                      "lineStyle": {"color": licha},
                      "label": {'show': True,
                                'formatter': '重量为',
                                'color': 'black'}})
    if 'producer' in result_dic and len(result_dic['producer']) > 0:
        nodes.append({"name": result_dic['producer'],
                      "symbolSize": 30,
                      "itemStyle": {"color": yanzhi}})
        links.append({'source': result_dic['name'],
                      'target': result_dic['producer'],
                      'symbolSize': 8,
                      "lineStyle": {"color": licha},
                      "label": {'show': True,
                                'formatter': '作者',
                                'color': 'black'}})
    if 'kiln' in result_dic and len(result_dic['kiln']) > 0:
        nodes.append({"name": result_dic['kiln'],
                      "symbolSize": 30,
                      "itemStyle": {"color": yanzhi}})
        links.append({'source': result_dic['name'],
                      'target': result_dic['kiln'],
                      'symbolSize': 8,
                      "lineStyle": {"color": licha},
                      "label": {'show': True,
                                'formatter': '窑口',
                                'color': 'black'}})
    if 'texture' in result_dic and len(result_dic['texture']) > 0:
        nodes.append({"name": result_dic['texture'],
                      "symbolSize": 30,
                      "itemStyle": {"color": yanzhi}})
        links.append({'source': result_dic['name'],
                      'target': result_dic['texture'],
                      'symbolSize': 8,
                      "lineStyle": {"color": licha},
                      "label": {'show': True,
                                'formatter': '材质为',
                                'color': 'black'}})
    if 'craft' in result_dic and len(result_dic['craft']) > 0:
        nodes.append({"name": result_dic['craft'],
                      "symbolSize": 30,
                      "itemStyle": {"color": yanzhi}})
        links.append({'source': result_dic['name'],
                      'target': result_dic['craft'],
                      'symbolSize': 8,
                      "lineStyle": {"color": licha},
                      "label": {'show': True,
                                'formatter': '制作工艺为',
                                'color': 'black'}})
    if 'culture' in result_dic and len(result_dic['culture']) > 0:
        nodes.append({"name": result_dic['culture'],
                      "symbolSize": 30,
                      "itemStyle": {"color": yanzhi}})
        links.append({'source': result_dic['name'],
                      'target': result_dic['culture'],
                      'symbolSize': 8,
                      "lineStyle": {"color": licha},
                      "label": {'show': True,
                                'formatter': '所属文化类型为',
                                'color': 'black'}})
    if 'pattern' in result_dic and len(result_dic['pattern']) > 0:
        nodes.append({"name": result_dic['pattern'],
                      "symbolSize": 30,
                      "itemStyle": {"color": yanzhi}})
        links.append({'source': result_dic['name'],
                      'target': result_dic['pattern'],
                      'symbolSize': 8,
                      "lineStyle": {"color": licha},
                      "label": {'show': True,
                                'formatter': '纹饰图案为',
                                'color': 'black'}})
    if 'story' in result_dic and len(result_dic['story']) > 0:
        nodes.append({"name": result_dic['time'],
                      "symbolSize": 30,
                      "itemStyle": {"color": yanzhi}})
        links.append({'source': result_dic['name'],
                      'target': result_dic['story'],
                      'symbolSize': 8,
                      "lineStyle": {"color": licha},
                      "label": {'show': True,
                                'formatter': '相关故事传说',
                                'color': 'black'}})
    if 'simple' in result_dic and len(result_dic['simple']) > 0:
        nodes.append({"name": result_dic['simple'],
                      "symbolSize": 30,
                      "itemStyle": {"color": yanzhi}})
        links.append({'source': result_dic['name'],
                      'target': result_dic['simple'],
                      'symbolSize': 8,
                      "lineStyle": {"color": licha},
                      "label": {'show': True,
                                'formatter': '象征意义',
                                'color': 'black'}})

    # 后面考虑把relevant也加进来。

    g = Graph("文物信息")

    g.add("", nodes, links,
          is_label_show=True,
          graph_layout='force',
          label_text_color=True,
          graph_edge_length=180,
          graph_edge_symbol=['', 'arrow'],
          graph_repulsion=400)

    # 此处如果打开会生成一个render.html
    # g.render()
    return g.render_embed()
