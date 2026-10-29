import numpy as np
from bayes import calculate_bayes


def simulate_factory(production_shares, defect_rates, n_products=100_000, seed=42):

    shares = np.asarray(production_shares, dtype=float)
    rates = np.asarray(defect_rates, dtype=float)

    # Check that the given probabilities are valid
    calculate_bayes(shares, rates)

    # Create a random number generator
    rng = np.random.default_rng(seed)

    # Assign each product to a production line
    selected_lines = rng.choice(
        len(shares),
        size=n_products,
        p=shares
    )

    # Determine which products are defective
    defective = rng.random(n_products) < rates[selected_lines]

    # Calculate the simulated defect rate
    defect_count = defective.sum()
    simulated_defect_rate = defect_count / n_products

    # Calculate the simulated posterior probabilities
    if defect_count == 0:
        simulated_posteriors = np.full(len(shares), np.nan)
    else:
        defect_counts = np.bincount(
            selected_lines[defective],
            minlength=len(shares)
        )

        simulated_posteriors = defect_counts / defect_count

    return simulated_defect_rate, simulated_posteriors


if __name__ == "__main__":

    shares = [0.50, 0.30, 0.20]
    rates = [0.02, 0.05, 0.10]

    theoretical_rate, theoretical_posteriors = calculate_bayes(shares, rates)

    simulated_rate, simulated_posteriors = simulate_factory(shares, rates)

    print(f"Theoretical defect rate: {theoretical_rate:.2%}")
    print(f"Simulated defect rate: {simulated_rate:.2%}")

    print(f"Theoretical P(Line 3 | D): {theoretical_posteriors[2]:.2%}")
    print(f"Simulated P(Line 3 | D): {simulated_posteriors[2]:.2%}")