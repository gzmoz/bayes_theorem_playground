import numpy as np


def calculate_bayes(production_shares, defect_rates):

    shares = np.asarray(production_shares, dtype=float)
    rates = np.asarray(defect_rates, dtype=float)

    # Validate the input probabilities
    if shares.shape != rates.shape:
        raise ValueError("Each production line must have a defect rate.")

    if np.any(shares < 0) or not np.isclose(shares.sum(), 1.0):
        raise ValueError("Production shares must be nonnegative and sum to 1.")

    if np.any((rates < 0) | (rates > 1)):
        raise ValueError("Defect rates must be between 0 and 1.")

    # Calculate joint probabilities
    joint_probabilities = shares * rates

    # Apply the Law of Total Probability
    total_defect_probability = joint_probabilities.sum()

    if total_defect_probability == 0:
        raise ValueError("The probability of a defective product is zero.")

    # Apply Bayes' Theorem
    posterior_probabilities = joint_probabilities / total_defect_probability

    return total_defect_probability, posterior_probabilities


if __name__ == "__main__":

    production_shares = [0.50, 0.30, 0.20]
    defect_rates = [0.02, 0.05, 0.10]

    total_defect, posteriors = calculate_bayes(
        production_shares, defect_rates
    )

    print(f"Overall defect probability: {total_defect:.2%}")

    for line_number, probability in enumerate(posteriors, start=1):
        print(f"P(Line {line_number} | Defective): {probability:.2%}")