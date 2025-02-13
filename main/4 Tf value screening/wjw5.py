import pandas as pd
import math

# 设置文件路径
input_file_path = r'C:\Users\lhl\Desktop\element_statistics_radii.xlsx'  # 输入文件路径
output_file_path = r'C:\Users\lhl\Desktop\element_statistics_radii_and_Tf_fen.xlsx'  # 输出文件路径

# 读取 Excel 表格
df = pd.read_excel(input_file_path)

# 提取不同 location 对应的元素和原子半径
elements_A = df.loc[df['location'] == 1, 'elemental'].tolist()  # location = 1
elements_B = df.loc[df['location'] == 2, 'elemental'].tolist()  # location = 2
elements_C = df.loc[df['location'] == 3, 'elemental'].tolist()  # location = 3
elements_D = df.loc[df['location'] == 4, 'elemental'].tolist()  # location = 4

# 提取原子半径值
radii_A = df.loc[df['location'] == 1, 'Atomic_Radius_Pm'].values  # location = 1
radii_B = df.loc[df['location'] == 2, 'Atomic_Radius_Pm'].values  # location = 2
radii_C = df.loc[df['location'] == 3, 'Atomic_Radius_Pm'].values  # location = 3
radii_D = df.loc[df['location'] == 4, 'Atomic_Radius_Pm'].values  # location = 4

# 生成化学式的排列组合并计算 Tf 值
results = []

for i, a in enumerate(elements_A):
    for j, b in enumerate(elements_B):
        for k, c in enumerate(elements_C):
            for l, d in enumerate(elements_D):
                if len({a, b, c, d}) == 4:  # 确保没有重复元素
                    # 生成化学式
                    chemical_formula = f"{a}3{b}2{c}3{d}12"

                    # 获取对应的原子半径
                    Ra = radii_A[i] if i < len(radii_A) else None
                    Rb = radii_B[j] if j < len(radii_B) else None
                    Rc = radii_C[k] if k < len(radii_C) else None
                    Rx = radii_D[l] if l < len(radii_D) else None

                     # 计算 Tf 值
                    if Ra is not None and Rb is not None and Rc is not None and Rx is not None:
                     # 计算 a
                        a_value = (Rb + Rx) ** 2 - (Ra + Rx) ** 2 * (4 / 9)
                        if a_value < 0:
                            Tf = None  # 如果 a_value 为负，则 Tf 设为 None
                        else:
                            a_value = math.pow(a_value, 1 / 2)  # 开二次方根
                            # 计算 b
                            b_value = 2 * (Rc + Rx)
                            # 计算 Tf
                            Tf = (3*a_value) / b_value if b_value != 0 else None  # 避免除以零
                    else:
                        Tf = None

                    # 将化学式和 Tf 值添加到结果列表
                    results.append({'Chemical_Formula': chemical_formula, 'Tf': Tf})

# 创建 DataFrame 来存储结果
results_df = pd.DataFrame(results)

# 筛选 Tf 值在 0.9 到 1.1 之间的化学式
filtered_results = results_df[(results_df['Tf'] > 0.9) & (results_df['Tf'] < 1.1)]

# 将筛选结果添加到新的列中
results_df['Filtered_Chemical_Formula'] = filtered_results['Chemical_Formula'].where(filtered_results['Tf'].notna())

# 输出到新的 Excel 文件
results_df.to_excel(output_file_path, index=False)

print(f"化学式和 Tf 值已输出到 {output_file_path}，并筛选出 Tf 值在 0.9 到 1.1 之间的化学式！")