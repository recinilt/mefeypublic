import subprocess

def create_wifi_hotspot(ssid, password):
    try:
        # Hotspot yapılandırmasını oluştur
        subprocess.run(
            f'netsh wlan set hostednetwork mode=allow ssid={ssid} key={password}',
            shell=True, check=True
        )
        
        # Hotspot'u başlat
        subprocess.run('netsh wlan start hostednetwork', shell=True, check=True)
        print(f"Wi-Fi hotspot '{ssid}' başarıyla başlatıldı.")
    except subprocess.CalledProcessError as e:
        print("Bir hata oluştu:", e)

def stop_wifi_hotspot():
    try:
        # Hotspot'u durdur
        subprocess.run('netsh wlan stop hostednetwork', shell=True, check=True)
        print("Wi-Fi hotspot başarıyla durduruldu.")
    except subprocess.CalledProcessError as e:
        print("Bir hata oluştu:", e)

# Örnek kullanım
create_wifi_hotspot('ReciPc', '88888888')  # SSID ve Şifre belirle
# stop_wifi_hotspot()  # Hotspot'u durdurmak için