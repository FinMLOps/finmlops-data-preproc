# finmlops-data-preproc

Collects raw financial news from Marketaux and Finnhub.

## Project structure

```
.
├── src/
│   ├── fetch/
│   │   ├── marketaux.py  # Marketaux news collector
│   │   └── finnhub.py    # Finnhub company-news collector
│   ├── finbert.py        # FinBERT sentiment model wrapper
│   └── try_finbert.py    # score a single text from the command line
├── pyproject.toml        # dependencies
├── uv.lock               # pinned versions
├── .python-version       # Python version for uv
├── .env.example          # template for API keys
├── .env                  # your real keys (gitignored)
└── data/                 # collected output (gitignored)
    ├── marketaux/YYYY-MM-DD/<timestamp>Z_<symbols>.json
    └── finnhub/date=YYYY-MM-DD/<timestamp>Z_<symbol>.json
```

## Setup

Requires [uv](https://docs.astral.sh/uv/). It reads `.python-version` and `uv.lock` to pin the Python and package versions, keeping the environment reproducible and stable across machines.

```bash
git clone https://github.com/FinMLOps/finmlops-data-preproc
cd finmlops-data-preproc
uv sync --frozen
```

`uv sync --frozen` installs exactly what is in `uv.lock` into `.venv`, and uv fetches the right Python if you don't have it.

To add a dependency, use `uv add <package>` and commit the updated `pyproject.toml` and `uv.lock`.

## API keys

Get free keys from [Marketaux](https://www.marketaux.com) and [Finnhub](https://finnhub.io), copy `.env.example` to `.env`, and fill in the API tokens there.

## Run

Running a script with no arguments prints its help.

```bash
# Marketaux
uv run python src/fetch/marketaux.py --symbols TSLA,AAPL

# Finnhub (dates optional; default is the last 7 days)
uv run python src/fetch/finnhub.py --symbols TSLA,AAPL --from 2026-10-01 --to 2026-10-05
```

Output is pretty-printed JSON, one folder per collection day (UTC).

### Try FinBERT on one text

```bash
uv run python src/try_finbert.py "Tesla beats earnings, stock surges"
```

Prints the positive, negative and neutral scores plus the verdict. The first run downloads the model (several hundred MB).
