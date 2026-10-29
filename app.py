import streamlit as st

from bayes import calculate_bayes
from simulation import simulate_factory
import matplotlib.pyplot as plt
from visualize import create_probability_chart


# Page configuration
st.set_page_config(
    page_title="Bayes' Theorem Playground",
    layout="wide"
)

st.title("Bayes' Theorem Playground")

st.write(
    "Explore how observing a defective product changes "
    "the probability that it came from each production line."
)


# Sidebar: Production proportions
st.sidebar.header("Production Proportions")

line1_share = st.sidebar.slider(
    "Line 1 (%)", 0, 100, 50
)

line2_share = st.sidebar.slider(
    "Line 2 (%)", 0, 100 - line1_share, min(30, 100 - line1_share)
)

line3_share = 100 - line1_share - line2_share

st.sidebar.write(f"Line 3: {line3_share}%")


# Sidebar: Defect rates
st.sidebar.header("Defect Rates")

rate1 = st.sidebar.slider("Line 1 defect rate (%)", 0.0, 100.0, 2.0, 0.5)
rate2 = st.sidebar.slider("Line 2 defect rate (%)", 0.0, 100.0, 5.0, 0.5)
rate3 = st.sidebar.slider("Line 3 defect rate (%)", 0.0, 100.0, 10.0, 0.5)

# Sidebar: Simulation settings
st.sidebar.header("Simulation Settings")

n_products = st.sidebar.slider(
    "Number of Products",
    min_value=1000,
    max_value=200000,
    value=100000,
    step=1000
)

seed = st.sidebar.number_input(
    "Random Seed",
    min_value=0,
    value=42,
    step=1
)


# Convert percentages to probabilities
shares = [line1_share / 100, line2_share / 100, line3_share / 100]
rates = [rate1 / 100, rate2 / 100, rate3 / 100]


# Calculate theoretical probabilities
try:
    total_defect, posteriors = calculate_bayes(shares, rates)

except ValueError as error:
    st.warning(str(error))
    st.stop()

    # Run Monte Carlo simulation
simulated_rate, simulated_posteriors = simulate_factory(
    shares,
    rates,
    n_products=n_products,
    seed=seed
)


# Display results
st.subheader("Results")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Theoretical Defect Probability",
        f"{total_defect:.2%}"
    )

with col2:
    st.metric(
        "Simulated Defect Probability",
        f"{simulated_rate:.2%}"
    )

st.subheader("Prior and Posterior Probabilities")

columns = st.columns(3)

for i, column in enumerate(columns):

    with column:
        st.metric(f"Line {i + 1} Prior", f"{shares[i]:.2%}")
        st.metric(f"Line {i + 1} Posterior", f"{posteriors[i]:.2%}")


st.subheader("Monte Carlo Simulation")

st.write(f"Number of simulated products: {n_products:,}")

if simulated_rate == 0:
    st.warning(
        "No defective products were observed in this simulation. "
        "Posterior probabilities cannot be estimated."
    )

else:
    comparison = {
        "Production Line": ["Line 1", "Line 2", "Line 3"],
        "Prior": [f"{p:.2%}" for p in shares],
        "Theoretical Posterior": [f"{p:.2%}" for p in posteriors],
        "Simulated Posterior": [f"{p:.2%}" for p in simulated_posteriors]
    }

    st.table(comparison, hide_index=True, hide_header=False)

# Interactive probability visualization
st.subheader("How Evidence Changes the Probabilities")

fig = create_probability_chart(shares, posteriors)

st.pyplot(fig)

plt.close(fig)    