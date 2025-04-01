from selenium import webdriver
import requests
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
            print(f"{page_url} için bulunan Akış URL'leri: {stream_urls}")
            return stream_urls
        else:
            print(f"{page_url} için herhangi bir akış URL'si bulunamadı.")
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
    Kanal isimlerinin başına otomatik sıralama ekler.
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
    "https://www.canlitv.my/trt1-canli",
    "https://www.canlitv.my/showtv",
    "https://www.canlitv.my/startv",
    "https://www.canlitv.my/kanal-7-canli",
    "https://www.canlitv.my/atv-canli-yayin-2",
    "https://www.canlitv.my/tv8-izle-3",
    "https://www.canlitv.my/kanald-izle",
    "https://www.canlitv.my/now-tv",
    "https://www.canlitv.my/trt-haber",
    "https://www.canlitv.my/cnnturkizle",
    "https://www.canlitv.my/ntv-izle",
    "https://www.canlitv.my/a-haber-canli-izle",
    "https://www.canlitv.my/haberturk",
    "https://www.canlitv.my/halk-tv-canli",
    "https://www.canlitv.my/sozcu-tv",
    "https://www.canlitv.my/cnbc-e",
    "https://www.canlitv.my/haber-global",
    "https://www.canlitv.my/tv-100",
    "https://www.canlitv.my/360-tv",
    "https://www.canlitv.my/beyaz-tv",
    "https://www.canlitv.my/bein-sports-haber",
    "https://www.canlitv.my/trt-spor-canli",
    "https://www.canlitv.my/ht-spor",
    "https://www.canlitv.my/tlc",
    "https://www.canlitv.my/dmax",
    "https://www.canlitv.my/trt-belgesel",
    "https://www.canlitv.my/yaban-tv",
    "https://www.canlitv.my/diyanet-cocuk",
    "https://www.canlitv.my/trt-cocuk",
    "https://www.canlitv.my/cartoon-network",
    "https://www.canlitv.my/minika-cocuk-canli-izle",
    "https://www.canlitv.my/minika-go-izle",
    "https://www.canlitv.my/zaroktv",
    "https://www.canlitv.my/arb-gunes-tv",
    "https://www.canlitv.my/tgrt-haber",
    "https://www.canlitv.my/fb-tv",
    "https://www.canlitv.my/tjk-tv-izle-1",
    "https://www.canlitv.my/aspor-canli-izle",
    "https://www.canlitv.my/krt-tv",
    "https://www.canlitv.my/tivibu-spor",
    "https://www.canlitv.my/ulusal-kanal",
    "https://www.canlitv.my/lider-haber-tv",
    "https://www.canlitv.my/bengu-turk",
    "https://www.canlitv.my/bloomberg-ht-tv",
    "https://www.canlitv.my/akit-tv",
    "https://www.canlitv.my/flash-tv",
    "https://www.canlitv.my/ulke-tv",
    "https://www.canlitv.my/ilke-tv",
    "https://www.canlitv.my/tele1-tv",
    "https://www.canlitv.my/yol-tv",
    "https://www.canlitv.my/tv85-izle",
    "https://www.canlitv.my/cine-1",
    "https://www.canlitv.my/ekol-tv",
    "https://www.canlitv.my/ekoturk-tv",
    "https://www.canlitv.my/tv-net",
    "https://www.canlitv.my/tv-5",
    "https://www.canlitv.my/24-tv",
    "https://www.canlitv.my/gzt-tv",
    "https://www.canlitv.my/tbmm-tv-1",
    "https://www.canlitv.my/kabe-tv",
    "https://www.canlitv.my/lalegul-tv",
    "https://www.canlitv.my/semerkand-tv",
    "https://www.canlitv.my/rehber-tv",
    "https://www.canlitv.my/dost-tv",
    "https://www.canlitv.my/diyanet-tv",
    "https://www.canlitv.my/ikra-tv",
    "https://www.canlitv.my/meltem-tv",
    "https://www.canlitv.my/trt-eba-tv-ilkokul",
    "https://www.canlitv.my/trt-eba-tv-ortaokul",
    "https://www.canlitv.my/trt-eba-tv-lise",
    "https://www.canlitv.my/trt-2",
    "https://www.canlitv.my/trt-turk",
    "https://www.canlitv.my/trt-spor-2",
    "https://www.canlitv.my/th-turk-haber",
    "https://www.canlitv.my/trt-world",
    "https://www.canlitv.my/trt-avaz",
    "https://www.canlitv.my/trt-6-kurdi",
    "https://www.canlitv.my/konya-olay-tv",
    "https://www.canlitv.my/luys-tv",
    "https://www.canlitv.my/trt-arapca",
    "https://www.canlitv.my/on4-tv",
    "https://www.canlitv.my/kanal-v",
    "https://www.canlitv.my/kon-tv",
    "https://www.canlitv.my/kanal-33",
    "https://www.canlitv.my/tv3",
    "https://www.canlitv.my/kanal38",
    "https://www.canlitv.my/al-rafidain-tv",
    "https://www.canlitv.my/tv-kayseri",
    "https://www.canlitv.my/tv-41",
    "https://www.canlitv.my/kanal-58",
    "https://www.canlitv.my/bir-tv",
    "https://www.canlitv.my/edessa-tv",
    "https://www.canlitv.my/gozde-tv",
    "https://www.canlitv.my/duzce-tv",
    "https://www.canlitv.my/tv-2020",
    "https://www.canlitv.my/kibris-genc-tv",
    "https://www.canlitv.my/kibris-ada-tv",
    "https://www.canlitv.my/kardelen-tv",
    "https://www.canlitv.my/torba-tv",
    "https://www.canlitv.my/sim-tv",
    "https://www.canlitv.my/tarim-tv",
    "https://www.canlitv.my/koy-tv",
    "https://www.canlitv.my/tgrt-belgesel",
    "https://www.canlitv.my/cifci-tv",
    "https://www.canlitv.my/toprak-tv",
    "https://www.canlitv.my/xezer-tv",
    "https://www.canlitv.my/az-tv",
    "https://www.canlitv.my/arb-tv",
    "https://www.canlitv.my/medeniyet-tv",
    "https://www.canlitv.my/kanal-s-azerbaycan",
    "https://www.canlitv.my/okku-tv",
    "https://www.canlitv.my/cbc-tv",
    "https://www.canlitv.my/ictimai-tv",
    "https://www.canlitv.my/gokkusagi-tv",
    "https://www.canlitv.my/cbc-sport-izle",
    "https://www.canlitv.my/idman-tv",
    "https://www.canlitv.my/space-tv",
    "https://www.canlitv.my/arb-24-tv",
    "https://www.canlitv.my/tmb-tv",
    "https://www.canlitv.my/dunyatv-az",
    "https://www.canlitv.my/azad-tv",
    "https://www.canlitv.my/real-tv",
    "https://www.canlitv.my/baku-tv",
    "https://www.canlitv.my/alvin-channel",
    "https://www.canlitv.my/inter-az",
    "https://www.canlitv.my/kanal-12",
    "https://www.canlitv.my/tv-1",
    "https://www.canlitv.my/kanal-3",
    "https://www.canlitv.my/kanal-5",
    "https://www.canlitv.my/azstar-tv",
    "https://www.canlitv.my/topaz-tv",
    "https://www.canlitv.my/kanal-19",
    "https://www.canlitv.my/kanal-23",
    "https://www.canlitv.my/on6-tv",
    "https://www.canlitv.my/kanal-26",
    "https://www.canlitv.my/super-kanal",
    "https://www.canlitv.my/kanal-32",
    "https://www.canlitv.my/drt-tv",
    "https://www.canlitv.my/kanal-34",
    "https://www.canlitv.my/kapadokya-tv",
    "https://www.canlitv.my/tv-52",
    "https://www.canlitv.my/kanal-56",
    "https://www.canlitv.my/guneydogu-tv",
    "https://www.canlitv.my/haber-61",
    "https://www.canlitv.my/kanal-68",
    "https://www.canlitv.my/engelsiz-tv",
    "https://www.canlitv.my/mercan-tv",
    "https://www.canlitv.my/es-tv",
    "https://www.canlitv.my/koroglu-tv",
    "https://www.canlitv.my/aksu-tv",
    "https://www.canlitv.my/ekin-turk-tv",
    "https://www.canlitv.my/world-turk-tv",
    "https://www.canlitv.my/as-tv-bursa",
    "https://www.canlitv.my/kay-tv",
    "https://www.canlitv.my/kanal-urfa",
    "https://www.canlitv.my/edirne-tv",
    "https://www.canlitv.my/trabzon-tv",
    "https://www.canlitv.my/vuslat-tv",
    "https://www.canlitv.my/ahi-tv",
    "https://www.canlitv.my/urfanatik-tv",
    "https://www.canlitv.my/kanal-s-samsun",
    "https://www.canlitv.my/milli-piyango-tv",
    "https://www.canlitv.my/kanal-firat",
    "https://www.canlitv.my/diyar-tv",
    "https://www.canlitv.my/disney-channel",
    "https://www.canlitv.my/tgrt-eu",
    "https://www.canlitv.my/kanal-t",
    "https://www.canlitv.my/tempo-tv",
    "https://www.canlitv.my/kanal-7-avrupa",
    "https://www.canlitv.my/icel-tv",
    "https://www.canlitv.my/kanal-b",
    "https://www.canlitv.my/kanal-z",
    "https://www.canlitv.my/akilli-tv",
    "https://www.canlitv.my/cay-tv",
    "https://www.canlitv.my/mavi-karadeniz-tv",
    "https://www.canlitv.my/kudus-tv",
    "https://www.canlitv.my/nur-tv",
    "https://www.canlitv.my/mpl-tv",
    "https://www.canlitv.my/tay-tv-canli",
    "https://www.canlitv.my/sports-tv",
    "https://www.canlitv.my/tv-4",
    "https://www.canlitv.my/kanal-avrupa",
    "https://www.canlitv.my/teve-2",
    "https://www.canlitv.my/brt-1",
    "https://www.canlitv.my/brt-2",
    "https://www.canlitv.my/erciyes-tv",
    "https://www.canlitv.my/kanal-likya",
    "https://www.canlitv.my/art-tv-amasya",
    "https://www.canlitv.my/rumeli-tv",
    "https://www.canlitv.my/marmara-tv",
    "https://www.canlitv.my/sun-tv",
    "https://www.canlitv.my/un-tv-konya",
    "https://www.canlitv.my/line-tv",
    "https://www.canlitv.my/kent-deha-tv",
    "https://www.canlitv.my/tarsus-guney-tv",
    "https://www.canlitv.my/e-tv-manisa",
    "https://www.canlitv.my/arastv",
    "https://www.canlitv.my/anadolutv",
    "https://www.canlitv.my/ertv",
    "https://www.canlitv.my/can-tv",
    "https://www.canlitv.my/euro-genc-tv",
    "https://www.canlitv.my/anadolu-dost-tv",
    "https://www.canlitv.my/universite-tv",
    "https://www.canlitv.my/brtv",
    "https://www.canlitv.my/grt-tv",
    "https://www.canlitv.my/munchen-tv",
    "https://www.canlitv.my/qvc",
    "https://www.canlitv.my/euronews-german",
    "https://www.canlitv.my/medine-tv",
    "https://www.canlitv.my/euro-news",
    "https://www.canlitv.my/imedi-tv",
    "https://www.canlitv.my/ege-live-tv",
    "https://www.canlitv.my/aljazeera",
    "https://www.canlitv.my/huda-tv",
    "https://www.canlitv.my/agro-tv",
    "https://www.canlitv.my/tokat-super-tv",
    "https://www.canlitv.my/hunat-tv",
    "https://www.canlitv.my/ton-tv",
    "https://www.canlitv.my/tv-a",
    "https://www.canlitv.my/bizimev-tv",
    "https://www.canlitv.my/altas-tv",
    "https://www.canlitv.my/deniz-postasi-tv",
    "https://www.canlitv.my/finans-turk-tv",
    "https://www.canlitv.my/kanal15",
    "https://www.canlitv.my/natural-tv",
    "https://www.canlitv.my/ege-aturk-tv",
    "https://www.canlitv.my/anadolu-net-tv",
    "https://www.canlitv.my/russia-today",
    "https://www.canlitv.my/sonmez-tv",
    "https://www.canlitv.my/olay-turk",
    "https://www.canlitv.my/kayseri-life-tv",
    "https://www.canlitv.my/uskudar-universitesi-tv",
    "https://www.canlitv.my/dim-tv",
    "https://www.canlitv.my/ibb-tv",
    "https://www.canlitv.my/ert-tokat",
    "https://www.canlitv.my/abb-tv",
    "https://www.canlitv.my/al-sunnah-tv",
    "https://www.canlitv.my/tv-38",
    "https://www.canlitv.my/etv-kayseri",
    "https://www.canlitv.my/sky-news",
    "https://www.canlitv.my/tivi6",
    "https://www.canlitv.my/dw-tv-europe",
    "https://www.canlitv.my/press-tv",
    "https://www.canlitv.my/fortunatv",
    "https://www.canlitv.my/ktv-kazakistan",
    "https://www.canlitv.my/cekmekoy",
    "https://www.canlitv.my/kontratv",
    "https://www.canlitv.my/elmas-tv",
    "https://www.canlitv.my/cankiri-tv",
    "https://www.canlitv.my/ert-sah-tv",
    "https://www.canlitv.my/silk-way-tv",
    "https://www.canlitv.my/nasa-tv",
    "https://www.canlitv.my/noa4-hamburg",
    "https://www.canlitv.my/sat-7",
    "https://www.canlitv.my/tv-sudbaden",
    "https://www.canlitv.my/rfh",
    "https://www.canlitv.my/kadirga-tv",
    "https://www.canlitv.my/franken-tv",
    "https://www.canlitv.my/hse-24",
    "https://www.canlitv.my/offener-kanal-berlin",
    "https://www.canlitv.my/oberpfalz-tv",
    "https://www.canlitv.my/frt-tv",
    "https://www.canlitv.my/lale-tv",
    "https://www.canlitv.my/niederbayern-tv",
    "https://www.canlitv.my/rudawtv",
    "https://www.canlitv.my/altin-asir-tv",
    "https://www.canlitv.my/askabat-tv",
    "https://www.canlitv.my/tolonews",
    "https://www.canlitv.my/india-today",
    "https://www.canlitv.my/joy-news",
    "https://www.canlitv.my/makkah-tv",
    "https://www.canlitv.my/tv9",
    "https://www.canlitv.my/kent-turk-tv",
    "https://www.canlitv.my/milyon-tv",
    "https://www.canlitv.my/owazy-tv",
    "https://www.canlitv.my/woman-tv",
    "https://www.canlitv.my/a-news",
    "https://www.canlitv.my/deutsche-welle",
    "https://www.canlitv.my/blue-sky-tv",
    "https://www.canlitv.my/manorama-news-tv",
    "https://www.canlitv.my/news-nation-tv",
    "https://www.canlitv.my/kibris-tv",
    "https://www.canlitv.my/trakya-turk-tv",
    "https://www.canlitv.my/tv9-izmir"

]

# Çalışan ve çalışmayan kanalları tutmak için liste
all_channels = []

# Her sayfa için akış URL'lerini bul ve kontrol et
for page_url in page_urls:
    print(f"Taranıyor: {page_url}")
    channel_name = page_url.split("/")[-1].capitalize()  # Kanal adı
    stream_urls = find_stream_url_with_selenium(page_url)

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
