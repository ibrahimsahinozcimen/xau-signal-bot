from indikatorler import ema, rsi, macd


def analiz_et(prices):
    if len(prices) < 50:
        return {
            "signal": "WAIT",
            "score": 0,
            "reason": "Yeterli veri yok"
        }

    ema_fast = ema(prices, 20)
    ema_slow = ema(prices, 50)
    rsi_value = rsi(prices, 14)
    macd_value = macd(prices)

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

    if score_buy > score_sell and score_buy >= 80:
        signal = "BUY"
        score = score_buy
    elif score_sell > score_buy and score_sell >= 80:
        signal = "SELL"
        score = score_sell
    else:
        signal = "WAIT"
        score = max(score_buy, score_sell)

    return {
        "signal": signal,
        "score": score,
        "reason": ", ".join(reasons)
        }
