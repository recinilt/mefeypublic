import os
import re
from pathlib import Path

def search_sentences_in_txt_files(folder_path, search_term, case_sensitive=False, debug=False):
    """
    Belirtilen klasördeki tüm .txt dosyalarında arama terimini içeren cümleleri bulur.
    
    Args:
        folder_path (str): Aranacak klasör yolu
        search_term (str): Aranacak metin
        case_sensitive (bool): Büyük/küçük harf duyarlılığı
        debug (bool): Debug bilgilerini göster
    
    Returns:
        dict: Dosya adları ve bulunan cümlelerin dictionary'si
    """
    results = {}
    
    # Klasörün var olup olmadığını kontrol et
    if not os.path.exists(folder_path):
        print(f"Hata: '{folder_path}' klasörü bulunamadı!")
        return results
    
    # Cümle ayırıcı regex pattern'i (nokta, ünlem, soru işareti)
    sentence_pattern = r'[.!?]+\s*'
    
    # Klasördeki tüm .txt dosyalarını bul
    txt_files = list(Path(folder_path).glob('*.txt'))
    
    if not txt_files:
        print(f"'{folder_path}' klasöründe hiç .txt dosyası bulunamadı!")
        return results
    
    print(f"{len(txt_files)} adet .txt dosyası bulundu. Aranıyor...")
    
    for file_path in txt_files:
        try:
            # Dosyayı UTF-8 ile oku
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Debug için: Dosyada hangi nokta karakterleri var kontrol et
            if debug and search_term == "...":
                dot_chars = set()
                for char in content:
                    if char == '.' or char == '…' or ord(char) in range(8230, 8240):
                        dot_chars.add(f"'{char}' (Unicode: {ord(char)})")
                if dot_chars:
                    print(f"  {file_path.name}: Bulunan nokta karakterleri: {', '.join(dot_chars)}")
            
            # Basit arama: Cümlelere bölmeden tüm metinde ara
            if search_term == "...":
                # Farklı nokta varyasyonları
                patterns_to_check = [
                    "...",      # Normal 3 nokta
                    "…",        # Ellipsis karakteri
                    ". . .",    # Boşluklu noktalar
                    "....",     # 4 nokta
                    ".....",    # 5 nokta
                    "......",   # 6 nokta
                ]
                
                # Her pattern için kontrol et
                found_patterns = []
                for pattern in patterns_to_check:
                    if pattern in content:
                        found_patterns.append(pattern)
                
                if found_patterns and debug:
                    print(f"  {file_path.name}: Bulunan pattern'ler: {found_patterns}")
            
            # Cümleleri ayır
            sentences = re.split(sentence_pattern, content)
            
            # Arama terimini içeren cümleleri bul
            matching_sentences = []
            for sentence in sentences:
                sentence = sentence.strip()
                if sentence:  # Boş cümleleri atla
                    # Özel durum: "..." aranıyorsa farklı nokta türlerini de kontrol et
                    if search_term == "...":
                        # Farklı nokta karakteri varyasyonları
                        dot_patterns = ["...", "…", ". . .", "....", "....."]
                        found = any(pattern in sentence for pattern in dot_patterns)
                        if found:
                            matching_sentences.append(sentence)
                    else:
                        # Normal arama
                        if case_sensitive:
                            if search_term in sentence:
                                matching_sentences.append(sentence)
                        else:
                            if search_term.lower() in sentence.lower():
                                matching_sentences.append(sentence)
            
            # Eğer eşleşen cümle varsa sonuçlara ekle
            if matching_sentences:
                results[file_path.name] = matching_sentences
                
        except UnicodeDecodeError:
            # UTF-8 ile okunamazsa farklı encoding'ler dene
            try:
                with open(file_path, 'r', encoding='cp1254') as file:  # Türkçe karakter desteği
                    content = file.read()
                # Yukarıdaki işlemleri tekrarla
                sentences = re.split(sentence_pattern, content)
                matching_sentences = []
                for sentence in sentences:
                    sentence = sentence.strip()
                    if sentence:
                        # Özel durum: "..." aranıyorsa farklı nokta türlerini de kontrol et
                        if search_term == "...":
                            dot_patterns = ["...", "…", ". . .", "....", "....."]
                            found = any(pattern in sentence for pattern in dot_patterns)
                            if found:
                                matching_sentences.append(sentence)
                        else:
                            # Normal arama
                            if case_sensitive:
                                if search_term in sentence:
                                    matching_sentences.append(sentence)
                            else:
                                if search_term.lower() in sentence.lower():
                                    matching_sentences.append(sentence)
                
                if matching_sentences:
                    results[file_path.name] = matching_sentences
                    
            except Exception as e:
                print(f"'{file_path.name}' dosyası okunamadı: {e}")
        
        except Exception as e:
            print(f"'{file_path.name}' dosyasında hata: {e}")
    
    return results

