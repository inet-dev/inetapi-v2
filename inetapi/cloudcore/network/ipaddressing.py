from bs4 import BeautifulSoup
import re
from inetapi.cloudcore.conf import BASE_URL
from inetapi.utils.clean import clean_dict

def clean_dict(dict):
    for k in dict:
        dict[k]=dict[k].text


def first_available(s,productid="209",customerid="30",voip=None):
    import json
    resp=s.get(f"{BASE_URL}/availableIpSubnets?productId={productid}&customerId={customerid}")
    subnets=json.loads(resp.text)
    for i in subnets:
        resp=s.get(f'{BASE_URL}/availableIpAddress?subnetId={i["id"]}&ipAddressId=')
        try:
            ip_list=json.loads(resp.text)
            if ip_list:
                if voip:
                    if "255" in ip_list[0]["value"]:
                        ip=ip_list[0]["value"]
                        ip_id=ip_list[0]["id"]
                        subnetId=i["id"]
                        ip_info = {"ip":str(ip),"selectedIpAddress":str(ip_id),"subnet":str(subnetId)}
                else:
                    if ".255." not in ip_list[0]["value"]:
                        ip=ip_list[0]["value"]
                        ip_id=ip_list[0]["id"]
                        subnetId=i["id"]
                        ip_info = {"ip":str(ip),"selectedIpAddress":str(ip_id),"subnet":str(subnetId)}
                return ip_info

        except:
            continue

def ip_query(ip,s):
    ips     = s.get(f"{BASE_URL}/ipAddresses?filter={ip}&pageSize=1")
    table   = BeautifulSoup(ips.text,features="html.parser")
    results = {k.text:v for k, v in zip(table.findAll("th"),table.findAll("td"))}
    sub     = re.search('<a href="(.*?)">(.*?)</a>', str(results.get("Subscription")))
    clean_dict(results)
    try:
        results.update({'subDesc': sub.group(2), 'subLink': sub.group(1).strip()})
    except:
        pass

    return results

def grelte(s):
    import pandas as pd
    url = 'https://cc.inetlte.com/ipAddresses?filter=172.31.0.&pageSize=507'
    html = s.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')
    df = pd.read_html(str(table))[0]
    filtered_df = df[(df['APN'] == 'w-datacom') & (df['Reserved'] == False)]
    last_ten = filtered_df.tail(18)

    # Print the filtered DataFrame
    print(last_ten['IP Address'])