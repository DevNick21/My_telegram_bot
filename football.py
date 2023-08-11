import requests
from datetime import datetime as dt

url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

day = dt.now().strftime("%Y-%m-%d")


querystring = {"date": day}

headers = {
    "X-RapidAPI-Key": "b6f0410149mshb1bb5fa6fa2d982p18a3f3jsn46c0b8898052",
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

res = requests.get(url, headers=headers, params=querystring)
data = res.json()

print(data)
