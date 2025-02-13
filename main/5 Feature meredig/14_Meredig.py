import pandas as pd
from pymatgen.core import Composition
from matminer.featurizers.composition import ElementFraction

# 从指定路径读取 Excel 文件，替换为你的文件路径
file_path = r'C:\Users\lhl\Desktop\Filtered_Chemical_Formula.xlsx'

# 读取 Excel 文件
# 假设你要提取的材料组成在名为 'Sheet1' 的工作表的 'Materials' 列中
# 根据你的表格结构适当修改
df = pd.read_excel(file_path, sheet_name='Sheet1')

# 确保列名称正确
print(df.columns.tolist())  # 显示前几行，验证列名称是否正确

# 提取指定列（假设列名为 'Materials'）
compositions = df['Materials'].tolist()

# 创建 Meredig 特征提取器实例
ef = ElementFraction()

# 用于存储每个材料特征的列表
feature_list = []

# 循环遍历每个成分并提取特征
for comp in compositions:
    try:
        a = Composition(comp)  # 创建材料组成
        features = ef.featurize(a)  # 提取特征
        feature_list.append(features)  # 将特征添加到列表中
    except Exception as e:
        print(f"Error processing {comp}: {e}")  # 错误处理

# 创建 DataFrame
df_features = pd.DataFrame(feature_list, columns=ef.feature_labels())

# 合并原始数据框和特征数据框
result_df = pd.concat([df, df_features], axis=1)

# 输出特征数据框
print(result_df)
# 将结果保存到新的 Excel 文件
result_df.to_excel(r'c:\Users\lhl\Desktop\garnet_compsoition\Filtered_Chemical_Formula_by_ElementFraction.xlsx', index=False)