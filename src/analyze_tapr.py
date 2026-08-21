


"""Reproduce the four selected EPISD TAPR charts and summary tables."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
FIGURES = ROOT / "figures"
OUTPUTS = ROOT / "outputs"

NAVY = "#294f78"
ORANGE = "#df7928"
RED = "#f53b36"
GRAY = "#7f8995"
INK = "#19324b"
GRID = "#d7e0e9"
LIGHT_BG = "#f5f7fa"


def validate_percentages(frame: pd.DataFrame, column: str) -> None:
    """Raise an error if a percentage is missing or outside 0–100."""
    if frame[column].isna().any():
        raise ValueError(f"Missing values found in {column}")
    if not frame[column].between(0, 100).all():
        raise ValueError(f"Invalid percentage found in {column}")


def label_bars(ax, bars, suffix="%", color=INK, fmt=".0f"):
    """Add readable value labels above bars."""
    for bar in bars:
        value = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + ax.get_ylim()[1] * 0.012,
            f"{value:{fmt}}{suffix}",
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold",
            color=color,
        )


def style_light(ax, ylabel: str):
    ax.set_facecolor(LIGHT_BG)
    ax.figure.set_facecolor(LIGHT_BG)
    ax.set_ylabel(ylabel, fontsize=12, fontweight="bold", color=INK)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.spines["bottom"].set_color("#9aaabd")


def chart_episd_eoc(episd: pd.DataFrame) -> None:
    """Chart EPISD EB/EL Did Not Meet rates by EOC and year."""
    order = ["English I", "Algebra I", "U.S. History"]
    pivot = episd.pivot(index="assessment", columns="school_year", values="did_not_meet_pct").loc[order]
    x = np.arange(len(order))
    width = 0.36
    fig, ax = plt.subplots(figsize=(12, 7))
    style_light(ax, "Did Not Meet Grade Level (%)")
    b1 = ax.bar(x - width / 2, pivot["2023-2024"], width, color=NAVY, label="2023–2024")
    b2 = ax.bar(x + width / 2, pivot["2024-2025"], width, color=ORANGE, label="2024–2025")
    ax.set_xticks(x, order, fontweight="bold")
    ax.set_ylim(0, 60)
    ax.set_title(
        "EPISD EB/EL Students at Did Not Meet Grade Level",
        fontsize=22,
        fontweight="bold",
        color=INK,
        pad=24,
    )
    ax.text(
        0.5,
        1.015,
        "STAAR EOC • Did Not Meet = 100% − Approaches Grade Level or Above",
        transform=ax.transAxes,
        ha="center",
        color="#596a7c",
        fontsize=12,
    )
    ax.legend(title="School year", frameon=False, ncol=2, loc="upper right")
    label_bars(ax, b1)
    label_bars(ax, b2)
    fig.text(
        0.01,
        0.01,
        "Source: 2023–24 and 2024–25 EPISD TAPR. Group: EB/EL (Current & Monitored).",
        fontsize=8,
        color="#596a7c",
    )
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(FIGURES / "01_episd_eb_el_did_not_meet.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


def chart_membership(
    membership: pd.DataFrame,
    classification: str,
    filename: str,
    title: str,
    alarming=False,
) -> None:
    """Compare EPISD and Texas membership percentages for one classification."""
    subset = membership[membership["classification"] == classification]
    pivot = subset.pivot(index="school_year", columns="geography", values="percent").loc[
        ["2023-2024", "2024-2025"]
    ]
    x = np.arange(2)
    width = 0.31
    fig, ax = plt.subplots(figsize=(12, 7))
    if alarming:
        fig.patch.set_facecolor("#13171d")
        ax.set_facecolor("#13171d")
        text_color, grid_color = "#f2f4f7", "#343b45"
        epid_color, texas_color = RED, GRAY
        ax.spines[:].set_visible(False)
        ax.tick_params(colors=text_color)
        ax.grid(axis="y", color=grid_color, linewidth=0.8)
        ax.set_ylabel(
            "Students classified EB/EL (%)",
            color=text_color,
            fontsize=12,
            fontweight="bold",
        )
    else:
        text_color = INK
        epid_color, texas_color = NAVY, ORANGE
        style_light(ax, f"Students classified as {classification} (%)")
    ax.set_axisbelow(True)
    b1 = ax.bar(x - width / 2, pivot["EPISD"], width, color=epid_color, label="EPISD")
    b2 = ax.bar(x + width / 2, pivot["Texas"], width, color=texas_color, label="Texas")
    ax.set_xticks(x, ["2023–2024", "2024–2025"], fontweight="bold")
    upper = max(50, float(pivot.to_numpy().max()) + 12)
    ax.set_ylim(0, upper)
    ax.set_title(title, fontsize=21, fontweight="bold", color=text_color, pad=22)
    ax.text(
        0.5,
        1.015,
        "TAPR student membership percentages",
        transform=ax.transAxes,
        ha="center",
        color=("#b9c0ca" if alarming else "#596a7c"),
        fontsize=11,
    )
    legend = ax.legend(frameon=False, ncol=2, loc="upper right")
    if alarming:
        for t in legend.get_texts():
            t.set_color(text_color)
    label_bars(ax, b1, fmt=".1f", color=text_color)
    label_bars(ax, b2, fmt=".1f", color=text_color)
    for i, year in enumerate(["2023-2024", "2024-2025"]):
        gap = pivot.loc[year, "EPISD"] - pivot.loc[year, "Texas"]
        ax.text(
            i,
            upper - 4,
            f"EPISD +{gap:.1f} pp",
            ha="center",
            color=("white" if alarming else ORANGE),
            fontweight="bold",
            bbox=(
                dict(
                    boxstyle="round,pad=0.3",
                    facecolor="#ad2828",
                    edgecolor="#ff6262",
                )
                if alarming
                else None
            ),
        )
    source_color = "#aeb6c2" if alarming else "#596a7c"
    fig.text(
        0.01,
        0.01,
        f"Source: EPISD and Texas TAPR, 2023–24 and 2024–25. Classification: {classification}.",
        fontsize=8,
        color=source_color,
    )
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(
        FIGURES / filename,
        dpi=200,
        bbox_inches="tight",
        facecolor=fig.get_facecolor(),
    )
    plt.close(fig)


def main() -> None:
    FIGURES.mkdir(exist_ok=True)
    OUTPUTS.mkdir(exist_ok=True)

    eoc = pd.read_csv(DATA / "eoc_eb_el_performance.csv")
    membership = pd.read_csv(DATA / "student_membership.csv")
    validate_percentages(eoc, "approaches_or_above_pct")
    validate_percentages(membership, "percent")

    # Derive the complementary Did Not Meet rate from Approaches or Above.
    eoc["did_not_meet_pct"] = 100 - eoc["approaches_or_above_pct"]
    eoc.to_csv(OUTPUTS / "eoc_eb_el_with_derived_rates.csv", index=False)

    # Compare EPISD with the corresponding Texas EB/EL group.
    compare = eoc.pivot_table(
        index=["school_year", "assessment"],
        columns="geography",
        values="did_not_meet_pct",
    ).reset_index()
    compare["episd_minus_texas_pp"] = compare["EPISD"] - compare["Texas"]
    compare.to_csv(OUTPUTS / "episd_vs_texas_eoc_did_not_meet.csv", index=False)

    # Calculate district-minus-state membership gaps.
    gaps = membership.pivot_table(
        index=["school_year", "classification"],
        columns="geography",
        values="percent",
    ).reset_index()
    gaps["episd_minus_texas_pp"] = gaps["EPISD"] - gaps["Texas"]
    gaps.to_csv(OUTPUTS / "membership_percentage_point_gaps.csv", index=False)

    chart_episd_eoc(eoc[eoc["geography"] == "EPISD"])
    chart_membership(
        membership,
        "EB Students/EL",
        "02_eb_el_membership_episd_vs_texas.png",
        "EPISD Serves a Far Larger Share of EB/EL Students",
        alarming=True,
    )
    chart_membership(
        membership,
        "At-Risk",
        "03_at_risk_membership_episd_vs_texas.png",
        "Students Classified as At-Risk: EPISD vs Texas",
    )
    chart_membership(
        membership,
        "Economically Disadvantaged",
        "04_economically_disadvantaged_episd_vs_texas.png",
        "Economically Disadvantaged Students: EPISD vs Texas",
    )

    print(f"Created 4 charts in {FIGURES}")
    print(f"Created 3 summary tables in {OUTPUTS}")


if __name__ == "__main__":
    main()