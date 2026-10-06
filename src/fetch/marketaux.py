import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
import requests
from dotenv import load_dotenv

load_dotenv()

URL = "https://api.marketaux.com/v1/news/all"


def main() -> None:
    p = argparse.ArgumentParser(
        description="Fetch raw Marketaux news.",
        epilog="example:\n  uv run python marketaux.py --symbols TSLA,AAPL",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--symbols", help="Comma-separated tickers, e.g. TSLA,AAPL")
    if len(sys.argv) == 1:
        p.print_help()
        sys.exit(0)
    symbols = p.parse_args().symbols

    token = os.environ.get("MARKETAUX_API_TOKEN")
    if not token:
        sys.exit("Set MARKETAUX_API_TOKEN in .env first.")

    resp = requests.get(
        URL,
        params={
            "api_token": token,
            "symbols": symbols,
            "language": "en",
            "filter_entities": "true",
        },
        timeout=30,
    )
    if resp.status_code != 200:
        sys.exit(f"HTTP {resp.status_code}: {resp.text[:300]}")

    now = datetime.now(timezone.utc)
    folder = Path("data/marketaux") / f"date={now:%Y-%m-%d}"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{now:%Y%m%dT%H%M%S}Z_{symbols.replace(',', '-')}.json"
    path.write_text(
        json.dumps(resp.json(), indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"saved -> {path}")


if __name__ == "__main__":
    main()
