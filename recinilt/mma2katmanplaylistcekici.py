#!/usr/bin/env python3
"""
YouTube Playlist Scraper
Bu program bir YouTube playlist'indeki tüm videoların isimlerini ve linklerini çeker.
"""

import subprocess
import json
import sys

def get_playlist_videos(playlist_url):
    """
    YouTube playlist URL'sinden video bilgilerini çeker.
    
    Args:
        playlist_url: YouTube playlist URL'si
        
    Returns:
        Video bilgilerini içeren liste
    """
    try:
        # yt-dlp komutu ile playlist bilgilerini JSON formatında al
        cmd = [
            'yt-dlp',
            '--flat-playlist',
            '--dump-json',
            playlist_url
        ]
        
        print("Playlist bilgileri çekiliyor...")
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # Her satır bir JSON objesi içeriyor
        videos = []
        for line in result.stdout.strip().split('\n'):
            if line:
                video_data = json.loads(line)
                videos.append({
                    'title': video_data.get('title', 'Bilinmeyen Başlık'),
                    'url': f"https://www.youtube.com/watch?v={video_data.get('id', '')}"
                })
        
        return videos
        
    except subprocess.CalledProcessError as e:
        print(f"Hata: yt-dlp komutu başarısız oldu.")
        print(f"Hata mesajı: {e.stderr}")
        return None
    except json.JSONDecodeError as e:
        print(f"Hata: JSON parse edilemedi: {e}")
        return None
    except Exception as e:
        print(f"Beklenmeyen hata: {e}")
        return None

def create_js_array(videos, output_file='video_listesi.txt'):
    """
    Video listesini JavaScript array formatında dosyaya yazar.
    
    Args:
        videos: Video bilgilerini içeren liste
        output_file: Çıktı dosyası adı
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('const videoListesi = [\n')
        
        for i, video in enumerate(videos):
            # Başlıkta özel karakterleri escape et
            title = video['title'].replace('\\', '\\\\').replace('"', '\\"')
            url = video['url']
            
            # Son eleman değilse virgül ekle
            comma = ',' if i < len(videos) - 1 else ''
            
            f.write(f'        {{ isim: "{title}", url: "{url}" }}{comma}\n')
        
        f.write('    ];\n')
    
    print(f"\n✓ {len(videos)} video bilgisi '{output_file}' dosyasına kaydedildi!")

def install_ytdlp():
    """yt-dlp'yi yükler"""
    print("yt-dlp yükleniyor...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--break-system-packages', 'yt-dlp'], 
                      check=True, capture_output=True)
        print("✓ yt-dlp başarıyla yüklendi!")
        return True
    except:
        print("✗ yt-dlp yüklenemedi!")
        return False

def main():
    # Playlist URL'si
    playlist_url = "https://www.youtube.com/watch?v=spTTbAHOpHY&list=PLOQwr___h1ioMxs68G9a5c4qdn96h50vn&index=1"
    
    # yt-dlp'nin yüklü olup olmadığını kontrol et
    try:
        subprocess.run(['yt-dlp', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("yt-dlp bulunamadı. Yükleniyor...")
        if not install_ytdlp():
            print("Program sonlandırılıyor.")
            return
    
    # Video bilgilerini çek
    videos = get_playlist_videos(playlist_url)
    
    if videos:
        print(f"\nToplam {len(videos)} video bulundu.\n")
        
        # İlk birkaç videoyu göster
        print("İlk 3 video:")
        for i, video in enumerate(videos[:3], 1):
            print(f"{i}. {video['title']}")
            print(f"   {video['url']}\n")
        
        # Dosyaya kaydet
        create_js_array(videos)
    else:
        print("Video bilgileri alınamadı.")

if __name__ == "__main__":
    main()
