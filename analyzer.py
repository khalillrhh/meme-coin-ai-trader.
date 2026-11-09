
def analyze_coin(coin):
    liquidity = float(coin.get("liquidity", 0))
    volume = float(coin.get("volume_24h", 0))
    price = float(coin.get("price", 0) or 0)

    score = 0
    reasons = []

    if liquidity >= 50000:
        score += 35
        reasons.append("Good liquidity")
    elif liquidity >= 10000:
        score += 20
        reasons.append("Moderate liquidity")
    else:
        reasons.append("Low liquidity")

    if volume >= 100000:
        score += 35
        reasons.append("High trading volume")
    elif volume >= 10000:
        score += 20
        reasons.append("Moderate trading volume")
    else:
        reasons.append("Low trading volume")

    if price > 0:
        score += 20
        reasons.append("Valid price")
    else:
        reasons.append("Invalid price")

    if volume > 0 and liquidity > 0:
        ratio = volume / liquidity

        if ratio <= 5:
            score += 10
            reasons.append("Volume/liquidity ratio acceptable")
        else:
            reasons.append("Unusually high volume/liquidity ratio")

    return {
        "symbol": coin.get("symbol", "UNKNOWN"),
        "score": score,
        "status": "WATCH" if score >= 60 else "REJECT",
        "reasons": reasons
    }
