import requests
import os
from dotenv import load_dotenv
import csv

load_dotenv()

POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")

print(POLYGON_API_KEY)

limit = 1000
url = f'https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit={limit}&sort=ticker&apiKey={POLYGON_API_KEY}'
response = requests.get(url)
tickers = []
data = response.json()
print(data.keys())
for ticker in data['results']:
    tickers.append(ticker)

while 'next_url' in data:
    print('Requesting Next Page', data['next_url'])
    response = requests.get(data['next_url'] + f'&apiKey={POLYGON_API_KEY}')
    data = response.json()
    print(data)
    if 'results' in data:
        for ticker in data['results']:
            tickers.append(ticker)
    else:
        print("No 'results' key found in response:", data)
        break

example_ticker = {
    'ticker': 'HQGO', 
    'name': 'Hartford US Quality Growth ETF', 
    'market': 'stocks', 
    'locale': 'us', 
    'primary_exchange': 'XNAS', 
    'type': 'ETF', 
    'active': True, 
    'currency_name': 'usd', 
    'composite_figi': 'BBG01KD9HBJ7', 
    'share_class_figi': 'BBG01KD9HCD1', 
    'last_updated_utc': '2025-10-20T06:05:26.687073818Z'
}

print(len(tickers))

fieldnames = list(example_ticker.keys())

with open("tickers.csv", mode="w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for ticker in tickers:
        row = {field: ticker.get(field, '') for field in fieldnames}
        writer.writerow(row)

print("✅ Data successfully written to tickers.csv")
