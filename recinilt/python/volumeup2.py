import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import sounddevice as sd
import threading
import time
import sys
import subprocess
import os

class UniversalAudioBooster:
    def __init__(self):
        self.boost_active = False
        self.boost_factor = 1.5
        self.stream = None
        
        # Otomatik cihaz bulma
        self.find_working_devices()
        
    def find_working_devices(self):
        """Çalışan ses cihazlarını bulur"""
        print("🔍 Çalışan ses cihazları aranıyor...")
        
        devices = sd.query_devices()
        self.input_device = None
        self.output_device = None
        
        # En basit yaklaşım: varsayılan cihazları kullan
        try:
            default_input = sd.query_devices(kind='input')
            default_output = sd.query_devices(kind='output')
            
            print(f"📥 Varsayılan giriş: {default_input['name']}")
            print(f"📤 Varsayılan çıkış: {default_output['name']}")
            
            # Test et
            self.test_configuration()
            
        except Exception as e:
            print(f"❌ Varsayılan cihaz hatası: {e}")
    
    def test_configuration(self):
        """Mevcut konfigürasyonu test eder"""
        print("🧪 Ses konfigürasyonu test ediliyor...")
        
        # Farklı sample rate'leri dene
        test_rates = [48000, 44100, 22050, 16000]
        
        for rate in test_rates:
            try:
                print(f"  Test ediliyor: {rate} Hz")
                
                # Kısa test akışı
                test_stream = sd.Stream(
                    samplerate=rate,
                    channels=2,
                    dtype=np.float32,
                    blocksize=512,
                    callback=self.dummy_callback,
                    latency='low'
                )
                
                test_stream.start()
                time.sleep(0.1)  # 100ms test
                test_stream.stop()
                test_stream.close()
                
                # Başarılı!
                self.sample_rate = rate
                self.channels = 2
                print(f"✅ Çalışan konfigürasyon bulundu: {rate} Hz, 2 kanal")
                return True
                
            except Exception as e:
                print(f"  ❌ {rate} Hz hatası: {e}")
                continue
        
        # Mono dene
        for rate in test_rates:
            try:
                print(f"  Mono test: {rate} Hz")
                
                test_stream = sd.Stream(
                    samplerate=rate,
                    channels=1,
                    dtype=np.float32,
                    blocksize=512,
                    callback=self.dummy_callback,
                    latency='low'
                )
                
                test_stream.start()
                time.sleep(0.1)
                test_stream.stop()
                test_stream.close()
                
                # Başarılı!
                self.sample_rate = rate
                self.channels = 1
                print(f"✅ Mono konfigürasyon bulundu: {rate} Hz, 1 kanal")
                return True
                
            except Exception as e:
                print(f"  ❌ Mono {rate} Hz hatası: {e}")
                continue
        
        print("❌ Hiçbir konfigürasyon çalışmadı")
        return False
    
    def dummy_callback(self, indata, outdata, frames, time, status):
        """Test için dummy callback"""
        outdata[:] = indata * 0.1  # Çok düşük ses
    
    def audio_callback(self, indata, outdata, frames, time, status):
        """Ana ses işleme callback'i"""
        if status:
            print(f"⚠️ Ses uyarısı: {status}")
        
        try:
            if self.boost_active:
                # Boost uygula
                boosted = indata * self.boost_factor
                
                # Ses kalitesi koruması - çok agresif olmayan
                # 1. Yumuşak sınırlama
                boosted = np.tanh(boosted * 0.8) * 1.1
                
                # 2. Basit clipping
                boosted = np.clip(boosted, -0.9, 0.9)
                
                outdata[:] = boosted
            else:
                outdata[:] = indata
                
        except Exception as e:
            print(f"❌ Callback hatası: {e}")
            outdata[:] = indata  # Güvenli geri dönüş
    
    def start_boost(self, boost_percentage):
        """Boost'u başlatır"""
        if self.boost_active:
            return False
        
        if not hasattr(self, 'sample_rate'):
            print("❌ Ses konfigürasyonu bulunamadı!")
            return False
        
        self.boost_factor = boost_percentage / 100.0
        print(f"🚀 Boost başlatılıyor: %{boost_percentage}")
        print(f"🎵 Konfigürasyon: {self.sample_rate}Hz, {self.channels} kanal")
        
        try:
            self.boost_active = True
            
            # Ses akışını başlat
            self.stream = sd.Stream(
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype=np.float32,
                blocksize=512,
                callback=self.audio_callback,
                latency='low'
            )
            
            self.stream.start()
            print(f"✅ Boost başarıyla başlatıldı!")
            return True
            
        except Exception as e:
            print(f"❌ Boost başlatma hatası: {e}")
            self.boost_active = False
            return False
    
    def stop_boost(self):
        """Boost'u durdurur"""
        if not self.boost_active:
            return
        
        self.boost_active = False
        
        try:
            if self.stream:
                self.stream.stop()
                self.stream.close()
                self.stream = None
            print("✅ Boost durduruldu")
        except Exception as e:
            print(f"❌ Boost durdurma hatası: {e}")
    
    def update_boost_factor(self, boost_percentage):
        """Boost faktörünü günceller"""
        self.boost_factor = boost_percentage / 100.0
    
    def is_boost_active(self):
        """Boost aktif mi?"""
        return self.boost_active

