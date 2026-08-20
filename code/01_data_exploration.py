# since dataset itself is monthly , I need to combine them together
# I only care about residential housing, so filter 
# 用 # %%来创立一个新的cell

# merge dataset + filter  --> pandas
# pandas是专门处理excel表格/table的。 如果数据是表格，就用pandas读取
# matplotlib + seaborn 是用来更漂亮的画统计图
# scikit-learn用来做 ML (regression, randomforest, train_test_split...)
# numpy用来做数学运算 （统计学，algebra, matrix, vector..)

# 当检查路径时： 先pwd (present work directory)，再ls (看list)

# %%
import pandas as pd

# 1. 先打印任意csv看一下列名，知道数据里有什么
listed_jan = pd.read_csv('/Users/chensirui/Desktop/real estate market analytics/data/listed/CRMLSListing202401.csv')
print(listed_jan.columns)    # 打印出的结果可以看到重复列名，这不是一个clean dataset
print(listed_jan.dtypes)

# %% 2. 检查为什么有重复列名
column_count = pd.Series(listed_jan.columns).value_counts()
print(column_count)  # 这里看不到count大于1的，因为pandas已经预处理了文件, 在文件后面加入了.1, .2等来区分。

# %%  3. 检查哪些名字后缀有.1, .2...
dup_column = []
for col in listed_jan.columns:
    if '.1' in col or '.2' in col:
        dup_column.append(col)

print(f'存在{len(dup_column)}个列被重命名过')

# %%   4. 打印出这些列
for col in dup_column:
    print(col)

# %% 5. 检查这些列是真的内容完全重复，还是错误命名
print((listed_jan['PropertyType'] == listed_jan['PropertyType.1']).all())
# .all()的作用是得出总结论，只要有一个不相等就是no

# %% 6.因为知道都是完全重复的，所以可以drop
listed_jan_clean = listed_jan.drop(columns = dup_column)

# %% 检查是否删除了11行
print(listed_jan.shape)
print(listed_jan_clean.shape)
# %%
