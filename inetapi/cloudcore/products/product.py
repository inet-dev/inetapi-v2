import pandas as pd

def Products(s, product_filter=None, customer_name=None):
    if product_filter:
        customerspage = s.get(f'https://cc.inetlte.com/products?filter={product_filter}&pageSize=920')
    else:
        customerspage = s.get('https://cc.inetlte.com/products?filter=&pageSize=920')
    df = pd.read_html(customerspage.content)[0]
    df.set_index('ID')
    df['Customer'] = df['Customer'].apply(lambda x: None if pd.isna(x) else str(x))
    if customer_name:
        customer_list = [customer_name]
        # Filter rows where 'Customer' matches the provided customer_name
        filtered_df = df.loc[(df['Customer'].isin(customer_list) | pd.isna(df['Customer'])) & (df['Available'] == True)]
        # Convert the DataFrame to JSON
        data = filtered_df.to_dict(orient='records')
        return data
    data = df.to_dict(orient='records')
    return data