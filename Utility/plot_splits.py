"""Plot and validate the saved evaluation splits for assets A through F.

Run from any directory: python path/to/Utility/plot_splits.py
Requires pandas and matplotlib. UnseenData is the separate final holdout and
is intentionally excluded from these evaluation training/testing plots.
"""

import argparse
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
ASSETS = tuple(f"Asset_{letter}" for letter in "ABCDEF")
TRAIN_COLOR = "#1976b8"
TEST_COLOR = "#e07818"


def load_splits(data_dir):
    """Read the actual saved files; preserve row order so checks can detect errors."""
    splits = {}
    for asset in ASSETS:
        paths = {
            "combined": data_dir / f"{asset}.csv",
            "training": data_dir / "Training" / f"{asset}_train.csv",
            "testing": data_dir / "Testing" / f"{asset}_test.csv",
        }
        splits[asset] = {}
        for name, path in paths.items():
            frame = pd.read_csv(path, parse_dates=["Date"])
            if frame.empty or frame["Date"].isna().any():
                raise ValueError(f"{path}: empty data or invalid dates")
            # Nasdaq CSVs store prices as strings such as '$28.43'.
            prices = pd.to_numeric(
                frame["Close/Last"].astype(str).str.replace(r"[$,]", "", regex=True),
                errors="raise",
            )
            if prices.isna().any():
                raise ValueError(f"{path}: missing closing prices")
            frame["Close/Last"] = prices
            splits[asset][name] = frame
    return splits


def validate_splits(splits):
    """Check the 80/20 split against every column of the sorted source data."""
    records = []
    for asset, frames in splits.items():
        source, train, test = (frames[key] for key in ("combined", "training", "testing"))
        expected = source.sort_values("Date").reset_index(drop=True)
        boundary = int(len(expected) * 0.8)
        issues = []
        for name, frame in frames.items():
            if not frame["Date"].is_monotonic_increasing:
                issues.append(f"{name} dates are not chronological")
            if frame["Date"].duplicated().any():
                issues.append(f"{name} has duplicate dates")
        overlap = len(set(train["Date"]) & set(test["Date"]))
        if overlap:
            issues.append(f"{overlap} overlapping dates")
        if train["Date"].max() >= test["Date"].min():
            issues.append("training does not end before testing")
        for name, actual, wanted in (
            ("training", train, expected.iloc[:boundary]),
            ("testing", test, expected.iloc[boundary:]),
            ("recombined", pd.concat([train, test]), expected),
        ):
            try:
                pd.testing.assert_frame_equal(
                    actual.reset_index(drop=True), wanted.reset_index(drop=True),
                    check_dtype=False, check_exact=True,
                )
            except AssertionError:
                issues.append(f"{name} rows differ from source / expected 80:20 split")
        records.append({
            "asset": asset,
            "source_rows": len(source),
            "training_rows": len(train),
            "testing_rows": len(test),
            "training_end": train["Date"].max().date().isoformat(),
            "testing_start": test["Date"].min().date().isoformat(),
            "overlap_dates": overlap,
            "status": "FAIL" if issues else "PASS",
            "issues": "; ".join(issues),
        })
    return pd.DataFrame(records)


def plot_splits(splits, summary):
    """Return an 18-panel figure with shared date and price scales per asset."""
    fig, axes = plt.subplots(6, 3, figsize=(21, 23), sharex=True, sharey="row",
                             layout="constrained")
    statuses = summary.set_index("asset")["status"]
    for row, (asset, frames) in enumerate(splits.items()):
        source, train, test = (frames[key] for key in ("combined", "training", "testing"))
        for col, (name, frame, color) in enumerate((
            ("Training", train, TRAIN_COLOR),
            ("Testing", test, TEST_COLOR),
            ("Combined", source, "#555555"),
        )):
            ax = axes[row, col]
            if col == 2:
                ax.plot(source["Date"], source["Close/Last"], color=color,
                        linewidth=2.5, alpha=0.5, label="Original evaluation data")
                for part, shade, label in ((train, TRAIN_COLOR, "Training"),
                                           (test, TEST_COLOR, "Testing")):
                    ax.plot(part["Date"], part["Close/Last"], color=shade,
                            linewidth=1, label=label)
                ax.legend(loc="upper left", fontsize=7)
            else:
                ax.plot(frame["Date"], frame["Close/Last"], color=color, linewidth=1)
            ax.axvline(test["Date"].min(), color="#555555", linestyle="--",
                       linewidth=0.8)
            dates = f"{frame['Date'].min():%Y-%m-%d} to {frame['Date'].max():%Y-%m-%d}"
            ax.set_title(f"{asset} | {name} | n={len(frame):,}\n{dates}", fontsize=10)
            ax.grid(alpha=0.2)
            locator = mdates.AutoDateLocator(minticks=3, maxticks=6)
            ax.xaxis.set_major_locator(locator)
            ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))
            ax.tick_params(axis="x", labelbottom=True)
        axes[row, 0].set_ylabel(f"Close price ($)\nSplit check: {statuses[asset]}")
    fig.suptitle(
        "Assets A–F: evaluation data split audit\n"
        "Training (blue), testing (orange); dashed line = first testing date. "
        "Shared scales expose split coverage.\n"
        "Combined overlays saved splits on the original evaluation data. "
        "Separate unseen holdout excluded.", fontsize=15,
    )
    return fig


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=ROOT / "Data" / "EvaluationData")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "StrategyDev" / "split_plots")
    parser.add_argument("--no-show", action="store_true", help="Save without opening a plot window")
    args = parser.parse_args(argv)
    if args.no_show:
        plt.switch_backend("Agg")
    splits = load_splits(args.data_dir)
    summary = validate_splits(splits)
    fig = plot_splits(splits, summary)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output_dir / "asset_splits.png", dpi=150)
    summary.to_csv(args.output_dir / "split_validation.csv", index=False)
    print(summary.to_string(index=False))
    print(f"\nSaved plots and validation report to {args.output_dir.resolve()}")
    if not args.no_show:
        plt.show()
    plt.close(fig)
    return 1 if summary["status"].eq("FAIL").any() else 0


if __name__ == "__main__":
    raise SystemExit(main())
