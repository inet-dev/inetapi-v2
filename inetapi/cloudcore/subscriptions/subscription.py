import pandas as pd
from bs4 import BeautifulSoup
from inetapi.cloudcore.conf import BASE_URL

def get_subscription_by_sublink(s,subLink,hReadable=False):

    def human_readable(soup):

        labels = soup.find_all("label", class_="control-label")
        data = {}
        for label in labels:
            field_data = {}
            next_tag = label.find_next_sibling()
            if next_tag:
                if 'order' in label.text.strip().lower():
                    try:
                        order = next_tag.find("a").text.strip()
                    except AttributeError as e:
                        order = None
                    data['name'].append("Order: " + order)
                    field_data['order'] = order

                elif "Description" == label.text.strip():
                    input_tag = next_tag.find("input")
                    if input_tag:
                        field_data['description'] = input_tag.get('value').strip().replace("\t", " ")

                elif "Service Group" == label.text.strip():
                    select_tag = next_tag.find("select")
                    try:
                        field_data['service_group'] = select_tag.find("option", selected=True).text.strip()
                    except AttributeError as e:
                        field_data['service_group'] = None
                    # field_data['service_group'] = next_tag.find('option', selected=True).text.strip()
                if field_data: data.append(field_data)

        if data: return data

    d        = {"id":[], "value":[], 'description': []}
    subInfo  = s.get(BASE_URL+subLink).text
    soup     = BeautifulSoup(subInfo, 'html.parser')

    if hReadable:
        data = human_readable(soup)
        return data
    
    for s in soup.find_all('select'):
        for o in s.find_all('option', selected=True):
            d['id'].append(s['name'])
            d['value'].append(o.get('value'))
            # d['description'].append(o.text)
    for i in soup.find_all("input"):
        try:
            d['id'].append(i['name'])
            d['value'].append(i.get('value'))
            # d['description'].append(i.text)
        except:
            pass

    df = pd.DataFrame({
        'name': d['id'],
        'value': d['value'],
        # 'hReadable': d['description']
    }).set_index('name')

    return df.to_dict()
