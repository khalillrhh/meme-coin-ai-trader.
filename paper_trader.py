
import json
import os
from datetime import datetime, timezone

STATE_FILE = "paper_state.json"

INITIAL_BALANCE = 1000.0
TRADE_SIZE = 20.0

TAKE_PROFIT = 30.0
STOP_LOSS = -15.0
SIMULATED_FEE = 0.01

MAX_OPEN_POSITIONS = 5


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)

    return {
        "balance": INITIAL_BALANCE,
        "positions": {},
        "history": []
    }


def save_state(state):
    temp_file = STATE_FILE + ".tmp"

    with open(temp_file, "w") as f:
        json.dump(state, f, indent=2)

    os.replace(temp_file, STATE_FILE)


def open_trade(state, coin):
    address = coin["address"]

    try:
        price = float(coin["price"])
    except (ValueError, TypeError):
        return

    if address in state["positions"]:
        return

    if len(state["positions"]) >= MAX_OPEN_POSITIONS:
        return

    if price <= 0 or state["balance"] < TRADE_SIZE:
        return

    quantity = TRADE_SIZE / price

    state["balance"] -= TRADE_SIZE

    state["positions"][address] = {
        "symbol": coin.get("symbol", "UNKNOWN"),
        "entry_price": price,
        "quantity": quantity,
        "invested": TRADE_SIZE,
        "opened_at": datetime.now(timezone.utc).isoformat()
    }

    print("PAPER BUY:", coin.get("symbol"))


def update_positions(state, coins):
    prices = {}

    for coin in coins:
        try:
            price = float(coin.get("price") or 0)
            if price > 0:
                prices[coin["address"]] = price
        except (ValueError, TypeError, KeyError):
            continue

    for address in list(state["positions"].keys()):
        position = state["positions"][address]
        current_price = prices.get(address)

        if current_price is None:
            continue

        entry = float(position["entry_price"])

        if entry <= 0:
            continue

        change = ((current_price / entry) - 1) * 100

        print(
            position["symbol"],
            "Change:",
            round(change, 2),
            "%"
        )

        if change >= TAKE_PROFIT or change <= STOP_LOSS:
            proceeds = (
                position["quantity"]
                * current_price
                * (1 - SIMULATED_FEE)
            )

            profit = proceeds - position["invested"]

            state["balance"] += proceeds

            state["history"].append({
                "symbol": position["symbol"],
                "entry_price": entry,
                "exit_price": current_price,
                "profit": round(profit, 4),
                "return_percent": round(change, 2),
                "closed_at": datetime.now(timezone.utc).isoformat()
            })

            print(
                "PAPER SELL:",
                position["symbol"],
                "Profit:",
                round(profit, 2)
            )

            del state["positions"][address]


def portfolio_summary(state):
    unrealized = 0.0

    print("Virtual cash:", round(state["balance"], 2))
    print("Open positions:", len(state["positions"]))
    print("Closed trades:", len(state["history"]))

    realized = sum(
        trade["profit"] for trade in state["history"]
    )

    print("Realized P/L:", round(realized, 2))
    print("Unrealized P/L: requires current market prices")
