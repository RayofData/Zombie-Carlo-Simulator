import streamlit as st 

from src.zombie_carlo.model import ZombieSIR
from src.zombie_carlo.plots import (
    single_run_plot,
    monte_carlo_band_plot,
    final_survivors_plot
)

st.title("Zombie Carlo Simulator")

st.write(
    """
    Explore how a fictional zombie outbreak can unfold under the same starting
    conditions. Zombie Carlo uses a stochastic SIR-style model and Monte Carlo
    simulation to show not just one possible outbreak, but the range of outcomes
    created by randomness.
    """
)

st.divider()

model = ZombieSIR(beta=.5, gamma=.2)
model.run_simulation()

st.subheader("Outbreak Setup")

st.caption(
    "Starting conditions and transmission parameters for this simulation."
)

pop_col, int_inf_col, days_col, R0_col =  st.columns(4)
pop_col.metric(label="Starting Population", value=model.susceptible+model.infected)
int_inf_col.metric(label="Initial Infected", value=model.infected)
days_col.metric(label="Total Days", value=model.days)
R0_col.metric(label=r"$R_0$", value=round(model.beta/model.gamma,2))

st.divider()

final_pop_col, final_inf_col, final_eliminated_col, final_decayed_col =  st.columns(4)
final_pop_col.metric(label="Final Population", value=model.results["Susceptible"].iloc[-1])
final_inf_col.metric(label="Final Infected", value=model.results["Infected"].iloc[-1])
final_eliminated_col.metric(label="Final Eliminated", value=model.results["Eliminated"].iloc[-1])
final_decayed_col.metric(label="Final Decayed", value=model.results["Decayed"].iloc[-1])

fig1 = single_run_plot(model.results)
st.pyplot(fig1)

results, daily_results = model.run_monte_carlo()

fig2 = monte_carlo_band_plot(daily_results, "Infected")
st.pyplot(fig2)

fig3 = final_survivors_plot(results["final_survivors"], model.population)
st.pyplot(fig3)