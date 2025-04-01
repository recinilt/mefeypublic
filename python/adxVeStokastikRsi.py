import pandas as pd
import ta
from binance.client import Client

# Binance API anahtarları (eğer özel erişim gerekiyorsa doldurabilirsiniz)
BINANCE_API_KEY = "PhtkBtWNspyWWUwjQX9rDekZPxVAN6blRvnBUzQsrhlrO4xbvzWvrJCtXircFfPU"  # Eğer gerekli değilse boş bırakabilirsiniz
BINANCE_API_SECRET = "iAJFQwVXHRVXvA2ffjxb5dxd5nlHEFZjv2yP12FzqUSXxic7mz02rILS54YWOEOH"

# Binance'ten veri çekme
def get_binance_data(symbol, interval="1h", limit=500):
    """
    Binance'ten OHLC (Open, High, Low, Close) verilerini çeker.

    Args:
        symbol (str): Kripto para çifti (ör: "BTCUSDT").
        interval (str): Zaman dilimi (ör: "1h", "4h").
        limit (int): Çekilecek mum sayısı (maksimum 1000).

    Returns:
        pandas.DataFrame: OHLC verileri.
    """
    client = Client(api_key=BINANCE_API_KEY, api_secret=BINANCE_API_SECRET)
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    
    # Veriyi pandas DataFrame'e dönüştürme
    data = pd.DataFrame(klines, columns=[
        "timestamp", "Open", "High", "Low", "Close", "Volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base", "taker_buy_quote", "ignore"
    ])
    data["Open"] = pd.to_numeric(data["Open"])
    data["High"] = pd.to_numeric(data["High"])
    data["Low"] = pd.to_numeric(data["Low"])
    data["Close"] = pd.to_numeric(data["Close"])
    data["Volume"] = pd.to_numeric(data["Volume"])
    data["timestamp"] = pd.to_datetime(data["timestamp"], unit="ms")
    data.set_index("timestamp", inplace=True)
    return data[["Open", "High", "Low", "Close", "Volume"]]

# Stokastik RSI ve ADX hesaplama
def calculate_indicators(data, adx_period=14, stoch_rsi_window=14):
    """
    ADX ve Stokastik RSI indikatörlerini hesaplar.

    Args:
        data (pd.DataFrame): OHLC verileri.

    Returns:
        pd.DataFrame: İndikatörler eklenmiş veri.
    """
    # ADX hesaplama
    data['ADX'] = ta.trend.adx(data['High'], data['Low'], data['Close'], window=adx_period)
    
    # Stokastik RSI hesaplama
    stoch_rsi = ta.momentum.StochRSIIndicator(data['Close'], window=stoch_rsi_window)
    data['Stoch_RSI_K'] = stoch_rsi.stochrsi_k()
    data['Stoch_RSI_D'] = stoch_rsi.stochrsi_d()
    
    return data

# Al sinyali tespiti
def generate_signals(data, adx_threshold=25, stoch_rsi_k_limit=20):
    """
    Al sinyali oluşturur.

    Args:
        data (pd.DataFrame): İndikatörler eklenmiş veri.

    Returns:
        pd.DataFrame: Al sinyali olan veriler.
    """
    data['Buy_Signal'] = (
        (data['ADX'] > adx_threshold) &  # ADX güçlü trend
        (data['Stoch_RSI_K'] < stoch_rsi_k_limit)  # Stokastik RSI aşırı satım
    )
    return data

# Çoklu coin listesi için kontrol
def get_buy_signals(coin_pairs, interval="1h", limit=500):
    """
    Birden fazla coin çifti için al sinyallerini kontrol eder.

    Args:
        coin_pairs (list): Coin çiftlerinin listesi (ör: ["BTCUSDT", "ETHUSDT"]).
        interval (str): Zaman dilimi (ör: "1h", "4h").
        limit (int): Her coin için çekilecek mum sayısı.

    Returns:
        list: Al sinyali veren coin çiftleri.
    """
    buy_signals = []
    for symbol in coin_pairs:
        try:
            # Verileri çekme
            data = get_binance_data(symbol, interval=interval, limit=limit)

            # İndikatör hesaplama
            data = calculate_indicators(data)

            # Sinyal üretme
            data = generate_signals(data)

            # Eğer son satırda sinyal varsa ekle
            if data['Buy_Signal'].iloc[-1]:
                buy_signals.append(symbol)
        except Exception as e:
            print(f"Hata oluştu: {symbol} - {e}")
    return buy_signals


binanceclient = Client(BINANCE_API_KEY, BINANCE_API_SECRET)
exchange_info = binanceclient.futures_exchange_info()
#time.sleep(2)
symbols = exchange_info['symbols']
mysymbols3=[]
for s in symbols:
    mysymbols3.append(s['symbol'])
print("Binancetaki futures coin çiftleri: \n",mysymbols3)

# Kullanım
if __name__ == "__main__":
    # Kontrol edilecek coin çiftleri
    #coin_list = ["BTCUSDT", "ETHUSDT", "ADAUSDT", "SOLUSDT"]

    # Sinyalleri kontrol et
    signals = get_buy_signals(mysymbols3)
    print("Al Sinyali Veren Coinler:")
    print(signals)
