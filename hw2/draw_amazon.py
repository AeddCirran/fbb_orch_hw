#!/usr/bin/env python3

import argparse
import json
import re
from pathlib import Path
import matplotlib.pyplot as plt


def parse_price(price_str):
    if not price_str:
        return None, None

    if "EUR" in price_str or "€" in price_str:
        currency = "EUR"
    elif "USD" in price_str or "$" in price_str:
        currency = "USD"
    elif "GBP" in price_str or "£" in price_str:
        currency = "GBP"
    elif "RUB" in price_str or "₽" in price_str:
        currency = "RUB"
    else:
        match = re.match(r"([^\d\s,.]+)\s*", price_str)
        if match:
            currency = match.group(1)
        else:
            currency = "???"

    cleaned = re.sub(r"[^\d.,]", "", price_str).replace(",", "")
    try:
        value = float(cleaned)
    except ValueError:
        return None, currency

    return value, currency


def main():
    parser = argparse.ArgumentParser(description="Draw Amazon hist")
    parser.add_argument("--json", required=True, help="Path to json file")
    args = parser.parse_args()

    with open(args.json, "r", encoding="utf-8") as f:
        data = json.load(f)

    prices = []
    currencies = set()
    for item in data:
        price_str = item.get("price")
        if not price_str:
            continue
        value, currency = parse_price(price_str)
        if value is not None:
            prices.append(value)
            if currency:
                currencies.add(currency)

    if not prices:
        raise SystemExit("No prices")

    if len(currencies) == 1:
        currency_label = list(currencies)[0]
    elif len(currencies) == 0:
        currency_label = "unknown curr"
    else:
        currency_label = "mixed curr"

    plt.figure(figsize=(10, 6))
    plt.hist(prices, bins=20, edgecolor="black", color="steelblue", alpha=0.85)
    plt.title(f"Price distribution")
    plt.xlabel(f"Price ({currency_label})")
    plt.ylabel("Num")
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    output_img = f"{args.json}.png"
    plt.savefig(output_img, dpi=150, bbox_inches="tight")
    print(f"Hist saved to {output_img}")
    plt.show()


if __name__ == "__main__":
    main()
