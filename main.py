import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_KEY = "your stock api key"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_KEY = "your news api key"
TWILIO_SID = "your twilio sid"
TWILIO_TOKEN = "your twilio token"
TWILIO_NUM = 'your twilio number'
USER_NUM = 'your number'

difference = 3    ### if stock change is bigger than this number (%)
stock_data_days = []
last_news = []


def positive_distance(current,prev):
    if current > prev:
        prev = float(prev)
        current = float(current)
        temp = (float(current) - float(prev)) / prev
    elif current < prev:
        prev = float(prev)
        current = float(current)
        temp =  (float(prev) - float(current)) / current
    else:
        temp = 0
    temp = "%.4f" % temp
    temp = float(temp)
    temp = temp * 100
    return temp
    

def get_news():
    parametre = {
        "apiKey": NEWS_KEY,
        "q": COMPANY_NAME,
    }
    cevap2 = requests.get(url= NEWS_ENDPOINT, params=parametre)
    cevap2.raise_for_status()

    haber = cevap2.json()
    for i in range(0,3):
        temp = {}
        title = haber["articles"][i]["title"]
        description = haber["articles"][i]["description"]

        temp = {
            "title": title,
            "description": description,
        }
        last_news.append(temp)
    return last_news



parametre_stock= {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_KEY
}

cevap = requests.get(STOCK_ENDPOINT, params=parametre_stock)
cevap.raise_for_status()
tesla = cevap.json()


### getting data from API
for stock in tesla["Time Series (Daily)"]:
    temp = []
    temp.append(stock)
    stock_data_days.append(temp)

current_stock = tesla["Time Series (Daily)"][stock_data_days[0][0]]["1. open"]
prev_stock = tesla["Time Series (Daily)"][stock_data_days[1][0]]["4. close"]

up_down = None
if current_stock > prev_stock:
    up_down = "🔺"
else:
    up_down = "🔻"

change = positive_distance(current=current_stock, prev= prev_stock)

last_news = get_news()

formatted_article = [f"{STOCK}: {up_down}{change}%\nHeadline: {i["title"]}.\nBrief: {i["description"]}." for i in last_news]

client = Client(TWILIO_SID, TWILIO_TOKEN)

if change > 0:
    for artic in formatted_article:
        message = client.messages.create(body=artic,from_=TWILIO_NUM,to=USER_NUM)
