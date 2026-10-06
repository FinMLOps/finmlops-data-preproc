# finmlops-data-preproc

Collects raw financial news from Marketaux and Finnhub.

> [!IMPORTANT]
> This project uses [uv](https://docs.astral.sh/uv/). Install with `uv sync --frozen`, run with `uv run`, add packages with `uv add`.

## Project structure

```
.
├── src/
│   ├── fetch/
│   │   ├── marketaux.py  # Marketaux news collector
│   │   └── finnhub.py    # Finnhub company-news collector
│   ├── finbert.py        # FinBERT sentiment model wrapper
│   ├── try_finbert.py    # score a single text from the command line
│   └── eval_phrasebank.py # score a model on the Financial PhraseBank test split
├── pyproject.toml        # dependencies
├── uv.lock               # pinned versions
├── .python-version       # Python version for uv
├── .env.example          # template for API keys
├── .env                  # your real keys (gitignored)
├── results/              # evaluation metrics
└── data/                 # collected output (gitignored)
    ├── marketaux/date=YYYY-MM-DD/<timestamp>Z_<symbols>.json
    └── finnhub/date=YYYY-MM-DD/<timestamp>Z_<symbol>.json
```

## Setup

```bash
git clone https://github.com/FinMLOps/finmlops-data-preproc
cd finmlops-data-preproc
uv sync --frozen
```

`uv sync --frozen` installs the exact versions pinned in `uv.lock`, so everyone gets the same environment.

After `uv add <package>`, commit `pyproject.toml` and `uv.lock`.

## API keys

Get free keys from [Marketaux](https://www.marketaux.com) and [Finnhub](https://finnhub.io), then copy `.env.example` to `.env` and add them.

## Run

Running a script with no arguments prints its help.

```bash
# Marketaux
uv run python src/fetch/marketaux.py --symbols TSLA,AAPL

# Finnhub (dates optional; default is the last 7 days)
uv run python src/fetch/finnhub.py --symbols TSLA,AAPL --from 2026-10-01 --to 2026-10-05
```

Output is pretty-printed JSON, one folder per UTC day.

### Try FinBERT on one text

```bash
uv run python src/try_finbert.py "Tesla beats earnings, stock surges"
```

Prints all three scores and a verdict. The first run downloads the model.

### Evaluate a model (baseline)

```bash
# pretrained FinBERT baseline -> results/baseline_phrasebank.json
uv run python src/eval_phrasebank.py

# a fine-tuned model (local HF-format directory), saved to a separate file
uv run python src/eval_phrasebank.py --model path/to/finetuned --out results/finetuned_phrasebank.json
```

Scores the fixed test split of [Financial PhraseBank](https://huggingface.co/datasets/atrost/financial_phrasebank), so runs compare directly. FinBERT trained on PhraseBank, so treat the baseline as an upper bound, not a measure on new news.

A fine-tuned model must be a full Hugging Face directory. For LoRA, run `merge_and_unload()` and then `save_pretrained`.
