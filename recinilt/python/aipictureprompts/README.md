# AI Picture Prompts - Image Generator

Bu Python scripti, HTML'deki her stil için otomatik olarak AI görselleri üretir ve HTML'e entegre eder.

## Kurulum

1. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

## Kullanım

1. **API Keylerini Ekleyin**
   - `ai_image_generator.py` dosyasını açın
   - Şu satırları bulun ve API keylerini ekleyin:
   ```python
   ANTHROPIC_API_KEY = "buraya ekle"  # Anthropic API Key
   OPENAI_API_KEY = "buraya ekle"     # OpenAI API Key
   ```

2. **HTML Dosyasını Yerleştirin**
   - HTML dosyanızı `aipictureprompts.html` olarak kaydedin
   - Script ile aynı klasöre koyun

3. **Scripti Çalıştırın**
   ```bash
   python ai_image_generator.py
   ```

## Script Ne Yapar?

1. ✅ HTML'deki tüm kategorileri ve stilleri analiz eder
2. ✅ Her kategori için Claude'dan **basit** bir temel prompt ister (SIRAYLA)
   - 1-2 cümlelik basit, temel prompt
3. ✅ "Format" kategorisindeyse, her stil için Claude'a boyut sorar
4. ✅ Her stil için DALL-E ile görsel üretir
   - Format: `"Category: [Türkçe] ([İngilizce]), Style: [Stil], [temel_prompt], Category: [Türkçe] ([İngilizce]), Style: [Stil]"`
   - Örnek: `"Category: Görsel Tarzı (style), Style: Realistik (Realistic), [basit prompt], Category: Görsel Tarzı (style), Style: Realistik (Realistic)"`
5. ✅ Görselleri şu formatta kaydeder: `001_style_001_realistic.png`
6. ✅ Her görsel için 150x150px thumbnail oluşturur
7. ✅ HTML'e thumbnail ekler (option elementinin içine)
8. ✅ Lightbox/modal sistemi ekler (tıklayınca büyüsün)
9. ✅ Güncellenmiş HTML'i `aipictureprompts_updated.html` olarak kaydeder

## Özellikler

- 🔄 **Sıralı İşlem**: Kategoriler ve stiller sırayla işlenir (karışma olmaz)
- 🎨 **Akıllı Boyutlandırma**: Format kategorisinde Claude'a boyut sorulur
- 🖼️ **Lightbox**: Resimlere tıklayınca büyür, ESC/X ile kapanır
- ⏱️ **Rate Limiting**: Her API isteği arası 2 saniye bekleme
- 🔁 **Otomatik Retry**: Her hata için 3 kez otomatik deneme
- 💾 **Progress Tracking**: Kaldığı yerden devam edebilme
- 🛡️ **Hata Yönetimi**: Hata olunca kullanıcıya sor (tekrar dene/atla/dur)
- 🌍 **Türkçe Karakter Temizleme**: Dosya adlarında İngilizce karakter kullanır

## Progress Sistemi

Script çalışırken `progress.json` dosyası oluşturur:
- ✅ Tamamlanan her görsel kaydedilir
- ✅ Script dursa bile kaldığı yerden devam edebilir
- ✅ Baştan başlamak istersen progress'i temizleyebilirsin

### Hata Durumunda:
Script 3 kez otomatik denedikten sonra başarısız olursa sorar:
```
❌ 3 deneme sonrası başarısız!
🔄 Ne yapmak istersiniz?
   1 - Tekrar dene
   2 - Bu görseli atla, devam et
   3 - Scripti durdur
```

## Çıktılar

- 📁 `generated_images/` - Tüm üretilen görseller
- 📄 `aipictureprompts_updated.html` - Güncellenmiş HTML dosyası
- 💾 `progress.json` - İlerleme kaydı (kaldığı yerden devam için)

## Notlar

- DALL-E 3 varsayılan boyut: 1024x1024
- Format kategorisi için: Claude'dan 1024x1024, 1024x1792 veya 1792x1024 önerilir
- Her request arası 2 saniye bekleme (API limitleri için)
- Thumbnail boyutu: 150x150px

## Sorun Giderme

**"API key not found" hatası:**
- Script içindeki API keyleri kontrol edin

**"HTML file not found" hatası:**
- HTML dosyasının adını `aipictureprompts.html` yapın
- Script ile aynı dizinde olduğundan emin olun

**API hataları:**
- İnternet bağlantınızı kontrol edin
- API key kotalarını kontrol edin
- Script devam eder, başarısız olanları loglar

Keyifli çalışmalar! 🎨✨
