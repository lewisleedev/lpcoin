from datetime import datetime, timedelta
import requests, csv

today = datetime.now()

COINS = ["KRW-BTC", # Order matters.
        "KRW-ETH",
        "KRW-BAT",
        "KRW-MANA",
        "KRW-THETA",
        "KRW-XLM",
        "KRW-ADA",
        "KRW-EOS",
        ]

headers = {"Accept": "application/json"}

def get_mvn_avg(coin, count, month_before = 0, fallback_count = 3):

    date = today - timedelta(days = (30 * month_before))
    date.strftime('%Y-%m-%d %H:%M:%S')
    formatted_date = str(date.replace(microsecond=0))
    def calculate(ct):
        r = requests.get("https://api.upbit.com/v1/candles/months?market={}&count={}&to={}".format(coin, ct, formatted_date),
        headers=headers)
        sum = 0
        for k in range(ct):
            result = r.json()[k]
            opening = result["opening_price"]
            closing = result["trade_price"]
            rtrn = (closing/opening - 1) * 100
            sum += rtrn

        return sum/ct
    try:
        return calculate(count)
    except:
        return calculate(fallback_count)

def make_csv(num_months, avg_months):
    header = ["coin_name"]

    for m in range(num_months):
        date = today - timedelta(days = (31 * m))
        formatted_date = str(date.replace(microsecond=0).strftime('%B, %Y'))
        header.append(formatted_date)
    
    data = []

    for i in COINS:
        avg_data = [i]
        for k in range(num_months):
            avg_data.append(get_mvn_avg(i, avg_months, k))
        data.append(avg_data)

    with open('data.csv', 'w', encoding='UTF8', newline='') as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(data)
    

if __name__ == "__main__":
    make_csv(24, 3)