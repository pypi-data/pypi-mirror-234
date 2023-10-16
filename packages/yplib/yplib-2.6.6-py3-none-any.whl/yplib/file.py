from yplib.index import *


# 有关文件的操作
# 查询指定文件夹下面的所有的文件信息, 也可以是指定的文件
# param list
# return list
def get_file(file_path=None, prefix=None, contain=None, suffix=None):
    if file_path is None:
        file_path = os.path.dirname(os.path.abspath('.'))
    list_data = []
    get_file_all(file_path, list_data, prefix, contain, suffix)
    # 去一下重复的数据
    return list(set(list_data))


# 有关文件的操作, 只查询文件夹
# 查询指定文件夹下面的所有的文件信息, 也可以是指定的文件
# param list
# return list
def get_folder(file_path=None, prefix=None, contain=None, suffix=None):
    if file_path is None:
        file_path = os.path.dirname(os.path.abspath('.'))
    list_data = []
    get_folder_all(file_path, list_data, prefix, contain, suffix)
    # 去一下重复的数据
    return list(set(list_data))


# 是否包含指定的文件
def contain_file(file_path=None, prefix=None, contain=None, suffix=None):
    return len(get_file(file_path, prefix, contain, suffix)) > 0


# 在指定的文件夹中查找包含指定字符串的数据
# file_path : 文件路径
# find_str : 查找的字符串
# from_last : 是否从文件的最后开始查找
def get_file_data_line(file_path=None, find_str='find_str', from_last=True):
    file_list = get_file(file_path)
    for one_file in file_list:
        one_list = to_list(one_file)
        index = 0
        if from_last:
            index = len(one_list) - 1
        while -1 < index < len(one_list):
            one_line = one_list[index]
            if from_last:
                index -= 1
            else:
                index += 1
            if one_line.find(find_str) > -1:
                return one_line
    return None


# 查询指定文件夹下面的所有的文件信息, 也可以是指定的文件
def get_file_all(file_path, list_data, prefix=None, contain=None, suffix=None):
    if os.path.isdir(file_path):
        for root, dir_names, file_names in os.walk(file_path):
            for file_name in file_names:
                if get_file_check(file_name, prefix, contain, suffix):
                    list_data.append(os.path.join(root, file_name))
            for dir_name in dir_names:
                get_file_all(os.path.join(root, dir_name), list_data)
    elif get_file_check(file_path, prefix, contain, suffix):
        list_data.append(file_path)


# 查询指定文件夹下面的所有的文件信息, 也可以是指定的文件
def get_folder_all(file_path, list_data, prefix=None, contain=None, suffix=None):
    if os.path.isdir(file_path):
        for root, dir_names, file_names in os.walk(file_path):
            for dir_name in dir_names:
                dir_name_path = os.path.join(root, dir_name)
                if get_file_check(dir_name_path, prefix, contain, suffix):
                    list_data.append(dir_name_path)
                else:
                    get_folder_all(dir_name_path, list_data, prefix, contain, suffix)


# 检查文件是否符合要求
# prefix : 前缀
# contain : 包含这个字符
# suffix : 后缀
def get_file_check(file_name='', prefix=None, contain=None, suffix=None):
    if file_name is None or file_name == '':
        return False
    p = True
    c = True
    s = True
    if prefix is not None:
        if file_name.startswith(prefix):
            p = True
        else:
            p = False
    if contain is not None:
        if file_name.find(contain) > -1:
            c = True
        else:
            c = False
    if suffix is not None:
        if file_name.endswith(suffix):
            s = True
        else:
            s = False
    return p and c and s


# 检查文件内容是否包含指定的字符串
# 慎用,否则, 执行时间可能比较长
def find_file_by_content(file_path='', contain_txt=None, prefix=None, contain=None, suffix=None):
    list_file = get_file(file_path, prefix, contain, suffix)
    if len(list_file) == 0:
        to_log(f'no_matched_file : {file_path} , {contain_txt} , {prefix} , {contain} , {suffix}')
        return False
    if contain_txt is None:
        to_log(list_file)
        return True
    for one_file in list_file:
        try:
            text_file = open(one_file, 'r', encoding='utf-8')
            for line in text_file.readlines():
                if line.find(contain_txt) > -1:
                    if line.endswith('\n'):
                        line = line[0:-1]
                    to_log(one_file, line)
        except Exception as e:
            to_log(one_file, e)
            continue

# print(get_file_data_line(r'D:\notepad_file\202306\fasdfsadfaf.txt', 'payout', from_last=False))

# get_file_data_line(r'D:\notepad_file\202306', 'a')
# get_file_by_content(r'D:\notepad_file\202306', 'a')
# print(get_file(r'D:\notepad_file\202306', 'a'))
# print(get_file(r'D:\notepad_file\202306'))
# print(get_file())
# print(os.path.abspath('.'))

#
# a_list = get_folder(r'D:\code\20220916\cjgeodatabase-java\platform', contain='build')
# for a in a_list:
#     os.remove(a)
#
# print(json.dumps(a_list))

# print('end')
