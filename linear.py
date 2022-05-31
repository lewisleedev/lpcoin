from pulp import LpMaximize, LpProblem, lpSum, LpVariable
import csv

def calculate_model(csv_name = "data.csv", month = 0):
    result_data = []
    header = []
    rows = []
    month += 1

    with open(csv_name) as f:
        csv_reader = csv.reader(f)
        header = next(csv_reader)
        for row in csv_reader:
            rows.append(row)

    model = LpProblem(name="portfolio-problem", sense=LpMaximize)

    btc = LpVariable(name="BTC", lowBound=0)
    eth = LpVariable(name="ETH", lowBound=0)
    bat = LpVariable(name="BAT", lowBound=0)
    mana = LpVariable(name="MANA", lowBound=0)
    theta = LpVariable(name="THETA", lowBound=0)
    xlm = LpVariable(name="XLM", lowBound=0)
    ada = LpVariable(name="ADA", lowBound=0)
    eos = LpVariable(name="EOS", lowBound=0)
     
    # 제약식
    model += (btc + eth + bat + mana + theta + xlm + ada + eos == 1, "ratio_constraint")
    model += btc + eth <= 0.8 # 30% <= BTC + ETH <= 80%
    model += btc + eth >= 0.3
    model += eth - 0.6 * btc <= 0 # 이더리움 투자액 <= 비트코인 투자율의 40%
    model += mana + theta + bat + eos + xlm <= 0.5 # 10% <= 고위험 코인들 <= 50%
    model += mana + theta + bat + eos + xlm >= 0.1
    model += bat >=0.05 # BAT 투자비율 최소 5%
    model += mana + theta <= 0.30 # NFT 관련 코인은 30% 이하

    # 3개월 이동평균 수익률 45% 이하의 제약식

    model += ((float(rows[0][month]))/100 - 0.45) * btc <= 0
    model += ((float(rows[1][month]))/100 - 0.45) * eth <= 0
    model += ((float(rows[2][month]))/100 - 0.45) * bat <= 0
    model += ((float(rows[3][month]))/100 - 0.45) * mana <= 0
    model += ((float(rows[4][month]))/100 - 0.45) * theta <= 0
    model += ((float(rows[5][month]))/100 - 0.45) * xlm <= 0
    model += ((float(rows[6][month]))/100 - 0.45) * ada <= 0
    model += ((float(rows[7][month]))/100 - 0.45) * eos <= 0


    # 목적함수
    # 코인 투자비율을 변수로, 수익률의 3개월 이동평균을 계수로 하는 목적함수

    obj_func = lpSum([float(rows[0][month]) * btc,
                    float(rows[1][month]) * eth,
                    float(rows[2][month]) * bat,
                    float(rows[3][month]) * mana,
                    float(rows[4][month]) * theta,
                    float(rows[5][month]) * xlm,
                    float(rows[6][month]) * ada,
                    float(rows[7][month]) * eos
                    ])

    model += obj_func

    result = model.solve()

    for var in model.variables():
        result_data.append([header[month], var.name, str(var.value()), model.objective.value()])

    return result_data

if __name__ == "__main__":
    with open("result.csv", 'w', encoding='UTF8', newline='') as f:
        w = csv.writer(f)
        for i in range(12):
            result = calculate_model(month = i)
            w.writerows(result)
    # print(calculate_model(month = 12))