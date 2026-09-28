# Use IQR to detect outliers
# 1. Housing prices are skewed (few very high-priced homes create a long tail), so mean/std-based methods will not work
# 2. No arbitrary fixed threshold (e.g. certain price) needed - IQR adapts to each field's own distribution
# Normal Range = [Q1 − 1.5×IQR,  Q3 + 1.5×IQR]

#%%
import pandas as pd
# %%
date = ['CloseDate', 'PurchaseContractDate', 'ListingContractDate', 'ContractStatusChangeDate']
sold_features = pd.read_csv(
    '/Users/chensirui/Desktop/real estate market analytics/data/middle_steps/sold_features.csv',
    parse_dates=date)

# %%
def outlier_IQR(df, col):
    Q1 = df[col].quantile(1/4)
    Q3 = df[col].quantile(3/4)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    flag_col = f'{col}_outlier'
    df[flag_col] = (df[col] < lower) | (df[col] > upper) 

    print(f"{col}: Q1={Q1:.1f}, Q3={Q3:.1f}, IQR={IQR:.1f}, normal range=[{lower:.1f}, {upper:.1f}]")
    print(f"{col} outliers: {df[flag_col].sum()}")
    return df

# %%
IQR_cols = ['ClosePrice', 'LivingArea', 'DaysOnMarket'] 
sold_outlier = sold_features.copy()
for col in IQR_cols:
    sold_outlier = outlier_IQR(sold_outlier, col)

#%%   verify above number
Q1 = sold_outlier['ClosePrice'].quantile(1/4)
Q3 = sold_outlier['ClosePrice'].quantile(3/4)
IQR = Q3 - Q1
upper = Q3 + 1.5 * IQR

print("higher:", (sold_outlier['ClosePrice'] > upper).sum())
print("lower:", (sold_outlier['ClosePrice'] < (Q1 - 1.5*IQR)).sum())



# %%
outlier_cols = []
for c in sold_outlier.columns:
    if c.endswith('_outlier'):   # get all outlier-related columns 
        outlier_cols.append(c)
print(sold_outlier[outlier_cols].sum())    # sum to see how many outliers each category have 

#%%
has_outlier = sold_outlier[outlier_cols].any(axis=1)   # in this row even 1 outlier counts
no_outlier = sold_outlier[~ has_outlier]
original_rows = len(sold_outlier)
clean_rows = len(no_outlier)
print("original rows:", original_rows)
print("clean rows:", clean_rows)

original_median = sold_outlier['ClosePrice'].median()
clean_median = no_outlier['ClosePrice'].median()
print("oringinal ClosePrice median:", original_median)
print("clean ClosePrice median:", clean_median)


# %%
sold_outlier.to_csv('/Users/chensirui/Desktop/real estate market analytics/data/middle_steps/sold_outlier.csv', index=False)
# %%
