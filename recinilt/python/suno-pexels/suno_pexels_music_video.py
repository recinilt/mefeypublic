#!/usr/bin/env python3
"""
🎵 Suno Müzik Klibi - Gerçek Video Edition
Lokal Bilgisayar Versiyonu

Özellikler:
- 🤖 Claude AI şarkı analizi
- 🎬 Pexels API ile gerçek stok videolar
- 📝 Altyazı desteği
- 🎨 Profesyonel videolar
- ⚡ Hızlı işlem
"""

import os
import json
import re
import time
import requests
import warnings
from datetime import datetime
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import anthropic
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip

warnings.filterwarnings('ignore')

# ==================== YAPILANDIRMA ====================

class Config:
    """Video ayarları"""
    
    # API Anahtarları
    ANTHROPIC_API_KEY = "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"  # https://console.anthropic.com/
    PEXELS_API_KEY = "pfvzXIvROsoXKIGt9yrXQVRz8UFgrO0lkvsleIYPxyRbzM8QrkhwefQ0"  # https://www.pexels.com/api/ (ÜCRETSİZ)
    
    # Video Formatı
    RESOLUTION_OPTIONS = {
        '1': ('TikTok/Reels - Dikey', (1080, 1920)),
        '2': ('YouTube - Yatay', (1920, 1080)),
        '3': ('Instagram - Kare', (1080, 1080))
    }
    
    # Video Kalitesi
    QUALITY_OPTIONS = {
        '1': ('HD (1280x720)', 'large'),
        '2': ('SD (640x360)', 'medium')
    }
    
    # Varsayılan ayarlar
    DEFAULT_RESOLUTION = (1080, 1920)  # Dikey
    DEFAULT_QUALITY = 'large'  # HD
    USE_SUBTITLES = True
    
    # Çıktı klasörü
    OUTPUT_DIR = "output"
    VIDEOS_DIR = "videos"

# ==================== YARDIMCI FONKSİYONLAR ====================

def print_header(text):
    """Başlık yazdır"""
    print(f"\n{'=' * 60}")
    print(f"  {text}")
    print(f"{'=' * 60}\n")

def check_api_keys():
    """API anahtarlarını kontrol et"""
    print_header("🔑 API Anahtarları Kontrol Ediliyor")
    
    if "xxxxx" not in Config.ANTHROPIC_API_KEY:
        print("✅ Anthropic API OK")
    else:
        print("❌ Anthropic API eksik!")
        print("   👉 https://console.anthropic.com/ adresinden alın")
        return False
    
    if "xxxxx" not in Config.PEXELS_API_KEY:
        print("✅ Pexels API OK")
    else:
        print("❌ Pexels API eksik!")
        print("   👉 https://www.pexels.com/api/ adresinden ücretsiz alın")
        return False
    
    return True

def setup_directories():
    """Gerekli klasörleri oluştur"""
    Path(Config.OUTPUT_DIR).mkdir(exist_ok=True)
    Path(Config.VIDEOS_DIR).mkdir(exist_ok=True)
    print("✅ Klasörler hazır")

def get_user_settings():
    """Kullanıcıdan ayarları al"""
    print_header("⚙️ Video Ayarları")
    
    # Format seçimi
    print("📱 Video Formatı:")
    for key, (name, _) in Config.RESOLUTION_OPTIONS.items():
        print(f"  {key}. {name}")
    
    choice = input("\nSeçiminiz (1-3, Enter=1): ").strip() or '1'
    _, resolution = Config.RESOLUTION_OPTIONS.get(choice, ('', Config.DEFAULT_RESOLUTION))
    
    # Kalite seçimi
    print("\n🎬 Video Kalitesi:")
    for key, (name, _) in Config.QUALITY_OPTIONS.items():
        print(f"  {key}. {name}")
    
    choice = input("\nSeçiminiz (1-2, Enter=1): ").strip() or '1'
    _, quality = Config.QUALITY_OPTIONS.get(choice, ('', Config.DEFAULT_QUALITY))
    
    # Altyazı seçimi
    subtitle = input("\n📝 Altyazı eklensin mi? (E/h, Enter=E): ").strip().lower() != 'h'
    
    print(f"\n✨ Ayarlar kaydedildi:")
    print(f"   - Format: {resolution[0]}x{resolution[1]}")
    print(f"   - Kalite: {quality}")
    print(f"   - Altyazı: {'Evet' if subtitle else 'Hayır'}")
    
    return {
        'resolution': resolution,
        'quality': quality,
        'use_subtitles': subtitle
    }

