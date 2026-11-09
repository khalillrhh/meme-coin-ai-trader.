
MAX_TRADE_SIZE = 20.0
MAX_OPEN_POSITIONS = 5
MAX_PORTFOLIO_RISK = 0.10

MIN_LIQUIDITY = 10000
MIN_VOLUME_24H = 5000


def check_risk(coin, open_positions, cash_balance):
    try:
        liquidity = float(coin.get("liquidity") or 0)
        volume = float(coin.get("volume_24h") or 0)
        price = float(coin.get("price") or 0)
    except (ValueError, TypeError):
        return False, "Invalid market data"

    if price <= 0:
        return False, "Invalid price"

    if liquidity < MIN_LIQUIDITY:
        return False, "Liquidity too low"

    if volume < MIN_VOLUME_24H:
        return False, "Trading volume too low"

    if len(open_positions) >= MAX_OPEN_POSITIONS:
        return False, "Maximum positions reached"

    address = coin.get("address")

    if not address:
        return False, "Missing token address"

    if address in open_positions:
        return False, "Position already exists"

    if cash_balance < MAX_TRADE_SIZE:
        return False, "Insufficient virtual balance"

    return True, "Risk checks passed"
