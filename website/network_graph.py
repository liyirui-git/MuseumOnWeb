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
    'name':
    'size':
    'number':
    'dynasty':
    'dynasty_detail':
    'province':
    'usage':
    'relevant':
}
'''


def graph(result_dic):
    # 节点
    if 'name' not in result_dic:
        return None
    nodes = [{"name": result_dic['name'],
              "symbolSize": 50,
              "value": 50,
              "itemStyle": {"color": shenxiangcha},
              "label": {"color": 'black',
                        'position': 'inside',
                        'fontWeight': 'bold'}}]
    links = []
    '''
    links 中的 symbolSize 在指定带箭头的边以后，显示的是箭头的大小
    '''
    if 'size' in result_dic:
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
    if 'dynasty' in result_dic:
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
    if 'dynasty_detail' in result_dic:
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
    if 'province' in result_dic:
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
    if 'usage' in result_dic:
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

    # 后面考虑把relevant也加进来。

    g = Graph("文物信息")

    g.add("", nodes, links,
          is_label_show=True,
          graph_layout='force',
          label_text_color=True,
          graph_edge_length=100,
          graph_edge_symbol=['', 'arrow'],
          graph_repulsion=400)
    # g.render()
    return g.render_embed()