def get_lyrics():
    """Şarkı sözlerini al"""
    print_header("📝 Şarkı Sözleri")
    
    print("Nasıl girmek istersiniz?")
    print("  1. Manuel yazacağım")
    print("  2. Dosyadan yükle (.txt)")
    
    choice = input("\nSeçim (1-2, Enter=1): ").strip() or '1'
    
    lyrics = None
    
    if choice == '2':
        # Dosyadan yükle
        try:
            import tkinter as tk
            from tkinter import filedialog
            
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            
            print("\n📂 Dosya seçici açılıyor...")
            
            file_path = filedialog.askopenfilename(
                title="Şarkı Sözü Dosyası Seçin",
                filetypes=[
                    ("Metin Dosyaları", "*.txt"),
                    ("Tüm Dosyalar", "*.*")
                ]
            )
            
            root.destroy()
            
            if file_path and os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    lyrics = f.read().strip()
                print(f"✅ Dosya yüklendi: {os.path.basename(file_path)}")
            else:
                print("❌ Dosya seçilmedi, manuel girişe geçiliyor...")
                choice = '1'
        except ImportError:
            print("⚠️ Tkinter bulunamadı, manuel girişe geçiliyor...")
            choice = '1'
    
    if choice == '1' or not lyrics:
        # Manuel giriş
        print("\nŞarkı sözlerini girin (bitirmek için boş satırda Ctrl+D veya Ctrl+Z):")
        print("(Manuel zamanlama için: [0:00] Şarkı sözü formatını kullanın)\n")
        
        lines = []
        try:
            while True:
                line = input()
                lines.append(line)
        except EOFError:
            pass
        
        lyrics = '\n'.join(lines).strip()
    
    if not lyrics:
        print("❌ Şarkı sözü girilmedi!")
        return None
    
    use_auto_mode = '[' not in lyrics
    print(f"\n{'🤖 Otomatik' if use_auto_mode else '✏️ Manuel'} mod aktif")
    
    return lyrics, use_auto_mode

def get_audio_file():
    """Ses dosyasını al"""
    print_header("🎵 Ses Dosyası")
    
    # Tkinter dosya seçici
    try:
        import tkinter as tk
        from tkinter import filedialog
        
        # Gizli root pencere oluştur
        root = tk.Tk()
        root.withdraw()  # Ana pencereyi gizle
        root.attributes('-topmost', True)  # Ön planda göster
        
        print("📂 Dosya seçici açılıyor...")
        
        audio_path = filedialog.askopenfilename(
            title="MP3 Dosyası Seçin",
            filetypes=[
                ("Ses Dosyaları", "*.mp3 *.wav *.m4a *.flac *.ogg"),
                ("MP3 Dosyaları", "*.mp3"),
                ("Tüm Dosyalar", "*.*")
            ]
        )
        
        root.destroy()  # Root penceresini kapat
        
        if not audio_path:
            print("❌ Dosya seçilmedi!")
            return None, None
            
    except ImportError:
        # Tkinter yoksa manuel giriş
        print("⚠️ Tkinter bulunamadı, manuel giriş yapın:")
        audio_path = input("MP3 dosya yolu: ").strip()
    
    if not os.path.exists(audio_path):
        print(f"❌ Dosya bulunamadı: {audio_path}")
        return None, None
    
    try:
        audio = AudioFileClip(audio_path)
        duration = audio.duration
        audio.close()
        
        print(f"✅ Yüklendi: {os.path.basename(audio_path)}")
        print(f"📁 Konum: {audio_path}")
        print(f"⏱️ Süre: {int(duration//60)}:{int(duration%60):02d}")
        
        return audio_path, duration
    except Exception as e:
        print(f"❌ Ses dosyası okunamadı: {e}")
        return None, None

# ==================== CLAUDE AI ANALİZİ ====================

