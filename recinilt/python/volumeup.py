import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import sounddevice as sd
import threading
import time
import sys
import queue
import pyaudio
import wave

class SystemAudioBooster:
    def __init__(self):
        self.boost_active = False
        self.boost_factor = 1.5
        self.recording_stream = None
        self.playback_stream = None
        self.audio_queue = queue.Queue(maxsize=10)
        self.processing_thread = None
        
        # Ses ayarları
        self.sample_rate = 44100
        self.channels = 2
        self.chunk_size = 1024
        self.format = pyaudio.paFloat32
        
        # PyAudio başlat
        self.audio = pyaudio.PyAudio()
        self.find_best_devices()
        
    def find_best_devices(self):
        """En iyi loopback ve çıkış cihazlarını bulur"""
        self.loopback_device = None
        self.output_device = None
        self.loopback_host_api = None
        self.output_host_api = None
        
        print("🔍 Ses cihazları analiz ediliyor...")
        
        # Host API'leri listele
        print("\n📋 Host API'ler:")
        for i in range(self.audio.get_host_api_count()):
            api_info = self.audio.get_host_api_info_by_index(i)
            print(f"  {i}: {api_info['name']}")
        
        # En iyi loopback cihazını bul
        loopback_candidates = []
        output_candidates = []
        
        print("\n🔍 Cihaz analizi:")
        for i in range(self.audio.get_device_count()):
            try:
                device_info = self.audio.get_device_info_by_index(i)
                device_name = device_info.get('name', '').lower()
                host_api = device_info.get('hostApi', 0)
                
                # Host API adını al
                try:
                    host_api_info = self.audio.get_host_api_info_by_index(host_api)
                    host_api_name = host_api_info.get('name', '').lower()
                except:
                    host_api_name = 'unknown'
                
                print(f"Cihaz {i}: {device_info.get('name', 'Bilinmeyen')}")
                print(f"  📥 Giriş: {device_info['maxInputChannels']}")
                print(f"  📤 Çıkış: {device_info['maxOutputChannels']}")
                print(f"  🔧 Host API: {host_api} ({host_api_name})")
                
                # Loopback cihazı arama - öncelik sırası
                if device_info['maxInputChannels'] > 0:
                    score = 0
                    
                    # Stereo Mix en yüksek öncelik
                    if any(keyword in device_name for keyword in ['stereo', 'karışım', 'mix']):
                        score += 100
                        print(f"  ✅ STEREO MIX bulundu! Öncelik: {score}")
                    
                    # What U Hear tarzı
                    elif any(keyword in device_name for keyword in ['what u hear', 'wave out']):
                        score += 90
                        print(f"  ✅ What U Hear tarzı: {score}")
                    
                    # Hoparlör/Speaker loopback
                    elif any(keyword in device_name for keyword in ['hoparlör', 'speaker']):
                        if 'pc' in device_name or 'loopback' in device_name:
                            score += 80
                            print(f"  ✅ Speaker loopback: {score}")
                        else:
                            score += 30
                    
                    # WASAPI bonus
                    if 'wasapi' in host_api_name:
                        score += 20
                        print(f"  🔧 WASAPI bonus: +20")
                    
                    if score > 0:
                        loopback_candidates.append({
                            'index': i,
                            'score': score,
                            'name': device_info.get('name', ''),
                            'host_api': host_api,
                            'host_api_name': host_api_name
                        })
                
                # Çıkış cihazı arama
                if device_info['maxOutputChannels'] > 0:
                    score = 0
                    
                    # Varsayılan çıkış
                    if 'default' in device_name or 'mapper' in device_name:
                        score += 50
                    
                    # Hoparlör
                    elif any(keyword in device_name for keyword in ['hoparlör', 'speaker']):
                        score += 40
                    
                    # WASAPI bonus
                    if 'wasapi' in host_api_name:
                        score += 10
                    
                    if score > 0:
                        output_candidates.append({
                            'index': i,
                            'score': score,
                            'name': device_info.get('name', ''),
                            'host_api': host_api,
                            'host_api_name': host_api_name
                        })
                
                print()  # Boş satır
                
            except Exception as e:
                print(f"  ❌ Cihaz {i} analiz edilemedi: {e}")
        
        # En iyi adayları seç
        if loopback_candidates:
            loopback_candidates.sort(key=lambda x: x['score'], reverse=True)
            best_loopback = loopback_candidates[0]
            self.loopback_device = best_loopback['index']
            self.loopback_host_api = best_loopback['host_api']
            
            print(f"🎯 En iyi loopback cihazı:")
            print(f"  📍 Index: {self.loopback_device}")
            print(f"  📝 Ad: {best_loopback['name']}")
            print(f"  🏆 Skor: {best_loopback['score']}")
            print(f"  🔧 Host API: {best_loopback['host_api_name']}")
        
        if output_candidates:
            output_candidates.sort(key=lambda x: x['score'], reverse=True)
            best_output = output_candidates[0]
            self.output_device = best_output['index']
            self.output_host_api = best_output['host_api']
            
            print(f"🎯 En iyi çıkış cihazı:")
            print(f"  📍 Index: {self.output_device}")
            print(f"  📝 Ad: {best_output['name']}")
            print(f"  🏆 Skor: {best_output['score']}")
            print(f"  🔧 Host API: {best_output['host_api_name']}")
        
        # Sonuç
        success = self.loopback_device is not None and self.output_device is not None
        if success:
            print(f"\n✅ Cihaz seçimi başarılı!")
        else:
            print(f"\n❌ Uygun cihaz bulunamadı!")
            if not loopback_candidates:
                print("  💡 Stereo Mix'i etkinleştirmeyi deneyin")
            
        return success
    
    def test_device_compatibility(self, device_index, host_api, is_input=True):
        """Cihazın uyumluluğunu test eder"""
        try:
            if is_input:
                test_stream = self.audio.open(
                    format=self.format,
                    channels=self.channels,
                    rate=self.sample_rate,
                    input=True,
                    input_device_index=device_index,
                    input_host_api_specific_stream_info=pyaudio.PaWin_DirectSoundHostApiSpecificStreamInfo(host_api) if host_api == 1 else None,
                    frames_per_buffer=512,
                    start=False
                )
            else:
                test_stream = self.audio.open(
                    format=self.format,
                    channels=self.channels,
                    rate=self.sample_rate,
                    output=True,
                    output_device_index=device_index,
                    output_host_api_specific_stream_info=pyaudio.PaWin_DirectSoundHostApiSpecificStreamInfo(host_api) if host_api == 1 else None,
                    frames_per_buffer=512,
                    start=False
                )
            
            test_stream.close()
            return True
            
        except Exception as e:
            print(f"❌ Cihaz {device_index} test hatası: {e}")
            return False
    
    def audio_processing_thread(self):
        """Ses işleme thread'i"""
        print("🎵 Ses işleme thread'i başlatıldı")
        
        while self.boost_active:
            try:
                if not self.audio_queue.empty():
                    audio_data = self.audio_queue.get_nowait()
                    
                    # NumPy array'e çevir
                    audio_array = np.frombuffer(audio_data, dtype=np.float32)
                    
                    # Stereo için reshape
                    if self.channels == 2 and len(audio_array) % 2 == 0:
                        audio_array = audio_array.reshape(-1, 2)
                    
                    # Boost uygula
                    boosted = audio_array * self.boost_factor
                    
                    # Gelişmiş ses kalitesi koruması
                    # 1. Soft compression
                    boosted = np.tanh(boosted * 0.7) * 1.3
                    
                    # 2. RMS normalization
                    if np.max(np.abs(boosted)) > 0:
                        current_rms = np.sqrt(np.mean(boosted**2))
                        target_rms = min(current_rms, 0.8)
                        if current_rms > target_rms:
                            boosted = boosted * (target_rms / current_rms)
                    
                    # 3. Final clipping
                    boosted = np.clip(boosted, -0.95, 0.95)
                    
                    # Tekrar byte'a çevir
                    output_data = boosted.astype(np.float32).tobytes()
                    
                    # Çıkış akışına gönder
                    if self.playback_stream and hasattr(self.playback_stream, '_stream'):
                        try:
                            if not self.playback_stream._stream.stopped:
                                self.playback_stream.write(output_data, exception_on_underflow=False)
                        except Exception as e:
                            if "Stream is stopped" not in str(e):
                                print(f"⚠️ Çıkış hatası: {e}")
                
                time.sleep(0.001)  # CPU kullanımını azalt
                
            except queue.Empty:
                time.sleep(0.001)
            except Exception as e:
                print(f"❌ Ses işleme hatası: {e}")
                time.sleep(0.01)
        
        print("🛑 Ses işleme thread'i durduruldu")
    
    def recording_callback(self, in_data, frame_count, time_info, status):
        """Kayıt callback'i - sistem sesini yakalar"""
        if status:
            print(f"⚠️ Kayıt uyarısı: {status}")
        
        try:
            if self.boost_active and in_data:
                # Ses verisini kuyruğa ekle
                if not self.audio_queue.full():
                    self.audio_queue.put_nowait(in_data)
        except Exception as e:
            print(f"❌ Callback hatası: {e}")
        
        return (None, pyaudio.paContinue)
    
    def start_boost(self, boost_percentage):
        """Boost'u başlatır"""
        if self.boost_active:
            print("⚠️ Boost zaten aktif!")
            return False
        
        if self.loopback_device is None or self.output_device is None:
            print("❌ Uygun cihaz bulunamadı!")
            return False
        
        self.boost_factor = boost_percentage / 100.0
        print(f"🚀 Boost başlatılıyor: %{boost_percentage}")
        print(f"📍 Loopback cihazı: {self.loopback_device}")
        print(f"📍 Çıkış cihazı: {self.output_device}")
        
        try:
            # Önce giriş akışını test et
            print("🧪 Giriş cihazı test ediliyor...")
            if not self.test_device_compatibility(self.loopback_device, self.loopback_host_api, True):
                print("❌ Giriş cihazı uyumlu değil")
                return False
            
            # Çıkış cihazını test et
            print("🧪 Çıkış cihazı test ediliyor...")
            if not self.test_device_compatibility(self.output_device, self.output_host_api, False):
                print("❌ Çıkış cihazı uyumlu değil")
                return False
            
            print("✅ Cihaz testleri başarılı")
            
            self.boost_active = True
            
            # Giriş akışını başlat
            print("📥 Giriş akışı açılıyor...")
            self.recording_stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                input_device_index=self.loopback_device,
                frames_per_buffer=self.chunk_size,
                stream_callback=self.recording_callback,
                start=False
            )
            
            # Çıkış akışını başlat
            print("📤 Çıkış akışı açılıyor...")
            self.playback_stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                output=True,
                output_device_index=self.output_device,
                frames_per_buffer=self.chunk_size,
                start=False
            )
            
            # Akışları başlat
            print("▶️ Akışlar başlatılıyor...")
            self.recording_stream.start_stream()
            self.playback_stream.start_stream()
            
            # İşleme thread'ini başlat
            print("🧵 İşleme thread'i başlatılıyor...")
            self.processing_thread = threading.Thread(target=self.audio_processing_thread, daemon=True)
            self.processing_thread.start()
            
            print(f"✅ Sistem ses boost'u başarıyla başlatıldı: %{boost_percentage}")
            return True
            
        except Exception as e:
            print(f"❌ Boost başlatma hatası: {e}")
            self.boost_active = False
            self.cleanup_streams()
            return False
    
    def cleanup_streams(self):
        """Akışları temizler"""
        try:
            if hasattr(self, 'recording_stream') and self.recording_stream:
                if hasattr(self.recording_stream, '_stream') and not self.recording_stream._stream.stopped:
                    self.recording_stream.stop_stream()
                self.recording_stream.close()
                self.recording_stream = None
        except Exception as e:
            print(f"⚠️ Giriş akışı temizleme hatası: {e}")
        
        try:
            if hasattr(self, 'playback_stream') and self.playback_stream:
                if hasattr(self.playback_stream, '_stream') and not self.playback_stream._stream.stopped:
                    self.playback_stream.stop_stream()
                self.playback_stream.close()
                self.playback_stream = None
        except Exception as e:
            print(f"⚠️ Çıkış akışı temizleme hatası: {e}")
    
    def stop_boost(self):
        """Boost'u durdurur"""
        if not self.boost_active:
            return
        
        print("🛑 Boost durduruluyor...")
        self.boost_active = False
        
        # Akışları durdur
        self.cleanup_streams()
        
        # Kuyruğu temizle
        while not self.audio_queue.empty():
            try:
                self.audio_queue.get_nowait()
            except:
                break
        
        print("✅ Boost başarıyla durduruldu")
    
    def update_boost_factor(self, boost_percentage):
        """Boost faktörünü günceller"""
        self.boost_factor = boost_percentage / 100.0
        if self.boost_active:
            print(f"🔄 Boost seviyesi güncellendi: %{boost_percentage}")
    
    def __del__(self):
        """Temizlik"""
        try:
            self.stop_boost()
            self.audio.terminate()
        except:
            pass

