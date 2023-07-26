from inetapi.cloudcore import BASE_URL
from bs4 import BeautifulSoup
import pandas as pd
import time

def getoffnetSimID(s, iccid):
    l = s.get(f'{BASE_URL}/offnetSimCards?filter={iccid}&pageSize=20').text
    soup = BeautifulSoup(l, 'html.parser')
    simId = soup.find('table')
    siminfo = simId.find('td').text
    return siminfo

def activation(subdata, s,orderSubId=None,accountId=None):
    l = s.get(f'{BASE_URL}/subscriptions/newForOrder?orderSubId=27014&accountId=38')
    soup = BeautifulSoup(l.text, 'html.parser')
    token = soup.find("input", {'name': 'authenticityToken'})['value']
    subdata['authenticityToken'] = token
    s.headers.update({"referer":f'{BASE_URL}/subscriptions/newForOrder?orderSubId=27014&accountId=38'})
    post = s.post(BASE_URL+'/subscriptions', data=subdata)
    time.sleep(1)

def get_new_sub_data(s):
    pass