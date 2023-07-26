import time,requests,pickle
from seleniumwire import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from requests_html import HTMLSession

BASE_URL="https://cc.inetlte.com"

def cloudcore(s, password):
    try:
        from inetapi.utils import driver
        driver.install()
        print('hello world')
    except ModuleNotFoundError: return print("Please download the latest version of geckodriver, from https://172.31.255.151/download2")
    except OSError: pass
    optionsw = {
    'request_storage_base_dir': '.tmp'
    }
    options = Options()
    options.headless = True
    fox = webdriver.Firefox(options=options, seleniumwire_options=optionsw)
    fox.get("https://infrnet.com/")
    try:
        myElem = WebDriverWait(fox, 3).until(EC.presence_of_element_located((By.NAME,"username")))  
    except TimeoutException as e:
        print(e)
        return e
    myElem.send_keys("inet-unifi-controller")
    fox.find_element(By.NAME,"password").send_keys(password, Keys.RETURN)
    time.sleep(4)     
    for k in fox.requests:
        if k.response:
            if k.response.headers:
                if 'Location' in k.response.headers:
                    if 'callback' in k.response.headers['Location']:
                        t=str(k.response.headers["location"])
                        start = t.find("&access_token=")+len("&access_token=")
                        end = t.find("&token_type=")
                        substring = t[start:end]
                        with open(".tmp/token", "w") as f:
                            f.write(substring)
                        fox.get(f"{BASE_URL}/customers?sessionToken="+substring)
                        time.sleep(2)
                        pickle.dump(fox.get_cookies(), open('.tmp/activation_cookie', 'wb'))
                        # for c in fox.get_cookies():
                        s=requests.Session()
                        t=s.get(f"{BASE_URL}/customers?sessionToken="+substring).text
                        with open('.tmp/cookies','wb') as f: pickle.dump(s.cookies, f)

    fox.quit()
    return s
            
def login(password):
    import os, time

    s = HTMLSession()
    # s = requests.Session()
    if not os.path.exists('.tmp'):
        os.makedirs('.tmp')
        s = cloudcore(s,password)
        return s
    else:
        try:
            with open('.tmp/cookies','rb') as f: s.cookies.update(pickle.load(f))
            t=s.get("https://cc.inetlte.com/customers").text
            soup = BeautifulSoup(t,'html.parser')
            a=soup.find('input', {"id":"filter"})
            if not a: raise Exception("Need to reset cookies!")

        except Exception as e:
            with open(".tmp/cookies", "wb") as f: pass
            s = cloudcore(s,password)

    return s