class SystemBoosterGUI:
    def __init__(self):
        self.booster = SystemAudioBooster()
        self.setup_gui()
        
    def setup_gui(self):
        """GUI'yi oluşturur"""
        self.root = tk.Tk()
        self.root.title("Sistem Ses Boost'u v2.1")
        self.root.geometry("420x380")
        self.root.resizable(False, False)
        
        # Ana çerçeve
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Başlık
        title_label = ttk.Label(main_frame, text="🔊 Sistem Ses Boost'u", 
                               font=("Arial", 18, "bold"))
        title_label.pack(pady=(0, 15))
        
        # Durum bilgisi
        status_frame = ttk.LabelFrame(main_frame, text="📊 Cihaz Durumu", padding="8")
        status_frame.pack(fill=tk.X, pady=(0, 15))
        
        loopback_status = "✅ Loopback Hazır" if self.booster.loopback_device is not None else "❌ Loopback Bulunamadı"
        output_status = "✅ Çıkış Hazır" if self.booster.output_device is not None else "❌ Çıkış Bulunamadı"
        
        status_text = f"{loopback_status}\n{output_status}"
        status_label = ttk.Label(status_frame, text=status_text, font=("Arial", 9))
        status_label.pack()
        
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
            from_=100, to=300, 
            orient=tk.HORIZONTAL, 
            length=320,
            command=self.on_scale_change,
            resolution=5,
            tickinterval=50,
            font=("Arial", 9)
        )
        self.boost_scale.set(150)
        self.boost_scale.pack(fill=tk.X)
        self.on_scale_change(150)  # İlk değeri ayarla
        
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
        
        self.help_button = ttk.Button(
            control_frame, 
            text="❓ Yardım", 
            command=self.show_help
        )
        self.help_button.pack(side=tk.LEFT)
        
        # Durum
        self.status_var = tk.StringVar()
        self.status_var.set("🔴 Boost Kapalı")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var, 
                                     font=("Arial", 12, "bold"))
        self.status_label.pack(pady=(15, 0))
        
        # Uyarılar
        warning_frame = ttk.LabelFrame(main_frame, text="⚠️ Önemli Uyarılar", 
                                      padding="8")
        warning_frame.pack(fill=tk.X, pady=(15, 0))
        
        warning_text = (
            "• Bu program sistem sesinin TAMAMINI yükseltir\n"
            "• %200+ çok yüksek - işitme hasarı riski\n"
            "• Hoparlörlerinize zarar verebilir\n"
            "• Stereo Mix etkinleştirilmeli"
        )
        warning_label = ttk.Label(warning_frame, text=warning_text, 
                                 font=("Arial", 8), foreground="red")
        warning_label.pack()
        
    def on_scale_change(self, value):
        """Slider değiştiğinde"""
        boost_value = int(float(value))
        self.boost_value_var.set(f"{boost_value}%")
        
        # Boost aktifse güncelle
        if hasattr(self, 'booster') and self.booster.boost_active:
            self.booster.update_boost_factor(boost_value)
            self.status_var.set(f"🟢 Boost Aktif (%{boost_value})")
    
    def toggle_boost(self):
        """Boost aç/kapat"""
        if self.booster.boost_active:
            # Kapat
            self.booster.stop_boost()
            self.start_button.config(text="🚀 Boost Başlat")
            self.status_var.set("🔴 Boost Kapalı")
        else:
            # Başlat
            boost_level = self.boost_scale.get()
            
            # Yüksek değer uyarısı
            if boost_level > 200:
                result = messagebox.askyesno(
                    "Tehlikeli Seviye!", 
                    f"⚠️ %{boost_level} çok yüksek bir seviye!\n\n"
                    "Bu seviye:\n"
                    "• İşitme kaybına neden olabilir\n"
                    "• Hoparlörleri yakabilir\n"
                    "• Ses bozukluğu yaratabilir\n\n"
                    "Gerçekten devam etmek istiyor musunuz?"
                )
                if not result:
                    return
            
            # Başlat
            if self.booster.start_boost(boost_level):
                self.start_button.config(text="🛑 Boost Durdur")
                self.status_var.set(f"🟢 Boost Aktif (%{boost_level})")
                
                # Başarı mesajı
                messagebox.showinfo("Boost Başlatıldı!", 
                    "✅ Sistem ses boost'u başarıyla başlatıldı!\n\n"
                    "💡 Test için:\n"
                    "• YouTube videosu açın\n"
                    "• Müzik çalın\n"
                    "• Test sesi butonunu kullanın\n\n"
                    "Ses seviyesi artmış olmalı!")
            else:
                error_msg = (
                    "❌ Boost başlatılamadı!\n\n"
                    "🔧 Çözüm önerileri:\n"
                    "1. Stereo Mix'i etkinleştirin:\n"
                    "   • Ses ayarları → Kayıt\n"
                    "   • Sağ tık → Devre dışı cihazları göster\n"
                    "   • Stereo Mix'i etkinleştir\n\n"
                    "2. Programı yönetici olarak çalıştırın\n"
                    "3. Ses sürücülerini güncelleyin"
                )
                messagebox.showerror("Başlatma Hatası", error_msg)
    
    def play_test_sound(self):
        """Test sesi çalar"""
        def play_beep():
            try:
                # Çok tatlı bir melodi
                notes = [
                    (262, 0.3),  # C4
                    (294, 0.3),  # D4
                    (330, 0.3),  # E4
                    (349, 0.3),  # F4
                    (392, 0.6),  # G4
                ]
                
                sample_rate = 44100
                full_wave = np.array([])
                
                for freq, duration in notes:
                    t = np.linspace(0, duration, int(sample_rate * duration))
                    wave = 0.3 * np.sin(2 * np.pi * freq * t)
                    
                    # Fade in/out
                    fade = int(0.05 * sample_rate)
                    if len(wave) > 2 * fade:
                        wave[:fade] *= np.linspace(0, 1, fade)
                        wave[-fade:] *= np.linspace(1, 0, fade)
                    
                    full_wave = np.concatenate([full_wave, wave])
                
                # Stereo yap
                stereo_wave = np.column_stack([full_wave, full_wave])
                
                sd.play(stereo_wave, sample_rate)
                
            except Exception as e:
                print(f"Test sesi hatası: {e}")
        
        threading.Thread(target=play_beep, daemon=True).start()
    
    def show_help(self):
        """Yardım gösterir"""
        help_text = (
            "🔊 Sistem Ses Boost'u Yardım\n\n"
            
            "📋 Nasıl Çalışır:\n"
            "• Sistem seslerini yakalar (Stereo Mix)\n"
            "• Boost uygular\n"
            "• Hoparlörlere geri gönderir\n\n"
            
            "🔧 Stereo Mix Etkinleştirme:\n"
            "1. Windows + R → 'mmsys.cpl'\n"
            "2. Kayıt sekmesi\n"
            "3. Sağ tık → Devre dışı cihazları göster\n"
            "4. 'Stereo Mix' bulup etkinleştir\n"
            "5. Varsayılan cihaz yap\n\n"
            
            "💡 İpuçları:\n"
            "• %150 ile başlayın\n"
            "• Kulaklık kullanın (geri besleme önleme)\n"
            "• YouTube ile test edin\n"
            "• Ses bozulursa boost'u düşürün"
        )
        messagebox.showinfo("Yardım", help_text)
    
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
        import pyaudio
        return True
    except ImportError as e:
        print(f"❌ Eksik kütüphane: {e}")
        print("\n📦 Kurulum:")
        print("pip install numpy sounddevice pyaudio")
        return False

if __name__ == "__main__":
    print("🎵 Sistem Ses Boost'u v2.1")
    print("=" * 35)
    
    if not check_requirements():
        input("\n❌ Çıkmak için Enter'a basın...")
        sys.exit(1)
    
    try:
        app = SystemBoosterGUI()
        app.run()
    except Exception as e:
        print(f"\n❌ Program hatası: {e}")
        input("Çıkmak için Enter'a basın...")