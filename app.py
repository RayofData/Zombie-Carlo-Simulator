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

with st.sidebar.form("simulation_controls"):
    st.subheader("Outbreak Setup")

    population = st.number_input(
        "Population",
        min_value=2,
        value=1000,
        help="Total number of humans and zombies at the start of the simulation."
    )

    initial_zombies = st.number_input(
        "Initial Zombies",
        min_value=1,
        max_value=population - 1,
        value=1,
        help="Number of zombies present when the outbreak begins."
    )

    days = st.slider(
        "Simulation Days",
        min_value=10,
        max_value=365,
        value=100,
        help="Number of days simulated for each outbreak."
    )

    trials = st.select_slider(
        "Monte Carlo Runs",
        options=[100, 500, 1_000, 5_000, 10_000, 50_000],
        value=1_000,
        help=(
            "Number of times the same outbreak scenario is simulated. "
            "More runs give more stable estimates but take longer."
        )
    )

    beta = st.number_input(
        "Beta",
        min_value=0.00001,
        max_value=1.0,
        value=0.2,
        help=(
            "Transmission rate. Beta controls how quickly susceptible humans "
            "become zombies. Higher values make infection spread more quickly. "
            "The daily infection probability also depends on the proportion "
            "of the population that is currently infected."
        )
    )
    st.caption("Higher beta = faster zombie spread.")

    gamma = st.number_input(
        "Gamma",
        min_value=0.00001,
        max_value=1.0,
        value=0.06,
        help=(
            "Removal rate. Gamma is the probability that an active zombie is "
            "removed from the outbreak during a day. Higher values remove "
            "zombie faster and make outbreaks easier to stop."
        )
    )
    st.caption("Higher gamma = zombies are removed faster.")

    run_simulation = st.form_submit_button("Run Simulation")

st.divider()

model = ZombieSIR(days=days, population=population, initial_zombies=initial_zombies, beta=beta, gamma=gamma)
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

with st.spinner("Running Monte Carlo simulations...", show_time=True):
    results, daily_results = model.run_monte_carlo(trials=trials)
st.success("Simulations complete!")

fig2 = monte_carlo_band_plot(daily_results, "Infected")
st.pyplot(fig2)

fig3 = final_survivors_plot(results["final_survivors"], model.population)
st.pyplot(fig3)
