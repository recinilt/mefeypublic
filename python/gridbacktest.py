import pandas as pd
import numpy as np
from tqdm import tqdm

def run_grid_bot(data_path, lower_price, upper_price, num_grids, starting_capital, starting_price, fee_rate):
    # Load the data
    data = pd.read_csv(data_path)
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    data = data.set_index('timestamp')
    data = data.sort_index()
    
    # Generate grids
    grid_levels = np.geomspace(lower_price, upper_price, num_grids)
    
    # Initialize balances
    usdt_balance = starting_capital
    sol_balance = 0
    trade_history = []
    
    # Initial buys
    for price in grid_levels:
        if price <= starting_price:
            sol_to_buy = usdt_balance / price
            sol_balance += sol_to_buy
            usdt_balance -= sol_to_buy * price
            usdt_balance -= sol_to_buy * price * fee_rate  # Applying the fee
            trade_history.append(("BUY", price, sol_to_buy, usdt_balance, sol_balance))
    
    # Perform simulation
    pbar = tqdm(total=len(data), desc="Simulating Grid Bot")
    for index, row in data.iterrows():
        current_price = row['close']
        for i in range(1, len(grid_levels)):
            if grid_levels[i-1] < current_price <= grid_levels[i]:
                # Sell if price goes up
                if sol_balance > 0:
                    sol_to_sell = sol_balance / num_grids
                    usdt_earned = sol_to_sell * current_price
                    usdt_balance += usdt_earned
                    usdt_balance -= usdt_earned * fee_rate  # Applying the fee
                    sol_balance -= sol_to_sell
                    trade_history.append(("SELL", current_price, sol_to_sell, usdt_balance, sol_balance))
                # Buy if price goes down
                elif usdt_balance > 0:
                    sol_to_buy = usdt_balance / (num_grids * current_price)
                    sol_balance += sol_to_buy
                    usdt_spent = sol_to_buy * current_price
                    usdt_balance -= usdt_spent
                    usdt_balance -= usdt_spent * fee_rate  # Applying the fee
                    trade_history.append(("BUY", current_price, sol_to_buy, usdt_balance, sol_balance))
        pbar.update(1)
    pbar.close()
    
    # Summary
    final_portfolio_value = usdt_balance + sol_balance * data['close'].iloc[-1]
    profit_or_loss = final_portfolio_value - starting_capital
    total_trades = len(trade_history)
    
    return {
        "Total Trades": total_trades,
        "Profit or Loss": profit_or_loss,
        "Final Portfolio Value": final_portfolio_value,
        "Trade History": trade_history
    }

# Example usage
result = run_grid_bot(
    data_path="SOLUSDT_1m.csv",
    lower_price=7,
    upper_price=300,
    num_grids=500,
    starting_capital=4300,
    starting_price=8,
    fee_rate=0.001
)

print(f"Total Trades: {result['Total Trades']}")
print(f"Profit or Loss: {result['Profit or Loss']}")
print(f"Final Portfolio Value: {result['Final Portfolio Value']}")
