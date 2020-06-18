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

# Creating variable to pull Time Series Daily respones > tsd > each date is a key with price information as values
# Then created list of those keys (already in chrono order) to pull the first in the list
# Finally pulling out latest date from that series to be used for latest close/prices
tsd = parsed_response['Time Series (Daily)']
tsd_keys = tsd.keys()
dates = list(tsd_keys)
latest_day = dates[0]
latest_close = tsd[latest_day]["4. close"]

# maximum of all high prices in request
#get high price in each day
high_prices = []
for date in dates:
    high_price = tsd[date]["2. high"]
    high_prices.append(float(high_price))
recent_high = max(high_prices)

# minimum of all low prices in requests
recent_low = 1
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
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")