def close_position():
    # Mevcut pozisyonu kapat
    positions = client.futures_position_information(symbol=symbol)
    for position in positions:
        if float(position['positionAmt']) != 0:
            side = SIDE_SELL if float(position['positionAmt']) > 0 else SIDE_BUY
            order = client.futures_create_order(
                symbol=symbol,
                side=side,
                type=ORDER_TYPE_MARKET,
                quantity=abs(float(position['positionAmt']))
            )
            print(f"Pozisyon kapatıldı: {order}")
            time.sleep(10)  # 10 saniye bekle


