import pandas as pd
import re
from collections import defaultdict
import os

# 读取 Excel 文件
file_path = r'C:\Users\lhl\Desktop\Mr_Yang_paper\garnet_compsoition\8.15_garnet.xlsx'
df = pd.read_excel(file_path)

# 打印DataFrame的内容和列名以进行调试
print("DataFrame内容:")
print(df.head())  # 打印前几行
print("列名:", df.columns)  # 打印列名

# 假设化学式在第十七列
chemical_formulas = df.iloc[:, 16]  # 确保使用正确的列索引

# 创建字典来存储每一位的元素统计
element_stats = defaultdict(lambda: defaultdict(int))

# 遍历每一个化学式
for formula in chemical_formulas:
    # 使用正则表达式分解化学式，找到所有的元素和其数量
    matches = re.findall(r'([A-Z][a-z]?)(\d*)', formula)

    # 遍历所有找到的元素
    for i, (element, count) in enumerate(matches):
        count = int(count) if count else 1  # 如果没有数量则默认为1
        element_stats[i + 1][element] += count

# 打印每一位上元素的统计信息
for position, elements in element_stats.items():
    print(f"第 {position} 位的元素统计:")
    for element, count in elements.items():
        print(f"元素: {element}, 计数: {count}")
    print()  # 打印空行以便于阅读

# 准备导出数据
export_data = []

# 填充导出数据
for position, elements in element_stats.items():
    for element, count in elements.items():
        export_data.append({'location': position, 'elemental': element, 'count': count})

# 创建一个 DataFrame
export_df = pd.DataFrame(export_data)

# 尝试导出为 Excel 文件，保存到桌面
output_file_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'element_statistics.xlsx')
try:
    export_df.to_excel(output_file_path, index=False)
    print(f"统计结果已导出到 {output_file_path}")
except PermissionError as e:
    print(f"无法导出文件，出现权限错误: {e}")

# 重新排列组合元素，形成新的化学式
combinations = []
first_elements = list(element_stats[1].keys())  # 提取第1位的元素
second_elements = list(element_stats[2].keys())  # 提取第2位的元素
third_elements = list(element_stats[3].keys())  # 提取第3位的元素
fourth_elements = list(element_stats[4].keys())  # 提取第4位的元素

# 生成所有可能的组合，使用指定的数字
for first in first_elements:
    for second in second_elements:
        for third in third_elements:
            for fourth in fourth_elements:
                # 检查是否有重复元素
                if len({first, second, third, fourth}) == 4:  # 确保没有重复元素
                    new_formula = f"{first}3{second}2{third}3{fourth}12"  # 固定格式
                    combinations.append(new_formula)

# 将组合结果导出到新的 Excel 文件
combinations_df = pd.DataFrame(combinations, columns=['Materials'])
combinations_output_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'new_chemical_formulas.xlsx')
try:
    combinations_df.to_excel(combinations_output_path, index=False)
    print(f"新化学式已导出到 {combinations_output_path}")
except PermissionError as e:
    print(f"无法导出文件，出现权限错误: {e}")