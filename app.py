import streamlit as st 

from src.zombie_carlo.model import ZombieSIR, SIED
from src.zombie_carlo.plots import (
    single_run_plot,
    monte_carlo_band_plot,
    final_survivors_plot
)
from src.zombie_carlo.metrics import (
    extinction_probability,
    apocalypse_probability,
    median_survivors,
    median_peak_zombies
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
        "gamma": 0.50,
        "decay_fraction": 0.10
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

PRESET_DESCRIPTIONS = {
    "Classic Movie Zombies": "Slower outbreak with moderate zombie removal.",
    "Apocalypse Zombies": "Fast spread with zombies that are difficult to remove.",
    "Runner Zombies": "Very fast spread with somewhat stronger zombie removal.",
    "Viral Zombies": "Extremely fast spread, but zombies are removed quickly.",
    "Rotter Zombies": "Moderate spread with heavy decay among removed zombies.",
    "Custom": "A neutral starting point for your own outbreak settings."
}

def load_preset():
    preset = PRESETS[st.session_state.preset]

    st.session_state.beta = preset["beta"]
    st.session_state.gamma = preset["gamma"]
    st.session_state.decay_fraction = preset["decay_fraction"]


if "preset" not in st.session_state:
    st.session_state.preset = "Classic Movie Zombies"
    load_preset()


st.image("static/zombie_banner.png")
st.caption("Zombie Carlo Simulator")



st.sidebar.header("Outbreak Setup")
st.sidebar.caption(
    "Choose the outbreak parameters, then select Run Simulation to see the results."
)

selected_preset = st.sidebar.selectbox(
    "Zombie Preset",
    PRESETS.keys(),
    key="preset",
    on_change=load_preset,
    help="Choose a starting scenario. You can adjust its parameters below."
)

st.sidebar.caption(PRESET_DESCRIPTIONS[selected_preset])


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
    humans = st.number_input(
        "Human Population",
        min_value=10,
        value=1000,
        max_value=1_000_000,
        help="Total number of humans and zombies at the start of the simulation."
    )

    initial_zombies = st.slider(
        "Initial Zombies",
        min_value=1,
        max_value=10,
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
    st.markdown(
        """
        ## About Zombie Carlo

        **Zombie Carlo Simulator** models a fictional zombie outbreak using a
        stochastic SIR-style model and Monte Carlo simulation. Instead of showing
        one fixed outcome, it shows how the same starting conditions can produce
        different results because of randomness.

        ### How It Works

        Each day, random draws determine how many humans become zombies and how
        many active zombies are removed.

        Three main parameters control the outbreak:

        - **Beta (β):** how quickly zombies infect humans
        - **Gamma (γ):** how quickly active zombies are removed
        - **Decay fraction:** how many removed zombies decay instead of being
          eliminated by survivors

        Presets provide starting values, and the sidebar lets you adjust them.

        ### What the Model Tracks

        - **Susceptible:** humans who can still become zombies
        - **Infected:** active zombies
        - **Eliminated:** zombies removed by survivors
        - **Decayed:** zombies removed through decay

        The total population remains constant throughout the simulation.

        ### What the Results Show

        After selecting **Run Simulation**, the app displays:

        - **One Possible Outbreak:** one randomized outbreak over time
        - **Possible Outbreak Range:** median and percentile ranges across many runs
        - **Final Survivor Distribution:** survivors remaining after each run
        - **Summary Metrics:** extinction probability, apocalypse probability,
          median survivors, and median peak zombies

        Adjust the sidebar controls, then select **Run Simulation** to begin.
        """
    )
    st.stop()

model = ZombieSIR(
    days=days, 
    humans=humans, 
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
R0_col.metric(
    label=r"$R_0$",
    value=round(model.beta / model.gamma, 2),
    help=(
        "Basic reproduction number: the expected number of new zombies "
        "produced by one active zombie when most of the population is susceptible. "
        "$R_0$ = $\\beta$ / $\\gamma$. Values above 1 favor outbreak growth; values below 1 favor decline."
    )
)

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

extinction_probability = extinction_probability(results=results)
apocalypse_probability = apocalypse_probability(results=results)
median_survivors = median_survivors(results=results)
median_peak_zombies = median_peak_zombies(results=results)

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
