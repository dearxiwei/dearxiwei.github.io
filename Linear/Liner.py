#This project is created by MH on 2025/1/2.
#Encoding:UTF-8

# 导入必需的库
import numpy as np  # 主要用来进行数值运算，特别是矩阵运算
import pandas as pd  # 主要用来读取Excel文件
import matplotlib.pyplot as plt
from matplotlib import font_manager
import os
from datetime import datetime, timedelta

global list_len  # 全局变量，用于保存有效值个数
list_len = 999999  # 初始值设为最大值

#自定义函数返回py文件所在的文件路径，但是不包括.py文件名
def get_file_path():
    path = os.path.abspath(__file__)
    return os.path.dirname(path)


    # """
    # 计算指定日期（字符串格式）加上x天后的日期，并返回新的日期。
    # 参数：
    # - date_str: str，输入的日期，格式为 "YYYY-MM-DD"
    # - x: int，增加的天数
    # 返回：
    # - 新的日期，格式为字符串 "YYYY-MM-DD"
    # """
def add_days(date_str, x):
    # 将输入的日期字符串转换为日期对象
    start_date = datetime.strptime(date_str, "%Y-%m-%d")
    
    # 通过 timedelta 增加 x 天
    new_date = start_date + timedelta(days=x)
    
    # 打印新的日期
    print(f"{x}天后的日期是: {new_date.strftime('%Y-%m-%d')}")
    
    # 返回新的日期（字符串格式）
    return new_date.strftime('%Y-%m-%d')





# """
# 根据指定列的线性拟合方程，预测list_len + 1 和 list_len + 2的值。
# 参数：
# - df: pandas DataFrame，包含数据
# - column_name: str，要预测的列名
# 返回：
# - predicted_value_1: 预测的list_len + 1位置的值
# - predicted_value_2: 预测的list_len + 2位置的值
# """
def predict(df, column_name, list_len, x):    
    # 获取该列数据并计算有效的list_len
    y_values = df[column_name][0:list_len]
    
    # 获取拟合方程的参数a和b
    a, b = linear_fit_auto(y_values)

    if a is None or b is None:
        print("无法进行预测，因为拟合失败。")
        return None, None
    
    # 计算 list_len + 1 的预测值
    x = list_len + 1
    
    # 使用拟合方程 y = a * x + b 进行预测
    predicted_value_1 = a * x + b
    

    return predicted_value_1

###############
#
# """
# 自动生成x轴数据为1, 2, 3, 4, 5...，并计算给定的y轴数据的线性拟合方程的参数
 # 拟合方程形式：y = a * x + b
# 参数：
# - y_values: 输入的因变量y值列表或数组
# 返回：
# - a: 拟合方程中的斜率
# - b: 拟合方程中的截距
# """
#
###############
# 定义线性拟合函数linear_fit_auto

def linear_fit_auto(y_values):

    # 计算y值的均值
    y_mean = np.mean(y_values)

    # 筛选出在均值±10范围内的值
    filtered_values = [y for y in y_values if (y_mean - 10) <= y <= (y_mean + 10)]

    # 若筛选后的数据为空，则返回None
    if len(filtered_values) == 0:
        print("没有符合条件的数据进行拟合")
        return None, None

    # 自动生成x轴数据，x = [1, 2, 3, ..., len(filtered_values)]
    x_values = np.arange(1, len(filtered_values) + 1)  # x = [1, 2, 3, ..., len(filtered_values)]

    # 将x_values和filtered_values转换为numpy数组
    x = np.array(x_values)
    y = np.array(filtered_values)

    # 计算x的平均值和y的平均值
    x_mean = np.mean(x)  # x值的平均数
    
    # 计算分子和分母
    numerator = np.sum((x - x_mean) * (y - y_mean))  # x与y差值乘积的和
    denominator = np.sum((x - x_mean) ** 2)  # x差值的平方和

    # 计算斜率a
    a = numerator / denominator  # 斜率的公式
    
    # 计算截距b
    b = y_mean - a * x_mean  # 截距的公式
    
    # 输出拟合方程
    print(f"拟合方程：y = {a:.2f} * x + {b:.2f}")

    # 返回拟合参数a和b
    return a, b



