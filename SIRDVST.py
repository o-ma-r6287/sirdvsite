import io
import time
import importlib.util
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# ---------------------------------------------------
# LOAD HELPER FUNCTION
# ---------------------------------------------------
def load_run_sim():
    possible_files = [
        "Assignment3_Functions_Solution.py",
        "Assignment3_Functions_Solutions.py",
        "Assignment3_Functions_Solutions-1.py",
    ]

    for file_name in possible_files:
        file_path = Path(__file__).parent / file_name

        if file_path.exists():
            spec = importlib.util.spec_from_file_location(
                "assignment3_functions",
                file_path
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module.run_sim

    raise FileNotFoundError("Simulation helper file not found.")


run_sim = load_run_sim()


# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="Epidemiological Decision Dashboard",
    page_icon="🦠",
    layout="wide"
)

st.title("🦠 Epidemiological Decision Dashboard")
st.caption("Interactive disease spread analytics for SIR / SIRD / SIRDV models")
st.caption("Built by Omar Rulida Abdul-Rahman | MPH Candidate")


# ---------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------
def run_model(model_choice, pop, infected, recovered, beta, gamma, mu, vac, days):
    susceptible = pop - infected - recovered

    sim_s, sim_i, sim_r, sim_d, sim_v = run_sim(
        S_0=susceptible,
        I_0=infected,
        R_0=recovered,
        beta=beta,
        gamma=gamma,
        mu=mu,
        vac_rate=vac,
        days=int(days),
        model_choice=model_choice
    )

    return pd.DataFrame(
        {
            "Day": range(int(days)),
            "Susceptible": sim_s,
            "Infected": sim_i,
            "Recovered": sim_r,
            "Dead": sim_d,
            "Vaccinated": sim_v
        }
    )


def get_columns(model):
    if model == "SIR":
        return ["Susceptible", "Infected", "Recovered"]
    elif model == "SIRD":
        return ["Susceptible", "Infected", "Recovered", "Dead"]
    return ["Susceptible", "Infected", "Recovered", "Dead", "Vaccinated"]


def make_plot(df, model):
    colors = {
        "Susceptible": "#1f77b4",
        "Infected": "#d62728",
        "Recovered": "#2ca02c",
        "Dead": "#7f7f7f",
        "Vaccinated": "#9467bd"
    }

    fig = go.Figure()

    for col in get_columns(model):
        fig.add_trace(
            go.Scatter(
                x=df["Day"],
                y=df[col],
                mode="lines",
                name=col,
                line=dict(width=3, color=colors[col]),
                hovertemplate=f"{col}: %{{y:.0f}}<extra></extra>"
            )
        )

    fig.update_layout(
        title=f"{model} Simulation Results",
        xaxis_title="Day",
        yaxis_title="Population",
        template="plotly_white",
        hovermode="x unified",
        height=600
    )

    return fig


def metrics_from_df(df):
    return {
        "Peak Infected": float(df["Infected"].max()),
        "Day of Peak": int(df["Infected"].idxmax()),
        "Recovered": float(df["Recovered"].iloc[-1]),
        "Deaths": float(df["Dead"].iloc[-1]),
        "Vaccinated": float(df["Vaccinated"].iloc[-1]),
        "Susceptible": float(df["Susceptible"].iloc[-1]),
    }


# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
st.sidebar.header("Simulation Controls")

model_choice = st.sidebar.selectbox(
    "Choose Model",
    ["SIR", "SIRD", "SIRDV"]
)

population = st.sidebar.number_input(
    "Total Population",
    min_value=1,
    value=1000
)

infected = st.sidebar.number_input(
    "Initial Infected",
    min_value=0,
    value=5
)

recovered = st.sidebar.number_input(
    "Initial Recovered",
    min_value=0,
    value=0
)

beta = st.sidebar.slider(
    "Beta (Infection Rate)",
    0.0, 1.0, 0.40, 0.01
)

gamma = st.sidebar.slider(
    "Gamma (Recovery Rate)",
    0.0, 1.0, 0.05, 0.01
)

mu = 0.0
vac = 0.0

if model_choice in ["SIRD", "SIRDV"]:
    mu = st.sidebar.slider(
        "Mu (Death Rate)",
        0.0, 1.0, 0.01, 0.01
    )

if model_choice == "SIRDV":
    vac = st.sidebar.slider(
        "Vaccination Rate",
        0.0, 1.0, 0.03, 0.01
    )

days = st.sidebar.slider(
    "Days",
    10, 365, 120
)

run_button = st.sidebar.button(
    "Run Simulation",
    type="primary"
)


