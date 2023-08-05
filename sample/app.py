'''

Test Scenario 

I. Customers
    1. Return list of customers
    
II. Products
    1. Return a list of products
        a. Return a list of products for a specific customer
        b. Return a list of products for a specific use case

III. Subscriptions
    1. Activation
        a. Get service order subscription request ID
        b. Prepare subscription json data
    2. Cancellation

IV. Network
    1. Return first available IP address
    2. Return IP address information

V. Inventory
    1. SIMs
        a. Return SIM information
        b. Add Off Network SIM information

'''
from inetapi.cloudcore.conf import login
from inetapi.cloudcore.customers.customer import Customer
from inetapi.cloudcore.products.product import Products
session = login('1d1el8wcA')

my_customer = Customer(session=session, filter='pion')

product = Products(s=session, customer_name=my_customer[0]['Customer'])
# for x in product:print(x)
my_product = [x for x in product if x['Product Type'] == 'ONNET']