import pandas as pd

def Products(s, product_filter=None):
    if product_filter:
        customerspage = s.get(f'https://cc.inetlte.com/products?filter={product_filter}&pageSize=920')
    else:
        customerspage = s.get('https://cc.inetlte.com/products?filter=&pageSize=920')
    df = pd.read_html(customerspage.content)[0]
    df.set_index('ID', inplace=True)
    df['Customer'] = df['Customer'].apply(lambda x: None if pd.isna(x) else str(x))
    data = df.to_json(orient='records')
    return data