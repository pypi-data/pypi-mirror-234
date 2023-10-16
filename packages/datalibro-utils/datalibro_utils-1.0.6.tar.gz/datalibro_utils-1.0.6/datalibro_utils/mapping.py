import pandas as pd
import tablemaster as tm
import re

def sku_get_brand(sku):
    try:
        return sku[:2]
    except:
        return 'unknown'

def sku_get_model(sku):
    try:
        return sku.split("-")[1]
    except:
        return 'unknown'

def sku_get_sku_code(sku):
    try:
        return sku.split("-")[1][:2]
    except:
        return 'unknown'

def sku_get_product_line(sku, map_sku_code):
    miss_info = ''
    sku_code = sku_get_sku_code(sku)
    try:
        product_line = map_sku_code.loc[map_sku_code['code']==sku_code, 'product_line'].iloc[0]
    except:
        product_line = ""
        miss_info = f'product line of {sku} not found, please update!'
    return product_line, miss_info

def sku_get_product_type(sku, map_sku_code):
    miss_info = ''
    sku_code = sku_get_sku_code(sku)
    try:
        product_type = map_sku_code.loc[map_sku_code['code']==sku_code, 'product_type'].iloc[0]
    except:
        product_type = ""
        miss_info = f'product type of {sku} not found, please update!'
    return product_type, miss_info

def sku_get_scu(sku, map_scu):
    try:
        if(sku in map_scu['SKU'].astype(str).to_list()):
            scu = map_scu.loc[map_scu['SKU']==sku, 'SCU'].iloc[0]
        else:
            scu = sku_get_model(sku)
        return scu
    except:
        return 'unknown'

def sku_get_app_product(sku, map_app_product):
    try:
        if(sku in map_app_product['Smart Products List'].astype(str).to_list()):
            return "Y"
        else:
            return "N"
    except:
        return 'unknown'
    
def sku_get_series(sku, map_series):
    miss_info = ''
    model = sku_get_model(sku)
    try:
        series = map_series.loc[map_series['Model']==model, 'Series'].iloc[0]
    except:
        series = ""
        miss_info = f'series of {sku} not found, please update!'
    return series, miss_info

def get_sku_extra(df_ori, fields, return_miss=False):
    if fields == 'all':
        print('total fields...')
        fields_list = ['brand','product_line','product_type','sku_code','model', 'scu', 'app_supported', 'series']
    else:
        fields_list = fields
    df = df_ori.copy()
    print('loading mapping info...')
    if "product_line" in fields_list or "product_type" in fields_list :
        df_map_sku_code = tm.gs_read_df(('Datalibro Mapping Master', 'sku_code'))
        if "product_line" in fields_list:
            df["product_line"], list_miss_product_line = zip(*df['sku'].apply(sku_get_product_line, map_sku_code = df_map_sku_code))
        if "product_type" in fields_list:
            df["product_type"], list_miss_product_type = zip(*df['sku'].apply(sku_get_product_type, map_sku_code = df_map_sku_code))
    if "scu" in fields_list:
        df_map_scu = tm.gs_read_df(('Datalibro Mapping Master', 'scu'))
        df['scu'] = df['sku'].apply(sku_get_scu, map_scu=df_map_scu)
    if "app_supported" in fields_list:
        df_map_app_product = tm.gs_read_df(('Datalibro Mapping Master', 'app_product'))
        df['app_supported'] = df['sku'].apply(sku_get_app_product, map_app_product=df_map_app_product)
    if "series" in fields_list:
        df_map_series = tm.gs_read_df(('Datalibro Mapping Master', 'series'))
        df['series'], list_miss_series = zip(*df['sku'].apply(sku_get_series, map_series=df_map_series))
    if "brand" in fields_list:
        df['brand'] = df['sku'].apply(sku_get_brand)
    if "model" in fields_list:
        df['model'] = df['sku'].apply(sku_get_model)
    if "sku_code" in fields_list:
        df['sku_code'] = df['sku'].apply(sku_get_sku_code)

    list_miss = pd.concat([pd.Series(list_miss_product_line), pd.Series(list_miss_product_type), pd.Series(list_miss_series)]).unique()

    if return_miss:
        return df, list_miss
    else:
        return df
