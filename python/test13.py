quantity = 0.44500000  # Örnek miktar
precision = 6  # İzin verilen maksimum hassasiyet

# Miktarı izin verilen hassasiyete yuvarla
quantity = float(round(quantity, precision))

print(quantity)
