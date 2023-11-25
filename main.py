import os
from twilio.rest import Client
import requests

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
NEWS_API_KEY = "4f6f0675bee54fb48533c912811c8dc1"
ACCOUNT_SID = "AC91645caffc79d75410b09aaf0d9542e6"
AUTH_TOKEN = "3466bf7ca7d3d5836e21eeb46d0dfe86"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"



    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

#TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python
# dictionaries. e.g. [new_value for (key, value) in dictionary.items()]

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TSLA&apikey=V52TKU53O1HNXPK1'
r = requests.get(url)
data = r.json()["Time Series (Daily)"]
#print(data)
#yesterday_price = data['Time Series (Daily)']['2023-11-16']['4. close']
data_list = [value for (key, value) in data.items()]
#print(data_list)
yesterday_data = data_list[0]
yesterday_price = yesterday_data["4. close"]
#TODO 2. - Get the day before yesterday's closing stock price
#day_before_price = data['Time Series (Daily)']['2023-11-15']['4. close']
day_before_yesterday_data = data_list[1]
day_before_price = day_before_yesterday_data['4. close']
#TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
difference = abs(float(yesterday_price) - float(day_before_price))
#print(difference)
#TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
diff_percent = (difference / float(yesterday_price)) * 100
#print(diff_percent)
#TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").
if diff_percent > 1:
    news_params = {
    "apiKey": NEWS_API_KEY,
    "qInTitle": COMPANY_NAME,
}
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
    three_articles = articles[:3]
    #print(three_articles)
    #titles = [article["title"] for article in three_articles]
    formatted_articles = [f"Headline: {article['title']}.\n Brief: {article['description']}"for article in three_articles]


    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number. 

#TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.

#TODO 9. - Send each article as a separate message via Twilio. 
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    for article in formatted_articles:
        message = client.messages \
                .create(
                     body="Something here",
                     from_='+18447552130',
                     to='+16825523338'
                 )

        print(message.sid)


#Optional TODO: Format the message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

