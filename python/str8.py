import time
import requests

def get_binance_klines(symbol: str, interval: str, limit: int = 5):
    """Binance API'den belirli bir işlem çiftinin kline (mum) verilerini al."""
    base_url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    return response.json()

def calculate_hlc3_vwap(data):
    """Verilen kline verilerinden HLC3 ve VWAP hesapla."""
    cumulative_tp_volume = 0.0
    cumulative_volume = 0.0

    for entry in data:
        high = float(entry[2])
        low = float(entry[3])
        close = float(entry[4])
        volume = float(entry[5])

        hlc3 = (high + low + close) / 3
        tp_volume = hlc3 * volume

        cumulative_tp_volume += tp_volume
        cumulative_volume += volume

    vwap = cumulative_tp_volume / cumulative_volume if cumulative_volume > 0 else 0
    latest_hlc3 = (float(data[-1][2]) + float(data[-1][3]) + float(data[-1][4])) / 3

    return latest_hlc3, vwap

def main():
    symbol = "BTCUSDT"  # İşlem çifti (örneğin, BTCUSDT)
    interval = "1m"  # 1 dakikalık zaman dilimi

    while True:
        try:
            # Binance API'den kline verilerini al
            data = get_binance_klines(symbol, interval)

            # HLC3 ve VWAP hesapla
            hlc3, vwap = calculate_hlc3_vwap(data)

            # HLC3, VWAP'ın üstünde mi?
            result = hlc3 > vwap
            print(f"HLC3: {hlc3}, VWAP: {vwap}, Result: {result}")

        except Exception as e:
            print(f"Hata: {e}")

        # 60 saniye bekle
        time.sleep(60)

if __name__ == "__main__":
    main()
