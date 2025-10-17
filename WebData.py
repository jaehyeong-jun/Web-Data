#https://www.alphavantage.co/
import requests
import json
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 한글 폰트 설정 -> 그래프 제목이나 축 라벨에서 한글이 깨지지 않도록 설정
font_path = "C:/Windows/Fonts/malgun.ttf"  # 맑은 고딕 폰트 경로
fontprop = fm.FontProperties(fname=font_path).get_name()
plt.rcParams["font.family"] = fontprop
plt.rcParams["axes.unicode_minus"] = False  # 마이너스 깨짐 방지

# Alpha Vantage API 설정
api_key = "XMM1B9RQWJZP6KU5"  # Alpha Vantage API 키
symbol = "AAPL"               # 조회할 종목 심볼 (예: Apple)

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

    # 날짜, 종가 데이터 추출
    dates = []
    close_prices = []

    # 최신 5일치 데이터를 콘솔에 출력
    print(f"\n📈 {symbol} 주식 일별 시세\n")
    for date, info in list(time_series.items())[
        :5]:  # 최신 5일 데이터만 출력
            open_price = info["1. open"]
            high_price = info["2. high"]
            low_price = info["3. low"]
            close_price = info["4. close"]
            volume = info["5. volume"]
            print(f"날짜: {date}")
            print(f"시가: {open_price}")
            print(f"고가: {high_price}")
            print(f"저가: {low_price}")
            print(f"종가: {close_price}")
            print(f"거래량: {volume}")
            print("-" * 40)
    # 최근 30일치 종가 데이터를 그래프용 리스트에 저장
    for date, info in list(time_series.items())[:30]:
        dates.append(date)
        close_prices.append(float(info["4. close"]))

    # 최근 날짜가 오른쪽으로 가도록 설정
    dates.reverse()
    close_prices.reverse()

    # Matplotlib을 이용한 그래프 출력
    plt.figure(figsize=(10, 5))     # 그래프 크기 설정
    plt.plot(dates, close_prices, marker='o', linestyle='-', color='blue')      # 선 그래프
    plt.title(f"{symbol} 주식 종가 (최근 30일)")
    plt.xlabel("날짜")
    plt.ylabel("종가 ($)")
    plt.xticks(rotation=45)                 # 날짜 라벨 회전 (가독성 향상)
    plt.grid(True)                          # 눈금선 표시
    plt.tight_layout()                      # 레이아웃 자동 조정
    plt.show()

# 오류 또는 API 제한 발생 시 출력
else:
    print("⚠️ 주식 데이터를 불러올 수 없습니다.")
    if "Note" in data:
        print("제한 경고:", data["Note"])                 # API 호출 제한 메시지
    elif "Error Message" in data:
        print("에러 메시지:", data["Error Message"])      # 잘못된 심볼 등 에러 메시지