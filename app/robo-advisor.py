# app/robo_advisor.py

import csv
import json
import os

import requests
from datetime import datetime, date
from dotenv import load_dotenv

load_dotenv()

# Utility function to convert float or integrer to usd formatted string
def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

# Utility checks if a string contains a number, space, or more than 4 digits --> used for validating stock ticker input
def has_numbers(input_string):
    return any(char.isdigit() for char in input_string)
def has_spaces(input_string):
    return any(char.isspace() for char in input_string)
def max_four(input_string):
    numbers = sum(char.isdigit() for char in input_string) # Counts numbers
    words = sum(char.isalpha() for char in input_string) # Counts text digits (i.e. "A" or "B")
    spaces = sum(char.isspace() for char in input_string) # Counts inputted spaces
    others  = len(input_string) - numbers - words - spaces # Catch-all for anything else (i.e. symbols)
    digit_count = numbers + words + spaces + others # Adds them all up for validation against max of 4 digits
    return any(digit_count > 4 for char in input_string)

current_date = date.today()
current_datetime = datetime.today()
#
# Information Inputs
#
while True:
    stock_symbol = input("Please specify which stock symbol you want to view data on: ")
    if has_numbers(stock_symbol) == True:
        print("Sorry, looks like you typed an invalid ticker!")
    elif has_spaces(stock_symbol) == True:
        print("Sorry, looks like you typed an invalid ticker!")
    elif max_four(stock_symbol) == True:
        print("Sorry, looks like you typed an invalid ticker!")
    else:
        break

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

# Recommendation
if latest_close < str(recent_high-(recent_high*.20)):
   recommendation = "Buy"
   recommendation_reason = "Latest close price is 20% less than recent high"
else:
    recommendation = "Do not buy"
    recommendation_reason = "Latest close price is near recent high"

#
# Information Outputs
#

# Write data to CSV for output
csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", f"{stock_symbol.upper()}_{current_date}.csv")
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
print(f"SELECTED SYMBOL: {stock_symbol.upper()}") # Pulls user input and ensures its in all caps
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print(f"REQUESTED AT: {current_datetime}") #Use datetime module to auto intput this
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print(f"RECOMMENDATION: {recommendation}")
print(f"RECOMMENDATION REASON: {recommendation_reason}")
print("-------------------------")
print(f"WRITING DATA TO CSV: {csv_file_path}")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")

