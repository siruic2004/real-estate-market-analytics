# use cleaned data to build market metrics
# 1. price ratio = closeprice/listprice. If >1, means house is popular
# 2. close_to_orig_price = closeprice/ORIGINALlistprice. Seller might already changed price before sell, we look at original price
# 3. ppsf = closeprice/liveing_area. Get per sqft price.
# 4. year/month/yr_mo. Closedata is by day, have to groupby month/year....
# 5. listing_to_contract = purchase_contract_date - listing_contract_date 从挂牌到买家签合同(接受报价),隔了几天
# 6. contract_to_close = closedate - purchasecontractdate . 过户流程花了几天
#%%
import pandas as pd
# %%
# Load cleaned data. CSV does not keep dtypes, so re-parse the dates here.
date = ['CloseDate', 'PurchaseContractDate', 'ListingContractDate', 'ContractStatusChangeDate']
sold_rate = pd.read_csv(
    '/Users/chensirui/Desktop/real estate market analytics/data/middle_steps/sold_rates.csv',
    parse_dates=date)   # parse_dates means auto-trans to date format

#%%
def new_features(df):
    df = df.copy()

    # price
    valid_area = ~df['invalid_area']
    valid_price = ~df['invalid_price']
    df['price_ratio'] = df['ClosePrice'] / df['ListPrice']
    df['close_to_orig_ratio'] = df['ClosePrice'] / df['OriginalListPrice']

    # only keep valid_area & valid_price = True; other invalid turn to Nan
    df['ppsf'] = (df['ClosePrice'] / df['LivingArea']).where(valid_area & valid_price)

    # get time features 
    df['year'] = df['CloseDate'].dt.year   # only year 
    df['month'] = df['CloseDate'].dt.month     # only month ( from 1 -12)
    df['yr_mo'] = df['CloseDate'].dt.to_period('M')   # year+month combo: 2xxx-01

    # uses days to get the peridd length . Day = 1 single day, days = a period length 
    listing_to_contract = (df['PurchaseContractDate'] - df['ListingContractDate']).dt.days
    contract_to_close = (df['CloseDate'] - df['PurchaseContractDate']).dt.days

    # label incorrect days 
    bad_dates = df['list_after_purchase'] | df['purchase_after_close']
    df['listing_to_contract'] = listing_to_contract.where(~bad_dates)
    df['contract_to_close'] = contract_to_close.where(~bad_dates)

    return df

sold_features = new_features(sold_rate)


# %%
new_cols = ['price_ratio', 'close_to_orig_ratio', 'ppsf', 'yr_mo',
            'listing_to_contract', 'contract_to_close']

print(sold_features[new_cols].isnull().sum())
# close_to__orig_ratio has most null, yr_mo = 0 


# %%
sold_features.to_csv(
    '/Users/chensirui/Desktop/real estate market analytics/data/middle_steps/sold_features.csv',index=False)
