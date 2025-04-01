from selenium import webdriver
import re
import time

def find_stream_url_with_selenium(page_url):
    """
    Selenium ile bir sayfadan .m3u8 veya .ts formatındaki akış URL'lerini bulur.
    """
    # Performans loglarını etkinleştir
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Tarayıcıyı arka planda çalıştırır
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})  # Performans logları etkinleştirildi

    # Tarayıcıyı başlat
    driver = webdriver.Chrome(options=options)

    try:
        # Sayfayı aç
        driver.get(page_url)
        time.sleep(5)  # Dinamik içeriklerin yüklenmesi için bekleyin

        # Performance loglarını alın
        logs = driver.get_log("performance")

        # .m3u8 ve .ts formatındaki bağlantıları ara
        stream_urls = []
        for log in logs:
            message = log["message"]
            matches = re.findall(r'https?://[^\s"]+\.m3u8', message)
            stream_urls.extend(matches)

        if stream_urls:
            print(f"Bulunan Akış URL'leri: {stream_urls}")
            return stream_urls
        else:
            print("Herhangi bir akış URL'si bulunamadı.")
            return None
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        return None
    finally:
        driver.quit()

# Örnek kullanım
page_url = "https://www.canlitv.my/showtv"  # Canlı yayın sayfası URL'si
stream_urls = find_stream_url_with_selenium(page_url)

if stream_urls:
    # İlk bulunan akış URL'sini al
    first_stream_url = stream_urls[0]
    print(f"İlk bulunan akış URL'si: {first_stream_url}")
