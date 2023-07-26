'''
This function returns a dataframe representing the customers as shown in Cloudcore

customer id is the cloudcore customer identifier

type is the type of customer (Retail or Wholesale)

sales person is the customer sales person

subscriptions is the count of subscriptions the customer has

'''

import pandas as pd
from inetapi.cloudcore.conf import BASE_URL


def Customer(session, filter=None):

    '''
    usage: customer table
    '''    
    if filter:
        customerpage = session.get(BASE_URL + f'/customers?filter={filter}&showProspects=on&pageSize=600')
    else:
        customerpage = session.get(BASE_URL + f'/customers?filter=&showProspects=on&pageSize=600')
    data = pd.read_html(customerpage.content)[0]
    data['Customer'] = data['Customer Account'].str.replace('Edit ', '')
    data['Subscriptions'] = data['Manage Subscriptions'].str.replace('View ', '')
    data['Subscriptions'] = data['Subscriptions'].str.replace(' Subscriptions', '')
    data = data.drop(columns=['Network Health'])
    data = data.drop(columns=['Manage Subscriptions'])
    data = data.drop(columns=['Short Name'])
    data = data.drop(columns=['Customer Account'])
    data.set_index('Customer ID')
    # print('\n',data)
    json_string = data.to_json(orient='records')


    return json_string
