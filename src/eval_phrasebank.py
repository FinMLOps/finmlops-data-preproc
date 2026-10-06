"""Score a FinBERT model on the fixed Financial PhraseBank test split.

Saves macro F1 / precision / recall to --out (default results/baseline_phrasebank.json).
Re-score the fine-tuned model on this same split to compare.
Note: ProsusAI/finbert was trained on PhraseBank, so this is an upper bound and a
regression check, not a measure of performance on new news.
"""

import argparse
import json
from pathlib import Path
from datasets import load_dataset
from sklearn.metrics import (
    classification_report,
    f1_score,
    precision_score,
    recall_score,
)
from finbert import SentimentAnalysisModel

DATASET = "atrost/financial_phrasebank"  # pre-split train/validation/test
BATCH = 64


def main() -> None:
    p = argparse.ArgumentParser(
        description="Score a FinBERT model on the fixed Financial PhraseBank test split.",
        epilog="example:\n  uv run python eval_phrasebank.py --model path/to/finetuned_model --out results/finetuned_phrasebank.json",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument(
        "--model", default="ProsusAI/finbert", help="Model name or local path"
    )
    p.add_argument(
        "--out", default="results/baseline_phrasebank.json", help="Metrics JSON path"
    )
    args = p.parse_args()
    out = Path(args.out)

    test = load_dataset(DATASET, split="test")
    names = test.features["label"].names  # negative, neutral, positive
    sentences = list(test["sentence"])
    y_true = [names[i] for i in test["label"]]

    model = SentimentAnalysisModel(args.model)
    y_pred: list[str] = []
    for i in range(0, len(sentences), BATCH):
        y_pred += [
            p["label"] for p in model.bulk_predict_sentiment(sentences[i : i + BATCH])
        ]
        print(f"scored {min(i + BATCH, len(sentences))}/{len(sentences)}")

    metrics = {
        "model": args.model,
        "dataset": DATASET,
        "split": "test",
        "n": len(y_true),
        "macro_f1": f1_score(y_true, y_pred, average="macro"),
        "macro_precision": precision_score(y_true, y_pred, average="macro"),
        "macro_recall": recall_score(y_true, y_pred, average="macro"),
        "per_class": classification_report(y_true, y_pred, output_dict=True),
    }

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(classification_report(y_true, y_pred))
    print(f"macro F1: {metrics['macro_f1']:.4f}  -> {out}")


if __name__ == "__main__":
    main()
