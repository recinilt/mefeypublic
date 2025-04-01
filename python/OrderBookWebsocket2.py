import requests

def get_order_book_depth(symbol, depth=1000):
    # Binance API'den order book verisini çekme
    url = f"https://api.binance.com/api/v3/depth"
    params = {
        'symbol': symbol.upper(),
        'limit': depth
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data

def calculate_order_sum(symbol, percentage_threshold=3):
    # Order book verilerini getir
    order_book = get_order_book_depth(symbol)
    satis = order_book['asks']  # Satış emirleri (fiyat, miktar)
    alis = order_book['bids']  # Alış emirleri (fiyat, miktar)

    # Mevcut fiyatı belirle (En düşük satış emri)
    current_price = float(satis[0][0])

    # Hedef fiyat aralıklarını hesapla
    upper_limit = current_price * (1 + percentage_threshold / 100)
    lower_limit = current_price * (1 - percentage_threshold / 100)

    # Belirlenen yüzdelik aralıklara göre emir miktarlarını topla
    satis_sum = sum(float(amount) for price, amount in satis if float(price) <= upper_limit)
    alis_sum = sum(float(amount) for price, amount in alis if float(price) >= lower_limit)

    return [alis_sum, satis_sum, round((alis_sum/satis_sum),2)]

# Örnek kullanım: 'BTCUSDT' için emir toplamları
result = calculate_order_sum('BTCUSDT')
print(result)

coins=['BTCUSDT', 'ETHUSDT', 'BCHUSDT', 'XRPUSDT', 'EOSUSDT', 'LTCUSDT', 'TRXUSDT', 'ETCUSDT', 'LINKUSDT', 'XLMUSDT', 'ADAUSDT', 'XMRUSDT', 'DASHUSDT', 'ZECUSDT', 'XTZUSDT', 'BNBUSDT', 'ATOMUSDT', 'ONTUSDT', 'IOTAUSDT', 'BATUSDT', 'VETUSDT', 'NEOUSDT', 'QTUMUSDT', 'IOSTUSDT', 'THETAUSDT', 'ALGOUSDT', 'ZILUSDT', 'KNCUSDT', 'ZRXUSDT', 'COMPUSDT', 'OMGUSDT', 'DOGEUSDT', 'SXPUSDT', 'KAVAUSDT', 'BANDUSDT', 'RLCUSDT', 'WAVESUSDT', 'MKRUSDT', 'SNXUSDT', 'DOTUSDT', 'DEFIUSDT', 'YFIUSDT', 'BALUSDT', 'CRVUSDT', 'TRBUSDT', 'RUNEUSDT', 'SUSHIUSDT', 'EGLDUSDT', 'SOLUSDT', 'ICXUSDT', 'STORJUSDT', 'BLZUSDT', 'UNIUSDT', 'AVAXUSDT', 'FTMUSDT', 'ENJUSDT', 'FLMUSDT', 'RENUSDT', 'KSMUSDT', 'NEARUSDT', 'AAVEUSDT', 'FILUSDT', 'RSRUSDT', 'LRCUSDT', 'OCEANUSDT', 'CVCUSDT', 'BELUSDT', 'CTKUSDT', 'AXSUSDT', 'ALPHAUSDT', 'ZENUSDT', 'SKLUSDT', 'GRTUSDT', '1INCHUSDT', 'CHZUSDT', 'SANDUSDT', 'ANKRUSDT', 'LITUSDT', 'UNFIUSDT', 'REEFUSDT', 'RVNUSDT', 'SFPUSDT', 'XEMUSDT', 'BTCSTUSDT', 'COTIUSDT', 'CHRUSDT', 'MANAUSDT', 'ALICEUSDT', 'HBARUSDT', 'ONEUSDT', 'LINAUSDT', 'STMXUSDT', 'DENTUSDT', 'CELRUSDT', 'HOTUSDT', 'MTLUSDT', 'OGNUSDT', 'NKNUSDT', 'SCUSDT', 'DGBUSDT', '1000SHIBUSDT', 'BAKEUSDT', 'GTCUSDT', 'BTCDOMUSDT', 'IOTXUSDT', 'RAYUSDT', 'C98USDT', 'MASKUSDT', 'ATAUSDT', 'DYDXUSDT', '1000XECUSDT', 'GALAUSDT', 'CELOUSDT', 'ARUSDT', 'KLAYUSDT', 'ARPAUSDT', 'CTSIUSDT', 'LPTUSDT', 'ENSUSDT', 'PEOPLEUSDT', 'ROSEUSDT', 'DUSKUSDT', 'FLOWUSDT', 'IMXUSDT', 'API3USDT', 'GMTUSDT', 'APEUSDT', 'WOOUSDT', 'FTTUSDT', 'JASMYUSDT', 'DARUSDT', 'OPUSDT', 'INJUSDT', 'STGUSDT', 'SPELLUSDT', '1000LUNCUSDT', 'LUNA2USDT', 'LDOUSDT', 'CVXUSDT', 'ICPUSDT', 'APTUSDT', 'QNTUSDT', 'FETUSDT', 'FXSUSDT', 'HOOKUSDT', 'MAGICUSDT', 'TUSDT', 'HIGHUSDT', 'MINAUSDT', 'ASTRUSDT', 'AGIXUSDT', 'PHBUSDT', 'GMXUSDT', 'CFXUSDT', 'STXUSDT', 'BNXUSDT', 'ACHUSDT', 'SSVUSDT', 'CKBUSDT', 'PERPUSDT', 'TRUUSDT', 'LQTYUSDT', 'USDCUSDT', 'IDUSDT', 'ARBUSDT', 'JOEUSDT', 'TLMUSDT', 'AMBUSDT', 'LEVERUSDT', 'RDNTUSDT', 'HFTUSDT', 'XVSUSDT', 'ETHBTC', 'BLURUSDT', 'EDUUSDT', 'IDEXUSDT', 'SUIUSDT', '1000PEPEUSDT', '1000FLOKIUSDT', 'UMAUSDT', 'RADUSDT', 'KEYUSDT', 'COMBOUSDT', 'NMRUSDT', 'MAVUSDT', 'MDTUSDT', 'XVGUSDT', 'WLDUSDT', 'PENDLEUSDT', 'ARKMUSDT', 'AGLDUSDT', 'YGGUSDT', 'DODOXUSDT', 'BNTUSDT', 'OXTUSDT', 'SEIUSDT', 'CYBERUSDT', 'HIFIUSDT', 'ARKUSDT', 'GLMRUSDT', 'BICOUSDT', 'STRAXUSDT', 'LOOMUSDT', 'BIGTIMEUSDT', 'BONDUSDT', 'ORBSUSDT', 'STPTUSDT', 'WAXPUSDT', 'BSVUSDT', 'RIFUSDT', 'POLYXUSDT', 'GASUSDT', 'POWRUSDT', 'SLPUSDT', 'TIAUSDT', 'SNTUSDT', 'CAKEUSDT', 'MEMEUSDT', 'TWTUSDT', 'TOKENUSDT', 'ORDIUSDT', 'STEEMUSDT', 'BADGERUSDT', 'ILVUSDT', 'NTRNUSDT', 'KASUSDT', 'BEAMXUSDT', '1000BONKUSDT', 'PYTHUSDT', 
'SUPERUSDT', 'USTCUSDT', 'ONGUSDT', 'ETHWUSDT', 'JTOUSDT', '1000SATSUSDT', 'AUCTIONUSDT', '1000RATSUSDT', 'ACEUSDT', 'MOVRUSDT', 'NFPUSDT', 'BTCUSDC', 'ETHUSDC', 'BNBUSDC', 'SOLUSDC', 'XRPUSDC', 'AIUSDT', 'XAIUSDT', 'DOGEUSDC', 'WIFUSDT', 'MANTAUSDT', 'ONDOUSDT', 'LSKUSDT', 'ALTUSDT', 'JUPUSDT', 'ZETAUSDT', 'RONINUSDT', 'DYMUSDT', 'SUIUSDC', 'OMUSDT', 'LINKUSDC', 'PIXELUSDT', 'STRKUSDT', 'MAVIAUSDT', 'ORDIUSDC', 'GLMUSDT', 'PORTALUSDT', 'TONUSDT', 'AXLUSDT', 'MYROUSDT', '1000PEPEUSDC', 'METISUSDT', 'AEVOUSDT', 'WLDUSDC', 'VANRYUSDT', 'BOMEUSDT', 'ETHFIUSDT', 'AVAXUSDC', '1000SHIBUSDC', 'ENAUSDT', 'WUSDT', 'WIFUSDC', 'BCHUSDC', 'TNSRUSDT', 'SAGAUSDT', 'LTCUSDC', 'NEARUSDC', 'TAOUSDT', 'OMNIUSDT', 'ARBUSDC', 'NEOUSDC', 'FILUSDC', 'TIAUSDC', 'BOMEUSDC', 'REZUSDT', 'ENAUSDC', 'ETHFIUSDC', '1000BONKUSDC', 'BBUSDT', 'NOTUSDT', 'TURBOUSDT', 'IOUSDT', 'ZKUSDT', 'MEWUSDT', 'LISTAUSDT', 'ZROUSDT', 'BTCUSDT_241227', 'ETHUSDT_241227', 'CRVUSDC', 'RENDERUSDT', 'BANANAUSDT', 'RAREUSDT', 'GUSDT', 'SYNUSDT', 'SYSUSDT', 'VOXELUSDT', 'BRETTUSDT', 'ALPACAUSDT', 'POPCATUSDT', 'SUNUSDT', 'VIDTUSDT', 'NULSUSDT', 'DOGSUSDT', 'MBOXUSDT', 'CHESSUSDT', 'FLUXUSDT', 'BSWUSDT', 'QUICKUSDT', 'NEIROETHUSDT', 'RPLUSDT', 'AERGOUSDT', 'POLUSDT', 'UXLINKUSDT', '1MBABYDOGEUSDT', 'NEIROUSDT', 'KDAUSDT', 'FIDAUSDT', 'FIOUSDT', 'CATIUSDT', 'GHSTUSDT', 'LOKAUSDT', 'HMSTRUSDT', 'BTCUSDT_250328', 'ETHUSDT_250328', 'REIUSDT', 'COSUSDT', 'EIGENUSDT', 'DIAUSDT', '1000CATUSDT', 'SCRUSDT', 'GOATUSDT', 'MOODENGUSDT', 'SAFEUSDT', 'SANTOSUSDT', 'TROYUSDT', 'PONKEUSDT', 'COWUSDT', 'CETUSUSDT', '1000000MOGUSDT', 'GRASSUSDT', 'DRIFTUSDT', 'SWELLUSDT', 'ACTUSDT', 'PNUTUSDT', 'HIPPOUSDT', '1000XUSDT', 'DEGENUSDT', 'BANUSDT', 'AKTUSDT', 'SLERFUSDT', 'SCRTUSDT', '1000CHEEMSUSDT', '1000WHYUSDT', 'THEUSDT', 'MORPHOUSDT', 'CHILLGUYUSDT', 'KAIAUSDT', 'AEROUSDT', 'ACXUSDT', 'ORCAUSDT', 'MOVEUSDT', 'RAYSOLUSDT', 'KOMAUSDT', 'VIRTUALUSDT', 'SPXUSDT', 'MEUSDT', 'AVAUSDT', 'DEGOUSDT', 'VELODROMEUSDT', 'MOCAUSDT', 'VANAUSDT']
#symbols = ['btcusdt', 'ethusdt', 'bnbusdt']
symbols=coins[:100]

longacilacaklar=[]
for mycoin in symbols:
    print("değerlendirilen coin: ",mycoin)
    result=1
    try:
        result = calculate_order_sum(mycoin)[2]
    except:
        print("hata")
    if result>1.2:
        longacilacaklar.append([mycoin,result])
if longacilacaklar:
    longacilacaklar.sort(key=lambda x: x[1], reverse=True)

print(longacilacaklar)