###############
# """
# 对指定列进行处理：计算大于0的值的个数，找出最小的大于0的值，
# 截取数据进行线性拟合。
# 参数：
# - df: pandas DataFrame，包含数据
# - column_names: list，列名数组，指定要处理的列
# 返回：
# - None
# """
###############
def process_columns(df, column_names):

    #设置matplotlib支持中文显示
    font = font_manager.FontProperties(fname='C:/Windows/Fonts/simhei.ttf')  # 指定字体路径（Windows系统）
    plt.rcParams['font.family'] = font.get_name()

    list_len = 999999  # 初始值设为最大值
    # 遍历每一列，计算大于1的值的个数
    for column in column_names:
        # 获取大于1的值
        positive_values = df[column][df[column] > 1]
        if len(positive_values) < list_len:
            list_len = len(positive_values)  # 更新为最小的有效值个数

    print(f"大于1的值的个数：{list_len}")

    # 创建一个目录保存图片
    save_dir = get_file_path()  # 保存图片的路径，当前目录

    # 遍历每一列数据
    for column in column_names:
        # 截取0~list_len行的数据
        df_processed = df[column][0:list_len]
        
        # 调用线性拟合函数并获取拟合结果
        a, b = linear_fit_auto(df_processed)

        # 绘制拟合图
        plt.figure(figsize=(8, 6))

        # 绘制原始数据点
        plt.scatter(np.arange(1, list_len + 1), df_processed, color='blue', label='原始数据')

        # 计算列的均值并绘制y=均值的淡绿色水平线
        y_mean = np.mean(df_processed)
        plt.axhline(y=y_mean, color='lightgreen', linestyle='-', linewidth=1.5, label=f'y = {y_mean:.2f} (均值)')

        # 绘制拟合线
        x_vals = np.arange(1, list_len + 1)
        y_vals = a * x_vals + b
        plt.plot(x_vals, y_vals, color='red', label=f'拟合线: y = {a:.2f}x + {b:.2f}')

        # 添加标题和标签
        plt.title(f"{column} 数据线性拟合")
        plt.xlabel('X轴(日期)')
        plt.ylabel('Y轴(天数)')

        # 添加网格和图例
        plt.grid(True)
        plt.legend()

        # 保存图像
        plt.savefig(f"{save_dir}/{column}_linear_fit.png")
        print(f"图片成功保存到：{save_dir}/{column}_linear_fit.png\n")
        # plt.show()  # 显示图像

        plt.close()  # 关闭当前图像，避免多次调用时覆盖图像






# ##############
# """
# 读取指定路径和指定工作表的Excel文件，并返回工作表内容作为DataFrame。
# 参数：
# - file_path: str，Excel文件的路径
# - sheet_name: str，工作表名称（或索引）
# 返回：
# - df: pandas DataFrame，包含工作表的内容
# """
# ##############

def read_excel_sheet(file_path, sheet_name):

    try:
        # 使用pandas读取Excel文件
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        # 输出读取的数据（可选）
        print(f"成功读取工作表：{sheet_name}")
        # print(df.head())  # 查看前几行数据，便于检查
        
        return df
    except Exception as e:
        print(f"读取文件 {file_path} 失败，错误信息：{e}")
        return None

############################################################################

# 示例使用：指定路径和工作表名称
# xlsx放入py文件同级目录，文件名为main.xlsx
# xlsx文件路径拼接（get_file_path()）
file_path = os.path.join(get_file_path(),'main.xlsx')  # 假设文件名为main.xlsx
# file_path = r'D:\HP\Desktop\Linear\main.xlsx'  # 实际的文件路径
sheet_name = 'Prediction'  # 实际的工作表名称

# 调用函数读取数据
df = read_excel_sheet(file_path, sheet_name)

# 如果成功读取，df会是DataFrame对象，可以继续处理
if df is not None:
    print("工作表数据读取成功！")



process_columns(df, ['持续时间','首首间隔','尾首间隔'])  # 处理指定列

# 预测指定列的list_len + 1 和 list_len + 2 的值
# predict(df, '持续时间', list_len)  # 预测持续时间的list_len + 1 和 list_len + 2 的值

print(get_file_path())  # 输出py文件所在的文件路径


# 示例调用
new_date = add_days("2024-1-18", 10)
