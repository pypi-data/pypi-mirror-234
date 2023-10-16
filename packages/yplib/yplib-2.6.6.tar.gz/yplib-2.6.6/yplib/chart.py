from yplib.chart_html import *
from yplib.index import *


# 将 html 中的占位符 替换成数据
# 并且 导出 生成后的 html 文件
def insert_data_to_chart(html_data,
                         name=None,
                         x_list=None,
                         y_list=None,
                         legend=None,
                         series=None,
                         smooth=0):
    p_list = [
        'chart_name', 'name', 'x_list', 'y_list', 'legend', 'series', 'smooth'
    ]
    p_data_list = [
        name, name, x_list, y_list, legend, series, smooth
    ]
    h_r = []
    for html_line in html_data:
        for index in range(len(p_list)):
            one_p = p_list[index]
            one_data = p_data_list[index]
            if one_data is None:
                continue
            one_p = f'-{one_p}-'
            if one_p in html_line:
                html_line = html_line.replace(one_p, str(one_data))
        h_r.append(html_line)
    to_txt(data_list=h_r,
           file_name=str(name),
           file_path='html',
           fixed_name=False,
           suffix='.html')


# 将数据整理成折线图
# 情况1:
# x轴数据 : x_list = [
#       ['x轴的数据', 'line1', 'line2', 'line3'],
#       ['2020-01-01', 120, 132, 101],
#       ['2020-01-02', 100, 102, 131],
#       ['2020-01-03', 123, 165, 157],
#       ['2020-01-04', 126, 109, 189],
#       ['2020-01-05', 150, 156, 128],
#       ['2020-01-06', 178, 134, 140],
#       ['2020-01-07', 157, 148, 161],
#  ]
#  --- 以上这种情况,当 y_list 为空的时候,就说明有可能是这种情况
#  --- 以上这种情况,数据与 excel 中的数据对齐
# 情况2:
# x轴数据 : x_list = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
# y轴数据 : y_list = [
#     [120, 132, 101, 134, 90, 230, 210],
# 	  [220, 182, 191, 234, 290, 330, 310],
# 	  [150, 232, 201, 154, 190, 330, 410],
# 	  [320, 332, 301, 334, 390, 330, 320],
# 	  [820, 932, 901, 934, 1290, 1330, 1320]
# ]
# 情况3--标准情况下的数据:
# x轴数据 : x_list = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
# y轴数据 : y_list = [
#             {
#                 name: 'Email',
#                 hide: True,
#                 smooth: True,
#                 data: [120, 132, 101, 134, 90, 230, 210],
#             },
#             {
#                 name: 'Union Ads',
#                 hide: 1,
#                 smooth: 1,
#                 data: [220, 182, 191, 234, 290, 330, 310],
#             },
#             {
#                 name: 'Video Ads',
#                 data: [150, 232, 201, 154, 190, 330, 410],
#             },
#             {
#                 name: 'Direct',
#                 data: [320, 332, 301, 334, 390, 330, 320],
#             },
#             {
#                 name: 'Search Engine',
#                 data: [820, 932, 901, 934, 1290, 1330, 1320],
#             },
#         ]
#  name : 文件名称,折线图的名称
#  name_raw : 用原始的名字,不用带上属性 line_stack
def to_chart(x_list,
             y_list=None,
             name=None,
             name_raw=False):
    # 当 y_list 没有的话, 需要整理出 y_list 的数据
    if y_list is None:
        data_list = x_list
        x_list = []
        y_list = []
        for index in range(len(data_list)):
            line_one = data_list[index]
            # 第一行数据
            if index == 0:
                for y in range(1, len(line_one)):
                    y_list.append({'name': line_one[y], 'data': []})
            # 第二行开始的数据
            if index > 0:
                x_list.append(line_one[0])
                for y in range(1, len(line_one)):
                    y_list[y - 1]['data'].append(line_one[y])
    name_list = []
    name_hide = {}
    for y_index in range(len(y_list)):
        y_one = y_list[y_index]
        name_one = y_one['name'] if 'name' in y_one else str(y_index + 1) + '_' + random_letter(3)
        name_list.append(name_one)
        if 'hide' in y_one and y_one['hide']:
            name_hide[name_one] = 0
    legend = 'data: ' + str(name_list) + ',\n            selected: ' + str(name_hide)
    # {
    #     name: 'Email',
    #     type: 'line',
    #     stack: 'Total',
    #     smooth: 1,
    #     data: [120, 132, 101, 134, 90, 230, 210],
    # }
    # [120, 132, 101, 134, 90, 230, 210],
    series = []
    for y_index in range(len(y_list)):
        y_o = {}
        y_one = y_list[y_index]
        y_o['name'] = name_list[y_index]
        y_o['data'] = y_one['data'] if 'data' in y_one else y_one
        y_o['type'] = 'line'
        y_o['stack'] = 'Total'
        if 'smooth' in y_one and y_one['smooth']:
            y_o['smooth'] = 1
        # 只有一条线,就不显示 name 了
        if len(y_list) == 1:
            del y_o['name']
        series.append(y_o)

    if not name_raw:
        name = 'line_stack' if name is None else name + '_line_stack'
    insert_data_to_chart(html_data=line_stack_html(),
                         name=name,
                         x_list=x_list,
                         legend=legend,
                         series=series)


