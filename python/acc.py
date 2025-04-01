import re

def usdt_veri_islemeACC(metin):
    #XLMUSDT 0,5059 17,1 2,01 0,24 + + + + + 1,86
    #[['XLMUSDT', [0.5059, 17.1, 2.01, 0.24], [True, True, True, True, True], 1.86]
    pattern = re.compile(r"(\w+USDT)\s([\d,]+)\s([\d,]+)\s([\d,]+)\s([\d,]+)\s([\+\-])\s([\+\-])\s([\+\-])\s([\+\-])\s([\+\-])\s([\d,]+)")
    matches = pattern.findall(metin)

    result = []

    for match in matches:
        coin = match[0]
        numbers = [float(num.replace(",", ".")) for num in match[1:5]]
        trend = [True if t == "+" else False for t in match[5:10]]
        score = float(match[10].replace(",", "."))
        result.append([coin, numbers, trend, score])

    return result

# Fonksiyonu kullanarak sonuçları alalım
metin = '''
XLMUSDT 0,5059 17,1 2,01 0,24 + + + + + 1,86
SKLUSDT 0,06369 10,9 3,80 0,31 + + + + + 1,57
BBUSDT 0,3884 10,3 2,54 0,51 + + + + + 1,71
COSUSDT 0,01221 8,1 0,89 0,04 + + + + + 1,76
XRPUSDT 1,455 6,3 1,48 0,18 + + + + + 1,26
PROSUSDT 0,7190 6,0 8,21 0,04 + + + + - 1,14
FTTUSDT 2,317 5,2 1,73 0,01 + + - - - 1,00
CLVUSDT 0,08796 5,0 1,26 0,01 + + - - - 0,91
AMPUSDT 0,005209 3,8 2,09 0,01 + + + + + 1,14
FTMUSDT 1,079 3,2 0,45 0,14 - + + + + 1,56
PHBUSDT 1,917 3,2 1,31 0,11 + + + + + 1,19
BTTCUSDT 0,00000130 3,1 0,77 0,02 + + + - + 1,11
NEARUSDT 6,756 2,6 0,58 0,10 + + + + + 1,30
OGUSDT 5,672 2,0 0,30 0,01 - - - + + 1,03
PNUTUSDT 1,106 1,4 1,07 0,02 + + - - - 0,84
'''

sonuc = usdt_veri_isleme(metin)
print(sonuc)
