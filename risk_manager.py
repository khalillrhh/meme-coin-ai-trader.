
MAX_TRADE_SIZE = 20.0
MAX_OPEN_POSITIONS = 5
MAX_PORTFOLIO_RISK = 0.10

MIN_LIQUIDITY = 10000
MIN_VOLUME_24H = 5000

def check_risk(coin, open_positions, cash_balance):
    liquidity = float(coin.get("liquidity", 0))
    volume = float(coin.get("volume_24h", 0))
    price = float(coin.get("price", 0) or 0)

    if price <= 0:
        return False, "Invalid price"

    if liquidity < MIN_LIQUIDITY:
        return False, "Liquidity too low"

    if volume < MIN_VOLUME_24H:
        return False, "Trading volume too low"

    if len(open_positions) >= MAX_OPEN_POSITIONS:
        return False, "Maximum positions reached"

    if cash_balance < MAX_TRADE_SIZE:
        return False, "Insufficient virtual balance"

    return True, "Risk checks passed"
