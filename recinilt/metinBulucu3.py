import os
import glob

def txt_dosyalarinda_ara(klasor_yolu, aranan_metin, buyuk_kucuk_harf_duyarsiz=True):
    """
    Belirtilen klasördeki .txt dosyalarında belirli bir metni arar
    
    Args:
        klasor_yolu (str): Arama yapılacak klasörün yolu
        aranan_metin (str): Aranacak metin
        buyuk_kucuk_harf_duyarsiz (bool): Büyük/küçük harf duyarlılığı
    
    Returns:
        list: Aranan metni içeren dosyaların listesi
    """
    bulunan_dosyalar = []
    
    # Klasör varlığını kontrol et
    if not os.path.exists(klasor_yolu):
        print(f"Hata: '{klasor_yolu}' klasörü bulunamadı!")
        return bulunan_dosyalar
    
    # .txt dosyalarını bul
    txt_dosyalari = glob.glob(os.path.join(klasor_yolu, "*.txt"))
    
    if not txt_dosyalari:
        print(f"'{klasor_yolu}' klasöründe .txt dosyası bulunamadı!")
        return bulunan_dosyalar
    
    print(f"{len(txt_dosyalari)} adet .txt dosyası bulundu. Arama başlıyor...\n")
    
    for dosya_yolu in txt_dosyalari:
        try:
            # Dosyayı oku (UTF-8 encoding ile)
            with open(dosya_yolu, 'r', encoding='utf-8') as dosya:
                icerik = dosya.read()
            
            # Arama yap
            if buyuk_kucuk_harf_duyarsiz:
                arama_sonucu = aranan_metin.lower() in icerik.lower()
            else:
                arama_sonucu = aranan_metin in icerik
            
            if arama_sonucu:
                dosya_adi = os.path.basename(dosya_yolu)
                bulunan_dosyalar.append(dosya_yolu)
                
                # Metni içeren satırları bul ve göster
                satirlar = icerik.split('\n')
                bulunan_satirlar = []
                
                for satir_no, satir in enumerate(satirlar, 1):
                    if buyuk_kucuk_harf_duyarsiz:
                        kontrol = aranan_metin.lower() in satir.lower()
                    else:
                        kontrol = aranan_metin in satir
                    
                    if kontrol:
                        bulunan_satirlar.append((satir_no, satir.strip()))
                
                print(f"✓ Dosya: {dosya_adi}")
                print(f"  Yol: {dosya_yolu}")
                print(f"  Bulunan satırlar ({len(bulunan_satirlar)} adet):")
                
                for satir_no, satir in bulunan_satirlar[:5]:  # İlk 5 satırı göster
                    print(f"    Satır {satir_no}: {satir}")
                
                if len(bulunan_satirlar) > 5:
                    print(f"    ... ve {len(bulunan_satirlar) - 5} satır daha")
                print()
        
        except UnicodeDecodeError:
            # UTF-8 ile okunamazsa, farklı encoding'ler dene
            try:
                with open(dosya_yolu, 'r', encoding='cp1254') as dosya:
                    icerik = dosya.read()
                # Aynı arama işlemini tekrarla
                if buyuk_kucuk_harf_duyarsiz:
                    arama_sonucu = aranan_metin.lower() in icerik.lower()
                else:
                    arama_sonucu = aranan_metin in icerik
                
                if arama_sonucu:
                    bulunan_dosyalar.append(dosya_yolu)
                    print(f"✓ Dosya: {os.path.basename(dosya_yolu)} (CP1254 encoding)")
                    print(f"  Yol: {dosya_yolu}\n")
            except:
                print(f"⚠ Uyarı: '{os.path.basename(dosya_yolu)}' dosyası okunamadı (encoding sorunu)")
        
        except Exception as e:
            print(f"⚠ Hata: '{os.path.basename(dosya_yolu)}' dosyası okunurken hata: {e}")
    
    return bulunan_dosyalar

# Kullanım örneği
if __name__ == "__main__":
    # Kullanıcıdan bilgileri al
    klasor = input("Arama yapılacak klasör yolunu girin: ").strip()
    if not klasor:
        klasor = "."  # Mevcut klasör
    
    aranan = input("Aranacak metni girin: ").strip()
    
    if not aranan:
        print("Aranacak metin boş olamaz!")
    else:
        print(f"\n'{aranan}' metni için arama başlıyor...\n")
        print("="*50)
        
        sonuclar = txt_dosyalarinda_ara(klasor, aranan)
        
        print("="*50)
        print(f"\nArama tamamlandı!")
        print(f"Toplam {len(sonuclar)} dosyada '{aranan}' metni bulundu.")
        
        if sonuclar:
            print("\nBulunan dosyalar:")
            for i, dosya in enumerate(sonuclar, 1):
                print(f"{i}. {dosya}")