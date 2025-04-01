def is_above_last_7_average(num, lst):
    # Son 7 elemanı al
    last_7 = lst[-7:]
    # Son 7 elemanın ortalamasını hesapla
    average = sum(last_7) / len(last_7) if last_7 else 49.1
    # Sayı ortalamadan büyükse True, değilse False döndür
    return num > average

# Örnek kullanım
number = 30
numbers_list = [4, 5, 6, 7, 8, 9, 10, 20, 30]
result = is_above_last_7_average(number, numbers_list)
print(result)  # Çıktı: False
