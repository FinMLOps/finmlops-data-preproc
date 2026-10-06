import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
import requests
from dotenv import load_dotenv

load_dotenv()

URL = "https://finnhub.io/api/v1/company-news"


def main() -> None:
    today = datetime.now(timezone.utc)
    p = argparse.ArgumentParser(
        description="Fetch raw Finnhub company news.",
        epilog="example:\n  uv run python finnhub.py --symbols TSLA,AAPL --from YYYY-MM-DD --to YYYY-MM-DD",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--symbols", help="Comma-separated tickers, e.g. TSLA,AAPL")
    p.add_argument(
        "--from",
        dest="start",
        default=f"{today - timedelta(days=7):%Y-%m-%d}",
        help="Start date YYYY-MM-DD (default: 7 days ago)",
    )
    p.add_argument(
        "--to",
        dest="end",
        default=f"{today:%Y-%m-%d}",
        help="End date YYYY-MM-DD (default: today)",
    )
    if len(sys.argv) == 1:
        p.print_help()
        sys.exit(0)
    args = p.parse_args()

    token = os.environ.get("FINNHUB_API_TOKEN")
    if not token:
        sys.exit("Set FINNHUB_API_TOKEN in .env first.")

    folder = Path("data/finnhub") / f"date={today:%Y-%m-%d}"
    folder.mkdir(parents=True, exist_ok=True)

    # Finnhub takes one symbol per request; token goes in a header so it never appears in a URL
    for symbol in args.symbols.split(","):
        resp = requests.get(
            URL,
            params={"symbol": symbol, "from": args.start, "to": args.end},
            headers={"X-Finnhub-Token": token},
            timeout=30,
        )
        if resp.status_code != 200:
            print(
                f"{symbol}: HTTP {resp.status_code}: {resp.text[:300]}", file=sys.stderr
            )
            continue

        path = folder / f"{today:%Y%m%dT%H%M%S}Z_{symbol}.json"
        path.write_text(
            json.dumps(resp.json(), indent=2, ensure_ascii=False), encoding="utf-8"
        )
        print(f"saved {len(resp.json())} articles -> {path}")


if __name__ == "__main__":
    main()
