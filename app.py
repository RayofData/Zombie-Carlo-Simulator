import streamlit as st 

from src.zombie_carlo.model import ZombieSIR
from src.zombie_carlo.plots import (
    single_run_plot,
    monte_carlo_band_plot,
    final_survivors_plot
)

st.title("Zombie Carlo Simulator")


model = ZombieSIR()
model.run_simulation()

R0_col, pop_col, int_inf_col =  st.columns(3)
R0_col.metric(label=r"$R_0$", value=round(model.beta/model.gamma,2))
pop_col.metric(label="Starting Population", value=model.susceptible+model.infected)
int_inf_col.metric(label="Initial Infected", value=model.infected)

st.divider()

final_pop, final_inf, final_decayed =  st.columns(3)
final_pop.metric(label="Final Population", value=model.results["Susceptible"].iloc[-1])
final_inf.metric(label="Final Infected", value=model.results["Infected"].iloc[-1])
final_decayed.metric(label="Final Decayed", value=model.results["Decayed"].iloc[-1])

fig1 = single_run_plot(model.results)
st.pyplot(fig1)



results, daily_results = model.run_monte_carlo()

fig2 = monte_carlo_band_plot(daily_results, "Infected")
st.pyplot(fig2)

fig3 = final_survivors_plot(results["final_survivors"])
st.pyplot(fig3)