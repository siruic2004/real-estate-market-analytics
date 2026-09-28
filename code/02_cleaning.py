#%%
from reusable_function import clean_duplicate
import os 
import pandas as pd
import numpy as np

folder_path = '/Users/chensirui/Desktop/real estate market analytics/data/listed/'
# ============================================
# Data Structure + Quality Check
# 1. duplicates, missing value, data type, datetime format, location format
# ============================================

# ============================================
# 1. Clean Duplicates + Filter Residential 
# ============================================
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
residential_table.to_csv('/Users/chensirui/Desktop/real estate market analytics/listed_clean.csv', index=False)


'''
开始调用function来对listed和sold一起处理
'''
# %%
# %%

sold_folder = '/Users/chensirui/Desktop/real estate market analytics/data/sold/'

cleaned_list = clean_csv(sold_folder)
big_table_listed = concat_df(cleaned_list)
residential_sold = clean_residential(big_table_listed)

residential_sold.to_csv('/Users/chensirui/Desktop/real estate market analytics/sold_clean.csv',index=False)

# ============================================
# 2. Clean Missing Value 
# ============================================
#%%
# %%
def missing_value_report(df, name):
    missing_count = df.isnull().sum()   # isnull return boolean, null = true = 1, sum=count all 1
    missing_percentage = (missing_count / len(df) * 100).round(2)
    report = pd.DataFrame({
        'missing_count': missing_count,
        'missing_percentage': missing_percentage}).sort_values('missing_percentage', ascending=False)

    print(f"{name}: originally {len(df)} rows")
    print(f"missing percentage >90% : {(report['missing_percentage'] > 90).sum()} ")
    return report

# %%
listed_missing = missing_value_report(residential_table, 'Listed')
print(listed_missing)

# %%
sold_missing = missing_value_report(residential_sold, 'Sold')
print(sold_missing)
# %%
miss_list_90 = listed_missing[listed_missing['missing_percentage']>90].index.tolist()
miss_sold_90 = sold_missing[sold_missing['missing_percentage']>90].index.tolist()
listed_nonull = residential_table.drop(columns=miss_list_90)
sold_nonull = residential_sold.drop(columns=miss_sold_90)

print(residential_table.shape, '->', listed_nonull.shape)
print(residential_sold.shape, '->', sold_nonull.shape)

# ============================================
# 3. data type + convert datetime + check wrong input 
# ============================================
# %%
important_factor = ['ClosePrice', 
                    'ListPrice', 
                    'OriginalListPrice', 
                    'LivingArea',
                    'DaysOnMarket', 
                    'BedroomsTotal',
                    'BathroomsTotalInteger',
                    'YearBuilt',
                    'CloseDate', 
                    'LotSizeAcres',
                    'PurchaseContractDate', 
                    'ListingContractDate',
                    'Latitude', 
                    'Longitude']
print(listed_nonull[important_factor].dtypes)
print(sold_nonull[important_factor].dtypes)   # output checked + passed

# convert date from str to datetime
# %%
def convert_date(df):
    df = df.copy()    # make sure original table not affected
    for i in ['CloseDate', 'PurchaseContractDate', 'ListingContractDate', 'ContractStatusChangeDate']:
        if i in df.columns:
            df[i] = pd.to_datetime(df[i], errors='coerce')    # errors = coerce把转不了的变成Nat
    return df

listed_nonull = convert_date(listed_nonull)
sold_nonull = convert_date(sold_nonull)

# check datetime logic is reasonable: Listing ≤ Purchase ≤ Close
# %%
# %%
def datetime_check(df):
    df = df.copy()
    df['list_after_close'] = df['ListingContractDate'] > df['CloseDate']
    df['purchase_after_close'] = df['PurchaseContractDate'] > df['CloseDate']
    df['list_after_purchase'] = df['ListingContractDate'] > df['PurchaseContractDate']
    return df

listed_dated = datetime_check(listed_nonull)
sold_dated = datetime_check(sold_nonull)

datetime_flag = ['list_after_close', 'purchase_after_close', 'list_after_purchase']
print(listed_dated[datetime_flag].sum())
print(sold_dated[datetime_flag].sum())
# %%

# check invalid input
# %%
def invalid_input(df):
    df = df.copy()
    df['invalid_price'] = df['ClosePrice'] <= 0
    df['invalid_area'] = df['LivingArea'] <= 0
    df['invalid_daysonmarket'] = df['DaysOnMarket'] < 0
    df['invalid_bedroom'] = (df['BedroomsTotal'] < 0) 
    df['invalid_bathroom']=(df['BathroomsTotalInteger']<0)
    return df

listed_flagged = invalid_input(listed_dated)
sold_flagged = invalid_input(sold_dated)

invalid_input_flag = ['invalid_price','invalid_area','invalid_daysonmarket','invalid_bedroom','invalid_bathroom']
print(listed_flagged[invalid_input_flag].sum())
print(sold_flagged[invalid_input_flag].sum())

# ============================================
# 4. geo location
# ============================================
# Check geo: bad coordinates put homes in the wrong place on Tableau maps. 
# dataset comes from California Regional MLS, so I focus on Cali. 
# Approximate Cali coordinates: latitude(32, 42.5) + longtitude(-125, -114)
# %%
def geo(df):
    df = df.copy()
    df['geo_missing'] = df['Latitude'].isnull() | df['Longitude'].isnull()   # | is or
    df['geo_zero'] = (df['Latitude'] == 0) | (df['Longitude'] == 0)
    df['geo_out_of_state'] = ~df['Latitude'].between(32, 42.5) | ~df['Longitude'].between(-125, -114)
    return df

listed_geo = geo(listed_flagged)
sold_geo = geo(sold_flagged)

geo_flag = ['geo_missing','geo_zero','geo_out_of_state']
print(listed_geo[geo_flag].sum())
print(sold_geo[geo_flag].sum())
# %%
listed_geo.to_csv('/Users/chensirui/Desktop/real estate market analytics/listed_geo_cleaned.csv', index=False)
sold_geo.to_csv('/Users/chensirui/Desktop/real estate market analytics/sold_geo_cleaned.csv', index=False)
# %%
