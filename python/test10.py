import re

data = """
PROSUSDT 0,7581 20,2 8,60 0,12 + + + + + 1,43
LTOUSDT 0,1704 14,3 0,76 0,13 + + + + + 1,73
CLVUSDT 0,1163 11,4 2,71 0,14 + + + + + 4,90
HARDUSDT 0,1517 8,6 2,47 0,03 + + - - - 0,94
XTZUSDT 1,060 8,4 1,40 0,06 + + - + + 1,53
XLMUSDT 0,2475 8,2 2,21 0,28 + + + + + 1,94
CREAMUSDT 17,27 6,9 5,31 0,04 + + + + + 1,19
RADUSDT 1,334 6,0 3,60 0,04 + + + + + 1,22
CTXCUSDT 0,3064 5,7 0,44 0,07 + + + + + 1,54
OAXUSDT 0,1608 5,0 6,82 0,05 + + + - - 1,02
DGBUSDT 0,009300 4,9 1,79 0,06 + + + + + 1,49
TUSDT 0,02817 4,0 0,76 0,14 + - + + + 1,20
SCRTUSDT 0,3285 4,0 3,01 0,05 + + + + + 1,47
XRPUSDT 1,122 2,9 1,69 0,16 + + + + + 1,32
SLPUSDT 0,003261 2,7 0,70 0,03 + + - + + 1,20
"""

pattern = re.compile(r'(\w+USDT)\s+\S+\s+(\S+)\s+(?:\S+\s+){7}(\S+)')

matches = pattern.findall(data)
result = [[match[0].replace(',', '.'), float(match[1].replace(',', '.')), float(match[2].replace(',', '.'))] for match in matches]

print(result)