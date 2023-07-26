from inetapi.cloudcore.conf import BASE_URL
from inetapi.utils.order_processor import OrderProcessor
from bs4 import BeautifulSoup
import pandas as pd

def asset_type(condition):
    result = {
        'None Selected': 'Unknown',
        'Agriculture - 8': 'Agriculture',
        'DEPRECATED - Tool Pusher - 2': 'Drilling',
        'Government - 9': 'Government',
        'Indirect - 12': 'Indirect',
        'Industrial - 11': 'Industrial',
        'Mining - 10': 'Mining',
        'New Markets - Other - 15': 'Unknown',
        'New Markets - Renewables - 14': 'Renewables',
        'Oil & Gas - Completions - 3': 'Completions',
        'Oil & Gas - Drilling - 1': 'Drilling',
        'Oil & Gas - Midstream - 13': 'Midstream',
        'Oil & Gas - Other - 6': 'Unknown',
        'Oil & Gas - Production - 4': 'Production',
        'Oil & Gas - Wholesale - 5': 'Wholesale',
        'Utilities - 7': 'Utilities',
        'Unknown': 'Unknown'
    }.get(condition, 'Unknown')
    return result

def order_search(s):
    orderPage = s.get(f"{BASE_URL}/serviceOrders?filter=baker&pageSize=20&optionState=exclude&hideStates=NEW_QUOTE&hideStates=SITE_SURVEY_PENDING&hideStates=NEW_CHANGES_REQUESTED&hideStates=SHIP_PARTIAL&hideStates=SHIP_COMPLETE&hideStates=INSTALL_PENDING&hideStates=INSTALL_COMPLETE&hideStates=ACCEPT_PENDING&hideStates=ACCEPT_COMPLETE&hideStates=ACTIVE&hideStates=COMPLETED&hideStates=CANCELED&showProspects=on&coordinator=&assignee=")
    df = pd.read_html(orderPage.content)[0]
    df['Service Order'] = df['Service Order'].str.extract(r'(\d+)')
    return df

def order_query(s, order_id=None):
    
    if not order_id:
        order_search(s)
        pass

    with s.get(f"{BASE_URL}/serviceOrders/{order_id}") as response:
        order_soup = BeautifulSoup(response.text, "html.parser")
    order_type = order_soup.find("input", {"id": "orderType"})["value"]
    OrderProcessor(order_type.lower(), order_id, order_soup)


def cancel_order(order_soup,data):
    table = order_soup.find("table", {"class": "table table-striped table-bordered table-condensed"})
    td_tags = table.select('tr td:nth-of-type(2)')
    column_values = [td.text for td in td_tags]
    data['sub_ids'] = column_values
    return data

