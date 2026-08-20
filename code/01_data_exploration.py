# since dataset itself is monthly , I need to combine them together
# I only care about residential housing, so filter 

# merge dataset + filter  --> pandas
# pandas是专门处理excel表格/table的。 如果数据是表格，就用pandas读取
# matplotlib + seaborn 是用来更漂亮的画统计图
# scikit-learn用来做 ML (regression, randomforest, train_test_split...)
# numpy用来做数学运算 （统计学，algebra, matrix, vector..)

# 当检查路径时： 先pwd (present work directory)，再ls (看list)

import pandas as pd


# 1. 先打印任意csv看一下列名，知道数据里有什么
listed_jan = pd.read_csv('/Users/chensirui/Desktop/real estate market analytics/data/listed/CRMLSListing202401.csv')
print(listed_jan.columns)    # 打印出的结果可以看到重复列名，这不是一个clean dataset

# %%
print(listed_jan.dtypes)