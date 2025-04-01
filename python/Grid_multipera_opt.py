import matplotlib
matplotlib.use('Agg')  # GUI gereksinimi olmayan backend kullanımı

import pandas as pd
import ccxt
import matplotlib.pyplot as plt
import mplcursors
from datetime import datetime



def grid_bot_strategy(df, start_date, end_date, initial_price, lower_limit, upper_limit,
                     grid_levels, initial_capital, leverage, lower_stop_loss, upper_stop_loss,
                     stop_loss_enabled):
    """
    Executes the grid bot strategy over historical data.
    """
    df['Open time'] = pd.to_datetime(df['Open time'])
    df = df[(df['Open time'] >= pd.to_datetime(start_date)) & (df['Open time'] <= pd.to_datetime(end_date))]
    df = df.sort_values(by='Open time').reset_index(drop=True)

    grid_range = (upper_limit - lower_limit) / grid_levels
    buy_levels = [initial_price - i * grid_range for i in range(1, grid_levels + 1)]
    sell_levels = [initial_price + i * grid_range for i in range(1, grid_levels + 1)]

    trade_log = []
    total_pnl = 0
    total_cost = 0
    working_capital = initial_capital * leverage

    open_positions = []
    stop_loss_triggered = False
    stop_loss_trigger_date = None
    stop_loss_trigger_price = None
    mtm_value = 0

    for _, row in df.iterrows():
        price = row['Close']
        date = row['Open time']

        # Stop-loss logic
        if stop_loss_enabled:
            if price >= upper_stop_loss or price <= lower_stop_loss:
                stop_loss_triggered = True
                stop_loss_trigger_date = date
                stop_loss_trigger_price = price
                for pos in open_positions:
                    if pos['type'] == 'Buy':
                        pnl = (price - pos['price']) * pos['quantity']
                    else:
                        pnl = (pos['price'] - price) * pos['quantity']
                    total_pnl += pnl
                open_positions.clear()
                break

        # Close positions if price hits the target
        for pos in open_positions[:]:
            if pos['type'] == 'Buy' and price >= pos['target_sell_level']:
                pnl = (price - pos['price']) * pos['quantity']
                total_pnl += pnl
                trade_log.append([date, price, 'Sell', pnl])
                open_positions.remove(pos)
            elif pos['type'] == 'Sell' and price <= pos['target_buy_level']:
                pnl = (pos['price'] - price) * pos['quantity']
                total_pnl += pnl
                trade_log.append([date, price, 'Buy', pnl])
                open_positions.remove(pos)

        # Open new positions
        if price < initial_price:
            for level in buy_levels:
                if price <= level and not any(pos['price'] == level for pos in open_positions):
                    quantity = working_capital / (grid_levels * price)
                    open_positions.append({'type': 'Buy', 'price': level, 'target_sell_level': level + grid_range, 'quantity': quantity})
                    trade_log.append([date, price, 'Buy', 0])

        if price > initial_price:
            for level in sell_levels:
                if price >= level and not any(pos['price'] == level for pos in open_positions):
                    quantity = working_capital / (grid_levels * price)
                    open_positions.append({'type': 'Sell', 'price': level, 'target_buy_level': level - grid_range, 'quantity': quantity})
                    trade_log.append([date, price, 'Sell', 0])

    # Calculate MTM value
    mtm_price = stop_loss_trigger_price if stop_loss_triggered else df.iloc[-1]['Close']
    for pos in open_positions:
        if pos['type'] == 'Buy':
            mtm_value += (mtm_price - pos['price']) * pos['quantity']
        elif pos['type'] == 'Sell':
            mtm_value += (pos['price'] - mtm_price) * pos['quantity']

    total_mtm = total_pnl + mtm_value - total_cost
    roi = (total_mtm / initial_capital) * 100

    return pd.DataFrame(trade_log, columns=['Date', 'Price', 'Action', 'PNL']), total_pnl, mtm_value, total_mtm, roi


def fetch_data(exchange_name, symbol, timeframe, start_date, end_date):
    """Fetch historical data from a cryptocurrency exchange."""
    exchange_class = getattr(ccxt, exchange_name)()
    since = int(pd.to_datetime(start_date).timestamp() * 1000)
    end_timestamp = int(pd.to_datetime(end_date).timestamp() * 1000)
    ohlcv = []

    while since < end_timestamp:
        data = exchange_class.fetch_ohlcv(symbol, timeframe, since=since, limit=1000)
        if not data:
            break
        ohlcv.extend(data)
        since = data[-1][0] + 1

    df = pd.DataFrame(ohlcv, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume'])
    df['Open time'] = pd.to_datetime(df['Open time'], unit='ms')
    return df


def main():
    """Command-line interface for the Grid Bot Strategy."""
    print("Grid Bot Strategy")

    # User inputs
    exchange_name = input("Enter exchange (e.g., binance): ")
    symbol = input("Enter trading pair (e.g., BTC/USDT): ")
    timeframe = input("Enter timeframe (e.g., 1h, 1d): ")
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")
    initial_price = float(input("Enter initial price: "))
    lower_limit = float(input("Enter lower price limit: "))
    upper_limit = float(input("Enter upper price limit: "))
    grid_levels = int(input("Enter number of grid levels: "))
    initial_capital = float(input("Enter initial capital: "))
    leverage = float(input("Enter leverage: "))
    lower_stop_loss = float(input("Enter lower stop-loss price: "))
    upper_stop_loss = float(input("Enter upper stop-loss price: "))
    stop_loss_enabled = input("Enable stop-loss? (yes/no): ").strip().lower() == 'yes'

    print("Fetching data...")
    df = fetch_data(exchange_name, symbol, timeframe, start_date, end_date)

    print("Running strategy...")
    trade_log, total_pnl, mtm_value, total_mtm, roi = grid_bot_strategy(
        df, start_date, end_date, initial_price, lower_limit, upper_limit,
        grid_levels, initial_capital, leverage, lower_stop_loss, upper_stop_loss,
        stop_loss_enabled
    )

    print("\nTrade Log:")
    print(trade_log)
    print(f"\nTotal PNL: {total_pnl:.2f}")
    print(f"MTM Value: {mtm_value:.2f}")
    print(f"Total MTM: {total_mtm:.2f}")
    print(f"ROI: {roi:.2f}%")

    # Plot equity curve
    trade_log['Cumulative PNL'] = trade_log['PNL'].cumsum()
    plt.figure(figsize=(12, 6))
    plt.plot(trade_log['Date'], trade_log['Cumulative PNL'], label='Equity Curve', color='blue')
    plt.xlabel('Date')
    plt.ylabel('Cumulative PNL')
    plt.title('Equity Curve')
    plt.legend()
    plt.grid(True)

    # Add interactive tooltips
    cursor = mplcursors.cursor(hover=True)
    @cursor.connect("add")
    def on_add(sel):
        x = sel.target[0]
        y = sel.target[1]
        sel.annotation.set_text(f"Date: {trade_log.iloc[int(x)]['Date']}\nPNL: {y:.2f}")

    plt.show()


if __name__ == "__main__":
    main()