# ---------------------------------------------------
# TABS
# ---------------------------------------------------
tabs = st.tabs(
    [
        "Simulation Results",
        "Data Table",
        "Model Explanation",
        "Compare Scenarios"
    ]
)


# ---------------------------------------------------
# MAIN SIMULATION
# ---------------------------------------------------
if run_button:

    with st.spinner("Running simulation..."):
        time.sleep(0.5)

        df = run_model(
            model_choice,
            population,
            infected,
            recovered,
            beta,
            gamma,
            mu,
            vac,
            days
        )

    fig = make_plot(df, model_choice)

    metrics = metrics_from_df(df)

    # ------------------------------------------------
    # TAB 1
    # ------------------------------------------------
    with tabs[0]:

        st.subheader("Simulation Dashboard")

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        c1, c2, c3 = st.columns(3)
        c4, c5, c6 = st.columns(3)

        c1.metric("Peak Infected", f"{metrics['Peak Infected']:,.0f}")
        c2.metric("Day of Peak", f"{metrics['Day of Peak']}")
        c3.metric("Recovered", f"{metrics['Recovered']:,.0f}")

        c4.metric("Deaths", f"{metrics['Deaths']:,.0f}")
        c5.metric("Vaccinated", f"{metrics['Vaccinated']:,.0f}")
        c6.metric("Susceptible Left", f"{metrics['Susceptible']:,.0f}")

        csv = df.to_csv(index=False).encode()

        st.download_button(
            "Download CSV",
            csv,
            file_name="simulation_results.csv",
            mime="text/csv"
        )

    # ------------------------------------------------
    # TAB 2
    # ------------------------------------------------
    with tabs[1]:
        st.subheader("Simulation Data")
        st.dataframe(df, use_container_width=True)

    # ------------------------------------------------
    # TAB 3
    # ------------------------------------------------
    with tabs[2]:
        st.subheader("Model Explanation")

        st.markdown("""
### SIR
Susceptible → Infected → Recovered

### SIRD
Adds Deaths

### SIRDV
Adds Vaccination

### Real Uses
- COVID-19 spread
- Seasonal flu
- Vaccine planning
- Hospital forecasting
""")

else:
    with tabs[0]:
        st.info("Choose parameters and click Run Simulation.")


# ---------------------------------------------------
# COMPARE TAB (ALWAYS WORKS)
# ---------------------------------------------------
with tabs[3]:

    st.subheader("Compare Two Scenarios")

    colA, colB = st.columns(2)

    with colA:
        st.markdown("### Scenario A")
        beta_a = st.slider("Beta A", 0.0, 1.0, beta, 0.01)
        gamma_a = st.slider("Gamma A", 0.0, 1.0, gamma, 0.01)

    with colB:
        st.markdown("### Scenario B")
        beta_b = st.slider("Beta B", 0.0, 1.0, min(beta + 0.2, 1.0), 0.01)
        gamma_b = st.slider("Gamma B", 0.0, 1.0, gamma, 0.01)

    if st.button("Compare Scenarios"):

        df_a = run_model(
            model_choice,
            population,
            infected,
            recovered,
            beta_a,
            gamma_a,
            mu,
            vac,
            days
        )

        df_b = run_model(
            model_choice,
            population,
            infected,
            recovered,
            beta_b,
            gamma_b,
            mu,
            vac,
            days
        )

        fig_compare = go.Figure()

        fig_compare.add_trace(
            go.Scatter(
                x=df_a["Day"],
                y=df_a["Infected"],
                mode="lines",
                name="Scenario A",
                line=dict(width=4)
            )
        )

        fig_compare.add_trace(
            go.Scatter(
                x=df_b["Day"],
                y=df_b["Infected"],
                mode="lines",
                name="Scenario B",
                line=dict(width=4, dash="dash")
            )
        )

        fig_compare.update_layout(
            title="Scenario Comparison",
            xaxis_title="Day",
            yaxis_title="Infected Population",
            template="plotly_white",
            height=600
        )

        st.plotly_chart(
            fig_compare,
            use_container_width=True
        )

        m1 = metrics_from_df(df_a)
        m2 = metrics_from_df(df_b)

        c1, c2 = st.columns(2)

        c1.metric(
            "Scenario A Peak",
            f"{m1['Peak Infected']:,.0f}"
        )

        c2.metric(
            "Scenario B Peak",
            f"{m2['Peak Infected']:,.0f}"
        )


# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.markdown("---")
st.caption("Built with Streamlit | Epidemiological Decision Dashboard")
