#!/usr/bin/env python3
"""
Test scripti - Sadece ilk 3 stil için görsel oluşturur
API anahtarınızı test etmek için kullanın
"""

import os
import re
import time
from pathlib import Path
from openai import OpenAI
import requests
from bs4 import BeautifulSoup

# API anahtarı
API_KEY = os.getenv("OPENAI_API_KEY", "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")

def test_api():
    """API anahtarını ve bağlantıyı test eder"""
    print("=" * 60)
    print("OpenAI API Test")
    print("=" * 60)
    
    if API_KEY == "your-api-key-here":
        print("\n❌ HATA: OpenAI API anahtarı ayarlanmamış!")
        print("\nLütfen şu komutla API anahtarınızı ayarlayın:")
        print("export OPENAI_API_KEY='sk-your-api-key-here'")
        return False
    
    print(f"\n✓ API Anahtarı bulundu: {API_KEY[:20]}...")
    
    try:
        client = OpenAI(api_key=API_KEY)
        print("✓ OpenAI client oluşturuldu")
        
        # Test görseli oluştur
        print("\n🎨 Test görseli oluşturuluyor...")
        response = client.images.generate(
            model="dall-e-3",
            prompt="A simple test image of a red apple on a white background",
            size="1024x1024",
            quality="standard",
            n=1,
        )
        
        print("✓ Test görseli başarıyla oluşturuldu!")
        print(f"  URL: {response.data[0].url[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"\n❌ HATA: {e}")
        return False

def generate_sample_images():
    """İlk 3 stil için örnek görseller oluşturur"""
    
    if not test_api():
        return
    
    print("\n" + "=" * 60)
    print("İlk 3 Stil İçin Görsel Oluşturma")
    print("=" * 60)
    
    # Test stilleri
    test_styles = [
        "Realistik (Realistic)",
        "Hiperrealistik (Hyperrealistic)",
        "3D (3D)"
    ]
    
    client = OpenAI(api_key=API_KEY)
    output_folder = Path("/mnt/user-data/outputs/test_images")
    output_folder.mkdir(exist_ok=True)
    
    for idx, style_text in enumerate(test_styles, start=1):
        print(f"\n[{idx}/3] '{style_text}' için görsel oluşturuluyor...")
        
        # İngilizce kısmı al
        english_match = re.search(r'\(([^)]+)\)', style_text)
        if english_match:
            style = english_match.group(1)
        else:
            style = style_text
        
        prompt = f"A beautiful artistic demonstration of {style} art style, high quality, detailed"
        print(f"  Prompt: {prompt}")
        
        try:
            # Görsel oluştur
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            
            image_url = response.data[0].url
            print(f"  ✓ URL alındı")
            
            # İndir
            safe_name = re.sub(r'[^\w\s-]', '', style).replace(' ', '_')
            filename = f"{idx:03d}_{safe_name}.png"
            filepath = output_folder / filename
            
            image_response = requests.get(image_url, timeout=30)
            image_response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                f.write(image_response.content)
            
            print(f"  ✓ Kaydedildi: {filepath}")
            
            # Rate limiting
            if idx < len(test_styles):
                print("  ⏳ 2 saniye bekleniyor...")
                time.sleep(2)
            
        except Exception as e:
            print(f"  ❌ Hata: {e}")
    
    print("\n" + "=" * 60)
    print("✓ Test tamamlandı!")
    print(f"✓ Görseller: {output_folder}")
    print("=" * 60)

if __name__ == "__main__":
    generate_sample_images()
