import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

class GridTradingBot:
    def __init__(self, grid_size_pct=0.01, grid_num=5, tp_pct=0.01, sl_pct=0.01, trade_size=0.1):
        self.grid_size_pct = grid_size_pct
        self.grid_num = grid_num
        self.tp_pct = tp_pct
        self.sl_pct = sl_pct
        self.trade_size = trade_size
        self.positions = []
        self.pending_orders = []
        self.timer = datetime(1970, 1, 1)
        self.grid_setup_time = datetime(1970, 1, 1)
        self.is_runningGrid = False

    def compute_chop(self, data, length=14):
        high = data['high']
        low = data['low']
        close = data['close']
        tr = np.maximum(high - low, np.maximum(abs(high - close.shift(1)), abs(low - close.shift(1))))
        atr = tr.rolling(window=length).mean()
        high_low_range = high.rolling(window=length).max() - low.rolling(window=length).min()
        chop_index = 100 * np.log10(atr / high_low_range) / np.log10(length)
        return chop_index

    def reset_grid(self):
        self.pending_orders = []
        print("Grid reset.")

    def place_orders(self, bid_price, ask_price):
        for i in range(1, self.grid_num + 1):
            # Buy Limit Order
            buy_price = bid_price * (1 - i * self.grid_size_pct)
            tp = buy_price * (1 + self.tp_pct)
            sl = buy_price * (1 - self.sl_pct)
            self.pending_orders.append({"type": "buy", "price": buy_price, "tp": tp, "sl": sl})

            # Sell Limit Order
            sell_price = ask_price * (1 + i * self.grid_size_pct)
            tp = sell_price * (1 - self.tp_pct)
            sl = sell_price * (1 + self.sl_pct)
            self.pending_orders.append({"type": "sell", "price": sell_price, "tp": tp, "sl": sl})

    def on_market_data(self, data):
        current_time = data['timestamp']

        if current_time >= self.timer + timedelta(hours=24):
            self.timer = current_time
            ohlc_data = data['ohlc']

            if len(ohlc_data) < 14:
                print("Not enough OHLC data.")
                return

            chop_series = self.compute_chop(ohlc_data)

            if chop_series.iloc[-1] > 50:
                print("Market is trending. No grid setup.")
                self.is_runningGrid = False
            else:
                print("Market is ranging. Setting up grid.")
                self.is_runningGrid = True
                self.grid_setup_time = current_time
                self.place_orders(data['bidPrice'], data['askPrice'])

        if current_time > self.grid_setup_time + timedelta(days=7):
            self.reset_grid()
            self.is_runningGrid = False

    def simulate(self, market_data):
        for data in market_data:
            self.on_market_data(data)

# Example Usage
def generate_mock_data():
    timestamps = pd.date_range(start="2023-01-01", periods=100, freq="D")
    ohlc = pd.DataFrame({
        "high": np.random.uniform(100, 200, 100),
        "low": np.random.uniform(50, 100, 100),
        "close": np.random.uniform(70, 150, 100)
    })
    market_data = []
    for t in timestamps:
        market_data.append({
            "timestamp": t,
            "bidPrice": np.random.uniform(90, 110),
            "askPrice": np.random.uniform(110, 130),
            "ohlc": ohlc
        })
    return market_data

bot = GridTradingBot()
mock_data = generate_mock_data()
bot.simulate(mock_data)