def analyze_with_claude(lyrics, duration):
    """Claude AI ile şarkı analizi"""
    client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
    
    prompt = f"""Müzik videosu için şarkı analizi. Her satır için:
1. Video konsepti (Pexels'te aranacak)
2. Zamanlama (toplam: {duration:.1f}s)
3. İngilizce arama kelimeleri (max 3 kelime)

ŞARKI:
{lyrics}

JSON formatı:
{{
  "scenes": [
    {{
      "line": "şarkı sözü",
      "description": "video konsepti (Türkçe)",
      "start_time": 0.0,
      "end_time": 8.0,
      "search_query": "ocean sunset"
    }}
  ]
}}

KURALLAR:
- Intro/outro için de sahne ekle
- Her sahne 5-10 saniye
- Zamanlamalar kesintisiz
- Arama kelimeleri basit ve genel (nature, city, night gibi)
- Şarkının duygusuna uygun videolar
- Sadece JSON çıktısı
"""
    
    print("🧠 Claude şarkınızı analiz ediyor...")
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    text = response.content[0].text
    json_match = re.search(r'\{.*\}', text, re.DOTALL)
    
    if json_match:
        result = json.loads(json_match.group())
        print(f"✅ {len(result['scenes'])} sahne oluşturuldu")
        return result['scenes']
    else:
        print("❌ Analiz başarısız!")
        return None

def parse_manual_lyrics(lyrics, duration):
    """Manuel zamanlamalı şarkı sözlerini ayrıştır"""
    print("✏️ Manuel zamanlamalar işleniyor...")
    
    scenes = []
    lines = lyrics.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Format 1: [0:00] Şarkı sözü
        match1 = re.match(r'\[(\d+):(\d+)\]\s*(.+)', line)
        if match1:
            mins, secs, text = match1.groups()
            start_time = int(mins) * 60 + int(secs)
            scenes.append({
                'line': text.strip(),
                'start_time': start_time,
                'end_time': None  # Sonra hesaplanacak
            })
            continue
        
        # Format 2: Şarkı sözü[başlangıç-bitiş]
        match2 = re.match(r'(.+?)\[(\d+)-(\d+)\]', line)
        if match2:
            text, start, end = match2.groups()
            scenes.append({
                'line': text.strip(),
                'start_time': int(start),
                'end_time': int(end)
            })
            continue
    
    if not scenes:
        print("❌ Hiç zamanlama bulunamadı!")
        print("   Desteklenen formatlar:")
        print("   - [0:00] Şarkı sözü")
        print("   - Şarkı sözü[0-14]")
        return None
    
    # Format 1 için bitiş zamanlarını hesapla
    for i in range(len(scenes)):
        if scenes[i]['end_time'] is None:
            if i < len(scenes) - 1:
                scenes[i]['end_time'] = scenes[i+1]['start_time']
            else:
                scenes[i]['end_time'] = duration
    
    print(f"✅ {len(scenes)} sahne bulundu")
    
    # Claude AI ile akıllı arama kelimeleri üret
    print("🤖 Claude AI ile arama kelimeleri oluşturuluyor...")
    
    try:
        client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
        
        # Şarkı sözlerini numaralı liste olarak hazırla
        numbered_lyrics = "\n".join([f"{i+1}. {s['line']}" for i, s in enumerate(scenes)])
        
        prompt = f"""Bu şarkı sözlerinin her satırı için Pexels'te aranacak İngilizce anahtar kelimeler üret.

ŞARKI SÖZLERİ:
{numbered_lyrics}

Her satır için 2-3 kelimelik basit İngilizce arama terimi ver. 
Şarkının duygusuna ve anlamına uygun, Pexels'te bulunabilecek videolar:
- Doğa (nature, ocean, mountains, forest, sky, sunset, stars)
- Şehir (city, urban, night, lights, streets)
- İnsanlar (people, running, dancing, meditation, yoga, walking)
- Soyut (abstract, particles, light, water, fire, flowing)
- Duygular (freedom, love, peace, energy, spiritual, joy)

ÖNEMLI: Tam olarak {len(scenes)} adet anahtar kelime ver, sırayla.

JSON formatı:
{{
  "keywords": [
    "kelime1 kelime2",
    "kelime1 kelime2",
    ...
  ]
}}

Sadece JSON çıktısı ver, başka açıklama yapma."""

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        text = response.content[0].text
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        
        if json_match:
            result = json.loads(json_match.group())
            keywords = result.get('keywords', [])
            
            # Anahtar kelimeleri sahnelere ata
            if len(keywords) == len(scenes):
                for i, scene in enumerate(scenes):
                    scene['search_query'] = keywords[i]
                    scene['description'] = f"Sahne {i+1}: {scene['line'][:30]}"
                print(f"✅ Claude AI ile {len(keywords)} anahtar kelime üretildi")
            else:
                print(f"⚠️ Kelime sayısı uyuşmuyor ({len(keywords)} != {len(scenes)}), fallback kullanılıyor...")
                raise Exception("Keyword count mismatch")
                
        else:
            raise Exception("JSON parse hatası")
            
    except Exception as e:
        print(f"⚠️ Claude AI kullanılamadı ({e}), varsayılan kelimeler kullanılıyor...")
        
        # Basit kelime eşleştirme (fallback)
        keyword_map = {
            'koş': 'running person', 'deniz': 'ocean waves', 'gökyüzü': 'blue sky',
            'yıldız': 'stars night', 'gece': 'night sky', 'gün': 'sunny day',
            'güneş': 'sun light', 'ay': 'moon night', 'orman': 'forest nature',
            'dağ': 'mountain landscape', 'şehir': 'city lights', 'yol': 'road path',
            'su': 'water flowing', 'ateş': 'fire flames', 'rüzgar': 'wind nature',
            'bulut': 'clouds sky', 'çiçek': 'flowers nature', 'ağaç': 'tree forest',
            'sevgi': 'love heart', 'özgür': 'freedom sky', 'uç': 'flying bird',
            'dans': 'dancing people', 'müzik': 'music concert', 'robot': 'robot technology',
            'hakikat': 'spiritual light', 'tekamül': 'evolution nature',
            'evrim': 'transformation', 'bilinç': 'meditation zen', 'çay': 'tea peaceful',
            'secde': 'prayer spiritual', 'varoluş': 'universe space', 'ara': 'searching alone',
            'hipnoz': 'hypnotic swirl', 'şartlan': 'chains breaking', 'mükafat': 'trophy reward',
            'karakter': 'theater mask', 'oyna': 'acting performance', 'anla': 'lightbulb moment',
            'yalnız': 'lonely person', 'yarış': 'race track', 'teşekkür': 'grateful hands',
            'söndür': 'extinguish fire', 'eriş': 'reaching goal', 'eri': 'melting ice',
            'hatırla': 'memory brain', 'kahkaha': 'laughing happy', 'yerli': 'balanced zen',
            'bak': 'observing eye', 'yavaş': 'slow motion', 'koku': 'smelling flowers',
            'gocun': 'calm peaceful'
        }
        
        for i, scene in enumerate(scenes):
            text_lower = scene['line'].lower()
            found_keyword = None
            
            for tr_word, en_phrase in keyword_map.items():
                if tr_word in text_lower:
                    found_keyword = en_phrase
                    break
            
            scene['search_query'] = found_keyword or "abstract meditation"
            scene['description'] = f"Sahne {i+1}: {scene['line'][:30]}"
    
    # İlk birkaç sahneyi göster
    print("\n📋 İlk 5 sahne:")
    for i, scene in enumerate(scenes[:5], 1):
        print(f"   {i}. [{scene['start_time']:.0f}s-{scene['end_time']:.0f}s] "
              f"{scene['line'][:40]} → '{scene['search_query']}'")
    if len(scenes) > 5:
        print(f"   ... ve {len(scenes)-5} sahne daha")
    
    return scenes

