
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
from telegram_bot import send_telegram
from datetime import datetime, timezone

def main():
    state = load_state()
    coins = scan_solana()

    update_positions(state, coins)

    opportunities = []

    for coin in coins:
        analysis = analyze_coin(coin)

        if analysis["status"] != "WATCH":
            continue

        allowed, reason = check_risk(
            coin,
            state["positions"],
            state["balance"]
        )

        if allowed:
            open_trade(state, coin)
            opportunities.append(
                f'{coin["symbol"]} | Score: {analysis["score"]}/100'
            )

    save_state(state)

    summary = (
        "MEME COIN PAPER TRADER\n"
        f"Time: {datetime.now(timezone.utc)}\n"
        f"Coins scanned: {len(coins)}\n"
        f"Virtual balance: ${state['balance']:.2f}\n"
        f"Open positions: {len(state['positions'])}\n"
        f"Opportunities: {len(opportunities)}\n\n"
        + "\n".join(opportunities[:10])
    )

    print(summary)
    send_telegram(summary)

if __name__ == "__main__":
    main()
