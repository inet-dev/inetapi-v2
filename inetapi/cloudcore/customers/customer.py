from inetapi.cloudcore.conf import BASE_URL


def Customer(s, name=None):
    import pandas as pd
    customerpage = s.get(BASE_URL + '/customers?filter=&showProspects=on&pageSize=20')
    df = pd.read_html(customerpage.content)[0]
    df['Customer'] = df['Customer Account'].str.replace('Edit ', '')
    df['Subscriptions'] = df['Manage Subscriptions'].str.replace('View ', '')
    df['Subscriptions'] = df['Subscriptions'].str.replace(' Subscriptions', '')
    df = df.drop(columns=['Network Health'])
    df = df.drop(columns=['Manage Subscriptions'])
    df = df.drop(columns=['Short Name'])
    df = df.drop(columns=['Customer Account'])
    df = df.set_index('Customer ID')
    print(df)