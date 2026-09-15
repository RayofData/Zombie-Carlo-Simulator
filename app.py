import streamlit as st 

from src.zombie_carlo.model import ZombieSIR, SIED
from src.zombie_carlo.plots import (
    single_run_plot,
    monte_carlo_band_plot,
    final_survivors_plot
)

PRESETS = {
    "Classic Movie Zombies": {
        "beta": 0.10,
        "gamma": 0.05,
        "decay_fraction": 0.10
    },
    "Apocalypse Zombies": {
        "beta": 0.30,
        "gamma": 0.03,
        "decay_fraction": 0.03
    },
    "Runner Zombies": {
        "beta": 0.45,
        "gamma": 0.08,
        "decay_fraction": 0.08
    },
    "Viral Zombies": {
        "beta": 0.75,
        "gamma": 0.25,
        "decay_fraction": 0.05
    },
    "Rotter Zombies": {
        "beta": 0.18,
        "gamma": 0.15,
        "decay_fraction": 0.70
    },
    "Custom": {
        "beta": 0.20,
        "gamma": 0.06,
        "decay_fraction": 0.05
    }
}


def load_preset():
    preset = PRESETS[st.session_state.preset]

    st.session_state.beta = preset["beta"]
    st.session_state.gamma = preset["gamma"]
    st.session_state.decay_fraction = preset["decay_fraction"]


if "preset" not in st.session_state:
    st.session_state.preset = "Classic Movie Zombies"
    load_preset()

st.title("Zombie Carlo Simulator")

st.write(
    """
    Explore how a fictional zombie outbreak can unfold under the same starting
    conditions. Zombie Carlo uses a stochastic SIR-style model and Monte Carlo
    simulation to show not just one possible outbreak, but the range of outcomes
    created by randomness.
    """
)

st.sidebar.header("Outbreak Setup")
st.sidebar.caption(
    "Choose the outbreak parameters, then select Run Simulation to see the results."
)

st.sidebar.selectbox(
    "Zombie Preset",
    PRESETS.keys(),
    key="preset",
    on_change=load_preset,
    help="Choose a starting scenario. You can adjust its parameters below."
)

use_seed = st.sidebar.toggle(
    "Use Seed",
    help="Use a fixed random seed to reproduce the same simulation results."
)

if use_seed:
    seed = st.sidebar.number_input(
        "Seed",
        min_value=0,
        value=42,
        step=1,
        help="Using the same seed and parameters produce the same reproducible randomness."
    )
else:
    seed = None


with st.sidebar.form("simulation_controls"):
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
        options=[100, 500, 1_000, 5_000, 10_000],
        value=1_000,
        help=(
            "Number of times the same outbreak scenario is simulated. "
            "More runs give more stable estimates but take longer."
        )
    )

    beta = st.number_input(
        "$\\beta$",
        min_value=0.00001,
        max_value=1.0,
        key="beta",
        help=(
            "Transmission rate (0 < beta <= 1). Controls how quickly susceptible "
            "humans become zombies."
        )
    )
    st.caption("Higher $\\beta$ = faster zombie spread.")

    gamma = st.number_input(
        "$\\gamma$",
        min_value=0.00001,
        max_value=1.0,
        key="gamma",
        help=(
            "Removal rate (0 < gamma <= 1). Represents the daily probability "
            "that an active zombie is removed from the outbreak."
        )
    )
    st.caption("Higher $\\gamma$ = zombies are removed faster.")

    decay_fraction = st.number_input(
        "Decay Fraction",
        min_value=0.0,
        max_value=1.0,
        key="decay_fraction",
        help="Share of removed zombies that decay instead of being eliminated."
    )

    run_simulation = st.form_submit_button("Run Simulation")

if not run_simulation:
    st.stop()

st.divider()

model = ZombieSIR(
    days=days, 
    population=population, 
    initial_zombies=initial_zombies, 
    beta=beta, 
    gamma=gamma,
    decay_fraction=decay_fraction,
    seed=seed    
)
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

st.subheader("One Possible Outbreak")
st.caption(
    "One randomly generated outbreak showing how each population changes over time."
)

final_pop_col, final_inf_col, final_eliminated_col, final_decayed_col =  st.columns(4)
final_pop_col.metric(label="Final Human Population", value=model.results["Susceptible"].iloc[-1])
final_inf_col.metric(label="Final Infected", value=model.results["Infected"].iloc[-1])
final_eliminated_col.metric(label="Final Eliminated", value=model.results["Eliminated"].iloc[-1])
final_decayed_col.metric(label="Final Decayed", value=model.results["Decayed"].iloc[-1])

fig1 = single_run_plot(model.results)
st.pyplot(fig1)

st.subheader("Monte Carlo Simulation")
st.caption(
    f"Summary of outcomes across {trials:,} simulated outbreaks."
)
with st.spinner("Running Monte Carlo simulations...", show_time=True):
    results, daily_results = model.run_monte_carlo(trials=trials)
st.success("Simulations complete!")

extinction_probability = results["zombie_extinct"].mean()*100
apocalypse_probability = results["apocalypse"].mean()*100
median_survivors = results["final_survivors"].median()
median_peak_zombies = results["peak_infected"].median()

extinct_col, apocalypse_col, survivors_col, zombie_col = st.columns(4)

extinct_col.metric(
    "Zombie Extinction",
    f"{extinction_probability:.1f}%"
)

apocalypse_col.metric(
    "Apocalypse",
    f"{apocalypse_probability:.1f}%"
)

survivors_col.metric(
    "Median Survivors",
    f"{median_survivors:,.0f}"
)

zombie_col.metric(
    "Median Peak Zombies",
    f"{median_peak_zombies:,.0f}"
)


@st.fragment
def outbreak_range_plot(daily_results):
    st.subheader("Possible Outbreak Range")

    category = st.radio(
        "Population Group",
        SIED,
        index=1,
        horizontal=True
    )

    st.caption(
        f"Shows how the number of {category.lower()} varies across simulations."
    )
    fig = monte_carlo_band_plot(daily_results, category)
    st.pyplot(fig)

outbreak_range_plot(daily_results)

st.subheader("Final Survivor outcomes")
st.caption(
    "Distribution of the number of humans remaining at the end of each simulation."
)



fig3 = final_survivors_plot(results["final_survivors"], model.population)
st.pyplot(fig3)
