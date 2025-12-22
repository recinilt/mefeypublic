# 🎵 Suno Müzik Klibi Oluşturucu - Kullanım Kılavuzu

Lokal bilgisayarınızda AI destekli müzik videoları oluşturun!

## 📋 Gereksinimler

### Sistem Gereksinimleri
- **Python**: 3.8 veya üzeri
- **İşletim Sistemi**: Windows, macOS, Linux
- **Boş Disk Alanı**: En az 2 GB (videolar için)
- **İnternet**: API çağrıları ve video indirme için gerekli

### API Anahtarları (ÜCRETSİZ!)

1. **Anthropic API** (Claude AI için)
   - 🔗 https://console.anthropic.com/
   - Ücretsiz deneme kredisi verilir
   - Kayıt ol → API Keys → Create Key

2. **Pexels API** (Videolar için)
   - 🔗 https://www.pexels.com/api/
   - Tamamen ücretsiz!
   - Kayıt ol → API → Your API Key

## 🚀 Kurulum

### 1. Python Paketlerini Yükle

```bash
pip install -r requirements.txt
```

Veya tek tek:

```bash
pip install anthropic pillow moviepy requests numpy
```

### 2. API Anahtarlarını Ayarla

`suno_pexels_music_video.py` dosyasını açın ve şu satırları düzenleyin:

```python
ANTHROPIC_API_KEY = "sk-ant-api03-BURAYA_ANAHTARINIZI_YAPIŞTIRIN"
PEXELS_API_KEY = "BURAYA_PEXELS_ANAHTARINIZI_YAPIŞTIRIN"
```

## 📖 Kullanım

### Basit Kullanım

```bash
python suno_pexels_music_video.py
```

Program sırayla şunları soracak:

1. **Video Formatı**
   - 1: TikTok/Reels (Dikey - 1080x1920)
   - 2: YouTube (Yatay - 1920x1080)
   - 3: Instagram (Kare - 1080x1080)

2. **Video Kalitesi**
   - 1: HD (1280x720)
   - 2: SD (640x360)

3. **Altyazı**
   - E: Evet (önerilen)
   - h: Hayır

4. **Şarkı Sözleri**
   - Şarkı sözlerini yapıştırın
   - Bitirmek için: Ctrl+D (Linux/Mac) veya Ctrl+Z (Windows)

5. **MP3 Dosyası**
   - Dosya yolunu girin (örn: `C:\Muzik\sarkim.mp3`)

### İki Mod

#### 🤖 Otomatik Mod (Önerilen)
Sadece şarkı sözlerini yapıştırın, Claude AI zamanlamaları otomatik oluşturur:

```
Gün batımında deniz kenarında
Rüzgar saçlarını dalgalandırır
Uzaklarda bir tekne kaybolur
```

#### ✏️ Manuel Mod
Zamanlamaları kendiniz belirleyin:

```
[0:00] Gün batımında deniz kenarında
[0:08] Rüzgar saçlarını dalgalandırır
[0:16] Uzaklarda bir tekne kaybolur
```

## 🎬 Çıktı

Video şu klasöre kaydedilir:
```
output/music_video_YYYYMMDD_HHMMSS.mp4
```

Geçici videolar:
```
videos/scene_001.mp4
videos/scene_002.mp4
...
```

## ⚙️ İleri Seviye Ayarlar

### Kod İçinden Ayarlar

`Config` sınıfını düzenleyerek varsayılan ayarları değiştirebilirsiniz:

```python
class Config:
    # Varsayılan format
    DEFAULT_RESOLUTION = (1080, 1920)  # Dikey
    
    # Varsayılan kalite
    DEFAULT_QUALITY = 'large'  # HD
    
    # Altyazı
    USE_SUBTITLES = True
    
    # Çıktı klasörleri
    OUTPUT_DIR = "output"
    VIDEOS_DIR = "videos"
```

### Font Ayarları

Altyazı fontunu değiştirmek için `add_subtitle_to_frame` fonksiyonundaki font yollarını düzenleyin:

```python
font_paths = [
    'C:/Windows/Fonts/arial.ttf',  # Windows
    '/usr/share/fonts/...',         # Linux
    '/System/Library/Fonts/...'     # macOS
]
```

## 🐛 Sorun Giderme

