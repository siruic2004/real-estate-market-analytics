# Prep for data entering tableau 
# key point: csv doesn't save format! so convert datetime again

# %%
import pandas as pd

date = ['CloseDate', 'PurchaseContractDate', 'ListingContractDate', 'ContractStatusChangeDate']

# %% 
sold = pd.read_csv('/Users/chensirui/Desktop/real estate market analytics/data/middle_steps/sold_outlier.csv', parse_dates=date)

outlier_columns = []
for i in sold.columns:
    if i.endswith('_outlier'):
        outlier_columns.append(i)

invalid_columns = ['invalid_price', 'invalid_area', 'invalid_daysonmarket', 'invalid_bedroom', 'invalid_bathroom']

# exclude outlier + invalid columns
exclude = sold[outlier_columns + invalid_columns].any(axis=1)
sold_clean = sold[~exclude].copy()

# group by month 
sold_clean['month_start'] = sold_clean['CloseDate'].dt.to_period('M').dt.to_timestamp()  # convert to timestamp 

sold_NoInvalidAndOutliers= sold_clean[(sold_clean['month_start'] >= '2024-01-01') & (sold_clean['month_start'] <= '2026-04-01')]

print('sold total rows:', len(sold), '-> clean rows:', len(sold_clean))
print('missing mortgage rates:', sold_clean['30years_fixed_rate'].isnull().sum())   
print('ClosePrice median before -> after:', sold['ClosePrice'].median(), '->', sold_clean['ClosePrice'].median())

sold_NoInvalidAndOutliers.to_csv('/Users/chensirui/Desktop/real estate market analytics/data/middle_steps/sold_NoInvalidAndOutliers.csv', index=False)   

# %% 
listed = pd.read_csv('/Users/chensirui/Desktop/real estate market analytics/data/middle_steps/listed_rates.csv', parse_dates=date)
listed['month_start'] = listed['ListingContractDate'].dt.to_period('M').dt.to_timestamp()
listed_NoInvalidAndOutliers = listed[(listed['month_start'] >= '2024-01-01') &(listed['month_start'] <= '2026-03-01')]

print('listed rows:', len(listed))
print('missing mortgage rates:', listed['30years_fixed_rate'].isnull().sum())

listed_NoInvalidAndOutliers.to_csv('/Users/chensirui/Desktop/real estate market analytics/data/middle_steps/listed_NoInvalidAndOutliers.csv', index=False)



# %%
