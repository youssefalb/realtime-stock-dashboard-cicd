from fastapi import FastAPI
import requests
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Replace with your Alpha Vantage API key
API_KEY = '8XWUQRSLGIMIUVGL'  
BASE_URL = 'https://www.alphavantage.co/query'

def get_stock_price(symbol: str):
    """
    Fetch the stock price for a given symbol from Alpha Vantage.
    """
    # API request URL for real-time intraday data
    url = f"{BASE_URL}?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={API_KEY}"
    
    # Make the API request
    response = requests.get(url)
    
    # Handle errors
    if response.status_code != 200:
        raise Exception("Error fetching stock price")

    data = response.json()

    # Check if the data contains time series data
    if "Time Series (5min)" not in data:
        raise Exception("Invalid symbol or API error")
    
    # Extract the latest time and stock price
    latest_time = list(data["Time Series (5min)"].keys())[0]
    latest_price = data["Time Series (5min)"][latest_time]["1. open"]
    
    return latest_price

@app.get("/stock/{symbol}")
async def get_stock(symbol: str):
    """
    Fetch the stock price for the given symbol.
    """
    try:
        price = get_stock_price(symbol)
        return {"symbol": symbol, "price": price}
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
async def root():
    return {"message": "Welcome to the Stock Price API!"}
