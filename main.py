
from scanner import scan_solana
from analyzer import analyze_coin
from risk_manager import check_risk
from paper_trader import (
    load_state,
    save_state,
    open_trade,
    update_positions,
    portfolio_summary
)

def main():
    print("=" * 45)
    print("MEME COIN AI TRADER")
    print("PAPER TRADING MODE")
    print("=" * 45)

    state = load_state()

    # 1. Scan market
    coins = scan_solana()
    print("Coins discovered:", len(coins))

    # 2. Update existing positions
    update_positions(state, coins)

    # 3. Analyze and filter coins
    for coin in coins:
        analysis = analyze_coin(coin)

        print(
            coin["symbol"],
            "Score:", analysis["score"],
            "Status:", analysis["status"]
        )

        if analysis["status"] != "WATCH":
            continue

        # 4. Risk management
        allowed, reason = check_risk(
            coin,
            state["positions"],
            state["balance"]
        )

        if allowed:
            open_trade(state, coin)
            print("Decision: PAPER BUY")
        else:
            print("Decision: SKIP -", reason)

    # 5. Save and report
    save_state(state)
    portfolio_summary(state)

    print("Scan finished successfully.")

if __name__ == "__main__":
    main()
