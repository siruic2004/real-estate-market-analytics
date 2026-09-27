#%%
def clean_duplicate(df):
    duplicate = []
    for name in df.columns:
        if '.1' in name or '.2' in name:
            duplicate.append(name)
    
    df_clean = df.drop(columns = duplicate)
    return df_clean 


# %%
def clean_csv(folder_path):
    files = os.listdir(folder_path)
    csv_file = []
    for i in files:
        if i.endswith('csv'):
            csv_file.append(i)
    print(f'There are {len(csv_file)} files.')

    all_cleaned = []
    for x in csv_file:
        pathname = folder_path + x
        df = pd.read_csv(pathname)
        cleaned_df = clean_duplicate(df)
        all_cleaned.append(cleaned_df)
    return all_cleaned

# %%
def concat_df(all_cleaned):
    big_table = pd.concat(all_cleaned,ignore_index=True)
    print(len(big_table.columns))
    return big_table

# %%
def clean_residential(big_table):
    print(big_table['PropertyType'].unique()) 
    residential_table = big_table[big_table['PropertyType'] == 'Residential']
    print(f'big_table rows:{len(big_table)}')
    print(f'residential_table rows: {len(residential_table)}')
    return residential_table









# %%
