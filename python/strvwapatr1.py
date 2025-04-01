import ccxt
from datetime import datetime, timedelta

# Binance API ile bağlantı kur
exchange = ccxt.binance({"rateLimit": 1200, "enableRateLimit": True})

def fetch_binance_data(symbol, timeframe, limit=500):
    """Binance'ten mum verilerini al."""
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    return ohlcv

def calculate_vwap(data):
    """VWAP hesaplama."""
    cumulative_pv = 0
    cumulative_volume = 0
    for candle in data:
        high, low, close, volume = candle[2], candle[3], candle[4], candle[5]
        typical_price = (high + low + close) / 3
        cumulative_pv += typical_price * volume
        cumulative_volume += volume
    return cumulative_pv / cumulative_volume if cumulative_volume != 0 else 0

def calculate_atr(data, period):
    """ATR hesaplama."""
    trs = []
    for i in range(1, len(data)):
        high = data[i][2]
        low = data[i][3]
        prev_close = data[i - 1][4]
        tr = max(high - low, abs(high - prev_close), abs(low - prev_close))
        trs.append(tr)
    return sum(trs[-period:]) / period if len(trs) >= period else 0

def vwap_based_scalping(symbol, timeframe="1m", long_threshold=0.002, short_threshold=-0.002, atr_multiplier=1.5):
    """
    VWAP tabanlı scalping stratejisi.
    """
    # Güncel mum verilerini al
    data = fetch_binance_data(symbol, timeframe, limit=15)
    
    # ATR ve VWAP hesapla
    vwap = calculate_vwap(data)
    atr = calculate_atr(data, period=14)

    close = data[-1][4]
    high = data[-1][2]
    low = data[-1][3]

    long_stop_loss = low - atr * atr_multiplier
    short_stop_loss = high + atr * atr_multiplier

    # Long ve Short koşullarını belirle
    long_condition = close > vwap * (1 + long_threshold)
    short_condition = close < vwap * (1 + short_threshold)

    if long_condition:
        return True, long_stop_loss  # Long pozisyonu öner, stop loss'u döndür
    elif short_condition:
        return False, short_stop_loss  # Short pozisyonu öner, stop loss'u döndür
    else:
        return None, close  # Pozisyon yoksa close fiyatını döndür

# Fonksiyonu IOTA/USDT için çalıştır
def main():
    symbol = "IOTA/USDT"
    result, stop_loss = vwap_based_scalping(symbol)
    if result is True:
        print("Buy sinyali: Stop Loss -", stop_loss)
    elif result is False:
        print("Sell sinyali: Stop Loss -", stop_loss)
    else:
        print("Pozisyon yok: Close fiyatı -", stop_loss)

if __name__ == "__main__":
    main()
