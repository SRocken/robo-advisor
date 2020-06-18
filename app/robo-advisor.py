# app/robo_advisor.py

import csv
import json
import os

import requests

# Utility function to convert float or integrer to usd formatted string
def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

#
# Information Inputs
#
stock_symbol = "MSFT" #TODO: Make dynamic
api_key = os.environ.get("ALPHAVANTAGE_API_KEY") 
request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock_symbol}&apikey={api_key}"
response = requests.get(request_url)

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

# maximum and minimum of all prices in request
high_prices = []
low_prices = []
for date in dates: # loop through each date and pull out the high and low price and add them to list
    high_price = tsd[date]["2. high"]
    high_prices.append(float(high_price))
    low_price = tsd[date]["3. low"]
    low_prices.append(float(low_price))
recent_high = max(high_prices)
recent_low = min(low_prices)


#
# Information Outputs
#

# Write data to CSV for output
csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")
csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]

with open(csv_file_path, "w", newline='') as csv_file: # "w" means "open the file for writing"
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader() # uses fieldnames set above
    # Going to need to do some looping to write each row
    for date in dates:
        daily_prices = tsd[date]
        writer.writerow({
            "timestamp": date,
            "open": daily_prices["1. open"],
            "high": daily_prices["2. high"],
            "low": daily_prices["3. low"],
            "close": daily_prices["4. close"],
            "volume": daily_prices["5. volume"]
        })


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
print(f"WRITING DATA TO CSV: {csv_file_path}")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")

