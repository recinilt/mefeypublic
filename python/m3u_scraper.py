import requests
from bs4 import BeautifulSoup

# Kaynak URL'leri Belirtin (M3U Listelerini İçeren Sayfalar)
source_urls = [
    "https://github.com/sefakozan/turkce-iptv",
    "https://github.com/canli54/vlc-m3u8-iptv-listesi/blob/main/turkiye-tv-kanallari.M3U",
    "https://itasli.github.io/TURKTV/"
]

# Çalışan Kanalları Tutmak İçin Liste
working_channels = []

def fetch_m3u_links(source_url):
    """Verilen URL'den M3U dosyası linklerini bulur."""
    try:
        response = requests.get(source_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        links = soup.find_all("a", href=True)
        m3u_links = [link['href'] for link in links if link['href'].endswith(".m3u")]
        return m3u_links
    except Exception as e:
        print(f"URL'den M3U Linkleri Alınamadı: {source_url}\nHata: {e}")
        return []

def check_url(url):
    """URL'nin çalışıp çalışmadığını kontrol eder."""
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

def parse_m3u_content(m3u_url):
    """M3U dosyasını indir ve içeriğindeki URL'leri kontrol et."""
    try:
        response = requests.get(m3u_url, timeout=10)
        response.raise_for_status()
        lines = response.text.splitlines()
        for i in range(len(lines)):
            if lines[i].startswith("#EXTINF"):
                channel_name = lines[i].split(",")[-1].strip()
                channel_url = lines[i + 1].strip()
                if check_url(channel_url):
                    print(f"Çalışıyor: {channel_name} - {channel_url}")
                    working_channels.append((channel_name, channel_url))
                else:
                    print(f"Çalışmıyor: {channel_name} - {channel_url}")
    except Exception as e:
        print(f"M3U içeriği işlenemedi: {m3u_url}\nHata: {e}")

# Kaynaklardan M3U Dosyalarını Bul ve İşle
for source_url in source_urls:
    print(f"Kaynak URL'den M3U Linkleri Alınıyor: {source_url}")
    m3u_links = fetch_m3u_links(source_url)
    for link in m3u_links:
        full_url = link if link.startswith("http") else f"{source_url.rstrip('/')}/{link}"
        if check_url(full_url):
            print(f"M3U Dosyası Çalışıyor: {full_url}")
            parse_m3u_content(full_url)
        else:
            print(f"M3U Dosyası Çalışmıyor: {full_url}")

# Çalışan Kanalları M3U Dosyasına Kaydet
output_file = "working_turkish_channels.m3u"
with open(output_file, "w", encoding="utf-8") as file:
    file.write("#EXTM3U\n")
    for channel_name, channel_url in working_channels:
        file.write(f"#EXTINF:-1, {channel_name}\n")
        file.write(f"{channel_url}\n")

print(f"Çalışan kanallar M3U dosyasına kaydedildi: {output_file}")
