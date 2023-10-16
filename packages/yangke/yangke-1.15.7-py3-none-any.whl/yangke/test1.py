import pandas as pd
from yangke.common.fileOperate import read_csv_ex, read_excel
from yangke.base import merge_two_dataframes
import numpy as np
data1 = read_excel(r"C:\Users\YangKe\Desktop\京能2022年1号机数据.xlsx", need_merge=True)
data2 = read_excel(r"C:\Users\YangKe\Desktop\华润2022年2号机间冷循环水数据.xlsx", need_merge=True)


# 多列滚动函数
# handle对滚动的数据框进行处理
def handle(x, df, name, n):
    df = df[name].iloc[x:x + n, :]
    print(df)
    return 1


# group_rolling 进行滚动
# n：滚动的行数
# df：目标数据框
# name：要滚动的列名
def group_rolling(n, df, name):
    df_roll = pd.DataFrame({'a': list(range(len(df) - n + 1))})
    df_roll['a'].rolling(window=1).apply(lambda x: handle(int(x[0]), df, name, n), raw=True)


data1.dropna(how='any', axis=0, inplace=True)
data2.dropna(how='any', axis=0, inplace=True)
from yangke.base import interpolate_df

data1 = interpolate_df(data1, time_interval=60)
data2 = interpolate_df(data2, time_interval=60)
# group_rolling(20, data, ['功率'])
gonglv = data['功率']

for i in range(gonglv.shape[0]):
    d = gonglv[i]

print("...")
numbers = [float(eval(f"self.lineEdit_{i}.text()")) for i in range(1, 10)]
np.array(numbers).tofile("test.txt")