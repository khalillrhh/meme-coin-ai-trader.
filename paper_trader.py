
import json
import os
from datetime import datetime, timezone

STATE_FILE = "paper_state.json"
INITIAL_BALANCE = 1000.0
TRADE_SIZE = 20.0

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
    price = float(coin["price"])

    if address in state["positions"]:
        return

    if price <= 0 or state["balance"] < TRADE_SIZE:
        return

    quantity = TRADE_SIZE / price

    state["balance"] -= TRADE_SIZE

    state["positions"][address] = {
        "symbol": coin["symbol"],
        "entry_price": price,
        "quantity": quantity,
        "invested": TRADE_SIZE,
        "opened_at": datetime.now(timezone.utc).isoformat()
    }

    print("PAPER BUY:", coin["symbol"])

def update_positions(state, coins):
    prices = {
        coin["address"]: float(coin["price"])
        for coin in coins
        if coin.get("price")
    }

    for address, position in state["positions"].items():
        current_price = prices.get(address)

        if current_price is None:
            continue

        entry = position["entry_price"]
        change = (current_price / entry - 1) * 100

        print(
            position["symbol"],
            "Change:",
            round(change, 2),
            "%"
        )

def portfolio_summary(state):
    print("Virtual cash:", round(state["balance"], 2))
    print("Open positions:", len(state["positions"]))
    print("Closed trades:", len(state["history"]))
