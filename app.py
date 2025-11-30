import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from simulation import BusinessSimulator

st.set_page_config(page_title="Business Decision Simulator", layout="wide")

# --- CSS for styling ---
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .stButton>button {
        width: 100%;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
    }
    
    /* Mobile-specific adjustments */
    @media (max-width: 768px) {
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 2rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        h1 {
            font-size: 1.8rem !important;
        }
        .stMetric {
            background-color: #f8f9fa;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
            color: black !important;
        }
        .stMetric label {
            color: #31333F !important;
        }
        .stMetric div[data-testid="stMetricValue"] {
            color: #31333F !important;
        }
    }
</style>
""", unsafe_allow_html=True)

st.title("Business Decision Simulator")
st.markdown("Test your startup strategy with Monte Carlo simulations.")

# --- Sidebar Inputs ---
with st.sidebar:
    st.header("1. Company State")
    start_cash = st.number_input("Starting Cash ($)", value=500000, step=10000)
    monthly_revenue = st.number_input("Monthly Revenue ($)", value=20000, step=1000)
    monthly_burn = st.number_input("Monthly Burn ($)", value=50000, step=1000)
    team_size = st.number_input("Current Team Size", value=5, step=1)
    
    st.subheader("Unit Economics")
    cac = st.number_input("CAC ($)", value=50.0, step=5.0, help="Customer Acquisition Cost")
    arpu = st.number_input("ARPU ($)", value=100.0, step=5.0, help="Average Revenue Per User per Month")

    st.header("2. Strategy Decisions")
    hiring_strategy = st.selectbox("Hiring Strategy", ["None", "Moderate", "Aggressive"], index=1)
    marketing_strategy = st.selectbox("Marketing Strategy", ["Same", "Double"], index=0)

    st.header("3. Simulation Settings")
    months = st.slider("Time Horizon (Months)", 6, 36, 12)
    runs = st.slider("Number of Simulations", 100, 1000, 500)
    
    run_btn = st.button("Run Simulation")

# --- Main Content ---
if run_btn:
    with st.spinner("Simulating 500 futures..."):
        sim = BusinessSimulator(start_cash, monthly_revenue, monthly_burn, team_size, cac, arpu)
        raw_results = sim.run_simulation(months, runs, hiring_strategy, marketing_strategy)
        agg_results = sim.process_results(raw_results)

    # --- Top Metrics ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Survival Probability", f"{agg_results['survival_rate']*100:.1f}%")
    with col2:
        st.metric("Median Final Cash", f"${agg_results['median_cash'][-1]:,.0f}")
    with col3:
        # Strategic Advisor Logic
        st.subheader("💡 Strategic Advisor")
        
        recommendations = []
        survival = agg_results['survival_rate']
        final_cash = agg_results['median_cash'][-1]
        
        # Survival Analysis
        if survival < 0.5:
            st.error(f"CRITICAL: {survival*100:.1f}% Survival Rate")
            recommendations.append("⛔ **High Risk of Failure**: Your current runway is insufficient.")
            if monthly_burn > monthly_revenue * 2:
                recommendations.append("• **Burn Alert**: Your burn is over 2x your revenue. Cut costs immediately.")
            if hiring_strategy == "Aggressive":
                recommendations.append("• **Hiring Freeze**: Aggressive hiring is draining cash too fast. Pause hiring.")
        elif survival < 0.8:
            st.warning(f"CAUTION: {survival*100:.1f}% Survival Rate")
            recommendations.append("⚠️ **Danger Zone**: You are surviving, but it's risky.")
            recommendations.append("• **Fundraising**: Consider raising capital to extend runway.")
        else:
            st.success(f"HEALTHY: {survival*100:.1f}% Survival Rate")
            recommendations.append("✅ **Sustainable Path**: High probability of survival.")
            
        # Growth Analysis
        if final_cash > start_cash * 1.5:
            recommendations.append("• **Growth Engine**: Your cash is growing significantly. You can afford to be more aggressive.")
        elif final_cash < start_cash:
            recommendations.append("• **Shrinking**: You are surviving, but burning cash reserves. Focus on revenue growth.")
            
        for rec in recommendations:
            st.markdown(rec)

    # --- Visualizations ---
    
    # 1. Cash Flow Over Time
    st.subheader("Cash Flow Projection")
    
    df_cash = pd.DataFrame({
        'Month': agg_results['months'],
        'Median Cash': agg_results['median_cash'],
        '10th Percentile': agg_results['p10_cash'],
        '90th Percentile': agg_results['p90_cash']
    })
    
    fig_cash = go.Figure()
    
    # Confidence Band
    fig_cash.add_trace(go.Scatter(
        x=pd.concat([df_cash['Month'], df_cash['Month'][::-1]]),
        y=pd.concat([df_cash['90th Percentile'], df_cash['10th Percentile'][::-1]]),
        fill='toself',
        fillcolor='rgba(0,100,80,0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        hoverinfo="skip",
        showlegend=True,
        name='10th-90th Percentile'
    ))
    
    # Median Line
    fig_cash.add_trace(go.Scatter(
        x=df_cash['Month'],
        y=df_cash['Median Cash'],
        line=dict(color='rgb(0,100,80)', width=3),
        mode='lines',
        name='Median Cash'
    ))
    
    fig_cash.update_layout(
        xaxis_title="Month",
        yaxis_title="Cash ($)",
        template="plotly_white",
        hovermode="x",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=20, r=20, t=50, b=20)
    )
    st.plotly_chart(fig_cash, use_container_width=True)

    # 2. Final Cash Distribution
    st.subheader("Final Cash Distribution")
    fig_hist = px.histogram(
        x=agg_results['final_cash'],
        nbins=30,
        labels={'x': 'Final Cash ($)'},
        color_discrete_sequence=['#636EFA']
    )
    fig_hist.update_layout(
        template="plotly_white", 
        showlegend=False,
        margin=dict(l=20, r=20, t=30, b=20)
    )
    st.plotly_chart(fig_hist, use_container_width=True)

else:
    st.info("👈 Adjust settings in the sidebar and click 'Run Simulation' to start.")
