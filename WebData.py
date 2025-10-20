# https://www.alphavantage.co/
import requests
import json
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd
import os

# 한글 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"   #맑은고딕 폰트 경로
fontprop = fm.FontProperties(fname=font_path).get_name()
plt.rcParams["font.family"] = fontprop
plt.rcParams["axes.unicode_minus"] = False #마이너스 깨짐 방지

# API 설정
api_key = "XMM1B9RQWJZP6KU5"    # Alpha Vantage API 키
symbol = "AAPL"                 # 조회할 종목 심볼 (예: Apple)

# API 호출 URL
url = "https://www.alphavantage.co/query"

# 요청에 사용할 파라미터 구성
params = {
    "function": "TIME_SERIES_DAILY",    # 일별 시세 데이터 요청
    "symbol": symbol,                   # 조회할 주식 심볼
    "apikey": api_key                   # 인증 키
}

# API 요청 보내기
response = requests.get(url, params=params)

# 응답을 JSON 형식으로 변환
data = response.json()


# 데이터가 정상적으로 수신되었는지 확인
if "Time Series (Daily)" in data:
    time_series = data["Time Series (Daily)"]

    # 리스트에 한 번에 저장 → 이후 그래프, 엑셀에서 재활용
    records = []
    # 최신 30일치 데이터를 콘솔에 출력
    print(f"\n📈 {symbol} 주식 일별 시세\n")
    for date, info in list(time_series.items())[:30]:
        open_price = float(info["1. open"])
        high_price = float(info["2. high"])
        low_price = float(info["3. low"])
        close_price = float(info["4. close"])
        volume = int(info["5. volume"])

        print(f"날짜: {date}")
        print(f"시가: {open_price}")
        print(f"고가: {high_price}")
        print(f"저가: {low_price}")
        print(f"종가: {close_price}")
        print(f"거래량: {volume}")
        print("-" * 40)

        records.append({
            "날짜": date,
            "시가": open_price,
            "고가": high_price,
            "저가": low_price,
            "종가": close_price,
            "거래량": volume
        })

    # 날짜순 정렬 (오름차순)
    records_sorted = sorted(records, key=lambda x: x["날짜"])

    # 그래프 데이터 준비
    dates = [r["날짜"] for r in records_sorted]
    close_prices = [r["종가"] for r in records_sorted]

    # 그래프 출력
    plt.figure(figsize=(10, 5))
    plt.plot(dates, close_prices, marker='o', linestyle='-', color='blue')
    plt.title(f"{symbol} 주식 종가 (최근 30일)")
    plt.xlabel("날짜")
    plt.ylabel("종가 ($)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # ✅ 엑셀 저장
    df = pd.DataFrame(records_sorted)
    excel_file = f"{symbol}_주식시세_최근30일.xlsx"
    df.to_excel(excel_file, index=False, engine="openpyxl")

    # 저장 경로 출력
    full_path = os.path.abspath(excel_file)
    print(f"\n📂 엑셀 파일로 저장 완료: {full_path}")

else:
    print("⚠️ 주식 데이터를 불러올 수 없습니다.")
    if "Note" in data:
        print("제한 경고:", data["Note"])
    elif "Error Message" in data:
        print("에러 메시지:", data["Error Message"])