# ==================== PEXELS API ====================

def search_pexels_video(query, orientation='portrait', size='large'):
    """Pexels'te video ara"""
    url = "https://api.pexels.com/videos/search"
    headers = {"Authorization": Config.PEXELS_API_KEY}
    params = {
        "query": query,
        "orientation": orientation,
        "size": size,
        "per_page": 5
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            
            if data.get('videos'):
                video = data['videos'][0]
                
                for file in video['video_files']:
                    if file['quality'] == size:
                        return file['link']
                
                return video['video_files'][0]['link']
        
        return None
    except Exception as e:
        print(f"   ⚠️ Arama hatası: {e}")
        return None

def download_video(url, filepath):
    """Video indir"""
    try:
        response = requests.get(url, stream=True, timeout=30)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
    except Exception as e:
        print(f"   ⚠️ İndirme hatası: {e}")
    
    return False

def download_all_videos(scenes, settings):
    """Tüm videoları indir"""
    print_header("📥 Videolar İndiriliyor")
    
    # Oryantasyon belirle
    width, height = settings['resolution']
    orientation = 'portrait' if height > width else 'landscape'
    
    for i, scene in enumerate(scenes, 1):
        print(f"🎬 Sahne {i}/{len(scenes)}")
        print(f"   📝 {scene.get('line', scene['description'])[:50]}")
        print(f"   🔍 Aranıyor: '{scene['search_query']}'")
        
        video_url = search_pexels_video(
            scene['search_query'],
            orientation=orientation,
            size=settings['quality']
        )
        
        if video_url:
            video_path = os.path.join(Config.VIDEOS_DIR, f"scene_{i:03d}.mp4")
            print(f"   📥 İndiriliyor...")
            
            if download_video(video_url, video_path):
                scene['video_path'] = video_path
                print(f"   ✅ Kaydedildi: {video_path}")
                
                try:
                    clip = VideoFileClip(video_path)
                    print(f"   ⏱️ Video süresi: {clip.duration:.1f}s")
                    clip.close()
                except:
                    pass
            else:
                print(f"   ❌ İndirilemedi!")
                scene['video_path'] = None
        else:
            print(f"   ⚠️ Video bulunamadı: '{scene['search_query']}'")
            scene['video_path'] = None
        
        time.sleep(1)
        print()
    
    successful = sum(1 for s in scenes if s.get('video_path'))
    print(f"📊 Sonuç: {successful}/{len(scenes)} video başarıyla indirildi\n")
    
    if successful < len(scenes):
        print("⚠️ Bazı videolar bulunamadı.")

# ==================== VİDEO OLUŞTURMA ====================

def add_subtitle_to_frame(image, subtitle_text):
    """Frame'e altyazı ekle"""
    img = Image.fromarray(image.astype('uint8'))
    draw = ImageDraw.Draw(img)
    
    # Font yükle
    font_paths = [
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
        '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
        'C:/Windows/Fonts/arial.ttf',  # Windows
        '/System/Library/Fonts/Helvetica.ttc'  # macOS
    ]
    
    font = None
    for font_path in font_paths:
        try:
            font = ImageFont.truetype(font_path, 32)
            break
        except:
            continue
    
    if font is None:
        font = ImageFont.load_default()
    
    # Uzun metinleri böl
    max_chars = 35
    if len(subtitle_text) > max_chars:
        words = subtitle_text.split()
        mid = len(words) // 2
        lines = [' '.join(words[:mid]), ' '.join(words[mid:])]
    else:
        lines = [subtitle_text]
    
    img_width, img_height = img.size
    y_offset = img_height - 120 - (len(lines) * 50)
    
    for line_text in lines:
        # Metin genişliğini hesapla
        try:
            bbox = draw.textbbox((0, 0), line_text, font=font)
            text_width = bbox[2] - bbox[0]
        except:
            text_width = len(line_text) * 20
        
        x_pos = (img_width - text_width) // 2
        
        # Siyah gölge (kontur)
        for offset_x in [-3, -2, -1, 0, 1, 2, 3]:
            for offset_y in [-3, -2, -1, 0, 1, 2, 3]:
                if offset_x != 0 or offset_y != 0:
                    draw.text(
                        (x_pos + offset_x, y_offset + offset_y),
                        line_text,
                        font=font,
                        fill='black'
                    )
        
        # Beyaz metin
        draw.text((x_pos, y_offset), line_text, font=font, fill='white')
        y_offset += 50
    
    return np.array(img)

def create_final_video(scenes, audio_path, settings):
    """Final videoyu oluştur"""
    print_header("🎬 Final Video Oluşturuluyor")
    
    video_clips = []
    width, height = settings['resolution']
    
    for i, scene in enumerate(scenes, 1):
        if not scene.get('video_path'):
            print(f"⏭️ Sahne {i} atlandı (video yok)")
            continue
        
        duration = scene['end_time'] - scene['start_time']
        
        print(f"🎞️ {i}/{len(scenes)}: İşleniyor...")
        clip = VideoFileClip(scene['video_path'])
        
        # Video süresini ayarla
        if clip.duration < duration:
            clip = clip.loop(duration=duration)
        else:
            clip = clip.subclip(0, min(clip.duration, duration))
        
        # Resize işlemini cv2 ile yap (PIL uyumluluk sorunu yok)
        def resize_frame(frame):
            import cv2
            return cv2.resize(frame, (width, height), interpolation=cv2.INTER_LINEAR)
        
        clip = clip.fl_image(resize_frame)
        clip = clip.set_duration(duration)
        clip = clip.set_start(scene['start_time'])
        
        # Altyazı ekle
        if settings['use_subtitles'] and 'line' in scene:
            print(f"   📝 Altyazı ekleniyor...")
            
            # Lambda closure sorununu önlemek için fonksiyon fabrikası kullan
            def make_subtitle_func(text):
                def add_subtitle_wrapper(frame):
                    return add_subtitle_to_frame(frame, text)
                return add_subtitle_wrapper
            
            clip = clip.fl_image(make_subtitle_func(scene['line']))
        
        # Geçiş efekti
        fade = min(0.5, duration / 4)
        clip = clip.crossfadein(fade).crossfadeout(fade)
        
        video_clips.append(clip)
        print(f"   ✓ Hazır [{scene['start_time']:.1f}-{scene['end_time']:.1f}s]")
    
    if not video_clips:
        print("\n❌ Hiç video yok! Lütfen önce videoları indirin.")
        return None
    
    # Ses ekle
    print("\n🔊 Ses ekleniyor...")
    audio = AudioFileClip(audio_path)
    
    # Videoları birleştir
    print("🎞️ Videolar birleştiriliyor...")
    final = CompositeVideoClip(video_clips, size=(width, height))
    final = final.set_audio(audio).set_duration(audio.duration)
    
    # Kaydet
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output = os.path.join(Config.OUTPUT_DIR, f"music_video_{timestamp}.mp4")
    
    print(f"\n💾 Kaydediliyor: {output}")
    print("⏱️ Bu işlem birkaç dakika sürebilir...\n")
    
    final.write_videofile(
        output,
        fps=30,
        codec='libx264',
        audio_codec='aac',
        preset='medium',
        threads=4
    )
    
    # Temizlik
    for clip in video_clips:
        clip.close()
    audio.close()
    final.close()
    
    print(f"\n🎉🎉🎉 TAMAMLANDI! 🎉🎉🎉")
    print(f"\n📹 Video: {output}")
    print(f"⏱️ Süre: {int(audio.duration//60)}:{int(audio.duration%60):02d}")
    print(f"🎨 Sahne: {len(video_clips)}")
    print(f"🎬 Kaynak: Gerçek videolar (Pexels)")
    
    return output

# ==================== ANA PROGRAM ====================

def main():
    """Ana program"""
    print_header("🎵 Suno Müzik Klibi Oluşturucu")
    print("Gerçek Video Edition - Lokal Versiyon\n")
    
    # 1. API anahtarlarını kontrol et
    if not check_api_keys():
        return
    
    # 2. Klasörleri hazırla
    setup_directories()
    
    # 3. Kullanıcı ayarları
    settings = get_user_settings()
    
    # 4. Şarkı sözleri
    lyrics_data = get_lyrics()
    if not lyrics_data:
        return
    
    lyrics, use_auto_mode = lyrics_data
    
    # 5. Ses dosyası
    audio_path, duration = get_audio_file()
    if not audio_path:
        return
    
    # 6. Sahne analizi
    print_header("🧠 Sahne Analizi")
    
    if use_auto_mode:
        scenes = analyze_with_claude(lyrics, duration)
    else:
        scenes = parse_manual_lyrics(lyrics, duration)
    
    if not scenes:
        print("❌ Sahne oluşturulamadı!")
        return
    
    # Sahne listesini göster
    print("\n📋 Sahne Listesi:")
    for i, scene in enumerate(scenes, 1):
        print(f"{i}. [{scene['start_time']:.1f}s-{scene['end_time']:.1f}s] "
              f"{scene.get('line', scene['description'])[:40]} - '{scene['search_query']}'")
    
    # 7. Videoları indir
    proceed = input("\n📥 Videoları indirmeye başlayalım mı? (E/h): ").strip().lower()
    if proceed != 'e' and proceed != '':
        print("❌ İptal edildi.")
        return
    
    download_all_videos(scenes, settings)
    
    # 8. Final video
    proceed = input("\n🎬 Final videoyu oluşturalım mı? (E/h): ").strip().lower()
    if proceed != 'e' and proceed != '':
        print("❌ İptal edildi.")
        return
    
    output_file = create_final_video(scenes, audio_path, settings)
    
    if output_file:
        print(f"\n✅ Video hazır: {output_file}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Program kullanıcı tarafından durduruldu.")
    except Exception as e:
        print(f"\n❌ Hata: {e}")
        import traceback
        traceback.print_exc()
