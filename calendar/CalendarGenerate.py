# Creater: MH
# Created Date: 2025-01-02
# Last Modified: 2025-02-10

import datetime
import numpy as np
import os
import pandas as pd  # 新增：用于处理 Excel 文件
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
from matplotlib import font_manager

# 示例配置（两个配色方案的配置组）
highlight_configs = [
    # 配色方案0的配置
    [
        ["2023-10-24", "2023-10-31"],  # 范围日期使用方案0的主色
        ["2023-12-20"]                 # 单日期使用方案0的次色
    ],
    # 配色方案1的配置 
    [
        ["2023-11-24", "2023-11-28"],  # 范围日期使用方案1的主色
        ["2023-12-25"]                 # 单日期使用方案1的次色
    ]
]

# 其他配置参数
month_names = ['一月', '二月', '三月', '四月', '五月', '六月',
               '七月', '八月', '九月', '十月', '十一月', '十二月']
weekdays = ['日', '一', '二', '三', '四', '五', '六']

# 尺寸参数
cell_size = (60, 40)        
title_height = 40           
week_title_height = 30      
margin = 20                 
font_size = 23         

# 预定义配色方案库
COLOR_SCHEMES = {
    0: {'range': '#FADBD8', 'single': '#F1948A'},  # 过去色系
    1: {'range': '#E8DAEF', 'single': '#E8DAEF'},  # 未来色系
    2: {'range': '#97c8ff', 'single': '#abd3ff'}   # 备用色系
}

# 计算尺寸
month_width = cell_size[0] * 7
month_height = title_height + week_title_height + cell_size[1] * 6
img_width = 3 * month_width + 4 * margin
img_height = 4 * month_height + 5 * margin

# 保存目录设置
save_dir = None  
if save_dir is None:
    save_dir = os.path.dirname(os.path.abspath(__file__))

