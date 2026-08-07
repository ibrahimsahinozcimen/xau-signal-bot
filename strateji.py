from indikatorler import ema, rsi, macd, atr


def analiz_et(highs, lows, closes):
    if len(closes) < 50:
        return {
            "signal": "WAIT",
            "score": 0,
            "reason": "Not enough data",
            "entry": None,
            "stop_loss": None,
            "take_profit": None
        }

    ema_fast = ema(closes, 20)
    ema_slow = ema(closes, 50)
    rsi_value = rsi(closes, 14)
    macd_value = macd(closes)
    atr_value = atr(highs, lows, closes, 14)

    score_buy = 0
    score_sell = 0
    reasons = []

    if ema_fast is not None and ema_slow is not None:
        if ema_fast > ema_slow:
            score_buy += 25
            reasons.append("EMA bullish")
        elif ema_fast < ema_slow:
            score_sell += 25
            reasons.append("EMA bearish")

    if rsi_value is not None:
        if 50 < rsi_value < 70:
            score_buy += 25
            reasons.append("RSI bullish")
        elif 30 < rsi_value < 50:
            score_sell += 25
            reasons.append("RSI bearish")

    if macd_value is not None:
        if macd_value["macd"] > macd_value["signal"]:
            score_buy += 30
            reasons.append("MACD bullish")
        elif macd_value["macd"] < macd_value["signal"]:
            score_sell += 30
            reasons.append("MACD bearish")

    signal = "WAIT"
    score = max(score_buy, score_sell)

    if score_buy > score_sell and score_buy >= 80:
        signal = "BUY"
        score = score_buy

    elif score_sell > score_buy and score_sell >= 80:
        signal = "SELL"
        score = score_sell

    entry = None
    stop_loss = None
    take_profit = None

    if signal in ["BUY", "SELL"] and atr_value is not None:
        entry = closes[-1]

        if signal == "BUY":
            stop_loss = entry - (atr_value * 1.5)
            take_profit = entry + (atr_value * 3.0)

        elif signal == "SELL":
            stop_loss = entry + (atr_value * 1.5)
            take_profit = entry - (atr_value * 3.0)

        reasons.append("ATR based SL/TP")

    return {
        "signal": signal,
        "score": score,
        "reason": ", ".join(reasons),
        "entry": entry,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "atr": atr_value
    }
