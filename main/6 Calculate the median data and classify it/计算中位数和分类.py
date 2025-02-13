import pandas as pd
df = pd.read_csv("BG.csv")
X = df.drop('Band Gap', axis=1)
y = df['Band Gap']
median_value =y.median()
print(f"The median value is: {median_value}")
df['Band Gap'] = (df['Band Gap'] >=median_value).astype(int)
print(f"processed_with_bool.csv")