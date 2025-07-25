from polygon import RESTClient
from datetime import date,timedelta
import pandas as pd

client = RESTClient("AgmVIXjnEAmbTzQc6wDT5n4xVoahcn7Z")

# request = client.get_daily_open_close_agg(
#     "AAPL",
#     "2025-07-24",
#     adjusted="true",
# )

# print(request)

today = date.today().strftime("%Y-%m-%d")
days_ago = (date.today() - timedelta(days=7)).strftime("%Y-%m-%d")

aggs = []
for a in client.list_aggs(
    "AAPL",
    1,
    "day",
    days_ago,
    today,
    adjusted="true",
    sort="asc",
    limit=120,
):
    aggs.append(a)

stock_df = pd.DataFrame(aggs)
print(stock_df.columns)