from binance.cm_futures import CMFutures
from binance.client import Client
api_key = 'PhtkBtWNspyWWUwjQX9rDekZPxVAN6blRvnBUzQsrhlrO4xbvzWvrJCtXircFfPU'
api_secret = 'iAJFQwVXHRVXvA2ffjxb5dxd5nlHEFZjv2yP12FzqUSXxic7mz02rILS54YWOEOH'

mclient = CMFutures(api_key, api_secret)

client = Client(api_key, api_secret)
# Hesap bilgilerinizi alın
#account_info = client.account()
#print(account_info)

#margin_balance = account_info['totalMarginBalance']
#print(f"Margin Balance: {margin_balance}")


# Futures cüzdan bakiyesini çekmek için 
futures_balance = client.futures_account_balance() 
for balance in futures_balance: 
    if balance['asset'] == 'USDT':
         # İstediğiniz varlığı buraya girin 
         print(f"Available Balance: {balance['balance']}")