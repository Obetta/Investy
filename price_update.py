import requests
import json
import mysqlconnector
import time

def stockPriceUpdate(stockname):
    url = "https://alpha-vantage.p.rapidapi.com/query"
    querystring = {"symbol":stockname,"function":"GLOBAL_QUOTE"}

    headers = {
        'x-rapidapi-host': "alpha-vantage.p.rapidapi.com",
        'x-rapidapi-key': "7f39e61d6bmsh382d8b0f6962ba5p1f892fjsn00ec813e021d"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    db = json.loads(response.text)

    print(db)
    name = ""
    price = -1
    if "05. price" in db['Global Quote']:
        price = db['Global Quote']["05. price"]
    if "01. symbol" in db['Global Quote']:
        name =  db['Global Quote']["01. symbol"]
    if name != "" and price != -1:
        mysqlconnector.updateallprices(name, price)
        time.sleep(13)

