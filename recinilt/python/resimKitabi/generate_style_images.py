#!/usr/bin/env python3
"""
HTML dosyasındaki görsel stillerini okur, her biri için OpenAI DALL-E ile görsel oluşturur
ve görselleri HTML'e geri ekler.
"""

import os
import re
import time
from pathlib import Path
from openai import OpenAI
import requests
from bs4 import BeautifulSoup

# OpenAI API anahtarınızı buraya ekleyin
API_KEY = os.getenv("OPENAI_API_KEY", "your-api-key-here")

def extract_styles_from_html(html_path):
    """HTML dosyasından tüm stil seçeneklerini çıkarır"""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Tüm option div'lerini bul
    options = soup.find_all('div', class_='option')
    
    styles = []
    for idx, option in enumerate(options, start=1):
        text = option.get_text(strip=True)
        styles.append({
            'number': f"{idx:03d}",  # 001, 002, etc.
            'text': text,
            'element': option
        })
    
    return styles, soup, content

def create_safe_filename(text):
    """Dosya adı için güvenli string oluşturur"""
    # Parantez içindeki İngilizce kısmı al
    english_match = re.search(r'\(([^)]+)\)', text)
    if english_match:
        base = english_match.group(1)
    else:
        base = text
    
    # Dosya adı için güvenli hale getir
    safe = re.sub(r'[^\w\s-]', '', base)
    safe = re.sub(r'[-\s]+', '_', safe)
    return safe.strip('_')

def generate_image_with_dalle(client, style_text, number):
    """OpenAI DALL-E kullanarak görsel oluşturur"""
    print(f"\n[{number}] '{style_text}' için görsel oluşturuluyor...")
    
    # Prompt oluştur - stilin İngilizce versiyonunu kullan
    english_match = re.search(r'\(([^)]+)\)', style_text)
    if english_match:
        style = english_match.group(1)
    else:
        style = style_text
    
    prompt = f"A beautiful artistic demonstration of {style} art style, high quality, detailed"
    
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        
        image_url = response.data[0].url
        print(f"✓ Görsel URL alındı: {image_url[:50]}...")
        
        return image_url
    
    except Exception as e:
        print(f"✗ Hata oluştu: {e}")
        return None

def download_image(url, filepath):
    """Görseli indirir ve kaydeder"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        print(f"✓ Görsel kaydedildi: {filepath}")
        return True
    
    except Exception as e:
        print(f"✗ Görsel indirme hatası: {e}")
        return False

def update_html_with_images(soup, styles, images_folder):
    """HTML'i görseller ile günceller"""
    for style_data in styles:
        number = style_data['number']
        text = style_data['text']
        element = style_data['element']
        
        safe_name = create_safe_filename(text)
        image_filename = f"{number}_{safe_name}.png"
        
        # Görsel varsa img etiketi ekle
        image_path = images_folder / image_filename
        if image_path.exists():
            # Mevcut img etiketini kaldır (varsa)
            existing_img = element.find('img')
            if existing_img:
                existing_img.decompose()
            
            # Yeni img etiketi oluştur
            img_tag = soup.new_tag('img', src=f"images/{image_filename}", width="50")
            element.append(" ")
            element.append(img_tag)
            print(f"✓ HTML güncellendi: {text}")
    
    return soup

def main():
    print("=" * 60)
    print("HTML Stil Görselleri Oluşturucu")
    print("=" * 60)
    
    # API anahtarı kontrolü
    if API_KEY == "your-api-key-here":
        print("\n⚠️  UYARI: OpenAI API anahtarınızı ayarlayın!")
        print("Scripti çalıştırmadan önce OPENAI_API_KEY environment variable'ını")
        print("ayarlayın veya kodda API_KEY değişkenini güncelleyin.\n")
        print("Windows: set OPENAI_API_KEY=sk-your-api-key-here")
        print("Linux/Mac: export OPENAI_API_KEY='sk-your-api-key-here'")
        return
    
    # Dosya yolları - scriptin bulunduğu klasör
    script_dir = Path(__file__).parent
    
    # HTML dosyasını bul
    html_files = list(script_dir.glob("*.html"))
    if not html_files:
        print("\n❌ HATA: Bu klasörde HTML dosyası bulunamadı!")
        print(f"Klasör: {script_dir}")
        return
    
    # İlk HTML dosyasını kullan (veya aipictureprompts.html varsa onu)
    input_html = None
    for html_file in html_files:
        if "aipictureprompts" in html_file.name.lower():
            input_html = html_file
            break
    if not input_html:
        input_html = html_files[0]
    
    output_html = script_dir / f"{input_html.stem}_with_images.html"
    images_folder = script_dir / "images"
    
    # Klasör oluştur
    images_folder.mkdir(exist_ok=True)
    
    print(f"\n📁 Çalışma Klasörü: {script_dir}")
    print(f"📄 HTML Dosyası: {input_html.name}")
    
    # OpenAI client oluştur
    client = OpenAI(api_key=API_KEY)
    
    # HTML'den stilleri çıkar
    print(f"\n1. HTML dosyası okunuyor...")
    styles, soup, original_content = extract_styles_from_html(input_html)
    print(f"✓ {len(styles)} stil bulundu")
    
    # Her stil için görsel oluştur
    print(f"\n2. Görseller oluşturuluyor (toplam {len(styles)})...")
    print("   Bu işlem uzun sürebilir...\n")
    
    for style_data in styles:
        number = style_data['number']
        text = style_data['text']
        
        # Dosya adı oluştur
        safe_name = create_safe_filename(text)
        image_filename = f"{number}_{safe_name}.png"
        image_path = images_folder / image_filename
        
        # Görsel zaten varsa atla
        if image_path.exists():
            print(f"[{number}] Görsel zaten mevcut, atlanıyor: {text}")
            continue
        
        # Görsel oluştur
        image_url = generate_image_with_dalle(client, text, number)
        
        if image_url:
            # Görseli indir
            download_image(image_url, image_path)
            
            # Rate limiting için bekle (OpenAI limitleri için)
            time.sleep(2)
        else:
            print(f"⚠️  Görsel oluşturulamadı, devam ediliyor...")
    
    # HTML'i güncelle
    print(f"\n3. HTML dosyası güncelleniyor...")
    updated_soup = update_html_with_images(soup, styles, images_folder)
    
    # Güncellenmiş HTML'i kaydet
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(str(updated_soup.prettify()))
    
    print(f"\n✓ İşlem tamamlandı!")
    print(f"✓ Güncellenmiş HTML: {output_html}")
    print(f"✓ Görseller: {images_folder}")
    print(f"✓ Toplam {len(list(images_folder.glob('*.png')))} görsel oluşturuldu")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
