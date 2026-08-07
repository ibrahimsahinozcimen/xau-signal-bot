def ema(prices, period):
    if len(prices) < period:
        return None

    multiplier = 2 / (period + 1)
    ema_value = sum(prices[:period]) / period

    for price in prices[period:]:
        ema_value = (price - ema_value) * multiplier + ema_value

    return ema_value


def rsi(prices, period=14):
    if len(prices) <= period:
        return None

    gains = []
    losses = []

    for i in range(1, len(prices)):
        change = prices[i] - prices[i - 1]

        if change > 0:
            gains.append(change)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(change))

    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    for i in range(period, len(gains)):
        avg_gain = ((avg_gain * (period - 1)) + gains[i]) / period
        avg_loss = ((avg_loss * (period - 1)) + losses[i]) / period

    if avg_loss == 0:
        return 100

    relative_strength = avg_gain / avg_loss
    return 100 - (100 / (1 + relative_strength))


def macd(prices, fast=12, slow=26, signal=9):
    if len(prices) < slow + signal:
        return None

    fast_values = []
    slow_values = []

    for i in range(slow, len(prices) + 1):
        fast_value = ema(prices[:i], fast)
        slow_value = ema(prices[:i], slow)

        if fast_value is not None and slow_value is not None:
            fast_values.append(fast_value)
            slow_values.append(slow_value)

    macd_values = [
        fast_values[i] - slow_values[i]
        for i in range(len(fast_values))
    ]

    if len(macd_values) < signal:
        return None

    signal_value = ema(macd_values, signal)

    return {
        "macd": macd_values[-1],
        "signal": signal_value
    }


def atr(highs, lows, closes, period=14):
    if len(highs) <= period:
        return None

    true_ranges = []

    for i in range(1, len(highs)):
        high = highs[i]
        low = lows[i]
        previous_close = closes[i - 1]

        true_range = max(
            high - low,
            abs(high - previous_close),
            abs(low - previous_close)
        )

        true_ranges.append(true_range)

    if len(true_ranges) < period:
        return None

    return sum(true_ranges[-period:]) / period
