# 🚀 Business Decision Simulator

> **A Monte Carlo simulation engine for testing startup strategies under uncertainty.**

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/)
[![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://business-simulator.onrender.com/)

## 📖 Overview

The **Business Decision Simulator** is a data-driven tool designed to help founders and operators quantify risk. Instead of relying on static spreadsheets, this application uses **Monte Carlo simulations** to model thousands of possible futures, accounting for market volatility, demand shocks, and operational risks.

It answers critical "What if?" questions:
- *If I double my marketing spend, what is the probability I run out of cash in 6 months?*
- *Can we survive a 20% revenue drop if we hire aggressively?*

## 🏗️ Technical Architecture

The application is built using a clean separation of concerns between the simulation engine and the presentation layer.

- **Backend Logic (`simulation.py`)**: A pure Python class-based engine that encapsulates the business physics and stochastic models. It uses `NumPy` for efficient random number generation.
- **Frontend UI (`app.py`)**: A reactive `Streamlit` dashboard that handles user input, triggers simulations, and renders interactive `Plotly` visualizations.
- **Data Processing**: `Pandas` is used for aggregating simulation results (percentiles, medians) to prepare them for visualization.

## 🧮 Simulation Logic & Mathematics

The core of the simulator is a discrete-time stochastic model. We simulate the state of the company $S_t$ at month $t$ where $S_t = \{Cash_t, Revenue_t, Burn_t, Headcount_t\}$.

### 1. State Update Equations

For each month $t$, the state updates as follows:

$$
Cash_{t+1} = Cash_t + Revenue_t - Burn_t
$$

$$
Revenue_{t+1} = Revenue_t \times (1 + Growth_t)
$$

$$
Burn_{t+1} = Burn_t \times (1 + CostShock_t) + \Delta Burn_{strategy}
$$

### 2. Stochastic Growth Model

Revenue growth is not linear. It is modeled as a random variable to simulate market uncertainty:

$$
Growth_t = BaseGrowth + StrategyImpact + \epsilon_{demand} + \delta_{shock}
$$

Where:
- $BaseGrowth$: Organic growth rate (e.g., 2%).
- $StrategyImpact$: Additional growth from marketing (e.g., +5% for "Double Marketing").
- $\epsilon_{demand} \sim U(-0.05, 0.05)$: Random monthly fluctuation (Uniform distribution).
- $\delta_{shock}$: A rare event variable modeling "Bad Months".
  - $P(\delta_{shock} = -0.20) = 0.10$ (10% chance of a 20% drop).
  - $P(\delta_{shock} = 0) = 0.90$.

### 3. Monte Carlo Engine

To estimate the probability of survival $P(\text{Survival})$, we run $N$ independent simulations (default $N=500$).

Let $I_i$ be an indicator function for the $i$-th simulation run:
$$
I_i = \begin{cases} 
1 & \text{if } \text{Cash}_t > 0 \text{ for all } t \in [0, T] \\\\
0 & \text{otherwise}
\end{cases}
$$

The survival probability is estimated as:
$$
P(\text{Survival}) \approx \frac{1}{N} \sum_{i=1}^{N} I_i
$$

We also calculate the **Confidence Interval** for cash flow at each time step $t$ by taking the 10th and 90th percentiles of the distribution of $\text{Cash}_{t}$ across all $N$ runs.

## 💡 Strategic Advisor Algorithm

The app includes a rule-based expert system that analyzes the simulation output to provide actionable advice.

| Condition | Recommendation |
|-----------|----------------|
| $P(Survival) < 0.5$ | **⛔ High Risk**: Immediate cost-cutting required. |
| $P(Survival) \in [0.5, 0.8)$ | **⚠️ Danger Zone**: Consider fundraising or improving unit economics. |
| $P(Survival) \ge 0.8$ | **✅ Sustainable**: Safe to scale or take more risks. |
| $Burn > 2 \times Revenue$ | **🔥 Burn Alert**: Unit economics are unsustainable. |
| $Cash_{final} > 1.5 \times Cash_{start}$ | **🚀 Growth Engine**: Business is generating significant free cash flow. |

## 💻 Installation & Usage

### Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/business_decision_simulator.git
   cd business_decision_simulator
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**:
   ```bash
   streamlit run app.py
   ```

### Deployment

This app is configured for easy deployment on **Render**.
1. Fork this repo.
2. Connect it to Render as a "Web Service".
3. Use the build command `pip install -r requirements.txt` and start command `streamlit run app.py`.

## 🔮 Future Improvements

- [ ] **Geometric Brownian Motion (GBM)**: Upgrade the revenue model to standard financial engineering models.
- [ ] **Customer Lifetime Value (LTV) / CAC Modeling**: More granular unit economics simulation.
- [ ] **PDF Export**: Generate a downloadable PDF report for investors.

---
*Built with ❤️ by Vibhor*


