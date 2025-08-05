# Multi-Coin Martingale Optimizasyon Sistemi - Google Colab Versiyonu
# Orijinal HTML kodundan tam port edilmiş versiyon

import pandas as pd
import numpy as np
import requests
import json
import time
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import ipywidgets as widgets
from IPython.display import display, HTML, clear_output
import io
import base64

class MultiCoinMartingaleOptimizer:
    def __init__(self):
        self.data = {}
        self.saved_data = {}
        self.original_data = {}
        self.training_results = []
        self.results = []
        self.params = None
        self.meta = None
        self.running = False
        self.sort_config = {'column': 'validationScore', 'direction': 'desc'}
        
    def setup_ui(self):
        """UI bileşenlerini oluştur"""
        print("🎯 Multi-Coin Martingale Optimizasyonu - Google Colab Versiyonu")
        print("⚡ Tam Özellikli Validation Sistemi - Walk-Forward, Cross-Validation, Gerçek Sharpe Ratio")
        print("="*80)
        
        # Veri Yönetimi Bölümü
        self.data_section = self.create_data_section()
        display(self.data_section)
        
        # Optimizasyon Bölümü  
        self.opt_section = self.create_optimization_section()
        display(self.opt_section)
        
        # Validation Bölümü
        self.validation_section = self.create_validation_section()
        
        # Sonuçlar için output widget
        self.results_output = widgets.Output()
        
    def create_data_section(self):
        """Veri yönetimi UI bileşenleri"""
        print("\n📊 VERİ YÖNETİMİ")
        print("🚀 Akıllı Veri Sistemi: Büyük veri setlerini çekin ve kaydedin")
        
        # Veri çekme parametreleri
        self.data_coins = widgets.Text(
            value='BTCUSDT',
            placeholder='BTCUSDT,ETHUSDT,ADAUSDT',
            description='🪙 Coin Çiftleri:',
            style={'description_width': 'initial'}
        )
        
        self.data_timeframe = widgets.Dropdown(
            options=[('1 Dakika', '1m'), ('5 Dakika', '5m'), ('15 Dakika', '15m'), 
                    ('30 Dakika', '30m'), ('1 Saat', '1h'), ('4 Saat', '4h'), 
                    ('12 Saat', '12h'), ('1 Gün', '1d')],
            value='5m',
            description='⏰ Zaman Dilimi:'
        )
        
        # Tarih seçiciler - default değerler
        end_date = datetime.now()
        start_date = end_date - timedelta(days=730)  # 2 yıl
        
        self.data_start_date = widgets.DatePicker(
            value=start_date.date(),
            description='📅 Başlangıç:'
        )
        
        self.data_end_date = widgets.DatePicker(
            value=end_date.date(),
            description='📅 Bitiş:'
        )
        
        # Butonlar
        self.fetch_data_btn = widgets.Button(
            description='💾 Verileri Çek ve Kaydet',
            button_style='info',
            layout=widgets.Layout(width='200px')
        )
        self.fetch_data_btn.on_click(self.fetch_and_save_data)
        
        self.load_data_btn = widgets.Button(
            description='📂 JSON Dosyasından Yükle',
            button_style='success',
            layout=widgets.Layout(width='200px')
        )
        
        # Progress bar
        self.data_progress = widgets.IntProgress(
            value=0,
            min=0,
            max=100,
            description='İlerleme:',
            bar_style='info'
        )
        
        self.data_status = widgets.HTML(value="")
        
        # Veri bilgileri
        self.data_info = widgets.HTML(value="")
        
        data_box = widgets.VBox([
            widgets.HTML("<h3>📊 Veri Yönetimi</h3>"),
            widgets.HBox([self.data_coins, self.data_timeframe]),
            widgets.HBox([self.data_start_date, self.data_end_date]),
            widgets.HBox([self.fetch_data_btn, self.load_data_btn]),
            self.data_progress,
            self.data_status,
            self.data_info
        ])
        
        return data_box
    
    def create_optimization_section(self):
        """Optimizasyon UI bileşenleri"""
        print("\n🎯 PARAMETRE OPTİMİZASYONU")
        
        # Optimizasyon parametreleri
        self.opt_coins = widgets.Text(
            value='BTCUSDT',
            placeholder='BTCUSDT,ETHUSDT,ADAUSDT',
            description='🪙 Coin Çiftleri:',
            style={'description_width': 'initial'}
        )
        
        self.opt_timeframe = widgets.Dropdown(
            options=[('1 Dakika', '1m'), ('5 Dakika', '5m'), ('15 Dakika', '15m'), 
                    ('30 Dakika', '30m'), ('1 Saat', '1h'), ('4 Saat', '4h'), 
                    ('12 Saat', '12h'), ('1 Gün', '1d')],
            value='5m',
            description='⏰ Zaman Dilimi:'
        )
        
        # Optimizasyon tarih aralığı - default 30 gün
        opt_end = datetime.now()
        opt_start = opt_end - timedelta(days=30)
        
        self.opt_start_date = widgets.DatePicker(
            value=opt_start.date(),
            description='📅 Başlangıç:'
        )
        
        self.opt_end_date = widgets.DatePicker(
            value=opt_end.date(),
            description='📅 Bitiş:'
        )
        
        self.initial_balance = widgets.FloatText(
            value=200,
            description='💰 Başlangıç Bakiyesi (USDT):',
            style={'description_width': 'initial'}
        )
        
        # Parametre aralıkları
        self.leverage_range = widgets.Text(
            value='5-55-5',
            description='⚡ Kaldıraç (Min-Max-Adım):',
            style={'description_width': 'initial'}
        )
        
        self.profit_range = widgets.Text(
            value='1-20-1',
            description='💹 Kar/Zarar % (Min-Max-Adım):',
            style={'description_width': 'initial'}
        )
        
        self.multiplier_range = widgets.Text(
            value='1.2-5-0.1',
            description='🚀 Bahis Çarpanı (Min-Max-Adım):',
            style={'description_width': 'initial'}
        )
        
        self.direction_options = widgets.Dropdown(
            options=[('Her İkisi (LONG + SHORT)', 'both'), 
                    ('Sadece LONG', 'long'), 
                    ('Sadece SHORT', 'short')],
            value='both',
            description='📊 Test Edilecek Yönler:'
        )
        
        self.min_bet_size = widgets.FloatText(
            value=10,
            description='⚖️ Bahis Alt Sınırı (USDT):',
            style={'description_width': 'initial'}
        )
        
        self.max_trades = widgets.IntText(
            value=1000000,
            description='🎯 Maksimum İşlem Sayısı:',
            style={'description_width': 'initial'}
        )
        
        # Butonlar
        self.optimize_btn = widgets.Button(
            description='🎯 Optimizasyonu Başlat',
            button_style='warning',
            layout=widgets.Layout(width='200px')
        )
        self.optimize_btn.on_click(self.start_optimization)
        
        self.reopt_btn = widgets.Button(
            description='🔄 Yeniden Optimizasyon',
            button_style='info',
            layout=widgets.Layout(width='200px'),
            disabled=True
        )
        self.reopt_btn.on_click(self.re_optimize)
        
        # Progress
        self.opt_progress = widgets.IntProgress(
            value=0,
            min=0,
            max=100,
            description='İlerleme:',
            bar_style='warning'
        )
        
        self.opt_status = widgets.HTML(value="")
        
        opt_box = widgets.VBox([
            widgets.HTML("<h3>🎯 Parametre Optimizasyonu</h3>"),
            widgets.HTML("🚀 Multi-Coin Otomatik Optimizasyon: 1-3 coin çifti ile paralel backtest"),
            widgets.HBox([self.opt_coins, self.opt_timeframe]),
            widgets.HBox([self.opt_start_date, self.opt_end_date]),
            widgets.HBox([self.initial_balance, self.min_bet_size]),
            widgets.HBox([self.leverage_range, self.profit_range]),
            widgets.HBox([self.multiplier_range, self.direction_options]),
            self.max_trades,
            widgets.HBox([self.optimize_btn, self.reopt_btn]),
            self.opt_progress,
            self.opt_status
        ])
        
        return opt_box
    
    def create_validation_section(self):
        """Validation UI bileşenleri"""
        self.validation_method = widgets.Dropdown(
            options=[('Validasyon Yok (Hızlı)', 'none'),
                    ('Basit Train/Test Split (%75/%25)', 'simple'),
                    ('Walk-Forward Analysis', 'walkforward'),
                    ('Cross-Validation (3-Fold)', 'crossval')],
            value='simple',
            description='🔬 Validasyon Yöntemi:'
        )
        
        self.validation_criteria = widgets.Dropdown(
            options=[('ROI (Return on Investment)', 'roi'),
                    ('Sharpe Ratio (Risk-Adjusted)', 'sharpe'),
                    ('Kompozit Skor (ROI + Sharpe)', 'composite'),
                    ('Tutarlılık (Low Variance)', 'consistency')],
            value='roi',
            description='📊 Validasyon Kriteri:'
        )
        
        self.top_combinations = widgets.IntText(
            value=100,
            description='🎯 En İyi N Kombinasyon:',
            style={'description_width': 'initial'}
        )
        
        self.overfitting_threshold = widgets.IntText(
            value=50,
            description='⚖️ Overfitting Eşiği (%):',
            style={'description_width': 'initial'}
        )
        
        # Walk-forward parametreleri
        self.window_size = widgets.IntText(
            value=25,
            description='📊 Pencere Boyutu (%):',
            style={'description_width': 'initial'}
        )
        
        self.step_size = widgets.IntText(
            value=10,
            description='⏩ Kaydırma Adımı (%):',
            style={'description_width': 'initial'}
        )
        
        self.revalidation_btn = widgets.Button(
            description='🧪 Sadece Validation Yeniden Çalıştır',
            button_style='danger',
            layout=widgets.Layout(width='250px'),
            disabled=True
        )
        self.revalidation_btn.on_click(self.re_run_validation)
        
        self.validation_progress = widgets.IntProgress(
            value=0,
            min=0,
            max=100,
            description='Validation:',
            bar_style='danger'
        )
        
        self.validation_status = widgets.HTML(value="")
        
        validation_box = widgets.VBox([
            widgets.HTML("<h3>🧠 Gelişmiş Validation Sistemi</h3>"),
            widgets.HTML("💡 Tam Özellikli Validation: Walk-Forward, Cross-Validation, Gerçek Sharpe Ratio"),
            widgets.HBox([self.validation_method, self.validation_criteria]),
            widgets.HBox([self.top_combinations, self.overfitting_threshold]),
            widgets.HBox([self.window_size, self.step_size]),
            self.revalidation_btn,
            self.validation_progress,
            self.validation_status
        ])
        
        return validation_box
    
    def parse_range(self, range_str):
        """Aralık string'ini parse et"""
        try:
            parts = [float(x.strip()) for x in range_str.split('-')]
            if len(parts) != 3:
                raise ValueError(f"Geçersiz format: {range_str}")
            return {'min': parts[0], 'max': parts[1], 'step': parts[2]}
        except Exception as e:
            raise ValueError(f"Aralık parse hatası: {e}")
    
    def generate_values(self, range_dict):
        """Aralıktan değerler üret"""
        values = []
        current = range_dict['min']
        while current <= range_dict['max']:
            values.append(round(current, 3))
            current += range_dict['step']
        return values
    
    def calculate_initial_bet(self, min_bet_size, leverage):
        """İlk bahis miktarını hesapla"""
        return max(min_bet_size / leverage, 0.1)
    
    def fetch_and_save_data(self, btn):
        """Binance'den veri çek ve kaydet"""
        if self.running:
            self.data_status.value = "⚠️ İşlem zaten çalışıyor!"
            return
            
        self.running = True
        btn.disabled = True
        
        try:
            # Parametreleri al
            coins_input = self.data_coins.value.strip().upper()
            coins = [c.strip() for c in coins_input.split(',') if c.strip()]
            
            if not coins:
                raise ValueError("En az 1 coin çifti girin!")
            
            timeframe = self.data_timeframe.value
            start_date = self.data_start_date.value.strftime('%Y-%m-%d')
            end_date = self.data_end_date.value.strftime('%Y-%m-%d')
            
            self.data_status.value = "⏳ Veriler çekiliyor..."
            self.data_progress.value = 0
            
            fetched_data = {}
            
            for i, coin in enumerate(coins):
                try:
                    self.data_status.value = f"⏳ {coin} verisi çekiliyor..."
                    
                    data = self.fetch_data_by_date_range(coin, timeframe, start_date, end_date)
                    if not data or len(data) == 0:
                        raise ValueError(f"{coin} verisi çekilemedi")
                    
                    fetched_data[coin] = data
                    
                    progress = ((i + 1) / len(coins)) * 100
                    self.data_progress.value = int(progress)
                    self.data_status.value = f"✅ {i+1}/{len(coins)} coin tamamlandı"
                    
                except Exception as e:
                    self.data_status.value = f"❌ {coin} hatası: {str(e)}"
                    return
            
            # Veriyi kaydet
            self.saved_data = fetched_data
            
            # Metadata oluştur
            metadata = {
                'coins': coins,
                'timeframe': timeframe,
                'startDate': start_date,
                'endDate': end_date,
                'totalCandles': len(list(fetched_data.values())[0]),
                'fetchDate': datetime.now().isoformat(),
                'version': "4.0"
            }
            
            # Bilgileri göster
            self.show_loaded_data_info(metadata)
            
            # Form verilerini güncelle
            self.opt_coins.value = coins_input
            self.opt_timeframe.value = timeframe
            
            self.data_status.value = f"✅ Veriler başarıyla kaydedildi: {len(coins)} coin, {len(list(fetched_data.values())[0])} mum"
            
        except Exception as e:
            self.data_status.value = f"❌ Veri çekme hatası: {str(e)}"
            
        finally:
            self.running = False
            btn.disabled = False
            self.data_progress.value = 100
    
    def fetch_data_by_date_range(self, symbol, interval, start_date, end_date):
        """Tarih aralığına göre veri çek"""
        start_time = int(datetime.strptime(start_date + ' 00:00:00', '%Y-%m-%d %H:%M:%S').timestamp() * 1000)
        end_time = int(datetime.strptime(end_date + ' 23:59:59', '%Y-%m-%d %H:%M:%S').timestamp() * 1000)
        
        return self.fetch_large_dataset(symbol, interval, start_time, end_time)
    
    def fetch_large_dataset(self, symbol, interval, start_time, end_time):
        """Büyük veri setini batch'ler halinde çek"""
        max_per_request = 1000
        all_data = []
        current_end_time = end_time
        
        while current_end_time > start_time:
            try:
                batch = self.fetch_binance_data(symbol, interval, max_per_request, current_end_time)
                if not batch:
                    break
                
                # Tarih aralığında filtrele
                filtered_batch = [candle for candle in batch 
                                if start_time <= int(candle[0]) <= end_time]
                
                if filtered_batch:
                    all_data = filtered_batch + all_data
                    if int(filtered_batch[0][0]) <= start_time:
                        break
                
                current_end_time = int(batch[0][0]) - 1
                time.sleep(0.1)  # Rate limiting
                
            except Exception as e:
                print(f"❌ {symbol} batch hatası: {e}")
                break
        
        # Tarihe göre sırala
        all_data.sort(key=lambda x: int(x[0]))
        return all_data
    
    def fetch_binance_data(self, symbol, interval, limit, end_time=None):
        """Binance API'den veri çek"""
        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
        if end_time:
            url += f"&endTime={end_time}"
        
        # Proxy listesi
        proxies = [
            f"https://api.codetabs.com/v1/proxy?quest={requests.utils.quote(url)}",
            f"https://api.allorigins.win/raw?url={requests.utils.quote(url)}",
            f"https://corsproxy.io/?{requests.utils.quote(url)}"
        ]
        
        for i, proxy_url in enumerate(proxies):
            try:
                response = requests.get(proxy_url, timeout=30)
                if response.status_code == 200:
                    data = response.json()
                    
                    # Veri formatını kontrol et
                    if isinstance(data, list):
                        return data
                    
                    # Proxy wrapper kontrolü
                    for key in ['data', 'contents', 'response', 'result']:
                        if key in data and isinstance(data[key], list):
                            return data[key]
                    
                    raise ValueError(f"Geçersiz veri formatı proxy {i+1}")
                    
            except Exception as e:
                print(f"Proxy {i+1} hatası: {e}")
                if i == len(proxies) - 1:
                    raise Exception(f"Tüm proxyler başarısız: {e}")
        
        return None
    
    def show_loaded_data_info(self, metadata):
        """Yüklenen veri bilgilerini göster"""
        info_html = f"""
        <div style='background: linear-gradient(135deg, rgba(139,92,246,0.15), rgba(124,58,237,0.1)); 
                    border: 2px solid rgba(139,92,246,0.3); border-radius: 10px; padding: 15px; margin: 10px 0;'>
            <strong>📊 Yüklenen Veri Bilgileri:</strong><br>
            • <strong>Coin Çiftleri:</strong> {', '.join(metadata.get('coins', []))}<br>
            • <strong>Zaman Dilimi:</strong> {metadata.get('timeframe', 'Bilinmiyor')}<br>
            • <strong>Tarih Aralığı:</strong> {metadata.get('startDate', '')} - {metadata.get('endDate', '')}<br>
            • <strong>Toplam Mum:</strong> {metadata.get('totalCandles', 0):,}<br>
            • <strong>Çekilme Tarihi:</strong> {metadata.get('fetchDate', 'Bilinmiyor')[:19]}
        </div>
        """
        self.data_info.value = info_html
    
    def start_optimization(self, btn):
        """Optimizasyonu başlat"""
        if self.running:
            self.opt_status.value = "⚠️ Optimizasyon zaten çalışıyor!"
            return
        
        try:
            # Parametreleri al ve validate et
            coins_input = self.opt_coins.value.strip().upper()
            coins = [c.strip() for c in coins_input.split(',') if c.strip()]
            
            if not coins or len(coins) > 3:
                raise ValueError("1-3 coin çifti girin!")
            
            # Veri kontrolü
            has_saved_data = bool(self.saved_data)
            has_current_data = bool(self.data)
            
            use_saved_data = has_saved_data
            fetch_data = not has_saved_data and not has_current_data
            
            self.run_optimization(coins, fetch_data, use_saved_data)
            
        except Exception as e:
            self.opt_status.value = f"❌ Optimizasyon hatası: {str(e)}"
    
    def re_optimize(self, btn):
        """Mevcut verilerle yeniden optimizasyon"""
        if self.running:
            self.opt_status.value = "⚠️ Optimizasyon zaten çalışıyor!"
            return
        
        try:
            coins_input = self.opt_coins.value.strip().upper()
            coins = [c.strip() for c in coins_input.split(',') if c.strip()]
            
            if not coins or len(coins) > 3:
                raise ValueError("1-3 coin çifti girin!")
            
            if self.saved_data:
                self.run_optimization(coins, False, True)
            elif self.data:
                self.run_optimization(coins, False, False)
            else:
                raise ValueError("Mevcut veri yok! Önce veri çekin.")
                
        except Exception as e:
            self.opt_status.value = f"❌ Re-optimizasyon hatası: {str(e)}"
    
    def run_optimization(self, coins, fetch_data, use_saved_data=False):
        """Ana optimizasyon fonksiyonu"""
        self.running = True
        self.optimize_btn.disabled = True
        self.reopt_btn.disabled = True
        
        try:
            # Parametreleri hazırla
            timeframe = self.opt_timeframe.value
            start_date = self.opt_start_date.value.strftime('%Y-%m-%d')
            end_date = self.opt_end_date.value.strftime('%Y-%m-%d')
            initial_balance = self.initial_balance.value
            max_trades = self.max_trades.value
            min_bet_size = self.min_bet_size.value
            
            leverage_range = self.parse_range(self.leverage_range.value)
            profit_range = self.parse_range(self.profit_range.value)
            multiplier_range = self.parse_range(self.multiplier_range.value)
            direction_options = self.direction_options.value
            
            self.params = {
                'coins': coins, 'timeframe': timeframe, 'startDate': start_date, 
                'endDate': end_date, 'initialBalance': initial_balance, 
                'maxTrades': max_trades, 'minBetSize': min_bet_size,
                'leverageRange': leverage_range, 'profitRange': profit_range,
                'multiplierRange': multiplier_range, 'directionOptions': direction_options
            }
            
            self.opt_status.value = "⏳ Veriler hazırlanıyor..."
            
            # Veri yönetimi
            if use_saved_data and self.saved_data:
                self.data = self.filter_data_by_date_range(self.saved_data, start_date, end_date)
                self.original_data = self.data.copy()
            elif fetch_data:
                self.opt_status.value = "⏳ API'den veriler çekiliyor..."
                self.data = {}
                for coin in coins:
                    self.data[coin] = self.fetch_data_by_date_range(coin, timeframe, start_date, end_date)
                    if not self.data[coin]:
                        raise ValueError(f"{coin} verisi çekilemedi")
                self.original_data = self.data.copy()
            else:
                self.data = self.filter_data_by_date_range(self.data, start_date, end_date)
                self.original_data = self.data.copy()
            
            # Veri kontrolü
            for coin in coins:
                if coin not in self.data or not self.data[coin]:
                    raise ValueError(f"{coin} için veri bulunamadı")
            
            self.opt_status.value = "⏳ Kombinasyonlar test ediliyor..."
            
            # Kombinasyonları oluştur
            leverage_values = self.generate_values(leverage_range)
            profit_values = self.generate_values(profit_range)
            multiplier_values = self.generate_values(multiplier_range)
            directions = ['long', 'short'] if direction_options == 'both' else [direction_options]
            
            total_combinations = len(leverage_values) * len(profit_values) * len(multiplier_values) * len(directions)
            self.opt_progress.max = total_combinations
            self.opt_progress.value = 0
            
            print(f"🎯 Toplam {total_combinations:,} kombinasyon test edilecek...")
            
            # Training sonuçları
            self.training_results = []
            combination_index = 0
            
            for leverage in leverage_values:
                for profit_percent in profit_values:
                    for multiplier in multiplier_values:
                        for direction in directions:
                            combination_index += 1
                            
                            initial_bet = self.calculate_initial_bet(min_bet_size, leverage)
                            
                            # Test parametreleri
                            test_params = {
                                'leverage': leverage,
                                'profitPercent': profit_percent,
                                'multiplier': multiplier,
                                'direction': direction,
                                'initialBalance': initial_balance,
                                'initialBet': initial_bet,
                                'maxTrades': max_trades,
                                'minBetSize': min_bet_size,
                                'coins': coins,
                                'index': combination_index
                            }
                            
                            # Kombinasyonu test et
                            result = self.test_multi_coin_combination(test_params)
                            if result:
                                self.training_results.append(result)
                            
                            # Progress güncelle
                            self.opt_progress.value = combination_index
                            if combination_index % 100 == 0:
                                progress_pct = (combination_index / total_combinations) * 100
                                self.opt_status.value = f"⏳ {combination_index:,} / {total_combinations:,} test edildi ({progress_pct:.1f}%)"
            
            # Training sonuçlarını sırala
            self.training_results.sort(key=lambda x: x.get('roi', 0), reverse=True)
            print(f"✅ Training tamamlandı: {len(self.training_results)} sonuç")
            
            # Validation
            validation_method = self.validation_method.value
            if validation_method != 'none':
                self.opt_status.value = "⏳ Validation yapılıyor..."
                top_n = self.top_combinations.value
                top_results = self.training_results[:top_n]
                
                validated_results = self.run_advanced_validation(top_results, coins, self.params, validation_method)
                validated_results.sort(key=lambda x: x.get('validationScore', 0), reverse=True)
                
                remaining_results = self.training_results[top_n:]
                for result in remaining_results:
                    result.update({
                        'trainingROI': result.get('roi', 0),
                        'validationROI': None,
                        'sharpeRatio': None,
                        'roiDifference': None,
                        'validationScore': 0,
                        'overfitting': False
                    })
                
                self.results = validated_results + remaining_results
            else:
                self.results = []
                for result in self.training_results:
                    result.update({
                        'trainingROI': result.get('roi', 0),
                        












                        'validationROI': result.get('roi', 0),
                        'sharpeRatio': 0,
                        'roiDifference': 0,
                        'validationScore': result.get('roi', 0),
                        'overfitting': False
                    })
                    self.results.append(result)
            
            # Sonuçları göster
            self.display_results()
            
            # UI güncellemeleri
            self.reopt_btn.disabled = False
            self.revalidation_btn.disabled = False
            display(self.validation_section)
            
            self.opt_status.value = f"✅ Optimizasyon tamamlandı: {len(self.results)} sonuç"
            
        except Exception as e:
            self.opt_status.value = f"❌ Optimizasyon hatası: {str(e)}"
            print(f"Detaylı hata: {e}")
            
        finally:
            self.running = False
            self.optimize_btn.disabled = False
            self.reopt_btn.disabled = False
            self.opt_progress.value = self.opt_progress.max
    
    def filter_data_by_date_range(self, data_source, start_date, end_date):
        """Veriyi tarih aralığına göre filtrele"""
        start_time = int(datetime.strptime(start_date + ' 00:00:00', '%Y-%m-%d %H:%M:%S').timestamp() * 1000)
        end_time = int(datetime.strptime(end_date + ' 23:59:59', '%Y-%m-%d %H:%M:%S').timestamp() * 1000)
        
        filtered = {}
        for coin, data in data_source.items():
            if not data:
                continue
            filtered[coin] = [
                candle for candle in data 
                if start_time <= int(candle[0]) <= end_time
            ]
        return filtered
    
    def test_multi_coin_combination(self, params):
        """Multi-coin kombinasyon testi"""
        try:
            total_initial_balance = 0
            total_final_balance = 0
            total_trades = 0
            total_wins = 0
            total_profit = 0
            total_loss = 0
            max_consecutive_losses = 0
            max_drawdown = 0
            exceeds_initial_balance = False
            all_returns = []
            
            for coin in params['coins']:
                if coin not in self.data or not self.data[coin]:
                    continue
                    
                state = {
                    'balance': params['initialBalance'],
                    'initialBalance': params['initialBalance'],
                    'currentBet': params['initialBet'],
                    'peakBalance': params['initialBalance'],
                    'maxDrawdown': 0,
                    'totalTrades': 0,
                    'winTrades': 0,
                    'consecutiveLosses': 0,
                    'maxConsecutiveLosses': 0,
                    'totalProfit': 0,
                    'totalLoss': 0,
                    'position': {'isOpen': False, 'entryPrice': 0, 'betAmount': 0},
                    'betExceededCapital': False,
                    'returns': []
                }
                
                last_balance = params['initialBalance']
                
                for i, candle in enumerate(self.data[coin]):
                    if state['totalTrades'] >= params['maxTrades']:
                        break
                        
                    if not self.process_candle(candle, state, params):
                        break
                        
                    self.update_drawdown(state)
                    
                    # Return hesaplama
                    if i > 0 and last_balance > 0:
                        return_val = (state['balance'] - last_balance) / last_balance
                        state['returns'].append(return_val)
                    last_balance = state['balance']
                
                # Toplamları güncelle
                total_initial_balance += params['initialBalance']
                total_final_balance += state['balance']
                total_trades += state['totalTrades']
                total_wins += state['winTrades']
                total_profit += state['totalProfit']
                total_loss += state['totalLoss']
                max_consecutive_losses = max(max_consecutive_losses, state['maxConsecutiveLosses'])
                max_drawdown = max(max_drawdown, state['maxDrawdown'])
                
                if state['betExceededCapital']:
                    exceeds_initial_balance = True
                
                all_returns.extend(state['returns'])
            
            # Sonuç hesaplama
            roi = total_final_balance / total_initial_balance if total_initial_balance > 0 else 0
            win_rate = (total_wins / total_trades * 100) if total_trades > 0 else 0
            profit_factor = (total_profit / total_loss) if total_loss > 0 else 0
            
            return {
                'leverage': params['leverage'],
                'profitPercent': params['profitPercent'],
                'multiplier': params['multiplier'],
                'direction': params['direction'],
                'initialBet': params['initialBet'],
                'roi': roi,
                'finalBalance': total_final_balance,
                'maxConsecutiveLosses': max_consecutive_losses,
                'totalTrades': total_trades,
                'maxDrawdown': max_drawdown,
                'winRate': win_rate,
                'profitFactor': profit_factor,
                'coins': len(params['coins']),
                'exceedsInitialBalance': exceeds_initial_balance,
                'returns': all_returns
            }
            
        except Exception as e:
            print(f"❌ Multi-coin test hatası: {e}")
            return None
    
    def process_candle(self, candle, state, params):
        """Tek mum işleme"""
        try:
            timestamp, open_price, high, low, close_price = candle[:5]
            open_price, high, low, close_price = map(float, [open_price, high, low, close_price])
            
            loss_percent = params['profitPercent']
            
            if not state['position']['isOpen']:
                # Bahis kontrolü
                if state['currentBet'] > state['initialBalance']:
                    state['betExceededCapital'] = True
                
                if state['balance'] < state['currentBet'] or state['currentBet'] > state['balance'] * 0.95:
                    return False
                
                # Pozisyon aç
                state['position']['isOpen'] = True
                state['position']['entryPrice'] = open_price
                state['position']['betAmount'] = state['currentBet']
                state['balance'] -= state['currentBet']
                state['totalTrades'] += 1
                return True
            
            # Pozisyon açık - kar/zarar kontrolü
            entry_price = state['position']['entryPrice']
            
            if params['direction'] == 'long':
                profit_target = entry_price * (1 + params['profitPercent'] / 100)
                stop_loss_price = entry_price * (1 - loss_percent / 100)
                
                if high >= profit_target:
                    # Kar al
                    profit = state['currentBet'] * params['leverage'] * (params['profitPercent'] / 100)
                    state['balance'] += state['currentBet'] + profit
                    state['totalProfit'] += profit
                    state['winTrades'] += 1
                    state['consecutiveLosses'] = 0
                    state['currentBet'] = params['initialBet']
                    state['position']['isOpen'] = False
                    return True
                
                if low <= stop_loss_price:
                    # Zarar kes
                    state['totalLoss'] += state['currentBet']
                    state['consecutiveLosses'] += 1
                    state['maxConsecutiveLosses'] = max(state['maxConsecutiveLosses'], state['consecutiveLosses'])
                    state['currentBet'] = min(state['currentBet'] * params['multiplier'], state['balance'] * 0.95)
                    state['position']['isOpen'] = False
                    return True
            
            else:  # short
                profit_target = entry_price * (1 - params['profitPercent'] / 100)
                stop_loss_price = entry_price * (1 + loss_percent / 100)
                
                if low <= profit_target:
                    # Kar al
                    profit = state['currentBet'] * params['leverage'] * (params['profitPercent'] / 100)
                    state['balance'] += state['currentBet'] + profit
                    state['totalProfit'] += profit
                    state['winTrades'] += 1
                    state['consecutiveLosses'] = 0
                    state['currentBet'] = params['initialBet']
                    state['position']['isOpen'] = False
                    return True
                
                if high >= stop_loss_price:
                    # Zarar kes
                    state['totalLoss'] += state['currentBet']
                    state['consecutiveLosses'] += 1
                    state['maxConsecutiveLosses'] = max(state['maxConsecutiveLosses'], state['consecutiveLosses'])
                    state['currentBet'] = min(state['currentBet'] * params['multiplier'], state['balance'] * 0.95)
                    state['position']['isOpen'] = False
                    return True
            
            return True
            
        except Exception as e:
            print(f"❌ Candle işleme hatası: {e}")
            return False
    
    def update_drawdown(self, state):
        """Drawdown güncelle"""
        if state['balance'] > state['peakBalance']:
            state['peakBalance'] = state['balance']
        
        if state['peakBalance'] > 0:
            current_drawdown = (state['peakBalance'] - state['balance']) / state['peakBalance'] * 100
            state['maxDrawdown'] = max(state['maxDrawdown'], current_drawdown)
    
    def run_advanced_validation(self, top_results, coins, params, method):
        """Gelişmiş validation metodları"""
        criteria = self.validation_criteria.value
        validated_results = []
        
        total_validations = len(top_results)
        self.validation_progress.max = total_validations
        self.validation_progress.value = 0
        
        for i, result in enumerate(top_results):
            validation_scores = []
            sharpe_ratios = []
            
            if method == 'simple':
                # 75/25 split
                validation_data = {}
                for coin in coins:
                    source_data = self.original_data.get(coin, self.data.get(coin, []))
                    split_data = self.split_data_for_validation(source_data, 0.75)
                    validation_data[coin] = split_data['validation']
                
                # Geçici olarak validation data kullan
                temp_data = self.data.copy()
                self.data = validation_data
                
                validation_result = self.test_single_combination_for_validation(result, coins, params)
                
                # Orijinal datayı geri yükle
                self.data = temp_data
                
                if validation_result:
                    validation_scores.append(validation_result['roi'])
                    sharpe_ratios.append(self.calculate_sharpe_ratio(validation_result.get('returns', [])))
            
            elif method == 'walkforward':
                # Walk-Forward Analysis
                window_size = self.window_size.value / 100
                step_size = self.step_size.value / 100
                
                for coin in coins:
                    source_data = self.original_data.get(coin, self.data.get(coin, []))
                    data_length = len(source_data)
                    window_length = int(data_length * window_size)
                    step_length = int(data_length * step_size)
                    
                    window_count = 0
                    max_windows = 10  # Memory management
                    
                    for start in range(0, data_length - window_length, step_length):
                        if window_count >= max_windows:
                            break
                            
                        end = start + window_length
                        train_end = start + int(window_length * 0.8)
                        
                        validation_window = source_data[train_end:end]
                        if len(validation_window) < 10:
                            continue
                        
                        # Geçici data assignment
                        temp_coin_data = self.data.get(coin)
                        self.data[coin] = validation_window
                        
                        window_result = self.test_single_combination_for_validation(result, [coin], params)
                        
                        # Restore
                        if temp_coin_data:
                            self.data[coin] = temp_coin_data
                        
                        if window_result:
                            validation_scores.append(window_result['roi'])
                            sharpe_ratios.append(self.calculate_sharpe_ratio(window_result.get('returns', [])))
                        
                        window_count += 1
            
            elif method == 'crossval':
                # 3-Fold Cross Validation
                for fold in range(3):
                    fold_data = {}
                    
                    for coin in coins:
                        data = self.original_data.get(coin, self.data.get(coin, []))
                        fold_size = len(data) // 3
                        test_start = fold * fold_size
                        test_end = len(data) if fold == 2 else (fold + 1) * fold_size
                        
                        fold_data[coin] = data[test_start:test_end]
                    
                    temp_data = self.data.copy()
                    self.data = fold_data
                    
                    fold_result = self.test_single_combination_for_validation(result, coins, params)
                    
                    self.data = temp_data
                    
                    if fold_result:
                        validation_scores.append(fold_result['roi'])
                        sharpe_ratios.append(self.calculate_sharpe_ratio(fold_result.get('returns', [])))
            
            # Final metrics calculation
            avg_validation_roi = sum(validation_scores) / len(validation_scores) if validation_scores else 0
            avg_sharpe_ratio = sum(sharpe_ratios) / len(sharpe_ratios) if sharpe_ratios else 0
            
            roi_difference = 0
            if result.get('roi', 0) > 0:
                roi_difference = abs(result['roi'] - avg_validation_roi) / result['roi'] * 100
            
            validation_score = self.calculate_advanced_validation_score(
                result.get('roi', 0), avg_validation_roi, avg_sharpe_ratio, validation_scores, criteria
            )
            
            overfitting_threshold = self.overfitting_threshold.value
            
            validated_result = result.copy()
            validated_result.update({
                'trainingROI': result.get('roi', 0),
                'validationROI': avg_validation_roi,
                'sharpeRatio': avg_sharpe_ratio,
                'roiDifference': roi_difference,
                'validationScore': validation_score,
                'overfitting': roi_difference > overfitting_threshold,
                'consistencyScore': 1 / (1 + self.calculate_standard_deviation(validation_scores)) if len(validation_scores) > 1 else 1
            })
            
            validated_results.append(validated_result)
            
            # Progress update
            self.validation_progress.value = i + 1
            if i % 10 == 0:
                progress_pct = ((i + 1) / total_validations) * 100
                self.validation_status.value = f"⏳ {method}: {i+1}/{total_validations} ({progress_pct:.1f}%)"
        
        return validated_results
    
    def test_single_combination_for_validation(self, result, coins, params):
        """Validation için tek kombinasyon testi"""
        try:
            test_params = {
                'leverage': result['leverage'],
                'profitPercent': result['profitPercent'],
                'multiplier': result['multiplier'],
                'direction': result['direction'],
                'initialBalance': params['initialBalance'],
                'initialBet': result['initialBet'],
                'maxTrades': params['maxTrades'],
                'minBetSize': params['minBetSize'],
                'coins': coins
            }
            
            return self.test_multi_coin_combination(test_params)
            
        except Exception as e:
            print(f"❌ Single combination validation hatası: {e}")
            return None
    
    def split_data_for_validation(self, data, split_ratio=0.75):
        """Veriyi training/validation olarak böl"""
        split_index = int(len(data) * split_ratio)
        return {
            'training': data[:split_index],
            'validation': data[split_index:]
        }
    
    def calculate_sharpe_ratio(self, returns, risk_free_rate=0.02):
        """Sharpe ratio hesapla"""
        if not returns or len(returns) < 2:
            return 0
        
        avg_return = sum(returns) / len(returns)
        annualized_return = avg_return * 252  # Daily returns assumption
        excess_return = annualized_return - risk_free_rate
        
        variance = sum((ret - avg_return) ** 2 for ret in returns) / len(returns)
        volatility = (variance * 252) ** 0.5
        
        return excess_return / volatility if volatility > 0 else 0
    
    def calculate_standard_deviation(self, values):
        """Standart sapma hesapla"""
        if len(values) < 2:
            return 0
        
        mean = sum(values) / len(values)
        variance = sum((val - mean) ** 2 for val in values) / len(values)
        return variance ** 0.5
    
    def calculate_advanced_validation_score(self, training_roi, validation_roi, sharpe_ratio, validation_scores, criteria):
        """Gelişmiş validation skoru hesapla"""
        consistency = 1 / (1 + self.calculate_standard_deviation(validation_scores)) if len(validation_scores) > 1 else 1
        
        if criteria == 'roi':
            return validation_roi
        elif criteria == 'sharpe':
            return sharpe_ratio
        elif criteria == 'composite':
            return validation_roi * 0.5 + sharpe_ratio * 0.3 + consistency * 0.2
        elif criteria == 'consistency':
            return validation_roi * consistency
        else:
            return validation_roi
    
    def re_run_validation(self, btn):
        """Sadece validation'ı yeniden çalıştır"""
        if self.running:
            self.validation_status.value = "⚠️ İşlem zaten çalışıyor!"
            return
        
        if not self.training_results:
            self.validation_status.value = "⚠️ Önce kombinasyon testlerini çalıştırın!"
            return
        
        self.running = True
        btn.disabled = True
        
        try:
            self.validation_status.value = "⏳ Validation başlatılıyor..."
            
            validation_method = self.validation_method.value
            if validation_method == 'none':
                self.results = []
                for result in self.training_results:
                    result.update({
                        'trainingROI': result.get('roi', 0),
                        'validationROI': result.get('roi', 0),
                        'sharpeRatio': 0,
                        'roiDifference': 0,
                        'validationScore': result.get('roi', 0),
                        'overfitting': False
                    })
                    self.results.append(result)
            else:
                top_n = self.top_combinations.value
                top_results = self.training_results[:top_n]
                
                validated_results = self.run_advanced_validation(
                    top_results, self.params['coins'], self.params, validation_method
                )
                validated_results.sort(key=lambda x: x.get('validationScore', 0), reverse=True)
                
                remaining_results = self.training_results[top_n:]
                for result in remaining_results:
                    result.update({
                        'trainingROI': result.get('roi', 0),
                        'validationROI': None,
                        'sharpeRatio': None,
                        'roiDifference': None,
                        'validationScore': 0,
                        'overfitting': False
                    })
                
                self.results = validated_results + remaining_results
            
            self.display_results()
            self.validation_status.value = f"✅ {validation_method} validation tamamlandı"
            
        except Exception as e:
            self.validation_status.value = f"❌ Validation hatası: {str(e)}"
            
        finally:
            self.running = False
            btn.disabled = False
    
    def display_results(self):
        """Sonuçları görüntüle"""
        if not self.results:
            return
        
        with self.results_output:
            clear_output(wait=True)
            
            print("\n" + "="*100)
            print("🏆 GELİŞMİŞ VALİDATİON İLE EN İYİ KOMBİNASYONLAR")
            print("="*100)
            
            # Validation açıklaması
            validation_method = self.validation_method.value
            method_names = {
                'none': 'Validasyon Yok',
                'simple': 'Basit Train/Test Split',
                'walkforward': 'Walk-Forward Analysis',
                'crossval': 'Cross-Validation (3-Fold)'
            }
            
            print(f"🔬 Validation Yöntemi: {method_names.get(validation_method, validation_method)}")
            print("💡 Validation Açıklaması:")
            print("• Training ROI: İlk eğitim verisi ile test")
            print("• Validation ROI: Validation verisi ile test")
            print("• Sharpe Ratio: Risk-ayarlı performans")
            print("• ROI Farkı: %50+ ise overfitting riski")
            print("• 🚨: Bahis miktarı başlangıç sermayesini aştı")
            
            # Overfitting uyarıları
            overfitted_count = sum(1 for r in self.results if r.get('overfitting', False))
            exceeds_capital_count = sum(1 for r in self.results if r.get('exceedsInitialBalance', False))
            
            if overfitted_count > 0 or exceeds_capital_count > 0:
                print(f"\n⚠️ OVERFITTING VE RİSK UYARILARI!")
                print(f"• {overfitted_count} kombinasyon overfitting riski taşıyor")
                print(f"• {exceeds_capital_count} kombinasyon bahis-sermaye aşımı yaşıyor")
                print(f"• Training ve Validation ROI farkı >{self.overfitting_threshold.value}%")
                print("• Tavsiye: Yüksek validation score, düşük overfitting riski olan kombinasyonları tercih edin")
            
            # Sonuçları DataFrame'e çevir
            df_data = []
            for i, result in enumerate(self.results[:200]):  # İlk 200 sonuç
                direction_icon = '📈' if result.get('direction') == 'long' else '📉'
                overfitting_icon = '⚠️' if result.get('overfitting', False) else '✅'
                bet_warning_icon = '🚨' if result.get('exceedsInitialBalance', False) else '✅'
                
                df_data.append({
                    '#': i + 1,
                    'Kaldıraç': f"{result.get('leverage', 0)}x",
                    'Kar%': f"%{result.get('profitPercent', 0)}",
                    'Çarpan': f"{result.get('multiplier', 0)}x",
                    'Yön': direction_icon,
                    'İlk Bahis': f"{result.get('initialBet', 0):.2f}",
                    'Training ROI': f"{result.get('trainingROI', 0):.3f}x",
                    'Validation ROI': f"{result.get('validationROI', 0):.3f}x" if result.get('validationROI') else 'N/A',
                    'Sharpe': f"{result.get('sharpeRatio', 0):.2f}" if result.get('sharpeRatio') else 'N/A',
                    'ROI Fark%': f"{result.get('roiDifference', 0):.1f}%" if result.get('roiDifference') else 'N/A',
                    'Validation Score': f"{result.get('validationScore', 0):.3f}",
                    'Overfitting': overfitting_icon,
                    'Bahis Uyarısı': bet_warning_icon
                })
            
            df = pd.DataFrame(df_data)
            
            # Renklendirme için stil
            def highlight_rows(row):
                styles = [''] * len(row)
                
                # İlk 3 sırayı altın, gümüş, bronz yap
                if row.name < 3:
                    colors = ['gold', 'silver', '#CD7F32']  # Bronze
                    styles = [f'background-color: {colors[row.name]}; color: black; font-weight: bold'] * len(row)
                
                # Overfitting olanları kırmızı yap
                elif '⚠️' in str(row['Overfitting']):
                    styles = ['background-color: rgba(248,113,113,0.3)'] * len(row)
                
                return styles
            
            styled_df = df.style.apply(highlight_rows, axis=1)
            display(styled_df)
            
            # Özet istatistikler
            if self.results:
                best_result = self.results[0]
                print(f"\n📊 ÖZET İSTATİSTİKLER:")
                print(f"• Toplam Test Edilen Kombinasyon: {len(self.training_results):,}")
                print(f"• Validation Uygulanan Kombinasyon: {min(self.top_combinations.value, len(self.results))}")
                print(f"• En İyi Training ROI: {best_result.get('trainingROI', 0):.3f}x")
                print(f"• En İyi Validation ROI: {best_result.get('validationROI', 0):.3f}x" if best_result.get('validationROI') else "")
                print(f"• En İyi Validation Score: {best_result.get('validationScore', 0):.3f}")
                print(f"• Overfitting Riski Olan: {overfitted_count} kombinasyon")
                print(f"• Bahis Aşımı Olan: {exceeds_capital_count} kombinasyon")
            
            # Grafiksel analiz
            self.create_performance_charts()
        
        display(self.results_output)
    
    def create_performance_charts(self):
        """Performans grafiklerini oluştur"""
        if not self.results:
            return
        
        # Top 50 sonuç için grafikler
        top_50 = self.results[:50]
        
        # ROI Comparison Chart
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Training vs Validation ROI', 'Sharpe Ratio Dağılımı', 
                            'ROI Farkı (Overfitting Riski)', 'Validation Score'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                    [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # 1. Training vs Validation ROI
        training_rois = [r.get('trainingROI', 0) for r in top_50]
        validation_rois = [r.get('validationROI', 0) if r.get('validationROI') else 0 for r in top_50]
        
        fig.add_trace(
            go.Scatter(x=list(range(1, 51)), y=training_rois, 
                        name='Training ROI', line=dict(color='green')),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=list(range(1, 51)), y=validation_rois, 
                        name='Validation ROI', line=dict(color='orange')),
            row=1, col=1
        )
        
        # 2. Sharpe Ratio histogram
        sharpe_ratios = [r.get('sharpeRatio', 0) for r in top_50 if r.get('sharpeRatio')]
        if sharpe_ratios:
            fig.add_trace(
                go.Histogram(x=sharpe_ratios, name='Sharpe Ratio', nbinsx=20),
                row=1, col=2
            )
        
        # 3. ROI Farkı (Overfitting)
        roi_differences = [r.get('roiDifference', 0) for r in top_50 if r.get('roiDifference')]
        overfitting_threshold = self.overfitting_threshold.value
        
        colors = ['red' if diff > overfitting_threshold else 'green' for diff in roi_differences]
        
        fig.add_trace(
            go.Bar(x=list(range(1, len(roi_differences) + 1)), y=roi_differences,
                    name='ROI Farkı %', marker_color=colors),
            row=2, col=1
        )
        
        # Overfitting threshold line
        fig.add_hline(y=overfitting_threshold, line_dash="dash", line_color="red", 
                        annotation_text=f"Overfitting Eşiği: {overfitting_threshold}%",
                        row=2, col=1)
        
        # 4. Validation Score
        validation_scores = [r.get('validationScore', 0) for r in top_50]
        fig.add_trace(
            go.Scatter(x=list(range(1, 51)), y=validation_scores, 
                        name='Validation Score', line=dict(color='purple')),
            row=2, col=2
        )
        
        fig.update_layout(
            title="🏆 Top 50 Kombinasyon Performans Analizi",
            height=800,
            showlegend=True
        )
        
        fig.show()
        
        













        # Kaldıraç ve Yön analizi
        fig2 = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Kaldıraç vs ROI Analizi', 'Yön Bazlı Performans')
        )
        
        # Kaldıraç analizi
        leverage_data = {}
        for result in top_50:
            lev = result.get('leverage', 0)
            roi = result.get('validationROI', result.get('trainingROI', 0))
            if lev not in leverage_data:
                leverage_data[lev] = []
            leverage_data[lev].append(roi)
        
        leverages = sorted(leverage_data.keys())
        avg_rois = [sum(leverage_data[lev]) / len(leverage_data[lev]) for lev in leverages]
        
        fig2.add_trace(
            go.Scatter(x=leverages, y=avg_rois, mode='markers+lines',
                        name='Ortalama ROI', marker=dict(size=10)),
            row=1, col=1
        )
        
        # Yön analizi
        direction_data = {'long': [], 'short': []}
        for result in top_50:
            direction = result.get('direction', 'long')
            roi = result.get('validationROI', result.get('trainingROI', 0))
            if direction in direction_data:
                direction_data[direction].append(roi)
        
        for direction, rois in direction_data.items():
            if rois:
                fig2.add_trace(
                    go.Box(y=rois, name=f'{direction.upper()} ROI'),
                    row=1, col=2
                )
        
        fig2.update_layout(
            title="📊 Parametre Analizi",
            height=400
        )
        
        fig2.show()
    
    def export_results_to_json(self):
        """Sonuçları JSON olarak export et"""
        if not self.results:
            print("⚠️ Henüz sonuç yok!")
            return
        
        validation_method = self.validation_method.value
        export_data = {
            'metadata': {
                **self.meta,
                'validationMethod': validation_method,
                'overfittingProtection': validation_method != 'none',
                'betExceedsCapitalTracking': True,
                'advancedValidationFeatures': {
                    'walkForward': True,
                    'crossValidation': True,
                    'realSharpeRatio': True,
                    'consistencyScoring': True
                }
            },
            'parameters': self.params,
            'validationSettings': {
                'method': validation_method,
                'criteria': self.validation_criteria.value,
                'topCombinations': self.top_combinations.value,
                'overfittingThreshold': self.overfitting_threshold.value,
                'windowSize': self.window_size.value if validation_method == 'walkforward' else None,
                'stepSize': self.step_size.value if validation_method == 'walkforward' else None
            },
            'summary': {
                'totalResults': len(self.results),
                'totalTrainingResults': len(self.training_results),
                'bestTrainingROI': self.results[0].get('trainingROI', 0) if self.results else 0,
                'bestValidationROI': self.results[0].get('validationROI', 0) if self.results else 0,
                'bestSharpeRatio': max((r.get('sharpeRatio', 0) for r in self.results), default=0),
                'overfittedCombinations': sum(1 for r in self.results if r.get('overfitting', False)),
                'betExceedsCombinations': sum(1 for r in self.results if r.get('exceedsInitialBalance', False))
            },
            'trainingResults': self.training_results,
            'results': self.results
        }
        
        # JSON string oluştur
        json_string = json.dumps(export_data, indent=2, ensure_ascii=False)
        
        # Dosya adı oluştur
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        coins_str = '-'.join(self.params.get('coins', ['unknown']))
        filename = f"advanced_results_{coins_str}_{validation_method}_{timestamp}.json"
        
        # Colab'da dosya indirme
        from google.colab import files
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(json_string)
        
        files.download(filename)
        print(f"✅ Gelişmiş sonuçlar kaydedildi: {filename}")
    
    def load_results_from_json(self, uploaded_files):
        """JSON dosyasından sonuçları yükle"""
        try:
            for filename, file_content in uploaded_files.items():
                json_data = json.loads(file_content.decode('utf-8'))
                
                if 'results' not in json_data or 'parameters' not in json_data:
                    raise ValueError('Geçersiz JSON formatı!')
                
                self.results = json_data['results']
                self.params = json_data['parameters']
                self.meta = json_data.get('metadata', {})
                
                if 'trainingResults' in json_data:
                    self.training_results = json_data['trainingResults']
                    self.revalidation_btn.disabled = False
                    print(f"📊 Training sonuçları yüklendi: {len(self.training_results)} kombinasyon")
                
                # Validation ayarlarını geri yükle
                if 'validationSettings' in json_data:
                    settings = json_data['validationSettings']
                    self.validation_method.value = settings.get('method', 'simple')
                    self.validation_criteria.value = settings.get('criteria', 'roi')
                    self.top_combinations.value = settings.get('topCombinations', 100)
                    self.overfitting_threshold.value = settings.get('overfittingThreshold', 50)
                    
                    if settings.get('windowSize'):
                        self.window_size.value = settings['windowSize']
                    if settings.get('stepSize'):
                        self.step_size.value = settings['stepSize']
                
                # Parametre formlarını güncelle
                if self.params:
                    self.opt_coins.value = ','.join(self.params.get('coins', []))
                    self.opt_timeframe.value = self.params.get('timeframe', '5m')
                    if self.params.get('startDate'):
                        self.opt_start_date.value = datetime.strptime(self.params['startDate'], '%Y-%m-%d').date()
                    if self.params.get('endDate'):
                        self.opt_end_date.value = datetime.strptime(self.params['endDate'], '%Y-%m-%d').date()
                
                # Sonuçları göster
                self.display_results()
                
                # UI güncellemeleri
                self.reopt_btn.disabled = False
                display(self.validation_section)
                
                training_info = f" ({len(self.training_results)} training sonucu dahil)" if self.training_results else ""
                validation_info = f" - {self.get_validation_method_name(json_data.get('validationSettings', {}).get('method', 'simple'))}"
                print(f"✅ Gelişmiş JSON yüklendi: {len(self.results)} sonuç{training_info}{validation_info}")
                
                break  # İlk dosyayı işle
                
        except Exception as e:
            print(f"❌ JSON yükleme hatası: {str(e)}")
    
    def get_validation_method_name(self, method):
        """Validation method adını döndür"""
        names = {
            'none': 'Validasyon Yok',
            'simple': 'Basit Train/Test Split',
            'walkforward': 'Walk-Forward Analysis',
            'crossval': 'Cross-Validation (3-Fold)'
        }
        return names.get(method, method)
    
    def create_file_upload_widget(self):
        """Dosya yükleme widget'ı oluştur"""
        from google.colab import files
        
        upload_btn = widgets.Button(
            description='📂 JSON Dosyası Yükle',
            button_style='success',
            layout=widgets.Layout(width='200px')
        )
        
        def on_upload_click(btn):
            try:
                uploaded = files.upload()
                if uploaded:
                    self.load_results_from_json(uploaded)
            except Exception as e:
                print(f"❌ Dosya yükleme hatası: {str(e)}")
        
        upload_btn.on_click(on_upload_click)
        return upload_btn
    
    def create_export_widget(self):
        """Export widget'ı oluştur"""
        export_btn = widgets.Button(
            description='💾 Sonuçları JSON Kaydet',
            button_style='warning',
            layout=widgets.Layout(width='200px')
        )
        
        export_btn.on_click(lambda btn: self.export_results_to_json())
        return export_btn
    
    def run_complete_analysis(self):
        """Tam analiz çalıştır - tek tuşla her şey"""
        print("🚀 TAM ANALİZ BAŞLATILIYOR...")
        print("Bu işlem uzun sürebilir, lütfen bekleyin...")
        
        if not self.data and not self.saved_data:
            print("❌ Önce veri çekin veya yükleyin!")
            return
        
        # Otomatik optimizasyon
        self.start_optimization(None)
    
    def create_control_panel(self):
        """Ana kontrol paneli"""
        print("\n" + "="*80)
        print("🎮 KONTROL PANELİ")
        print("="*80)
        
        # Ana butonlar
        upload_btn = self.create_file_upload_widget()
        export_btn = self.create_export_widget()
        
        full_analysis_btn = widgets.Button(
            description='🚀 Tam Analiz (Tek Tuş)',
            button_style='danger',
            layout=widgets.Layout(width='200px')
        )
        full_analysis_btn.on_click(lambda btn: self.run_complete_analysis())
        
        # Durum paneli
        status_panel = widgets.VBox([
            widgets.HTML("<h4>📊 Sistem Durumu</h4>"),
            widgets.HTML(f"• Kaydedilen Veri: {'✅ Var' if self.saved_data else '❌ Yok'}"),
            widgets.HTML(f"• Training Sonuçları: {'✅ Var' if self.training_results else '❌ Yok'}"),
            widgets.HTML(f"• Final Sonuçlar: {'✅ Var' if self.results else '❌ Yok'}"),
        ])
        
        control_box = widgets.VBox([
            widgets.HTML("<h3>🎮 Kontrol Paneli</h3>"),
            widgets.HBox([upload_btn, export_btn, full_analysis_btn]),
            status_panel
        ])
        
        display(control_box)
    
    def show_help(self):
        """Yardım ve kullanım kılavuzu"""
        help_html = """
        <div style='background: linear-gradient(135deg, rgba(59,130,246,0.15), rgba(37,99,235,0.1)); 
                    border: 2px solid rgba(59,130,246,0.3); border-radius: 15px; padding: 20px; margin: 20px 0;'>
            <h3>📖 Multi-Coin Martingale Optimizasyon Kılavuzu</h3>
            
            <h4>🔄 Kullanım Adımları:</h4>
            <ol>
                <li><strong>Veri Çekme:</strong> Coin çiftleri ve tarih aralığı belirleyip verileri çekin</li>
                <li><strong>Parametre Ayarlama:</strong> Optimizasyon parametrelerini (kaldıraç, kar%, çarpan) ayarlayın</li>
                <li><strong>Validation Seçimi:</strong> Walk-Forward, Cross-Validation veya basit split seçin</li>
                <li><strong>Optimizasyon:</strong> "Optimizasyonu Başlat" butonuna tıklayın</li>
                <li><strong>Sonuç Analizi:</strong> Grafik ve tablolarla sonuçları inceleyin</li>
            </ol>
            
            <h4>🧠 Validation Metodları:</h4>
            <ul>
                <li><strong>Simple Split:</strong> %75 training, %25 validation - Hızlı ve basit</li>
                <li><strong>Walk-Forward:</strong> Zaman bazlı pencereler - En gerçekçi</li>
                <li><strong>Cross-Validation:</strong> 3-fold çapraz doğrulama - En güvenilir</li>
            </ul>
            
            <h4>⚠️ Dikkat Edilecekler:</h4>
            <ul>
                <li>ROI farkı %50+ ise overfitting riski var</li>
                <li>🚨 işareti bahis-sermaye aşımını gösterir</li>
                <li>Sharpe Ratio risk-ayarlı performansı ölçer</li>
                <li>Validation Score final sıralama kriteri</li>
            </ul>
            
            <h4>💡 İpuçları:</h4>
            <ul>
                <li>Büyük veri setleri için önce verileri kaydedin</li>
                <li>Optimizasyon 1-3 coin ile sınırlı</li>
                <li>JSON export/import ile sonuçları saklayın</li>
                <li>Top 100-200 kombinasyonu validation'a sokmak yeterli</li>
            </ul>
        </div>
        """
        display(widgets.HTML(help_html))

    # Ana sistem başlatma fonksiyonu
