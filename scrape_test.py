import requests
from datetime import datetime, timedelta
from stocks_apiKey import news_token



url = "https://api.benzinga.com/api/v2/news"
news_token = news_token
ticker = "VOO"
date_offset = datetime.now().date() - timedelta(days=5)

querystring = {f"token":{news_token},"pageSize":"15","displayOutput":"headline","tickers":{ticker},"dateFrom":{date_offset}}
headers = {"accept": "application/json"}

response = requests.get(url, headers=headers, params=querystring)

articles = response.json()

for article in articles:
    print("Title", article["title"])