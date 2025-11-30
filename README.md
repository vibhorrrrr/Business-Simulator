# Business Decision Simulator

A lightweight Monte Carlo simulation tool designed to help startup founders test business strategies and visualize outcomes under uncertainty.

## 🚀 Features

- **Monte Carlo Simulation**: Runs 500+ iterations to predict probabilistic outcomes.
- **Strategy Testing**: Evaluate the impact of "Aggressive Hiring" or "Double Marketing" on your runway.
- **Uncertainty Modeling**: Accounts for random demand shocks, "bad months," and unexpected cost spikes.
- **Strategic Advisor**: Provides actionable recommendations (e.g., "Cut costs", "Safe to scale") based on survival probability.
- **Visualizations**:
  - Cash flow projections with confidence intervals (10th-90th percentile).
  - Survival probability metrics.
  - Final cash distribution histograms.

## 🛠️ Installation

1. **Prerequisites**: Ensure you have Python installed (3.8+ recommended).
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## ▶️ Usage

Run the Streamlit application:

```bash
streamlit run app.py
```

The app will open in your default web browser.

## ☁️ Deployment (Render)

This app is ready to be deployed on [Render](https://render.com).

1. **Push to GitHub**: Ensure your code is in a GitHub repository.
2. **Create Web Service**:
   - Go to the Render Dashboard and click "New +".
   - Select "Web Service".
   - Connect your GitHub repository.
3. **Configure**:
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py`
4. **Deploy**: Click "Create Web Service".

Alternatively, you can use the included `render.yaml` file with Render Blueprints.

## 📂 Project Structure

- `app.py`: Main Streamlit application and UI logic.
- `simulation.py`: Core simulation engine and business logic.
- `test_simulation.py`: Unit tests for the simulation logic.
- `requirements.txt`: Python dependencies.

## 🧠 How it Works

The simulator models monthly business states (Cash, Revenue, Burn, Headcount) and applies your strategy choices. It introduces random variables for market conditions to generate a range of possible futures, helping you understand not just the *expected* outcome, but the *risk* of failure.
