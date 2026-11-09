
import requests

BASE_URL = "https://api.dexscreener.com"

def scan_solana():
    url = f"{BASE_URL}/token-profiles/latest/v1"

    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()

        tokens = response.json()

        solana_tokens = [
            token for token in tokens
            if token.get("chainId") == "solana"
        ]

        results = []

        for token in solana_tokens[:20]:
            address = token.get("tokenAddress")

            if not address:
                continue

            pair_url = f"{BASE_URL}/latest/dex/tokens/{address}"
            pair_response = requests.get(pair_url, timeout=20)
            pair_response.raise_for_status()

            pairs = pair_response.json().get("pairs") or []

            if not pairs:
                continue

            pair = max(
                pairs,
                key=lambda p: float(
                    (p.get("liquidity") or {}).get("usd") or 0
                )
            )

            liquidity = float(
                (pair.get("liquidity") or {}).get("usd") or 0
            )

            volume = float(
                (pair.get("volume") or {}).get("h24") or 0
            )

            if liquidity >= 10000 and volume >= 5000:
                results.append({
                    "name": pair["baseToken"]["name"],
                    "symbol": pair["baseToken"]["symbol"],
                    "address": address,
                    "price": pair.get("priceUsd"),
                    "liquidity": liquidity,
                    "volume_24h": volume,
                    "url": pair.get("url")
                })

        return results

    except requests.RequestException as error:
        print("Scanner error:", error)
        return []

if __name__ == "__main__":
    coins = scan_solana()

    print("Coins found:", len(coins))

    for coin in coins:
        print(coin)
