# app/robo_advisor.py

import requests
import json

# Utility function to convert float or integrer to usd formatted string
def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

#
# Information Inputs
#

request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo"
response = requests.get(request_url)
#print(type(response)) #> <class 'requests.models.Response'>
#print(response.status_code) #> 200
#print(response.text) #>string of dictonary

parsed_response = json.loads(response.text)

last_refreshed = parsed_response["Meta Data"]['3. Last Refreshed']

latest_close = parsed_response['Time Series (Daily)']["2020-06-17"]["4. close"]


#breakpoint()


#
#Information Outputs
#

print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUESTED AT: 2018-02-20 02:00pm") #Use datetime module to auto intput this
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print("RECENT HIGH: $101,000.00")
print("RECENT LOW: $99,000.00")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")