from inetapi.subscriptions import get_subscription_by_sublink
from inetapi.cloudcore import BASE_URL
from datetime import datetime

class OrderProcessor:

    def __init__(self,order_type,order_id,order_soup,s):
        function_map = {"sale": self.sale_order, "service_cancelation": self.cancel_order}
        if order_type in function_map:
            function_map[order_type](order_id, order_soup, s)
            
    def sale_order(self, order_id, order_soup,s):
        from bs4 import BeautifulSoup

        table = order_soup.find("table", {"class": "table table-striped table-bordered table-condensed"})
        activation_link = BASE_URL+table.find("a", href=True).get("href")
        win = s.get(activation_link).text
        soup = BeautifulSoup(win,'html.parser')
        sub_activation_link = BASE_URL + soup.find('a', class_='btn btn-success', href=True).get('href')
        # html_session = HTMLSession()

        # transfer cookies to HTMLSession
        # html_session.cookies = s.cookies

        # make a request using html_session with transferred cookies
        # response = html_session.get(sub_activation_link)
        # response.html.render()

        # get the fully rendered HTML content
        # html_content = response.html.html
        # print(html_content)
        sub_page = s.get(sub_activation_link)

        sub_soup = BeautifulSoup(sub_page,'html.parser')
        print(sub_soup)
        
    def cancel_order(self, order_id, order_soup,s):
        table = order_soup.find("table", {"class": "table table-striped table-bordered table-condensed"})
        sub_ids = [td.text for td in table.select('tr td:nth-of-type(2)')]

        for x in sub_ids:
            print(x)
            subs                                            = get_subscription_by_sublink(s=s, subLink='/subscriptions/'+x)
            subs['value']["subscription.product"]           = subs['value']['productId']
            subs['value']["returnSimToInventoryOnCancel"]   = "on"
            subs['value']["returnUEToInventoryOnCancel"]    = "on"
            subs['value']["subscription.state"]             = "CANCELED"
            subs['value']["description"]                    = subs['value']["description"]+' cxnl'
            subs['value']["canceledAt"]                     = datetime.today().strftime("%Y-%m-%d")
            subs['value']["selectedAcct"]                   = subs['value']["currentAcctId"]
            s.headers.update({"referer": f"{BASE_URL}/subscriptions/{x}"})
            cancelsubPost=s.post(f'{BASE_URL}/subscriptions/{x}',data=subs['value'])
            print(cancelsubPost)

        # return data
    