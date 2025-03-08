import yfinance as yf

def get_stocks_data(tickers):
    result = []
    for ticker in tickers:
        stock = yf.Ticker(ticker)

        hist = stock.history(period="2d", interval="1h")

        if hist.empty:
            return {"ticker": ticker, "error": "Failed to fetch data"}

        latest_price = hist["Close"].iloc[-1]
        yesterday_price = hist["Close"].iloc[0]

        status = "Up" if latest_price > yesterday_price else "Down"
        
        result.append({
        "ticker": ticker,
        "price": int(latest_price),
        "status": status,
        })
        
    return  result