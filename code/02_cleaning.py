#%%
from reusable_function import clean_duplicate
import os 
import pandas as pd
import numpy as np

folder_path = '/Users/chensirui/Desktop/real estate market analytics/data/listed/'

# %%
files = os.listdir(folder_path)
print(files)

# %%
# 清理一下data保证只有csv结尾的在
csv_file = []
for i in files:
    if i.endswith('csv'):
        csv_file.append(i)
print(f'There are {len(csv_file)} files.')
print(csv_file)
# 这里结束后得到27个独立的csv文件。每个文件都是一个月的数据
# 之前写了df_clean这个function，现在所有月份都需要扔进去跑一轮

# %%
all_cleaned = []
for x in csv_file:
    pathname = folder_path + x
    df = pd.read_csv(pathname)
    cleaned_df = clean_duplicate(df)
    all_cleaned.append(cleaned_df)

# 27个文件都清理完了，现在要合并到一张大表格
# %%
big_table = pd.concat(all_cleaned,ignore_index=True)
print(len(big_table.columns))

#现在只关注residential住宅，所以要filter
# %%
print(big_table['PropertyType'].unique())  # 先看一下房子的类型，确定residential的拼写

#%%
residential_table = big_table[big_table['PropertyType'] == 'Residential']
# []内的== 代表T or F，外面的才是筛选条件
print(f'big_table rows:{len(big_table)}')
print(f'residential_table rows: {len(residential_table)}')

#存成一个新的csv文件
# %%
residential_table.to_csv('/Users/chensirui/Desktop/real estate market analytics/listed_clean', index=False)


'''
开始调用function来对listed和sold一起处理
'''
# %%
# %%
sold_folder = '/Users/chensirui/Desktop/real estate market analytics/data/sold/'

cleaned_list = clean_csv(sold_folder)
big_table_listed = concat_df(cleaned_list)
residential_listed = clean_residential(big_table_listed)

residential_listed.to_csv('/Users/chensirui/Desktop/real estate market analytics/sold_clean',index=False)