### "ModuleNotFoundError: No module named 'moviepy'"
```bash
pip install moviepy
```

### "ImageMagick is not installed"
MoviePy için ImageMagick gerekli değil, ancak gelişmiş efektler için:

**Windows:**
```
https://imagemagick.org/script/download.php#windows
```

**Linux:**
```bash
sudo apt-get install imagemagick
```

**macOS:**
```bash
brew install imagemagick
```

### Video İndirilemedi
- İnternet bağlantınızı kontrol edin
- Pexels API anahtarınızı kontrol edin
- Arama kelimelerini değiştirin (daha basit kelimeler deneyin)

### Claude Analizi Başarısız
- Anthropic API anahtarınızı kontrol edin
- API kredinizin olduğundan emin olun
- Şarkı sözlerinin çok uzun olmadığından emin olun

### Memory Error
- Video kalitesini düşürün (SD seçin)
- Çözünürlüğü küçültün
- Daha az sahne kullanın

## 💡 İpuçları

### Daha İyi Sonuçlar İçin

1. **Şarkı Sözleri**
   - Net ve anlamlı sözler yazın
   - Her satır bir sahneye denk gelir
   - Çok uzun sözler yerine kısa ve öz olun

2. **Arama Kelimeleri**
   - Basit ve genel terimler kullanın (nature, city, night)
   - Çok spesifik aramalar video bulamayabilir
   - İngilizce kelimeler daha iyi sonuç verir

3. **Video Süresi**
   - Kısa şarkılar (2-3 dk) daha hızlı işlenir
   - Uzun şarkılar için manuel mod kullanın

4. **Performans**
   - İlk çalıştırma daha uzun sürebilir
   - Videoları tekrar kullanmak için `videos/` klasörünü silmeyin
   - SSD disk kullanıyorsanız çok daha hızlıdır

## 📊 Özellik Karşılaştırması

| Özellik | Colab Versiyonu | Lokal Versiyon |
|---------|----------------|----------------|
| Claude AI Analizi | ✅ | ✅ |
| Pexels Gerçek Videolar | ✅ | ✅ |
| Altyazı Desteği | ✅ | ✅ |
| Tüm Formatlar | ✅ | ✅ |
| Manuel/Otomatik Mod | ✅ | ✅ |
| Widget UI | ✅ | ❌ (Konsol) |
| GPU Hızlandırma | ✅ | ⚠️ (Opsiyonel) |
| İnternet Gereksinimi | ✅ | ✅ |
| Kurulum | Kolay | Orta |

## 🔒 Gizlilik

- Tüm işlemler lokal bilgisayarınızda yapılır
- API'lere sadece analiz ve video arama için bağlanılır
- Ses dosyanız hiçbir yere yüklenmez
- Oluşturulan videolar tamamen sizin kontrolünüzde

## 📝 Lisans

Bu kod açık kaynaklıdır ve eğitim amaçlı kullanılabilir.

## 🤝 Destek

Sorunlarınız için:
1. Bu README'yi dikkatlice okuyun
2. Hata mesajlarını kontrol edin
3. API anahtarlarınızı doğrulayın
4. Python ve paket versiyonlarınızı kontrol edin

## 🎉 Başarılı Çalıştırma Örneği

```
==============================================================
  🔑 API Anahtarları Kontrol Ediliyor
==============================================================

✅ Anthropic API OK
✅ Pexels API OK

==============================================================
  ⚙️ Video Ayarları
==============================================================

📱 Video Formatı:
  1. TikTok/Reels - Dikey
  2. YouTube - Yatay
  3. Instagram - Kare

Seçiminiz (1-3, Enter=1): 1

🎬 Video Kalitesi:
  1. HD (1280x720)
  2. SD (640x360)

Seçiminiz (1-2, Enter=1): 1

📝 Altyazı eklensin mi? (E/h, Enter=E): E

✨ Ayarlar kaydedildi:
   - Format: 1080x1920
   - Kalite: large
   - Altyazı: Evet

[...]

🎉🎉🎉 TAMAMLANDI! 🎉🎉🎉

📹 Video: output/music_video_20241220_145623.mp4
⏱️ Süre: 3:24
🎨 Sahne: 12
🎬 Kaynak: Gerçek videolar (Pexels)
```

Keyifli videolar! 🎵🎬
