const ccxt = require('ccxt');
const { DataFrame } = require('pandas-js');

// Binance API ve Secret Key'inizi buraya girin
const apiKey = 'XCmIMjw0JJYe18WGQ7zI5GYq2D930tagNZ7rampgzgHSJOieenSJqGPxIT4HtWjU';
const apiSecret = '0QlevlazX4plngg3sFfhbLMuS7nTJAZ6lBiXvSSldt1TD2ab26v7H34YZ4xyOkcD';

// Binance istemcisini başlatın
const exchange = new ccxt.binance({
    'apiKey': apiKey,
    'secret': apiSecret,
    'enableRateLimit': true,
});

// Supertrend hesaplama fonksiyonu
function supertrend(df, period = 7, multiplier = 3) {
    // ... Supertrend hesaplama kodları ...
    const hl2 = df.get(['high', 'low']).mean(1);
    const atr = hl2.rolling({ period }).apply(values => {
        return Math.abs(values[values.length - 1] - values[0]).mean();
    });
    const upperBand = hl2.add(atr.mul(multiplier));
    const lowerBand = hl2.sub(atr.mul(multiplier));
    let st = new DataFrame({ 'st': [] });
    df.get('close').forEach((close, i) => {
        if (close > upperBand.iloc(i - 1)) {
            st = st.append([lowerBand.iloc(i)]);
        } else {
            st = st.append([upperBand.iloc(i)]);
        }
    });
    return st;
}

// Veri çekme fonksiyonu
async function fetch_data(symbol, timeframe = '15m', limit = 400) {
    // ... Veri çekme kodları ...
    const ohlcv = await exchange.fetchOHLCV(symbol, timeframe, undefined, limit);
    const df = new DataFrame(ohlcv, ['timestamp', 'open', 'high', 'low', 'close', 'volume']);
    df.set_index('timestamp', inplace = true);
    return df;
}

// Alım satım sinyallerini üretme fonksiyonu
function generate_signals(df, st) {
    // ... Alım satım sinyalleri üretme kodları ...
    const buySignals = df.get('close').gt(st.shift(1));
    const sellSignals = df.get('close').lt(st.shift(1));
    return { buySignals, sellSignals };
}

// Kar zarar hesaplama fonksiyonu
function calculate_pnl(trades) {
    let totalProfit = 0;
    trades.forEach(trade => {
        totalProfit += trade.profit_loss;
    });
    return totalProfit;
}

// Alım satım işlemleri fonksiyonu
async function execute_trades(df, buySignals, sellSignals) {
    let position = null;
    let trades = new DataFrame({ 'buy_price': [], 'sell_price': [], 'profit_loss': [] });

    for (let i = 0; i < df.length; i++) {
        if (!position && buySignals.iloc(i)) {
            position = df.get('close').iloc(i);
            console.log(`Alım: ${position}`);
        } else if (position && sellSignals.iloc(i)) {
            const sellPrice = df.get('close').iloc(i);
            const profitLoss = sellPrice - position;
            trades = trades.append({ 'buy_price': position, 'sell_price': sellPrice, 'profit_loss': profitLoss });
            console.log(`Satım: ${sellPrice}, Kar/Zarar: ${profitLoss}`);
            position = null;
        }
    }

    return trades;
}

// Ana fonksiyon
(async function main() {
    const symbol = 'BTC/USDT'; // İşlem yapmak istediğiniz sembolü buraya girin
    const df = await fetch_data(symbol);
    const st = supertrend(df);
    const { buySignals, sellSignals } = generate_signals(df, st);

    // Alım satım işlemlerini gerçekleştirin ve kar zarar tablosunu hesaplayın
    const trades = await execute_trades(df, buySignals, sellSignals);
    const totalProfit = calculate_pnl(trades.to_json({ orient: 'records' }));
    console.log(`Toplam Kar/Zarar: ${totalProfit}`);
})();
