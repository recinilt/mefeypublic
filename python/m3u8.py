from mitmproxy import http  # Burada `http` doğru şekilde içe aktarılıyor
from mitmproxy.tools.dump import DumpMaster
from mitmproxy.options import Options
from selenium import webdriver
import re
import time
from tqdm import tqdm  # Progress bar için

# Mitmproxy'den yakalanan akış URL'lerini depolamak için bir liste
captured_streams = []

class StreamInterceptor:
    """
    Mitmproxy'nin HTTP ve HTTPS trafiğini yakalaması için bir sınıf.
    """
    def request(self, flow: http.HTTPFlow):
        """
        Gelen HTTP isteklerini yakalar.
        """
        if ".m3u8" in flow.request.pretty_url:  # .m3u8 uzantılı bağlantıları yakala
            captured_streams.append(flow.request.pretty_url)
            print(f"Yakalanan Akış URL'si: {flow.request.pretty_url}")

def start_mitmproxy():
    """
    Mitmproxy'yi çalıştıran bir fonksiyon.
    """
    options = Options(listen_host="127.0.0.1", listen_port=8080)
    proxy = DumpMaster(options)
    proxy.addons.add(StreamInterceptor())
    try:
        proxy.run()
    except KeyboardInterrupt:
        proxy.shutdown()

def find_stream_url_with_mitmproxy(page_url):
    """
    Mitmproxy ile bir sayfadan video akışı URL'sini yakalar.
    """
    # Selenium ChromeOptions yapılandırması
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--user-data-dir=C:\\Users\\yenir\\AppData\\Local\\Google\\Chrome\\SeleniumProfile")
    options.add_argument("--proxy-server=http://127.0.0.1:8080")  # Mitmproxy'nin çalıştığı varsayılan proxy portu

    driver = webdriver.Chrome(options=options)

    try:
        # Sayfayı aç
        driver.get(page_url)
        print("Lütfen giriş yapın ve video akışını başlatın...")
        time.sleep(60)  # Giriş ve video için bekleme süresi

        # Mitmproxy ile yakalanan akış URL'lerini döndür
        if captured_streams:
            print(f"Bulunan Akış URL'leri: {captured_streams}")
            return captured_streams
        else:
            print("Herhangi bir akış URL'si yakalanamadı.")
            return None
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        return None
    finally:
        driver.quit()

def check_url(url):
    """
    URL'nin çalışıp çalışmadığını kontrol eder.
    """
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

def save_to_m3u(working_streams, output_file="working_channels.m3u"):
    """
    Çalışan ve çalışmayan kanalları bir M3U dosyasına kaydeder.
    """
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("#EXTM3U\n")
        for index, (channel_name, stream_url) in enumerate(working_streams, start=1):
            numbered_channel_name = f"{index}- {channel_name}"  # Kanal adının başına sıralama numarası ekleniyor
            file.write(f"#EXTINF:-1, {numbered_channel_name}\n")
            file.write(f"{stream_url}\n")
    print(f"Tüm kanallar {output_file} dosyasına kaydedildi.")

# Taranacak sayfa URL'leri
page_urls = [
    "https://tvplus.com.tr/canli-tv"
]

# Çalışan ve çalışmayan kanalları tutmak için liste
all_channels = []

# Mitmproxy'yi başlat
import threading
proxy_thread = threading.Thread(target=start_mitmproxy, daemon=True)
proxy_thread.start()

# Her sayfa için akış URL'lerini bul ve kontrol et
for page_url in tqdm(page_urls, desc="Sayfalar Taraniyor", unit="sayfa"):
    print(f"Taranıyor: {page_url}")
    channel_name = page_url.split("/")[-1].capitalize()  # Kanal adı
    stream_urls = find_stream_url_with_mitmproxy(page_url)

    if stream_urls:
        first_stream_url = stream_urls[0]
        if check_url(first_stream_url):
            print(f"Çalışıyor: {first_stream_url}")
            all_channels.append((channel_name, first_stream_url))
        else:
            print(f"Çalışmıyor: {first_stream_url}")
            all_channels.append((channel_name, "bulunamadı"))
    else:
        print(f"{channel_name} için akış URL'si bulunamadı.")
        all_channels.append((channel_name, "bulunamadı"))

# Çalışan ve çalışmayan kanalları bir M3U dosyasına kaydet
save_to_m3u(all_channels)
