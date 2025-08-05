// martingale-worker.js
self.onmessage = function(e) {
    const { combinations, data, params } = e.data;
    const results = [];
    let processed = 0;
    
    // Worker içinde progress gönder
    const sendProgress = () => {
        self.postMessage({ 
            type: 'progress', 
            processed: processed, 
            total: combinations.length 
        });
    };
    
    for (const combo of combinations) {
        const result = testMultiCoinCombination(combo, data, params);
        if (result) results.push(result);
        processed++;
        
        // Her 50 kombinasyonda progress gönder
        if (processed % 50 === 0) {
            sendProgress();
        }
    }
    
    // Final sonuçları gönder
    self.postMessage({ 
        type: 'complete', 
        results: results 
    });
};

// testMultiCoinCombination fonksiyonunu worker'a kopyala
const testMultiCoinCombination = (params, data, globalParams) => {
    try {
        let totalInitialBalance = 0, totalFinalBalance = 0, totalTrades = 0, totalWins = 0;
        let totalProfit = 0, totalLoss = 0, maxConsecutiveLosses = 0, maxDrawdown = 0;
        let exceedsInitialBalance = false;
        let allReturns = [];
        
        for (const coin of params.coins) {
            const state = {
                balance: params.initialBalance,
                initialBalance: params.initialBalance,
                currentBet: params.initialBet,
                peakBalance: params.initialBalance,
                maxDrawdown: 0,
                totalTrades: 0,
                winTrades: 0,
                consecutiveLosses: 0,
                maxConsecutiveLosses: 0,
                totalProfit: 0,
                totalLoss: 0,
                position: { isOpen: false, entryPrice: 0, betAmount: 0 },
                betExceededCapital: false,
                returns: []
            };
            
            let lastBalance = params.initialBalance;
            
            for (let i = 0; i < data[coin].length && state.totalTrades < params.maxTrades; i++) {
                if (!processCandle(data[coin][i], state, params)) break;
                updateDrawdown(state);
                
                if (i > 0 && lastBalance > 0) {
                    const return_ = (state.balance - lastBalance) / lastBalance;
                    state.returns.push(return_);
                }
                lastBalance = state.balance;
            }
            
            totalInitialBalance += params.initialBalance;
            totalFinalBalance += state.balance;
            totalTrades += state.totalTrades;
            totalWins += state.winTrades;
            totalProfit += state.totalProfit;
            totalLoss += state.totalLoss;
            maxConsecutiveLosses = Math.max(maxConsecutiveLosses, state.maxConsecutiveLosses);
            maxDrawdown = Math.max(maxDrawdown, state.maxDrawdown);
            
            if (state.betExceededCapital) {
                exceedsInitialBalance = true;
            }
            
            allReturns.push(...state.returns);
        }
        
        const roi = totalFinalBalance / totalInitialBalance;
        const winRate = totalTrades > 0 ? (totalWins / totalTrades) * 100 : 0;
        const profitFactor = totalLoss > 0 ? totalProfit / totalLoss : 0;
        
        return {
            leverage: params.leverage,
            profitPercent: params.profitPercent,
            multiplier: params.multiplier,
            direction: params.direction,
            initialBet: params.initialBet,
            roi, finalBalance: totalFinalBalance, maxConsecutiveLosses,
            totalTrades, maxDrawdown, winRate, profitFactor,
            coins: params.coins.length,
            exceedsInitialBalance,
            returns: allReturns
        };
    } catch (error) {
        return null;
    }
};

// processCandle ve updateDrawdown fonksiyonlarını da kopyala
const processCandle = (candle, state, params) => {
    const [, open, high, low] = candle.map((val, i) => i === 0 ? parseInt(val) : parseFloat(val));
    
    const lossPercent = params.profitPercent;
    
    if (!state.position.isOpen) {
        if (state.currentBet > state.initialBalance) {
            state.betExceededCapital = true;
        }
        
        if (state.balance < state.currentBet || state.currentBet > state.balance * 0.95) {
            return false;
        }
        
        state.position.isOpen = true;
        state.position.entryPrice = open;
        state.position.betAmount = state.currentBet;
        state.balance -= state.currentBet;
        state.totalTrades++;
        return true;
    }
    
    let profitTarget, stopLossPrice;
    
    if (params.direction === 'long') {
        profitTarget = state.position.entryPrice * (1 + params.profitPercent / 100);
        stopLossPrice = state.position.entryPrice * (1 - lossPercent / 100);
        
        if (high >= profitTarget) {
            const profit = state.currentBet * params.leverage * (params.profitPercent / 100);
            state.balance += state.currentBet + profit;
            state.totalProfit += profit;
            state.winTrades++;
            state.consecutiveLosses = 0;
            state.currentBet = calculateInitialBet(params.minBetSize, params.leverage);
            state.position.isOpen = false;
            return true;
        }
        
        if (low <= stopLossPrice) {
            state.totalLoss += state.currentBet;
            state.consecutiveLosses++;
            state.maxConsecutiveLosses = Math.max(state.maxConsecutiveLosses, state.consecutiveLosses);
            state.currentBet = Math.min(state.currentBet * params.multiplier, state.balance * 0.95);
            state.position.isOpen = false;
            return true;
        }
    } else {
        profitTarget = state.position.entryPrice * (1 - params.profitPercent / 100);
        stopLossPrice = state.position.entryPrice * (1 + lossPercent / 100);
        
        if (low <= profitTarget) {
            const profit = state.currentBet * params.leverage * (params.profitPercent / 100);
            state.balance += state.currentBet + profit;
            state.totalProfit += profit;
            state.winTrades++;
            state.consecutiveLosses = 0;
            state.currentBet = calculateInitialBet(params.minBetSize, params.leverage);
            state.position.isOpen = false;
            return true;
        }
        
        if (high >= stopLossPrice) {
            state.totalLoss += state.currentBet;
            state.consecutiveLosses++;
            state.maxConsecutiveLosses = Math.max(state.maxConsecutiveLosses, state.consecutiveLosses);
            state.currentBet = Math.min(state.currentBet * params.multiplier, state.balance * 0.95);
            state.position.isOpen = false;
            return true;
        }
    }
    return true;
};

const updateDrawdown = (state) => {
    if (state.balance > state.peakBalance) state.peakBalance = state.balance;
    const currentDrawdown = state.peakBalance > 0 ? (state.peakBalance - state.balance) / state.peakBalance * 100 : 0;
    state.maxDrawdown = Math.max(state.maxDrawdown, currentDrawdown);
};

const calculateInitialBet = (minBetSize, leverage) => Math.max(minBetSize / leverage, 0.1);