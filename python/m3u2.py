import requests
from bs4 import BeautifulSoup
import re

def find_stream_url(page_url):
    """
    Verilen canlı yayın sayfasından .m3u8 veya .ts URL'lerini bulur.
    """
    try:
        # Sayfanın HTML içeriğini al
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        response = requests.get(page_url, headers=headers)
        response.raise_for_status()
        html_content = response.text

        # HTML içeriğini analiz et
        soup = BeautifulSoup(html_content, "html.parser")

        # .m3u8 ve .ts formatındaki bağlantıları ara
        stream_urls = re.findall(r'https?://[^\s"]+\.m3u8', html_content)
        stream_urls.extend(re.findall(r'https?://[^\s"]+\.ts', html_content))

        # Çıktıyı döndür
        if stream_urls:
            print(f"Bulunan Akış URL'leri: {stream_urls}")
            return stream_urls
        else:
            print("Herhangi bir akış URL'si bulunamadı.")
            return None
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        return None

# Örnek kullanım
page_url = "https://www.canlitv.my/showtv"  # Canlı yayın sayfası URL'si
stream_urls = find_stream_url(page_url)

if stream_urls:
    # İlk bulunan akış URL'sini al
    first_stream_url = stream_urls[0]
    print(f"İlk bulunan akış URL'si: {first_stream_url}")
