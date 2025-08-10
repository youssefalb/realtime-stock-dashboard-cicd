import React, { useState } from "react";
import './App.css';

function App() {
  // State variables to store input value and stock price
  const [symbol, setSymbol] = useState("");
  const [price, setPrice] = useState(null);
  const [error, setError] = useState("");

  // Function to fetch stock price
  const fetchStockPrice = async () => {
    if (!symbol) {
      setError("Please enter a stock symbol!");
      return;
    }

    try {
      setError(""); // Clear any previous error
      const response = await fetch(`http://127.0.0.1:8000/stock/${symbol.toUpperCase()}`);
      const data = await response.json();

      // Check if an error is returned from the backend
      if (data.error) {
        setError(data.error);
        setPrice(null);
      } else {
        setPrice(data.price);
        setError(""); // Clear any previous error
      }
    } catch (err) {
      setError("Failed to fetch stock data. Please try again later.");
      setPrice(null);
    }
  };

  return (
    <div className="App">
      <div className="container">
        <h1>Real-Time Stock Price Dashboard</h1>
        <div className="input-group">
          <input
            type="text"
            placeholder="Enter stock symbol (e.g., AAPL)"
            value={symbol}
            onChange={(e) => setSymbol(e.target.value)}
          />
          <button onClick={fetchStockPrice}>Get Price</button>
        </div>

        {error && <div className="error">{error}</div>}

        {price && (
          <div className="stock-price">
            <p>The latest price for <strong>{symbol.toUpperCase()}</strong> is <strong>${price}</strong></p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
