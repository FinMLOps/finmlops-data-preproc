import argparse
import sys

from finbert import SentimentAnalysisModel


def main() -> None:
    p = argparse.ArgumentParser(
        description="Get FinBERT sentiment for one text.",
        epilog='example:\n  uv run python try_finbert.py "Tesla beats earnings, stock surges"',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("text", help="Text to score, in quotes")
    if len(sys.argv) == 1:
        p.print_help()
        sys.exit(0)
    result = SentimentAnalysisModel().predict_sentiment(p.parse_args().text)
    for label, prob in result["all_scores"].items():
        print(f"{label}: {prob:.1%}")
    print(f"verdict: {result['label']}")


if __name__ == "__main__":
    main()
