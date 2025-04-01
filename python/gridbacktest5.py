import backtrader as bt
import pandas as pd
import math
from tqdm import tqdm

class GridStrategy(bt.Strategy):
    params = (
        ('lower_limit', 0),
        ('upper_limit', 0),
        ('grid_levels', 10),
        ('initial_capital', 1000),
    )

    def __init__(self):
        self.grid_prices = self.calculate_grid_levels()
        self.cash = self.params.initial_capital
        self.position_size = 0
        self.profit_from_grids = 0
        self.trades = []

    def calculate_grid_levels(self):
        """Calculate geometrically spaced grid levels."""
        lower = self.params.lower_limit
        upper = self.params.upper_limit
        levels = self.params.grid_levels
        return [lower * ((upper / lower) ** (i / (levels - 1))) for i in range(levels)]

    def next(self):
        current_price = self.data.close[0]

        for i, grid_price in enumerate(self.grid_prices):
            if current_price <= grid_price and self.cash > 0:  # Buy
                size = self.cash / current_price
                self.buy(size=size)
                self.cash = 0
                self.trades.append((self.datetime.datetime(), 'BUY', current_price, size))
            elif current_price >= grid_price and self.position_size > 0:  # Sell
                self.sell(size=self.position_size)
                self.cash += current_price * self.position_size
                self.profit_from_grids += (current_price - grid_price) * self.position_size
                self.position_size = 0
                self.trades.append((self.datetime.datetime(), 'SELL', current_price, self.position_size))

    def notify_order(self, order):
        if order.status in [order.Completed]:
            if order.isbuy():
                self.position_size += order.executed.size
            elif order.issell():
                self.position_size -= order.executed.size

    def stop(self):
        final_value = self.cash + (self.position_size * self.data.close[0])
        print(f"Final Portfolio Value: {final_value}")
        print(f"Profit from Grids: {self.profit_from_grids}")
        print(f"Total Trades: {len(self.trades)}")

# Load CSV Data
def load_csv_to_backtrader(csv_file):
    data = pd.read_csv(csv_file, parse_dates=['timestamp'])
    data.set_index('timestamp', inplace=True)

    return bt.feeds.PandasData(
        dataname=data,
        timeframe=bt.TimeFrame.Minutes,
        openinterest=-1
    )

# Main Function
def run_backtest(csv_file, lower_limit, upper_limit, grid_levels, initial_capital):
    cerebro = bt.Cerebro()

    data = load_csv_to_backtrader(csv_file)
    cerebro.adddata(data)

    cerebro.addstrategy(
        GridStrategy,
        lower_limit=lower_limit,
        upper_limit=upper_limit,
        grid_levels=grid_levels,
        initial_capital=initial_capital
    )

    cerebro.broker.set_cash(initial_capital)
    cerebro.broker.setcommission(commission=0.001)

    print("Starting Portfolio Value:", cerebro.broker.getvalue())
    cerebro.run()
    print("Ending Portfolio Value:", cerebro.broker.getvalue())

if __name__ == "__main__":
    # User Inputs
    csv_file = "SOLUSDT_1m.csv"  # Replace with your CSV file path
    lower_limit = float(input("Enter lower price limit: "))
    upper_limit = float(input("Enter upper price limit: "))
    grid_levels = int(input("Enter number of grid levels: "))
    initial_capital = float(input("Enter initial capital: "))

    run_backtest(csv_file, lower_limit, upper_limit, grid_levels, initial_capital)
