#!/usr/bin/python3

import time,json,os

def t():
    t = time.localtime(time.time())
    localtime = time.asctime(t)
    str = "当前时间:" + time.asctime(t)
    print(str);


# x 是目录的路径
x = "/storage/emulated/0/Venter/HopWeb/Projects/1循环test/blog/js/1.json"


def refresh(data):
    i = 0
    for a in data:
        a["tab"] = i + 1
        i+=1
    return data



# 1 #
def output(json_file_path):
    # 检查文件是否为 JSON 文件
    if json_file_path.endswith(".json"):
        # 打开 JSON 文件
        with open(json_file_path, 'r') as json_file:
            try:
                # 解析 JSON 数据
                data = json.load(json_file)
                data = refresh(data)
                # 如果 data 是一个列表，遍历其中的字典对象
                if isinstance(data, list):
                    for obj in data:
                        # 读取每个对象的 "time" 和 "title" 字段的值
                        time_value = obj.get("time")
                        title_value = obj.get("title")
                        img_value = obj.get("img")
                        tab_value = obj.get("tab")
            
                        if True:
                            # 输出 "time" 和 "title" 字段的值
                            print("╭═════════════════════════╮")
                            print(f"tab: {tab_value}")
                            print(f"title: {title_value}")
                            print(f"img: {img_value}")
                            print(f"time: {time_value}")
                            print("╰═════════════════════════╯\n")
                        else:
                            print("JSON 文件中的某个对象缺少 'time' 或 'title' 字段")

                else:
                    print("JSON 文件根部不是一个列表")

            except json.JSONDecodeError as e:
                print(f"解析 JSON 文件 {json_file_path} 时出现错误: {e}")

    else:
        print(f"{json_file_path} 不是一个 JSON 文件")



# 2 #

def insert(json_file_path, x):
    # 检查文件是否为 JSON 文件
    if json_file_path.endswith(".json"):
        # 打开 JSON 文件
        with open(json_file_path, 'r') as json_file:
            try:
                # 解析 JSON 数据
                data = json.load(json_file)

                # 检查数据是否为列表
                if isinstance(data, list):
                    new_data = {
                    "title": input("请输入标题: "),
                    "content": input("请输入内容: "),
                    "img": input("请输入图片链接: "),
                    "tab" : x,
                    "time": input("请输入时间: ")
                    }
                    # print(type(data))
            
            
                    data.append({})
                    for i in range(len(data)-1,x-1,-1):
                        data[i]=data[i-1]
                    # 插入新单元数据到指定位置 x
                    data[x-1]=new_data
                    # 更新后面元素的索引
                    for i in range(x, len(data)):
                        data[i]['tab'] = i + 1
                    
                    data = refresh(data)
            
                    # 写回 JSON 文件
                    with open(json_file_path, 'w') as json_file:
                        json.dump(data, json_file, ensure_ascii=False , indent=2)
                        # json.dump里面的ensure_ascii=False表示写入的不是ascll码，会在json里表示为正常字符
                        # 如果不写的话，中文会变成\ud83c\udf39的样子
                    print("成功插入新单元到 JSON 文件。")

                else:
                    print("JSON 文件根部不是一个列表")

            except json.JSONDecodeError as e:
                print(f"解析 JSON 文件 {json_file_path} 时出现错误: {e}")

    else:
        print(f"{json_file_path} 不是一个 JSON 文件")




# 3 #

def add(json_file_path):
    # 检查文件是否为 JSON 文件
    if json_file_path.endswith(".json"):
        # 打开 JSON 文件
        with open(json_file_path, 'r') as json_file:
            try:
                # 解析 JSON 数据
                data = json.load(json_file)

                # 检查数据是否为列表
                if isinstance(data, list):
                    new_data = {
                    "title": input("请输入标题: "),
                    "content": input("请输入内容: "),
                    "img": input("请输入图片链接: "),
                    "tab" : len(data) + 1,
                    "time": input("请输入时间: ")
                    }
                    # print(type(data))
            
            
                    data.append(new_data)
                    data = refresh(data)
                    # 写回 JSON 文件
                    with open(json_file_path, 'w') as json_file:
                        json.dump(data, json_file, ensure_ascii=False , indent=2)
                        # json.dump里面的ensure_ascii=False表示写入的不是ascll码，会在json里表示为正常字符
                        # 如果不写的话，中文会变成\ud83c\udf39的样子
                    print("成功插入新单元到 JSON 文件。")

                else:
                    print("JSON 文件根部不是一个列表")

            except json.JSONDecodeError as e:
                print(f"解析 JSON 文件 {json_file_path} 时出现错误: {e}")

    else:
        print(f"{json_file_path} 不是一个 JSON 文件")




# 4 #

def delete(json_file_path, x):
    # 检查文件是否为 JSON 文件
    if json_file_path.endswith(".json"):
        # 打开 JSON 文件
        with open(json_file_path, 'r') as json_file:
            try:
                # 解析 JSON 数据
                data = json.load(json_file)

                # 检查数据是否为列表
                if isinstance(data, list):

                    for i in range(x -1, len(data) - 1):
                        data[i] = data[i + 1]
                    data.pop()
                    data = refresh(data)
                   
                    # 写回 JSON 文件
                    with open(json_file_path, 'w') as json_file:
                        json.dump(data, json_file, ensure_ascii=False , indent=2)
                        # json.dump里面的ensure_ascii=False表示写入的不是ascll码，会在json里表示为正常字符
                        # 如果不写的话，中文会变成\ud83c\udf39的样子
                    print("成功插入新单元到 JSON 文件。")

                else:
                    print("JSON 文件根部不是一个列表")

            except json.JSONDecodeError as e:
                print(f"解析 JSON 文件 {json_file_path} 时出现错误: {e}")

    else:
        print(f"{json_file_path} 不是一个 JSON 文件")





def div():
    print('\n███████████████████████████████████████\n')
    t()
    print('\n███████████████████████████████████████\n\n\n')
# 示例数据



# 使用示例
path = "/storage/emulated/0/Venter/HopWeb/Projects/1循环test/blog/js/1.json"

div()

# insert(path, 12)  # 在第 2 个位置插入新单元
# delete(path,11)
# add(path)
output(path)

div()

flag = '1'
while flag != '0':
    div()
    print('[1]add尾部增加模式\n\n[2]insert插入模式\n\n[3]delete删除模式\n\n[4]scan预览模式\n\n[5]修改json文件目录\n\n')
    flag = input('请选择操作模式：')
    if flag == '1':
        add(path)
    elif flag == '2':
        x = input("请输入插入的位置：")
        insert(path,x)
    elif flag == '3':
        x = input("请输入删除的位置：")
        delete(path,x)
    elif flag == '4':
        output(path)
    elif flag == '5':
        path = input("请输入json的目录位置：")





