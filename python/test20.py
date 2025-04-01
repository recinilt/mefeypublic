import requests
import hmac
import hashlib
import time

API_KEY = 'PhtkBtWNspyWWUwjQX9rDekZPxVAN6blRvnBUzQsrhlrO4xbvzWvrJCtXircFfPU'
API_SECRET = 'iAJFQwVXHRVXvA2ffjxb5dxd5nlHEFZjv2yP12FzqUSXxic7mz02rILS54YWOEOH'

def get_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    response = requests.get(url)
    data = response.json()
    return float(data['price'])

def calculate_amount(usdt_amount, price):
    return usdt_amount / price

def create_signature(query_string, secret):
    return hmac.new(secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

def open_long_position(symbol, amount, leverage):
    base_url = "https://fapi.binance.com"
    endpoint = "/fapi/v1/order"
    timestamp = int(time.time() * 1000)
    
    params = {
        "symbol": symbol,
        "side": "BUY",
        "type": "MARKET",
        "quantity": round(amount * leverage, 3),
        "timestamp": timestamp
    }
    
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    signature = create_signature(query_string, API_SECRET)
    params["signature"] = signature
    
    headers = {
        "X-MBX-APIKEY": API_KEY
    }
    
    response = requests.post(base_url + endpoint, params=params, headers=headers)
    data = response.json()
    
    if response.status_code == 200:
        print(f"Order successful: {data}")
    else:
        print(f"Order failed: {data}")

def main():
    symbol = "BTCUSDT"  # İstediğiniz coin çiftini buraya yazın
    usdt_amount = 2.0
    leverage = 10

    price = get_price(symbol)
    amount = calculate_amount(usdt_amount, price)
    open_long_position(symbol, amount, leverage)

if __name__ == "__main__":
    main()