def hex_to_rgb(hex_color):
    """十六进制转RGB元组"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def parse_highlight_dates(configs):
    """解析多个配色方案的高亮配置"""
    date_colors = {}
    
    for config_idx, config in enumerate(configs):
        scheme = COLOR_SCHEMES[config_idx]
        
        for entry in config:
            # 确定颜色类型
            if len(entry) == 2:
                color_type = 'range'
            elif len(entry) == 1:
                color_type = 'single'
            color = scheme[color_type]

            # 处理日期范围
            start_str = entry[0]
            end_str = entry[-1] if len(entry)==2 else entry[0]
            
            start_date = start_str
            end_date = end_str
            # print(type(start_date), type(end_date))
            # print(start_date, end_date, "\n")

            # 遍历日期范围
            current_date = start_date
            while current_date <= end_date:
                year = current_date.year
                month = current_date.month
                day = current_date.day

                # 如果日期已被其他配色方案标记，跳过（避免覆盖）
                if year not in date_colors:
                    date_colors[year] = {}
                if month not in date_colors[year]:
                    date_colors[year][month] = {}
                if day not in date_colors[year][month]:
                    date_colors[year][month][day] = color
                current_date += datetime.timedelta(days=1)

    return date_colors

def generate_calendar(year, highlight_data):
    """生成带高亮日期的日历"""
    img = Image.new('RGB', (img_width, img_height), 'white')
    draw = ImageDraw.Draw(img)
    
    try:
        # 设置为宋体字体
        # font = ImageFont.truetype("simhei.ttf", font_size)

        # 设置为楷书字体
        font = ImageFont.truetype("simkai.ttf", font_size)
    except:
        font = ImageFont.load_default()

    for month in range(1, 13):
        # 定位月份位置
        row = (month-1) // 3
        col = (month-1) % 3
        x = margin + col * (month_width + margin)
        y = margin + row * (month_height + margin)


        # 计算月份信息
        first_day = datetime.date(year, month, 1)
        total_days = (datetime.date(year+1 if month==12 else year, 
                                  1 if month==12 else month+1, 1) 
                     - datetime.timedelta(days=1)).day
        start_col = first_day.isoweekday() % 7

        # 生成日期布局
        days = [''] * start_col + [str(d) for d in range(1, total_days+1)]
        days += [''] * ((6*7) - len(days))
        month_highlights = highlight_data.get(year, {}).get(month, {})

        # 绘制标题
        title = f"{year} {month_names[month-1]}"
        draw.text((x+30+cell_size[0]*2, y+10), title, font=font, fill='black')

        # 绘制星期栏
        for i, wd in enumerate(weekdays):
            cx = x + i*cell_size[0] + cell_size[0]//2
            cy = y + title_height + week_title_height//2
            draw.text((cx, cy), wd, font=font, fill='black', anchor='mm')

        # 绘制日期格子
        for week in range(6):
            for day_col in range(7):
                idx = week*7 + day_col
                if idx >= len(days) or not days[idx]:
                    continue
                
                day_num = int(days[idx])
                left = x + day_col * cell_size[0]
                top = y + title_height + week_title_height + week * cell_size[1]
                right, bottom = left+cell_size[0], top+cell_size[1]
                
                # 绘制背景色
                hex_color = month_highlights.get(day_num, '#FFFFFF')
                draw.rectangle([left, top, right, bottom], fill=hex_to_rgb(hex_color))
                
                # 绘制日期文字
                dx, dy = left + cell_size[0]//2, top + cell_size[1]//2
                draw.text((dx, dy), str(day_num), font=font, fill='black', anchor='mm')

        # 绘制表格线
        draw.rectangle([x, y, x+month_width, y+month_height], outline='black')
        for i in range(8):
            draw.line([x+i*cell_size[0], y + 40, x+i*cell_size[0], y+month_height], fill='black')
        for i in range(7):
            draw.line([x, y+title_height+week_title_height+i*cell_size[1], 
                      x+month_width, y+title_height+week_title_height+i*cell_size[1]], fill='black')

        draw.line([x, y+title_height, 
                      x+month_width, y+title_height], fill='black')

        # 覆盖空白格子的内部线条（新增部分）
        for week in range(6):
            for day_col in range(7):
                idx = week*7 + day_col
                if idx < len(days) and days[idx] == '':  # 空白单元格
                    # 计算单元格边界
                    cell_left = x + day_col * cell_size[0]
                    cell_top = y + title_height + week_title_height + week * cell_size[1] + 1
                    cell_right = cell_left + cell_size[0]
                    cell_bottom = cell_top + cell_size[1] - 2

                    # 覆盖右侧垂直线（非最后一列）
                    if day_col < 6 and days[idx + 1] == '':
                        draw.line([cell_right, cell_top, cell_right, cell_bottom], 
                                 fill='white', width=1)
                    
                    # 覆盖底部水平线（非最后一行）
                    if week == 4 :
                        draw.line([cell_left, cell_bottom + 1, cell_right - 1, cell_bottom + 1],
                                 fill='white', width=1)

    # 保存图片
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    save_path = os.path.join(save_dir, f'calendar_{year}.png')
    img.save(save_path, dpi=(500, 500), quality=100)


def read_excel_to_df():
    """
    读取当前目录下的 main.xlsx 文件的 prediction 工作表，返回 DataFrame。
    如果文件或工作表不存在，返回 None。
    """
    try:
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'main.xlsx')
        df = pd.read_excel(file_path, sheet_name='Prediction')
        return df
    except Exception as e:
        print(f"读取 Excel 文件失败: {e}")
        return None

def calculate_column_average(df, column_name):
    """
    计算指定列的平均值，并返回保留 0 位小数的结果。
    如果列不存在或列中无非数值数据，返回 None。
    """
    if column_name not in df.columns:
        print(f"列 '{column_name}' 不存在")
        return None
    
    try:
        # 计算平均值并四舍五入到 0 位小数
        average = round(df[column_name].mean(), 0)
        return int(average)  # 将结果转换为整数
    except Exception as e:
        print(f"计算平均值失败: {e}")
        return None
# 数据处理
def data_process(df):
    """（已由advanced_data_processing替代，可删除）"""
    return advanced_data_processing(df)

# 计算df列表里非空值的个数
def len_not_null(df, col):
    return len(df[df[col].notnull()])


# 生成高亮日期
def generate_highlight_dates(df):
    # 读取历史记录
    start_dates = df['开始日期']
    end_dates   = df['结束日期']
    history_dates = []
    future_dates = []
    
    scale = min(len_not_null(df, '开始日期'), len_not_null(df, '结束日期'))       
    for i in range(scale):
        history_dates.append([start_dates[i].date(), end_dates[i].date()])

    # 计算平均持续时间和平均首首间隔
    average_duration, average_gap = data_process(df)

    if len_not_null(df, '开始日期') != len_not_null(df, '结束日期'):
        # 最后一个值
        history_dates.append([start_dates[scale].date()])
        print(f"历史记录条目数不一致，截取前 {scale} 条")
        last_date = history_dates[-1][0]
        print(f"最后日期: {last_date}")
        # 计算未来日期
        future_dates.append([last_date + datetime.timedelta(days=1) ,last_date + datetime.timedelta(days=average_duration)])
    else:
        last_date = history_dates[-1][0]
        print("日期记录完整！！！")

# 循环次数A为预测之后的A次日期
    for i in range(20):
        future_dates.append([last_date + datetime.timedelta(days=average_gap*(i+1)), last_date + datetime.timedelta(days=average_gap*(i+1) + average_duration)])

    highlight_configs = [history_dates, future_dates]
    return highlight_configs

def combine_calendar_images():
    """
    将生成的日历图片垂直拼接成一张长图
    """
    # 获取需要拼接的年份范围
    current_year = datetime.datetime.now().year
    years = range(2023, current_year + 1)
    
    # 加载所有图片
    images = []
    for year in years:
        img_path = os.path.join(save_dir, f'calendar_{year}.png')
        try:
            img = Image.open(img_path)
            images.append(img)
        except FileNotFoundError:
            print(f"警告：{year}年的日历图片不存在，已跳过")
            continue
    
    if not images:
        print("没有找到可拼接的图片")
        return

    # 计算总尺寸
    total_height = sum(img.height for img in images)
    max_width = max(img.width for img in images)

    # 创建新画布
    combined_img = Image.new('RGB', (max_width, total_height), 'white')
    
    # 垂直拼接
    y_offset = 0
    for img in images:
        combined_img.paste(img, (0, y_offset))
        y_offset += img.height

    # 保存结果
    save_path = os.path.join(save_dir, 'combined_calendars.png')
    combined_img.save(save_path, dpi=(500, 500), quality=100)
    print(f"已生成拼接后的完整日历：{save_path}")


# 在现有代码基础上新增/修改以下内容：
# 新增字体配置（在尺寸参数后添加）
font_path = 'C:/Windows/Fonts/simhei.ttf'  # 黑体字体路径

def linear_fit_auto(y_values):
    """线性拟合函数（移植自Liner.py并优化）"""
    try:
        y_mean = np.mean(y_values)
        filtered_values = [y for y in y_values if (y_mean - 10) <= y <= (y_mean + 10)]
        if len(filtered_values) == 0:
            print("没有符合条件的数据进行拟合")
            return None, None

        x_values = np.arange(1, len(filtered_values) + 1)
        x = np.array(x_values)
        y = np.array(filtered_values)

        x_mean = np.mean(x)
        y_mean = np.mean(y)

        numerator = np.sum((x - x_mean) * (y - y_mean))
        denominator = np.sum((x - x_mean) ** 2)

        a = numerator / denominator if denominator != 0 else 0
        b = y_mean - a * x_mean

        print(f"拟合方程：y = {a:.2f} * x + {b:.2f}")
        return a, b
    except Exception as e:
        print(f"拟合失败: {e}")
        return None, None

def plot_linear_fit(df, column_name, list_len):
    """生成单列的拟合图表（优化版）"""
    try:
        # 设置中文字体
        font = font_manager.FontProperties(fname=font_path)
        plt.rcParams['font.family'] = font.get_name()

        # 获取处理后的数据
        processed_data = df[column_name][0:list_len]
        
        # 执行线性拟合
        a, b = linear_fit_auto(processed_data)
        if a is None or b is None:
            return

        # 创建图表
        plt.figure(figsize=(10, 6))
        x_vals = np.arange(1, list_len + 1)
        
        # 绘制原始数据
        plt.scatter(x_vals, processed_data, color='#3498db', label='原始数据', zorder=3)
        
        # 绘制拟合线
        if a != 0:
            y_vals = a * x_vals + b
            plt.plot(x_vals, y_vals, color='#e74c3c', 
                    linewidth=2.5, label=f'拟合线: y = {a:.2f}x + {b:.2f}')
        
        # 绘制均值线
        mean_val = np.mean(processed_data)
        plt.axhline(mean_val, color='#2ecc71', linestyle='--', 
                   label=f'均值线: y = {mean_val:.2f}')

        # 图表装饰
        plt.title(f'{column_name} 线性拟合分析', fontsize=14, pad=20)
        plt.xlabel('周期数', fontsize=12)
        plt.ylabel('天数', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.legend(loc='upper left', frameon=False)
        
        # 保存图表
        save_path = os.path.join(save_dir, f'{column_name}_拟合分析.png')
        plt.savefig(save_path, dpi=120, bbox_inches='tight')
        print(f"成功生成拟合图表：{save_path}")
        plt.close()
    except Exception as e:
        print(f"生成图表失败: {e}")

def plot_interval_trend(df, column_name, list_len):
    """
    绘制指定列的折线图并保存
    参数：
    - df: 包含数据的DataFrame
    - column_name: 要绘制的列名（如'首首间隔'）
    - list_len: 有效数据长度
    """
    try:
        # 设置中文字体
        font = font_manager.FontProperties(fname=font_path)
        plt.rcParams['font.family'] = font.get_name()
        
        # 准备数据
        data = df[column_name].iloc[:list_len]
        x = np.arange(1, len(data)+1)
        y = data.values
        
        # 创建画布
        plt.figure(figsize=(10, 6))
        
        # 绘制主折线
        plt.plot(x, y, 
                color='#2980b9',   # 主线条颜色
                linewidth=2.5, 
                marker='o',        # 数据点标记
                markersize=8,
                markerfacecolor='#ffffff',
                markeredgewidth=1.5,
                markeredgecolor='#2980b9',
                label=column_name)
        
        # 添加趋势线（可选）
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        plt.plot(x, p(x), 
                color='#e74c3c', 
                linestyle='--', 
                linewidth=1.8,
                label='趋势线')
        
        # 图表装饰
        plt.title(f'{column_name} 周期变化趋势', fontsize=14, pad=15)
        plt.xlabel('周期序号', fontsize=12)
        plt.ylabel('间隔天数', fontsize=12)
        plt.xticks(np.arange(1, len(x)+1, step=max(1, len(x)//10)))  # 自动刻度密度
        plt.grid(True, alpha=0.3)
        plt.legend(frameon=False)
        
        # 自动调整布局
        plt.tight_layout()
        
        # 保存文件
        save_path = os.path.join(save_dir, f'{column_name}_趋势分析.png')
        plt.savefig(save_path, dpi=120, bbox_inches='tight')
        print(f"趋势图已保存至：{save_path}")
        plt.close()
        
    except Exception as e:
        print(f"生成趋势图失败：{str(e)}")

def advanced_data_processing(df):
    """增强版数据处理（整合原有data_process和拟合功能）"""
    # 计算有效数据长度
    list_len = min(
        len_not_null(df, '持续时间'),
        len_not_null(df, '首首间隔')
    )
    
    # 计算平均值
    avg_duration = calculate_column_average(df, '持续时间')
    avg_interval = calculate_column_average(df, '首首间隔')
    
    # print("\n----- 统计分析结果 -----")
    # print(f"有效数据周期数: {list_len}")
    # print(f"平均持续时间: {avg_duration} 天")
    # print(f"平均首首间隔: {avg_interval} 天\n")
    
    # 生成拟合图表
    print("----- 生成拟合图表 -----")
    plot_linear_fit(df, '持续时间', list_len)
    plot_linear_fit(df, '首首间隔', list_len)
    plot_interval_trend(df, '持续时间', list_len)
    plot_interval_trend(df, '首首间隔', list_len)
    
    return avg_duration, avg_interval

# 新增生成图表图片功能
def combine_graph_images():
    """
    垂直拼接四张图表图片：
    1. 持续时间_拟合分析.png
    2. 首首间隔_拟合分析.png
    3. 持续时间_趋势分析.png
    4. 首首间隔_趋势分析.png
    保存为 data_analys_graph.png
    """
    try:
        # 定义要拼接的图片文件名
        image_files = [
            '持续时间_拟合分析.png',
            '首首间隔_拟合分析.png',
            '持续时间_趋势分析.png',
            '首首间隔_趋势分析.png'
        ]
        
        # 加载所有图片
        images = []
        for file in image_files:
            img_path = os.path.join(save_dir, file)
            if os.path.exists(img_path):
                img = Image.open(img_path)
                images.append(img)
            else:
                print(f"警告：{file} 不存在，已跳过")
        
        if not images:
            print("没有找到可拼接的图片")
            return
        
        # 计算总高度和最大宽度
        total_height = sum(img.height for img in images)
        max_width = max(img.width for img in images)
        
        # 创建新画布
        combined_img = Image.new('RGB', (max_width, total_height), 'white')
        
        # 垂直拼接
        y_offset = 0
        for img in images:
            combined_img.paste(img, (0, y_offset))
            y_offset += img.height
        
        # 保存结果
        save_path = os.path.join(save_dir, 'data_analys_graph.png')
        combined_img.save(save_path, dpi=(300, 300), quality=100)
        print(f"图表拼接完成，保存至：{save_path}")
    except Exception as e:
        print(f"图表拼接失败：{e}")

def combine_all_results():
    """
    1. 调用 combine_calendar_images 生成 combined_calendars.png
    2. 调用 combine_graph_images 生成 data_analys_graph.png
    3. 将两张图片左右拼接，保存为 数据分析结果.jpg
    """
    try:
        # 生成日历拼接图
        combine_calendar_images()
        
        # 生成图表拼接图
        combine_graph_images()
        
        # 加载两张图片
        calendar_img_path = os.path.join(save_dir, 'combined_calendars.png')
        graph_img_path = os.path.join(save_dir, 'data_analys_graph.png')
        
        if not os.path.exists(calendar_img_path) or not os.path.exists(graph_img_path):
            print("无法拼接，部分图片缺失")
            return
        
        calendar_img = Image.open(calendar_img_path)
        graph_img = Image.open(graph_img_path)
        
        # 计算总宽度和最大高度
        total_width = calendar_img.width + graph_img.width
        max_height = max(calendar_img.height, graph_img.height)
        
        # 创建新画布
        combined_img = Image.new('RGB', (total_width, max_height), 'white')
        
        # 左右拼接
        combined_img.paste(calendar_img, (0, 0))
        combined_img.paste(graph_img, (calendar_img.width, 0))
        
        # 保存结果
        save_path = os.path.join(save_dir, '数据分析结果.jpg')
        combined_img.save(save_path, dpi=(300, 300), quality=100)
        print(f"最终拼接完成，保存至：{save_path}")
    except Exception as e:
        print(f"最终拼接失败：{e}")


if __name__ == '__main__':
    # 读取数据
    df = read_excel_to_df()
    if df is None:
        exit()
    
    # 执行增强数据处理
    avg_duration, avg_interval = advanced_data_processing(df)
    
    # 生成日历相关逻辑
    highlight_configs = generate_highlight_dates(df)
    highlight_dates = parse_highlight_dates(highlight_configs)
    
    # 生成日历
    current_year = datetime.datetime.now().year
    for year in range(2023, current_year + 1):
        generate_calendar(year, highlight_dates)
        print(f"生成 {year} 年日历成功")
    
    # 生成最终拼接结果
    combine_all_results()
    print("拼接成功")