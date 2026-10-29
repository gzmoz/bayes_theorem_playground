import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter


def create_probability_chart(production_shares, posterior_probabilities):

    shares = np.asarray(production_shares, dtype=float)
    posteriors = np.asarray(posterior_probabilities, dtype=float)

    x = np.arange(len(shares))
    bar_width = 0.35

    fig, ax = plt.subplots(figsize=(9, 5))

    prior_bars = ax.bar(
        x - bar_width / 2,
        shares,
        width=bar_width,
        label="Prior probability",
        color="#334155"
    )

    posterior_bars = ax.bar(
        x + bar_width / 2,
        posteriors,
        width=bar_width,
        label="Posterior probability",
        color="#0D9488"
    )

    for bars in [prior_bars, posterior_bars]:
        ax.bar_label(
            bars,
            labels=[f"{bar.get_height():.2%}" for bar in bars],
            padding=4
        )

    ax.set_title("How Observing a Defect Changes the Probabilities")
    ax.set_ylabel("Probability")

    ax.set_xticks(x)
    ax.set_xticklabels([f"Line {i + 1}" for i in x])

    max_probability = max(shares.max(), posteriors.max())
    ax.set_ylim(0, min(1.10, max(0.60, max_probability * 1.15)))

    ax.yaxis.set_major_formatter(PercentFormatter(1.0))

    ax.legend(frameon=False)
    ax.grid(axis="y", alpha=0.2)
    ax.set_axisbelow(True)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()

    return fig


if __name__ == "__main__":

    from bayes import calculate_bayes

    shares = [0.50, 0.30, 0.20]
    rates = [0.02, 0.05, 0.10]

    _, posteriors = calculate_bayes(shares, rates)

    fig = create_probability_chart(shares, posteriors)

    fig.savefig(
        "images/prior_vs_posterior.png",
        dpi=200,
        bbox_inches="tight"
    )

    plt.show()