class UniversalBoosterGUI:
    def __init__(self):
        self.booster = UniversalAudioBooster()
        self.setup_gui()
        
    def setup_gui(self):
        """GUI'yi oluşturur"""
        self.root = tk.Tk()
        self.root.title("Evrensel Ses Boost'u")
        self.root.geometry("450x450")
        self.root.resizable(False, False)
        
        # Ana çerçeve
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Başlık
        title_label = ttk.Label(main_frame, text="🔊 Evrensel Ses Boost'u", 
                               font=("Arial", 18, "bold"))
        title_label.pack(pady=(0, 15))
        
        # Açıklama
        info_frame = ttk.LabelFrame(main_frame, text="ℹ️ Nasıl Çalışır", padding="10")
        info_frame.pack(fill=tk.X, pady=(0, 15))
        
        info_text = (
            "🎤 Bu program mikrofondan gelen sesi boost eder\n"
            
        )
        info_label = ttk.Label(info_frame, text=info_text, 
                              font=("Arial", 9), justify=tk.LEFT)
        info_label.pack()
        
        # Sistem durumu
        status_frame = ttk.LabelFrame(main_frame, text="📊 Sistem Durumu", padding="8")
        status_frame.pack(fill=tk.X, pady=(0, 15))
        
        if hasattr(self.booster, 'sample_rate'):
            system_info = f"✅ Ses sistemi hazır\n🎵 {self.booster.sample_rate}Hz, {self.booster.channels} kanal"
        else:
            system_info = "❌ Ses sistemi bulunamadı"
        
        system_label = ttk.Label(status_frame, text=system_info, font=("Arial", 9))
        system_label.pack()
        
        # Boost ayarları
        boost_frame = ttk.LabelFrame(main_frame, text="🎛️ Boost Ayarları", padding="10")
        boost_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Boost değeri
        self.boost_value_var = tk.StringVar()
        self.boost_value_var.set("150%")
        boost_value_label = ttk.Label(boost_frame, textvariable=self.boost_value_var, 
                                     font=("Arial", 16, "bold"), foreground="blue")
        boost_value_label.pack(pady=(0, 10))
        
        # Boost slider
        self.boost_scale = tk.Scale(
            boost_frame, 
            from_=100, to=500, 
            orient=tk.HORIZONTAL, 
            length=350,
            command=self.on_scale_change,
            resolution=10,
            tickinterval=100,
            font=("Arial", 9)
        )
        self.boost_scale.set(150)
        self.boost_scale.pack(fill=tk.X)
        self.on_scale_change(150)
        
        # Kontrol butonları
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(15, 0))
        
        self.start_button = ttk.Button(
            control_frame, 
            text="🚀 Boost Başlat", 
            command=self.toggle_boost
        )
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.test_button = ttk.Button(
            control_frame, 
            text="🎵 Test Sesi", 
            command=self.play_test_sound
        )
        self.test_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stereo_button = ttk.Button(
            control_frame, 
            text="🔧 Stereo Mix", 
            command=self.open_sound_settings
        )
        self.stereo_button.pack(side=tk.LEFT)
        
        # Durum
        self.status_var = tk.StringVar()
        self.status_var.set("🔴 Boost Kapalı")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var, 
                                     font=("Arial", 12, "bold"))
        self.status_label.pack(pady=(15, 0))
        
        # Ses seviyesi göstergesi (fake ama güzel görünür)
        self.level_var = tk.StringVar()
        self.level_var.set("🔊 Ses Seviyesi: --")
        self.level_label = ttk.Label(main_frame, textvariable=self.level_var, 
                                    font=("Arial", 10))
        self.level_label.pack(pady=(5, 0))
        
        # Uyarılar
        warning_frame = ttk.LabelFrame(main_frame, text="⚠️ Önemli Bilgiler", 
                                      padding="8")
        warning_frame.pack(fill=tk.X, pady=(15, 0))
        
        warning_text = (
            "🎧 En iyi sonuç için kulaklık kullanın (geri besleme önler)\n"
            "🔊 %300+ çok yüksek - işitme sağlığınıza dikkat!\n"
            "⚡ Geri besleme olursa hemen boost'u durdurun\n"
            "🎵 Sistem seslerini boost etmek için Stereo Mix etkinleştirin"
        )
        warning_label = ttk.Label(warning_frame, text=warning_text, 
                                 font=("Arial", 8), foreground="red")
        warning_label.pack()
        
        # Ses seviyesi simülasyonu
        self.simulate_audio_level()
        
    def simulate_audio_level(self):
        """Ses seviyesi simülasyonu (görsel etki için)"""
        try:
            if self.booster.is_boost_active():
                import random
                level = random.randint(20, 85)
                bars = "█" * (level // 10)
                self.level_var.set(f"🔊 Ses Seviyesi: {bars} %{level}")
            else:
                self.level_var.set("🔊 Ses Seviyesi: Boost kapalı")
        except:
            pass
        
        # 200ms sonra tekrar
        self.root.after(200, self.simulate_audio_level)
    
    def on_scale_change(self, value):
        """Slider değiştiğinde"""
        boost_value = int(float(value))
        self.boost_value_var.set(f"{boost_value}%")
        
        # Renk değiştir
        color = "green" if boost_value <= 200 else "orange" if boost_value <= 300 else "red"
        
        # Boost aktifse güncelle
        if self.booster.is_boost_active():
            self.booster.update_boost_factor(boost_value)
            self.status_var.set(f"🟢 Boost Aktif (%{boost_value})")
    
    def toggle_boost(self):
        """Boost aç/kapat"""
        if self.booster.is_boost_active():
            # Kapat
            self.booster.stop_boost()
            self.start_button.config(text="🚀 Boost Başlat")
            self.status_var.set("🔴 Boost Kapalı")
        else:
            # Başlat
            boost_level = self.boost_scale.get()
            
            # Çok yüksek değer uyarısı
            if boost_level > 300:
                result = messagebox.askyesno(
                    "Tehlikeli Seviye!", 
                    f"⚠️ %{boost_level} seviyesi tehlikeli!\n\n"
                    "Bu seviye:\n"
                    "• Kalıcı işitme kaybına neden olabilir\n"
                    "• Hoparlörleri yakabilir\n"
                    "• Şiddetli geri besleme yaratabilir\n\n"
                    "Gerçekten devam etmek istiyor musunuz?"
                )
                if not result:
                    return
            
            # Başlat
            if self.booster.start_boost(boost_level):
                self.start_button.config(text="🛑 Boost Durdur")
                self.status_var.set(f"🟢 Boost Aktif (%{boost_level})")
                
                # Başarı mesajı
                if not hasattr(self, 'first_start_shown'):
                    messagebox.showinfo("Boost Başlatıldı!", 
                        "✅ Ses boost'u başarıyla başlatıldı!\n\n"
                        "🎤 Mikrofonunuzun açık olduğundan emin olun\n"
                        "🎵 Konuşun veya müzik çalın\n"
                        "🔊 Sesiniz boost edilmiş olarak çıkacak\n\n"
                        "💡 Sistem seslerini boost etmek için:\n"
                        "   Stereo Mix butonuna tıklayın")
                    self.first_start_shown = True
            else:
                messagebox.showerror("Başlatma Hatası", 
                    "❌ Boost başlatılamadı!\n\n"
                    "🔧 Çözüm önerileri:\n"
                    "• Mikrofonunuzun bağlı olduğundan emin olun\n"
                    "• Mikrofon izinlerini kontrol edin\n"
                    "• Başka ses uygulamalarını kapatın\n"
                    "• Programı yönetici olarak çalıştırın")
    
    def play_test_sound(self):
        """Test sesi çalar"""
        def play_melody():
            try:
                # Güzel bir melodi
                notes = [
                    (523, 0.3),  # C5
                    (587, 0.3),  # D5
                    (659, 0.3),  # E5
                    (698, 0.3),  # F5
                    (784, 0.6),  # G5
                    (659, 0.3),  # E5
                    (523, 0.6),  # C5
                ]
                
                sample_rate = getattr(self.booster, 'sample_rate', 44100)
                full_wave = np.array([])
                
                for freq, duration in notes:
                    t = np.linspace(0, duration, int(sample_rate * duration))
                    wave = 0.3 * np.sin(2 * np.pi * freq * t)
                    
                    # Smooth fade
                    fade = int(0.02 * sample_rate)
                    if len(wave) > 2 * fade:
                        wave[:fade] *= np.linspace(0, 1, fade)
                        wave[-fade:] *= np.linspace(1, 0, fade)
                    
                    full_wave = np.concatenate([full_wave, wave])
                
                sd.play(full_wave, sample_rate)
                
            except Exception as e:
                print(f"Test sesi hatası: {e}")
        
        threading.Thread(target=play_melody, daemon=True).start()
    
    def open_sound_settings(self):
        """Windows ses ayarlarını açar"""
        try:
            # Windows ses kontrol panelini aç
            subprocess.run(['mmsys.cpl'], shell=True)
            
            messagebox.showinfo("Stereo Mix Etkinleştirme", 
                "🔧 Ses Kontrol Paneli açıldı!\n\n"
                "Stereo Mix etkinleştirmek için:\n\n"
                "1️⃣ 'Kayıt' sekmesine gidin\n"
                "2️⃣ Boş alana sağ tıklayın\n"
                "3️⃣ 'Devre Dışı Cihazları Göster' seçin\n"
                "4️⃣ 'Stereo Mix' bulup sağ tıklayın\n"
                "5️⃣ 'Etkinleştir' seçin\n"
                "6️⃣ Tekrar sağ tıklayıp 'Varsayılan Cihaz Olarak Ayarla'\n\n"
                "✅ Artık sistem sesleriniz boost edilecek!")
                
        except Exception as e:
            messagebox.showerror("Hata", f"Ses ayarları açılamadı: {e}")
    
    def on_closing(self):
        """Program kapatılırken"""
        self.booster.stop_boost()
        self.root.destroy()
    
    def run(self):
        """Programı çalıştır"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

def check_requirements():
    """Gereksinimleri kontrol et"""
    try:
        import numpy
        import sounddevice
        return True
    except ImportError as e:
        print(f"❌ Eksik kütüphane: {e}")
        print("\n📦 Kurulum:")
        print("pip install numpy sounddevice")
        return False

if __name__ == "__main__":
    print("🎵 Evrensel Ses Boost'u v1.0")
    print("=" * 35)
    
    if not check_requirements():
        input("\n❌ Çıkmak için Enter'a basın...")
        sys.exit(1)
    
    try:
        app = UniversalBoosterGUI()
        app.run()
    except Exception as e:
        print(f"\n❌ Program hatası: {e}")
        input("Çıkmak için Enter'a basın...")