# 将数据整理成折线图
# 一条折线
# 数据 : data_list = [
#             ['2020-01-01', 132],
#             ['2021-01-01', 181],
#             ['2022-01-01', 147]
#         ]
# x_index : x 轴数据的下标
# y_index : y 轴数据的下标
# 或者
# 数据 : data = [
#        {name: "Search Engine", value: 1048 },
#        {name: "Direct", value: 735 },
#        {name: "Email", value:580 },
#        {name: "Union Ads", value:484 },
#        {name: "Video Ads", value:300 }
#       }]
#  x_key : 当元素为对象的时候, x 的 key
#  y_key : 当元素为对象的时候, y 的 key
# is_area : 是否使用 area 图
# smooth : 曲线是否平滑
def to_chart_one(data_list,
                 name=None,
                 x_index=0,
                 x_key='name',
                 y_index=1,
                 y_key='value',
                 is_area=False,
                 smooth=False):
    x_list = []
    y_list = []
    name = 'line' if name is None else name + '_line'
    name = name + '_smooth' if smooth else name
    name = name + '_area' if is_area else name
    sm = 1 if smooth else 0
    for d_one in data_list:
        if isinstance(d_one, list):
            x = d_one[x_index]
            y = d_one[y_index]
        else:
            x = d_one[x_key]
            y = d_one[y_key]
        x_list.append(x)
        y_list.append(y)
    if is_area:
        insert_data_to_chart(html_data=line_area_html(),
                             name=name,
                             x_list=x_list,
                             y_list=y_list,
                             smooth=sm)
    else:
        to_chart(x_list=x_list,
                 y_list=[{'name': name, 'data': y_list, 'smooth': sm}],
                 name=name,
                 name_raw=True)


# 将数据整理成饼状图
# 数据 : data = [
#         { value: 1048, name: "Search Engine" },
#         { value: 735, name: "Direct" },
#         { value: 580, name: "Email" },
#         { value: 484, name: "Union Ads" },
#         { value: 300, name: "Video Ads" }
#       ]
#  name_key : 当元素为对象的时候, x 的 key
#  value_key : 当元素为对象的时候, y 的 key
# 或者
# 数据 : data = [
#         [ "Search Engine", 1048 ],
#         [ "Direct", 735 ],
#         [ "Email",580 ],
#         [ "Union Ads",484 ],
#         [ "Video Ads",300 ]
#       ]
#  name_index : 当元素为数组的时候, name 的下标
#  value_index : 当元素为数组的时候, value 的下标
def to_chart_pie(data_list,
                 name=None,
                 name_index=0,
                 name_key='name',
                 value_index=1,
                 value_key='value'):
    x_list = []
    name = 'pie' if name is None else name + '_pie'
    for one_data in data_list:
        if isinstance(one_data, list):
            x = one_data[name_index]
            y = one_data[value_index]
        else:
            x = one_data[name_key]
            y = one_data[value_key]
        x_list.append({'name': x, 'value': y})
    insert_data_to_chart(html_data=pie_html(),
                         name=name,
                         x_list=x_list)


# 将数据整理成柱状图
# 数据 : data = [
#         { value: 1048, name: "Search Engine" },
#         { value: 735, name: "Direct" },
#         { value: 580, name: "Email" },
#         { value: 484, name: "Union Ads" },
#         { value: 300, name: "Video Ads" }
#       ]
#  name_key : 当元素为对象的时候, x 的 key
#  value_key : 当元素为对象的时候, y 的 key
# 或者
# 数据 : data = [
#         [ "Search Engine", 1048 ],
#         [ "Direct", 735 ],
#         [ "Email",580 ],
#         [ "Union Ads",484 ],
#         [ "Video Ads",300 ]
#       ]
#  name_index : 当元素为数组的时候, name 的下标
#  value_index : 当元素为数组的时候, value 的下标
def to_chart_bar(data_list,
                 name=None,
                 name_index=0,
                 name_key='name',
                 value_index=1,
                 value_key='value'):
    x_list = []
    y_list = []
    name = 'bar' if name is None else name + '_bar'
    for one_data in data_list:
        if isinstance(one_data, list):
            x = one_data[name_index]
            y = one_data[value_index]
        else:
            x = one_data[name_key]
            y = one_data[value_key]
        x_list.append(x)
        y_list.append(y)
    insert_data_to_chart(html_data=bar_html(),
                         name=name,
                         x_list=x_list,
                         y_list=y_list)