def start_martingale_optimizer():
    """Martingale optimizasyon sistemini başlat"""
    optimizer = MultiCoinMartingaleOptimizer()
    
    # Yardım göster
    optimizer.show_help()
    
    # UI'ı kur
    optimizer.setup_ui()
    
    # Kontrol panelini göster
    optimizer.create_control_panel() 
    
    print("\n✅ Multi-Coin Martingale Optimizasyon Sistemi hazır!")
    print("🚀 Kullanım için yukarıdaki form alanlarını doldurun ve 'Optimizasyonu Başlat' butonuna tıklayın.")
    
    return optimizer

# Sistem başlatma
print("🎯 Multi-Coin Martingale Optimizasyon Sistemi v4.0")
print("⚡ Google Colab Versiyonu - Tam Özellikli Validation Sistemi")
print("📊 Walk-Forward, Cross-Validation, Gerçek Sharpe Ratio")
print("\nSistemi başlatmak için aşağıdaki komutu çalıştırın:")
print("optimizer = start_martingale_optimizer()")

# Kullanım örneği
"""
# Sistemi başlat
optimizer = start_martingale_optimizer()

# Manuel kullanım örneği:
# 1. Veri çek (UI'dan veya kod ile)
# 2. Optimizasyon parametrelerini ayarla
# 3. Validation metodunu seç
# 4. Optimizasyonu başlat
# 5. Sonuçları analiz et

# Gelişmiş özellikler:
# - optimizer.export_results_to_json() - Sonuçları kaydet
# - optimizer.create_performance_charts() - Grafik analiz
# - optimizer.display_results() - Sonuçları göster
"""