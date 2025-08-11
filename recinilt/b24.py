import time, requests, hmac, hashlib, json
from urllib.parse import urlencode
from datetime import datetime

class BinanceFuturesBot:
  def __init__(self, api_key, api_secret, demo_mode=True):
      self.api_key, self.api_secret = api_key, api_secret
      self.base_url = "https://testnet.binancefuture.com" if demo_mode else "https://fapi.binance.com"
      self.demo_mode = demo_mode
      self.symbol_info = {}
      self.reset_position()
      self.stats = {
          'session_start': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
          'initial_balance': 0, 'current_balance': 0, 'total_pnl': 0,
          'total_trades': 0, 'winning_trades': 0, 'losing_trades': 0,
          'max_consecutive_losses': 0, 'current_consecutive_losses': 0,
          'trade_history': []
      }
      
      # Sermaye oranı bahis sistemi için yeni değişkenler
      self.capital_ratio_enabled = False
      self.capital_threshold = 0
      self.base_initial_bet = 0
      self.current_initial_bet = 0
      self.max_initial_bet = 0
      self.multiplier = 2.0
      
  def reset_position(self):
      self.position_opened = False
      self.last_entry_price = 0
      self.current_quantity = 0
      self.leverage = 1
      self.limit_order_id = None
      self.limit_price = 0
  
  def update_initial_bet(self):
      """Sermaye oranına göre ilk bahsi güncelle"""
      if not self.capital_ratio_enabled:
          return
        
      capital_multiplier = int(self.stats['current_balance'] / self.capital_threshold)
      calculated_bet = self.base_initial_bet * capital_multiplier
    
      # Maksimum bahisten yüksek hesaplanırsa güncelle
      if calculated_bet > self.max_initial_bet:
          self.max_initial_bet = calculated_bet
          self.current_initial_bet = calculated_bet
          print(f"💰 Mevcut Sermaye: ${self.stats['current_balance']:.2f}")
          print(f"🎯 Sermaye Çarpanı: {capital_multiplier}x")
          print(f"💵 Güncel İlk Bahis: ${self.current_initial_bet:.2f}")
      else:
          # Maksimum bahisten düşükse değiştirme
          self.current_initial_bet = self.max_initial_bet


  def check_capital_ratio_update(self):
      """Sermaye oranı kontrolü yap"""
      if not self.capital_ratio_enabled or self.position_opened:
          return
        
      old_bet = self.current_initial_bet
      self.update_initial_bet()
    
      if old_bet != self.current_initial_bet:
          print(f"🚀 İLK BAHİS ARTIŞI! ${old_bet:.2f} → ${self.current_initial_bet:.2f}")
          print(f"📈 Maksimum Bahis: ${self.max_initial_bet:.2f}")
          self.update_stats("İLK_BAHİS_ARTIŞI", self.current_initial_bet, 0, 0)


  def get_signature(self, params):
      return hmac.new(self.api_secret.encode(), urlencode(params).encode(), hashlib.sha256).hexdigest()
  
  def get_balance(self):
      if self.demo_mode:
          return self.stats['current_balance']
      
      try:
          timestamp = int(time.time() * 1000)
          params = {"timestamp": timestamp}
          params["signature"] = self.get_signature(params)
          response = requests.get(f"{self.base_url}/fapi/v2/account", params=params, 
                                headers={"X-MBX-APIKEY": self.api_key}).json()
          
          for asset in response.get('assets', []):
              if asset['asset'] == 'USDT':
                  balance = float(asset['walletBalance'])
                  self.stats['current_balance'] = balance
                  return balance
          return 0
      except Exception as e:
          print(f"❌ Bakiye alınamadı: {e}")
          return self.stats['current_balance']
  
  def get_position_info(self, symbol):
      """Açık pozisyon var mı kontrol et"""
      if self.demo_mode:
          return self.position_opened
      
      try:
          timestamp = int(time.time() * 1000)
          params = {"symbol": symbol, "timestamp": timestamp}
          params["signature"] = self.get_signature(params)
          response = requests.get(f"{self.base_url}/fapi/v2/positionRisk", params=params, 
                                headers={"X-MBX-APIKEY": self.api_key}).json()
          
          for pos in response:
              if pos['symbol'] == symbol and float(pos['positionAmt']) != 0:
                  return True
          return False
      except:
          return self.position_opened
  
  def get_symbol_info(self, symbol):
      url = "https://fapi.binance.com/fapi/v1/exchangeInfo"
      response = requests.get(url)
      data = response.json()
      
      for s in data['symbols']:
          if s['symbol'] == symbol:
              symbol_data = {
                  'quantityPrecision': s['quantityPrecision'],
                  'pricePrecision': s['pricePrecision']
              }
              for f in s['filters']:
                  if f['filterType'] == 'LOT_SIZE':
                      symbol_data['minQty'] = float(f['minQty'])
                      symbol_data['stepSize'] = float(f['stepSize'])
                  elif f['filterType'] == 'PRICE_FILTER':
                      symbol_data['tickSize'] = float(f['tickSize'])
              
              self.symbol_info[symbol] = symbol_data
              print(f"📋 {symbol} - MinQty: {symbol_data['minQty']}, QtyPrec: {symbol_data['quantityPrecision']}, PricePrec: {symbol_data['pricePrecision']}")
              return
      print(f"⚠️ Symbol bilgisi bulunamadı: {symbol}")
  
  def format_quantity(self, symbol, quantity):
      if symbol not in self.symbol_info:
          return quantity
      
      precision = self.symbol_info[symbol]['quantityPrecision']
      step_size = self.symbol_info[symbol]['stepSize']
      min_qty = self.symbol_info[symbol]['minQty']
      
      quantity = round(quantity / step_size) * step_size
      quantity = round(quantity, precision)
      quantity = max(quantity, min_qty)
      
      return quantity
  
  def format_price(self, symbol, price):
      if symbol not in self.symbol_info:
          return price
      
      precision = self.symbol_info[symbol]['pricePrecision']
      tick_size = self.symbol_info[symbol]['tickSize']
      
      price = round(price / tick_size) * tick_size
      price = round(price, precision)
      
      return price
  
  def get_price(self, symbol):
      url = "https://fapi.binance.com/fapi/v1/ticker/price"
      response = requests.get(url, params={"symbol": symbol})
      return float(response.json()["price"])
  
  def calculate_pnl(self, current_price, side):
      """Leverage etkili PnL hesaplama"""
      if not self.position_opened or self.current_quantity <= 0:
          return 0
      
      if side == "BUY":  # Long pozisyon
          pnl = (current_price - self.last_entry_price) * self.current_quantity
      else:  # Short pozisyon  
          pnl = (self.last_entry_price - current_price) * self.current_quantity
      
      return pnl
  
  def cancel_limit_order(self, symbol):
      if not self.limit_order_id:
          return
      
      if self.demo_mode:
          print(f"🎮 DEMO: Limit emir iptal edildi")
          self.limit_order_id = None
          return
      
      timestamp = int(time.time() * 1000)
      params = {"symbol": symbol, "orderId": self.limit_order_id, "timestamp": timestamp}
      params["signature"] = self.get_signature(params)
      try:
          requests.delete(f"{self.base_url}/fapi/v1/order", params=params, 
                        headers={"X-MBX-APIKEY": self.api_key})
          self.limit_order_id = None
      except:
          pass
  
  def check_limit_order(self, symbol, direction):
      if not self.limit_order_id:
          return False
      
      if self.demo_mode:
          current_price = self.get_price(symbol)
          if (direction == "long" and current_price >= self.limit_price) or \
             (direction == "short" and current_price <= self.limit_price):
              print(f"🎮 DEMO: Kar al limit emri tetiklendi! ${current_price:.8f}")
              return True
          return False
      
      timestamp = int(time.time() * 1000)
      params = {"symbol": symbol, "orderId": self.limit_order_id, "timestamp": timestamp}
      params["signature"] = self.get_signature(params)
      try:
          response = requests.get(f"{self.base_url}/fapi/v1/order", params=params, 
                                headers={"X-MBX-APIKEY": self.api_key}).json()
          return response["status"] == "FILLED"
      except:
          return False
  
  def close_position(self, symbol, side):
      if not self.position_opened or self.current_quantity <= 0:
          return True
      
      close_side = "SELL" if side == "BUY" else "BUY"
      
      if self.demo_mode:
          current_price = self.get_price(symbol)
          pnl = self.calculate_pnl(current_price, side)
          self.stats['current_balance'] += pnl
          self.update_stats("KAPAT", 0, pnl, current_price)
          print(f"🎮 DEMO: Pozisyon kapatıldı - PnL: ${pnl:.2f}")
          self.reset_position()
          return True
      
      timestamp = int(time.time() * 1000)
      formatted_qty = self.format_quantity(symbol, self.current_quantity)
      
      params = {"symbol": symbol, "side": close_side, "type": "MARKET", 
               "quantity": formatted_qty, "timestamp": timestamp}
      params["signature"] = self.get_signature(params)
      
      try:
          response = requests.post(f"{self.base_url}/fapi/v1/order", params=params, 
                                 headers={"X-MBX-APIKEY": self.api_key}).json()
          
          if 'code' in response:
              print(f"❌ Kapatma Hatası: {response['msg']}")
              return False
          
          print(f"✅ Pozisyon kapatıldı")
          self.reset_position()
          return True
      except Exception as e:
          print(f"❌ Kapatma hatası: {e}")
          return False
  
  def place_limit_order(self, symbol, side, quantity, price):
      formatted_qty = self.format_quantity(symbol, quantity)
      formatted_price = self.format_price(symbol, price)
      
      if self.demo_mode:
          print(f"🎮 DEMO: Kar al limit emri ${formatted_price:.8f} fiyatına koyuldu (Qty: {formatted_qty})")
          self.limit_order_id = "demo_limit"
          self.limit_price = formatted_price
          return {"orderId": "demo_limit"}
      
      timestamp = int(time.time() * 1000)
      params = {"symbol": symbol, "side": side, "type": "LIMIT", "timeInForce": "GTC",
               "quantity": formatted_qty, "price": formatted_price, "timestamp": timestamp}
      params["signature"] = self.get_signature(params)
      response = requests.post(f"{self.base_url}/fapi/v1/order", params=params, 
                             headers={"X-MBX-APIKEY": self.api_key}).json()
      
      if 'code' in response:
          print(f"❌ Limit Order Hatası: {response['msg']}")
          return None
      
      self.limit_order_id = response["orderId"]
      self.limit_price = formatted_price
      return response
  
  def place_order(self, symbol, side, amount, leverage):
      current_price = self.get_price(symbol)
      leveraged_quantity = (amount * leverage) / current_price
      formatted_qty = self.format_quantity(symbol, leveraged_quantity)
      
      if self.demo_mode:
          print(f"🎮 DEMO: {side} emri simüle edildi - {formatted_qty} {symbol[:3]}")
          return {"status": "FILLED", "executedQty": str(formatted_qty), "avgPrice": str(current_price)}
      
      timestamp = int(time.time() * 1000)
      # Kaldıraç ayarla
      lev_params = {"symbol": symbol, "leverage": leverage, "timestamp": timestamp}
      lev_params["signature"] = self.get_signature(lev_params)
      requests.post(f"{self.base_url}/fapi/v1/leverage", params=lev_params, 
                   headers={"X-MBX-APIKEY": self.api_key})
      
      # Emir ver
      params = {"symbol": symbol, "side": side, "type": "MARKET", "quantity": formatted_qty, "timestamp": timestamp}
      params["signature"] = self.get_signature(params)
      response = requests.post(f"{self.base_url}/fapi/v1/order", params=params, 
                         headers={"X-MBX-APIKEY": self.api_key}).json()
      
      if 'code' in response:
          print(f"❌ Market Order Hatası: {response['msg']}")
          return None
      
      return response
  
  def set_limit_order(self, symbol, direction, profit_percent):
      """Sadece kar al için limit emir koy"""
      if self.current_quantity <= 0:
          print("❌ Pozisyon bilgisi eksik, limit emir koyulamadı!")
          return
      
      if direction == "long":
          limit_price = self.last_entry_price * (1 + profit_percent / 100)
          side = "SELL"
      else:
          limit_price = self.last_entry_price * (1 - profit_percent / 100)
          side = "BUY"
      
      result = self.place_limit_order(symbol, side, self.current_quantity, limit_price)
      if result:
          print(f"🎯 Kar al limit emri: ${limit_price:.8f} (Giriş: ${self.last_entry_price:.8f})")
      else:
          print("❌ Kar al limit emri koyulamadı!")
  
  def handle_position_closed(self, symbol, direction, current_bet, leverage, side, profit_percent, stop_loss_percent):
      """Pozisyon kapandığında ne yapılacağını belirle"""
      limit_triggered = self.check_limit_order(symbol, direction)
      
      if limit_triggered:
          # Kar! Bahis sıfırla ve sermaye oranı kontrolü yap
          print(f"✅ Kar al limit emriyle kapandı! Kar elde edildi!")
          self.update_stats("KAR_AL_LIMIT", 0, 0, self.limit_price)
          self.reset_position()
          self.check_capital_ratio_update()
          return self.current_initial_bet
      else:
          # Likidation veya manuel kapatma! Bahis arttır ve yeni pozisyon aç
          print(f"💥 Pozisyon zorla kapatıldı (Likidation/Manuel)!")
          self.cancel_limit_order(symbol)
          new_bet = current_bet * self.multiplier
          
          # Yeni pozisyon aç
          current_price = self.get_price(symbol)
          print(f"🔥 Likidation/Manuel kapanma sonrası yeni pozisyon: ${new_bet:.2f} ({leverage}x)")
          order = self.place_order(symbol, side, new_bet, leverage)
          if order is None:
              print("❌ Yeni pozisyon açılamadı!")
              return current_bet
          
          # Pozisyon bilgilerini güncelle
          executed_qty = float(order["executedQty"]) if order.get("status") == "FILLED" else float(order.get("origQty", "0"))
          executed_price = float(order["avgPrice"]) if order.get("status") == "FILLED" else current_price
          
          if executed_qty == 0:
              print("❌ Yeni pozisyon açılamadı!")
              return current_bet
              
          self.position_opened = True
          self.last_entry_price = executed_price
          self.current_quantity = executed_qty
          self.leverage = leverage
          
          # Yeni kar al limit emri
          self.set_limit_order(symbol, direction, profit_percent)
          self.update_stats("LİKİDASYON_YENİ", new_bet, 0, executed_price)
          
          return new_bet
  
  def update_stats(self, trade_type, amount, pnl=0, price=0):
      self.stats['total_trades'] += 1
      if not self.demo_mode and pnl != 0:
          self.get_balance()
      else:
          self.stats['current_balance'] += pnl
      self.stats['total_pnl'] += pnl
      
      if pnl > 0:
          self.stats['winning_trades'] += 1
          self.stats['current_consecutive_losses'] = 0
      elif pnl < 0:
          self.stats['losing_trades'] += 1
          self.stats['current_consecutive_losses'] += 1
          self.stats['max_consecutive_losses'] = max(self.stats['max_consecutive_losses'], 
                                                   self.stats['current_consecutive_losses'])
      
      trade_data = {
          'time': datetime.now().strftime('%H:%M:%S'),
          'type': trade_type, 'amount': amount, 'price': price, 'pnl': pnl,
          'balance': self.stats['current_balance'], 'consecutive_losses': self.stats['current_consecutive_losses']
      }
      self.stats['trade_history'].append(trade_data)
      self.save_stats(trade_data)
  
  def save_stats(self, trade_data):
      with open('binancestatistics.txt', 'a', encoding='utf-8') as f:
          if trade_data['type'] == 'SESSION_START':
              f.write(f"\n{'='*80}\n🚀 YENİ SESSİON BAŞLADI - {self.stats['session_start']} 🚀\n{'='*80}\n")
              f.write(f"💰 Başlangıç Sermayesi: {self.stats['initial_balance']} USDT\n")
              f.write(f"🎮 Mod: {'DEMO (Test)' if self.demo_mode else 'GERÇEK'}\n")
              f.write(f"💱 Symbol: {self.stats['symbol']} | ⚡ Kaldıraç: {self.stats['leverage']}x\n")
              f.write(f"📈 Yön: {self.stats['direction']} | 💵 İlk Bahis: ${self.stats['initial_bet']}\n")
              f.write(f"🔢 Çarpan: {self.stats['multiplier']}x | 📈 Kar Al: {self.stats['profit_percent']}% | 🛑 Zarar Durdur: {self.stats['stop_loss_percent']}%\n")
              f.write(f"🎯 Sistem: AYRI KAR AL / ZARAR DURDUR + LİKİDASYON KONTROLÜ\n")
              if self.capital_ratio_enabled:
                  f.write(f"🚀 Sermaye Oranı Sistemi: AÇIK (Eşik: ${self.capital_threshold:.2f}, Temel Bahis: ${self.base_initial_bet:.2f})\n")
              else:
                  f.write(f"🚀 Sermaye Oranı Sistemi: KAPALI\n")
              f.write(f"{'-'*80}\n")
          else:
              if trade_data['type'] == 'İLK_BAHİS_ARTIŞI':
                  f.write(f"[{trade_data['time']}] 🚀 İLK BAHİS ARTIŞI | "
                         f"💵 Yeni İlk Bahis: ${trade_data['amount']:.2f} | "
                         f"💰 Bakiye: ${trade_data['balance']:.2f}\n")
              else:
                  f.write(f"[{trade_data['time']}] {trade_data['type']} | "
                         f"💵 ${trade_data['amount']:.2f} | 📈 {trade_data['price']:.8f} | "
                         f"{'💚' if trade_data['pnl'] >= 0 else '💔'} PnL: ${trade_data['pnl']:.2f} | "
                         f"💰 Bakiye: ${trade_data['balance']:.2f} | "
                         f"🔥 Ard.Kayıp: {trade_data['consecutive_losses']}\n")
  
  def run_bot(self):
      print("\n" + "="*60)
      print("🤖 BİNANCE FUTURES BOT - AYRI KAR AL / ZARAR DURDUR SİSTEMİ 🤖")
      print("="*60)
      
      mode = input("🎮 Mod seçin (1=Demo/Test, 2=Gerçek): ")
      self.demo_mode = mode != "2"
      self.base_url = "https://testnet.binancefuture.com" if self.demo_mode else "https://fapi.binance.com"
      
      symbol = input("💱 İşlem çifti (BTCUSDT): ").upper() or "BTCUSDT"
      
      print("📋 Symbol bilgileri alınıyor...")
      self.get_symbol_info(symbol)
      
      leverage = int(input("⚡ Kaldıraç (100): ") or "100")
      direction = input("📈 Yön (long/short): ").lower()
      initial_amount = float(input("💰 İlk bahis (USDT): "))
      multiplier = float(input("🔢 Çarpan (2): ") or "2")
      self.multiplier = multiplier
      profit_percent = float(input("📈 Kar Al % (4): ") or "4")
      stop_loss_percent = float(input("🛑 Zarar Durdur % (4): ") or "4")
      
      # Sermaye oranı bahis sistemi ayarları
      capital_ratio = input("\n💰 Sermaye oranında bahis artırımı aktif edilsin mi? (e/h): ").lower()

      if capital_ratio in ['e', 'evet', 'y', 'yes']:
          self.capital_ratio_enabled = True
          self.capital_threshold = float(input("🎯 Sermaye eşik değeri (örn: 200 USDT): "))
          self.base_initial_bet = initial_amount
          self.current_initial_bet = initial_amount
          self.max_initial_bet = initial_amount
          
          if self.demo_mode:
              demo_balance = float(input("💼 Demo başlangıç sermayesi (1000): ") or "1000")
              self.stats['current_balance'] = demo_balance
          else:
              print("💰 Gerçek bakiye kontrol ediliyor...")
              real_balance = self.get_balance()
              print(f"💰 Mevcut bakiye: ${real_balance:.2f} USDT")
          
          # İlk bahis hesapla
          self.update_initial_bet()
          
          print(f"\n✅ Sermaye Oranı Sistemi Aktif!")
          print(f"🎯 Eşik Değer: ${self.capital_threshold:.2f} USDT")
          print(f"💵 Başlangıç Bahis: ${self.base_initial_bet:.2f}")
          print(f"💰 Mevcut İlk Bahis: ${self.current_initial_bet:.2f}")

      else:
          self.capital_ratio_enabled = False
          self.current_initial_bet = initial_amount
          
          if self.demo_mode:
              demo_balance = float(input("💼 Demo başlangıç sermayesi (1000): ") or "1000")
              self.stats['current_balance'] = demo_balance
          else:
              print("💰 Gerçek bakiye kontrol ediliyor...")
              real_balance = self.get_balance()
              print(f"💰 Mevcut bakiye: ${real_balance:.2f} USDT")
      
      self.stats['initial_balance'] = self.stats['current_balance']
      self.stats['symbol'] = symbol
      self.stats['leverage'] = leverage
      self.stats['direction'] = direction.upper()
      self.stats['initial_bet'] = initial_amount
      self.stats['multiplier'] = multiplier
      self.stats['profit_percent'] = profit_percent
      self.stats['stop_loss_percent'] = stop_loss_percent
      self.update_stats("SESSION_START", 0)
      
      side = "BUY" if direction == "long" else "SELL"
      current_bet = self.current_initial_bet
      
      # Zarar durdur seviyesi hesaplama
      liquidation_percent = 100 / leverage
      actual_stop_loss = min(liquidation_percent, stop_loss_percent)
      
      print(f"\n🚀 Bot başlatıldı: {symbol} {direction.upper()} {leverage}x")
      print(f"💰 Sermaye: ${self.stats['current_balance']:.2f} | Mod: {'DEMO' if self.demo_mode else 'GERÇEK'}")
      print(f"📈 Kar Al: {profit_percent}% | 🛑 Zarar Durdur: {stop_loss_percent}% | ⚡ Likidite: {liquidation_percent:.2f}%")
      print(f"🛑 Kullanılan Stop Loss: {actual_stop_loss:.2f}% (Min(Zarar Durdur, Likidite))")
      if self.capital_ratio_enabled:
          print(f"🚀 Sermaye Oranı Sistemi: AÇIK | Mevcut İlk Bahis: ${self.current_initial_bet:.2f}")
      
      while True:
          try:
              if not self.demo_mode:
                  self.get_balance()
              
              current_price = self.get_price(symbol)
              print(f"\n📊 Fiyat: ${current_price:.8f} |Bakiye: ${self.stats['current_balance']:.2f}")
              if self.capital_ratio_enabled:
                  print(f"🚀 Mevcut İlk Bahis: ${self.current_initial_bet:.2f} | Eşik: ${self.capital_threshold:.2f}")
              
              # Pozisyon durumu kontrolü
              actual_position_exists = self.get_position_info(symbol)
              
              if self.position_opened and not actual_position_exists:
                  # Pozisyon kapanmış (likidation veya limit)
                  current_bet = self.handle_position_closed(symbol, direction, current_bet, leverage, side, profit_percent, stop_loss_percent)
                  time.sleep(2)
                  continue
              
              if not self.position_opened:
                  # Sermaye oranı kontrolü
                  self.check_capital_ratio_update()
                  current_bet = self.current_initial_bet
                  
                  # Bakiye kontrolü
                  if self.stats['current_balance'] < current_bet:
                      print("⚠️ Yetersiz bakiye! Bot durduruluyor.")
                      break
                      
                  print(f"🎯 Yeni pozisyon: ${current_bet:.2f} ({leverage}x kaldıraç)")
                  order = self.place_order(symbol, side, current_bet, leverage)
                  if order is None:
                      print("💰 Hesap bakiyenizi kontrol edin!")
                      break
                  
                  # Demo modda bakiye güncellemesi
                  if self.demo_mode:
                      self.stats['current_balance'] -= current_bet
                  
                  # Pozisyon bilgilerini kaydet
                  executed_qty = float(order["executedQty"]) if order.get("status") == "FILLED" else float(order.get("origQty", "0"))
                  executed_price = float(order["avgPrice"]) if order.get("status") == "FILLED" else current_price
                  
                  if executed_qty == 0:
                      print("❌ Pozisyon açılamadı, tekrar deneniyor...")
                      time.sleep(3)
                      continue
                  
                  self.position_opened = True
                  self.last_entry_price = executed_price
                  self.current_quantity = executed_qty
                  self.leverage = leverage
                  
                  # Kar al limit emri koy
                  self.set_limit_order(symbol, direction, profit_percent)
                  self.update_stats("AÇILIŞ", current_bet, 0, executed_price)
                  
              else:
                  # Sıralı kontrol sistemi
                  
                  # 1. KAR AL KONTROLÜ (Limit Order)
                  if self.check_limit_order(symbol, direction):
                      print(f"💚 KAR AL! Limit emir tetiklendi!")
                      # Limit emri iptal et
                      self.cancel_limit_order(symbol)
                      
                      # Pozisyonu kapat (PnL hesaplaması içinde)
                      if not self.close_position(symbol, side):
                          print("❌ Pozisyon kapatılamadı!")
                          time.sleep(3)
                          continue
                      
                      # Sermaye oranı kontrolü yap ve başa dön
                      self.check_capital_ratio_update()
                      current_bet = self.current_initial_bet
                      
                      time.sleep(1)
                      continue
                  
                  # 0.5 saniye bekle
                  time.sleep(0.5)
                  
                  # 2. ZARAR DURDUR KONTROLÜ
                  change_pct = ((current_price - self.last_entry_price) / self.last_entry_price) * 100
                  
                  if (direction == "long" and change_pct <= -actual_stop_loss) or \
                     (direction == "short" and change_pct >= actual_stop_loss):
                      
                      print(f"🔴 ZARAR DURDUR! Değişim: {change_pct:.2f}%, Eşik: {actual_stop_loss:.2f}%")
                      
                      # Limit emri iptal et
                      self.cancel_limit_order(symbol)
                      
                      # Mevcut pozisyonu kapat (PnL hesaplaması içinde)
                      print(f"🔄 Pozisyon kapatılıyor...")
                      if not self.close_position(symbol, side):
                          print("❌ Pozisyon kapatılamadı!")
                          time.sleep(3)
                          continue
                      
                      time.sleep(0.5)
                      
                      # Yeni bahis miktarı (Martingale)
                      current_bet *= multiplier
                      
                      if self.stats['current_balance'] < current_bet:
                          print("⚠️ Yetersiz bakiye!")
                          break
                          
                      print(f"🔥 Martingale - Yeni pozisyon: ${current_bet:.2f} ({leverage}x)")
                      order = self.place_order(symbol, side, current_bet, leverage)
                      if order is None:
                          print("❌ Yeni pozisyon açılamadı!")
                          continue
                      
                      # Demo modda bakiye güncellemesi
                      if self.demo_mode:
                          self.stats['current_balance'] -= current_bet
                      
                      # Yeni pozisyon bilgileri
                      executed_qty = float(order["executedQty"]) if order.get("status") == "FILLED" else float(order.get("origQty", "0"))
                      executed_price = float(order["avgPrice"]) if order.get("status") == "FILLED" else current_price
                      
                      if executed_qty == 0:
                          print("❌ Yeni pozisyon açılamadı!")
                          continue
                          
                      self.position_opened = True
                      self.last_entry_price = executed_price
                      self.current_quantity = executed_qty
                      
                      # Yeni kar al limit emri
                      self.set_limit_order(symbol, direction, profit_percent)
                      self.update_stats("MARTINGALE_POZİSYON", current_bet, 0, executed_price)
                  
                  # 0.5 saniye bekle
                  time.sleep(0.5)
              
              # Ana loop bekleme
              time.sleep(2)
              
          except KeyboardInterrupt:
              print(f"\n🛑 Bot durduruldu!")
              if self.position_opened:
                  self.cancel_limit_order(symbol)
              break
          except Exception as e:
              print(f"❌ Hata: {e}")
              time.sleep(3)

if __name__ == "__main__":
  print("🔐 API Bilgileri (Demo modda da gerçek fiyat için gerekli)")
  api_key = input("Binance API Key: ")
  api_secret = input("API Secret: ")
  
  if not api_key or not api_secret:
      print("⚠️ API bilgileri gerekli! (Gerçek fiyat çekmek için)")
      exit()
  
  bot = BinanceFuturesBot(api_key, api_secret)
  bot.run_bot()