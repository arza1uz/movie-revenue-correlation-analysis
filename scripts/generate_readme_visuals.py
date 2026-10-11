from __future__ import annotations

from pathlib import Path

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "movies.csv"
ASSET_DIR = ROOT / "assets"
ASSET_DIR.mkdir(exist_ok=True)


def load_movies() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.strip().str.lower()

    numeric_columns = ["year", "score", "votes", "budget", "gross", "runtime"]
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    return df


def save(path: Path) -> None:
    plt.tight_layout()
    plt.savefig(path, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close()


def gross_distribution(df: pd.DataFrame) -> None:
    plt.figure(figsize=(10, 4))
    sns.boxplot(x=df["gross"], color="#2f6b9a")
    plt.xscale("log")
    plt.title("Gross Revenue Distribution")
    plt.xlabel("Gross Revenue (log scale)")
    save(ASSET_DIR / "01-gross-revenue-distribution.png")


def score_vs_gross(df: pd.DataFrame) -> None:
    plt.figure(figsize=(10, 6))
    sns.regplot(
        x="score",
        y="gross",
        data=df,
        scatter_kws={"alpha": 0.35, "s": 28, "color": "#2f6b9a"},
        line_kws={"color": "#b42318", "linewidth": 2},
    )
    plt.title("Movie Score vs Gross Revenue")
    plt.xlabel("IMDb Score")
    plt.ylabel("Gross Revenue")
    plt.grid(alpha=0.2)
    save(ASSET_DIR / "02-score-vs-gross.png")


def numeric_correlation(df: pd.DataFrame) -> None:
    numeric_df = df.select_dtypes(include=["number"])
    corr = numeric_df.corr(method="pearson")

    plt.figure(figsize=(10, 6))
    sns.heatmap(
        corr,
        annot=True,
        cmap="coolwarm",
        linewidths=0.5,
        fmt=".2f",
        vmin=-1,
        vmax=1,
    )
    plt.title("Correlation Matrix for Numeric Features")
    plt.xlabel("Movie Features")
    plt.ylabel("Movie Features")
    save(ASSET_DIR / "03-numeric-correlation-matrix.png")


def top_companies(df: pd.DataFrame) -> None:
    company_gross_sum = df.groupby("company", dropna=False)[["gross"]].sum()
    company_gross_sum_sorted = (
        company_gross_sum.sort_values(by="gross", ascending=False).head(15)
    )

    plt.figure(figsize=(12, 6))
    sns.barplot(
        x="gross",
        y=company_gross_sum_sorted.index,
        data=company_gross_sum_sorted,
        hue=company_gross_sum_sorted.index,
        palette="Blues_r",
        legend=False,
    )
    plt.title("Top 15 Companies by Gross Revenue")
    plt.xlabel("Total Gross Revenue")
    plt.ylabel("Company")
    save(ASSET_DIR / "04-top-companies-by-gross.png")


def main() -> None:
    df = load_movies()
    gross_distribution(df)
    score_vs_gross(df)
    numeric_correlation(df)
    top_companies(df)
    print(f"Generated visuals in {ASSET_DIR}")


if __name__ == "__main__":
    main()
