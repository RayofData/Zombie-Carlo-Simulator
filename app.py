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
st.write(model.results)

fig1 = single_run_plot(model.results)

st.pyplot(fig1)


results, daily_results = model.run_monte_carlo()

st.write(results)

fig2 = monte_carlo_band_plot(daily_results, "Infected")

st.pyplot(fig2)

fig3 = final_survivors_plot(results["final_survivors"])

st.pyplot(fig3)