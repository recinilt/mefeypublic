#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kodlama Klasörü Temizleyici
Ana kaynak dosyalarını korur, gereksiz dosya ve klasörleri siler
"""

import os
import shutil
from pathlib import Path

# KORUNACAK DOSYA UZANTILARI
KORUNACAK_UZANTILAR = {
    '.py',      # Python
    '.html',    # HTML
    '.js',      # JavaScript
    '.css',     # CSS
    '.jpg',     # JPEG resim
    '.jpeg',    # JPEG resim
    '.png',     # PNG resim
    '.gif',     # GIF resim
    '.mp4',     # MP4 video
    '.mov',     # MOV video
    '.avi',     # AVI video
    '.mp3',     # MP3 ses
    '.wav',     # WAV ses
    '.ogg',     # OGG ses
    '.m4a',     # M4A ses
    '.flac',    # FLAC ses
    '.aac',     # AAC ses
    '.wma',     # WMA ses
    '.json',    # JSON veri
    '.xml',     # XML veri
    '.txt',     # Metin
    '.md',      # Markdown
    '.sql',     # SQL
    '.csv',     # CSV veri
    '.svg',     # SVG vektör
}

# SİLİNECEK KLASÖR İSİMLERİ
SILINECEK_KLASORLER = {
    '__pycache__',      # Python cache
    '.pytest_cache',    # Pytest cache
    'node_modules',     # Node.js bağımlılıkları
    'venv',             # Python virtual environment
    'env',              # Python virtual environment
    '.env',             # Python virtual environment
    'virtualenv',       # Python virtual environment
    '.venv',            # Python virtual environment
    'dist',             # Build çıktıları
    'build',            # Build çıktıları
    '.next',            # Next.js build
    '.nuxt',            # Nuxt.js build
    'target',           # Rust/Java build
    'bin',              # Binary çıktıları
    'obj',              # Object dosyaları
    '.gradle',          # Gradle cache
    '.cache',           # Genel cache
    '.sass-cache',      # Sass cache
    '.parcel-cache',    # Parcel cache
    '.mypy_cache',      # MyPy cache
    '.tox',             # Tox test
    'htmlcov',          # Coverage reports
    '.coverage',        # Coverage data
    '.eggs',            # Python eggs
    '*.egg-info',       # Python egg info
}

# SİLİNECEK DOSYA DESENLERI
SILINECEK_DOSYA_UZANTILARI = {
    '.pyc',         # Python compiled
    '.pyo',         # Python optimized
    '.pyd',         # Python DLL
    '.so',          # Shared object
    '.dll',         # Dynamic link library
    '.dylib',       # macOS dynamic library
    '.class',       # Java compiled
    '.o',           # Object file
    '.a',           # Archive
    '.lib',         # Library
    '.exe',         # Executable
    '.log',         # Log dosyası
    '.tmp',         # Temporary
    '.temp',        # Temporary
    '.bak',         # Backup
    '.swp',         # Vim swap
    '.DS_Store',    # macOS
    'Thumbs.db',    # Windows
}

class KlasorTemizleyici:
    def __init__(self, hedef_klasor):
        self.hedef_klasor = Path(hedef_klasor)
        self.silinen_klasorler = []
        self.silinen_dosyalar = []
        self.hata_listesi = []
        
    def klasor_silinmeli_mi(self, klasor_adi):
        """Klasörün silinip silinmeyeceğini kontrol eder"""
        return klasor_adi in SILINECEK_KLASORLER
    
    def dosya_silinmeli_mi(self, dosya_yolu):
        """Dosyanın silinip silinmeyeceğini kontrol eder"""
        dosya_adi = dosya_yolu.name
        uzanti = dosya_yolu.suffix.lower()
        
        # Korunacak uzantılardan biriyse silinmez
        if uzanti in KORUNACAK_UZANTILAR:
            return False
        
        # Silinecek uzantılardan biriyse silinir
        if uzanti in SILINECEK_DOSYA_UZANTILARI:
            return True
        
        # Özel dosya isimleri
        if dosya_adi in ['.DS_Store', 'Thumbs.db', 'desktop.ini']:
            return True
            
        return False
    
    def boyut_hesapla(self, yol):
        """Dosya veya klasör boyutunu hesaplar"""
        if yol.is_file():
            return yol.stat().st_size
        
        toplam = 0
        try:
            for item in yol.rglob('*'):
                if item.is_file():
                    toplam += item.stat().st_size
        except (PermissionError, OSError):
            pass
        return toplam
    
    def boyut_formatla(self, boyut):
        """Boyutu okunabilir formata çevirir"""
        for birim in ['B', 'KB', 'MB', 'GB', 'TB']:
            if boyut < 1024.0:
                return f"{boyut:.2f} {birim}"
            boyut /= 1024.0
        return f"{boyut:.2f} PB"
    
    def temizle(self, kuru_calistir=True):
        """Temizleme işlemini yapar"""
        print(f"\n{'='*60}")
        print(f"Klasör Temizleme {'(KURU ÇALIŞTIRMA)' if kuru_calistir else '(GERÇEKTEKİ SİLME)'}")
        print(f"{'='*60}")
        print(f"Hedef: {self.hedef_klasor.absolute()}\n")
        
        if not self.hedef_klasor.exists():
            print(f"❌ HATA: '{self.hedef_klasor}' klasörü bulunamadı!")
            return
        
        toplam_boyut = 0
        
        # Klasörleri tara
        for root, dirs, files in os.walk(self.hedef_klasor, topdown=False):
            root_path = Path(root)
            
            # Klasörleri kontrol et
            for dir_name in dirs[:]:  # Kopyasını kullan
                dir_path = root_path / dir_name
                
                if self.klasor_silinmeli_mi(dir_name):
                    boyut = self.boyut_hesapla(dir_path)
                    toplam_boyut += boyut
                    
                    print(f"📁 Klasör: {dir_path.relative_to(self.hedef_klasor)}")
                    print(f"   Boyut: {self.boyut_formatla(boyut)}")
                    
                    if not kuru_calistir:
                        try:
                            shutil.rmtree(dir_path)
                            self.silinen_klasorler.append(str(dir_path))
                            print(f"   ✅ Silindi")
                        except Exception as e:
                            print(f"   ❌ Silinemedi: {e}")
                            self.hata_listesi.append(str(dir_path))
                    else:
                        print(f"   ⚠️  Silinecek (kuru çalıştırma)")
                    
                    print()
            
            # Dosyaları kontrol et
            for file_name in files:
                file_path = root_path / file_name
                
                if self.dosya_silinmeli_mi(file_path):
                    boyut = self.boyut_hesapla(file_path)
                    toplam_boyut += boyut
                    
                    print(f"📄 Dosya: {file_path.relative_to(self.hedef_klasor)}")
                    print(f"   Boyut: {self.boyut_formatla(boyut)}")
                    
                    if not kuru_calistir:
                        try:
                            file_path.unlink()
                            self.silinen_dosyalar.append(str(file_path))
                            print(f"   ✅ Silindi")
                        except Exception as e:
                            print(f"   ❌ Silinemedi: {e}")
                            self.hata_listesi.append(str(file_path))
                    else:
                        print(f"   ⚠️  Silinecek (kuru çalıştırma)")
                    
                    print()
        
        # Özet
        print(f"\n{'='*60}")
        print("ÖZET")
        print(f"{'='*60}")
        
        if kuru_calistir:
            print(f"⚠️  Bu bir KURU ÇALIŞTIRMA - Hiçbir dosya silinmedi")
            print(f"Gerçekten silmek için: python klasor_temizleyici.py --sil")
        else:
            print(f"✅ Silinen klasör sayısı: {len(self.silinen_klasorler)}")
            print(f"✅ Silinen dosya sayısı: {len(self.silinen_dosyalar)}")
            if self.hata_listesi:
                print(f"❌ Hata oluşan sayısı: {len(self.hata_listesi)}")
        
        print(f"💾 Toplam kazanılan alan: {self.boyut_formatla(toplam_boyut)}")
        print(f"{'='*60}\n")


def main():
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Kodlama klasörlerini temizleyen araç',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnekler:
  # Önce kuru çalıştırma yapın (hiçbir şey silinmez)
  python klasor_temizleyici.py /path/to/kodlamalar
  
  # Gerçekten silmek için
  python klasor_temizleyici.py /path/to/kodlamalar --sil
  
  # Mevcut klasörü temizle
  python klasor_temizleyici.py . --sil
        """
    )
    
    parser.add_argument(
        'klasor',
        nargs='?',
        default='.',
        help='Temizlenecek klasör yolu (varsayılan: mevcut klasör)'
    )
    
    parser.add_argument(
        '--sil',
        action='store_true',
        help='Gerçekten sil (varsayılan: sadece göster)'
    )
    
    args = parser.parse_args()
    
    temizleyici = KlasorTemizleyici(args.klasor)
    temizleyici.temizle(kuru_calistir=not args.sil)


if __name__ == "__main__":
    main()
