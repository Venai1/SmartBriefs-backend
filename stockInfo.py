import yfinance as yf
from datetime import datetime, timedelta


def get_stock_price(ticker):
    stock = yf.Ticker(ticker)

    hist = stock.history(period="2d", interval="1h")
    
    if hist.empty:
        return {"ticker": ticker, "error": "Failed to fetch data"}

    latest_price = hist["Close"].iloc[-1]
    yesterday_price = hist["Close"].iloc[0]

    status = "Up" if latest_price > yesterday_price else "Down"

    return {
        "ticker": ticker,
        "price": round(latest_price, 2),
        "status": status,
    }


def getMainStocks():
    tickers = ["^GSPC", "^DJI", "^IXIC"]
    results = []

    for ticker in tickers:
        result = get_stock_price(ticker)
        results.append(result)

    print(results)
    return results


if __name__ == "__main__":
    getMainStocks()