def print_results(results, search_term):
    """Sonuçları düzenli bir şekilde yazdır"""
    if not results:
        print(f"'{search_term}' için hiç sonuç bulunamadı.")
        return
    
    print(f"\n=== '{search_term}' ARAMA SONUÇLARI ===")
    print(f"Toplam {len(results)} dosyada sonuç bulundu.\n")
    
    for filename, sentences in results.items():
        print(f"📄 {filename} ({len(sentences)} cümle):")
        print("-" * 50)
        for i, sentence in enumerate(sentences, 1):
            print(f"{i}. {sentence[:100]}{'...' if len(sentence) > 100 else ''}")
        print()

def save_results_to_file(results, search_term, output_file="arama_sonuclari.txt"):
    """Sonuçları dosyaya kaydet"""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"=== '{search_term}' ARAMA SONUÇLARI ===\n")
            f.write(f"Toplam {len(results)} dosyada sonuç bulundu.\n\n")
            
            for filename, sentences in results.items():
                f.write(f"📄 {filename} ({len(sentences)} cümle):\n")
                f.write("-" * 50 + "\n")
                for i, sentence in enumerate(sentences, 1):
                    f.write(f"{i}. {sentence}\n")
                f.write("\n")
        
        print(f"Sonuçlar '{output_file}' dosyasına kaydedildi.")
    except Exception as e:
        print(f"Dosya kaydetme hatası: {e}")

# Ana program
if __name__ == "__main__":
    # Kullanım örneği
    folder_path = input("Klasör yolunu girin: ").strip()
    if not folder_path:
        folder_path = "."  # Mevcut klasör
    
    search_term = input("Aranacak metni girin: ").strip()
    if not search_term:
        print("Arama terimi boş olamaz!")
        exit()
    
    # Büyük/küçük harf duyarlılığı
    case_choice = input("Büyük/küçük harf duyarlı arama? (e/h, varsayılan: h): ").strip().lower()
    case_sensitive = case_choice == 'e'
    
    # Debug modu
    debug_choice = input("Debug modunu açmak ister misiniz? (detaylı bilgi gösterir) (e/h): ").strip().lower()
    debug_mode = debug_choice == 'e'
    
    print(f"\nAranıyor: '{search_term}'")
    print(f"Klasör: '{folder_path}'")
    print(f"Büyük/küçük harf duyarlı: {'Evet' if case_sensitive else 'Hayır'}")
    print(f"Debug modu: {'Açık' if debug_mode else 'Kapalı'}\n")
    
    # Aramayı gerçekleştir
    results = search_sentences_in_txt_files(folder_path, search_term, case_sensitive, debug_mode)
    
    # Sonuçları göster
    print_results(results, search_term)
    
    # Sonuçları dosyaya kaydetmek istiyor mu?
    if results:
        save_choice = input("Sonuçları dosyaya kaydetmek ister misiniz? (e/h): ").strip().lower()
        if save_choice == 'e':
            output_filename = input("Çıktı dosyası adı (varsayılan: arama_sonuclari.txt): ").strip()
            if not output_filename:
                output_filename = "arama_sonuclari.txt"
            save_results_to_file(results, search_term, output_filename)