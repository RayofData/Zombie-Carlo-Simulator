# Zombie Carlo Simulator

[![Live App](https://img.shields.io/badge/Live_App-Launch-FF4B4B?logo=streamlit&logoColor=white)](https://zombie-carlo-simulator-mksnkffwj9w8nc2nwpqxh7.streamlit.app/)

Zombie Carlo is a Streamlit Monte Carlo simulator for a fictional zombie
outbreak. It uses a stochastic SIR-style compartment model to show both one
possible outbreak and the range of outcomes that can occur under the same
starting conditions.

## Core Model

The model tracks four population groups:

* `Susceptible`: humans who can still become zombies
* `Infected`: active zombies spreading the outbreak
* `Eliminated`: zombies removed by survivors
* `Decayed`: zombies removed through decay

The total population is conserved throughout each simulation:

$$
Susceptible + Infected + Eliminated + Decayed = Population
$$

Each day, the model uses binomial random draws to determine:

1. how many susceptible humans become infected
2. how many active zombies are removed
3. how the removed zombies are split between eliminated and decayed

The daily infection probability is:

$$
p_{infection} = \beta \frac{Infected}{Population}
$$

The main parameters are:

* **$\beta$ (beta)**: transmission rate, which controls how quickly zombies
  create new zombies
* **$\gamma$ (gamma)**: removal rate, or the daily probability that an active
  zombie is removed from the outbreak
* **decay fraction**: the share of removed zombies that decay instead of being
  eliminated by survivors

The app also reports:

$$
R_0 = \frac{\beta}{\gamma}
$$

A larger beta generally causes faster spread. A larger gamma removes active
zombies more quickly. The decay fraction changes how removed zombies are
classified, but it does not change the total number removed.

## Presets and Editable Parameters

Presets provide starting values for beta, gamma, and decay fraction.

| Preset | Beta | Gamma | Decay fraction |
| --- | ---: | ---: | ---: |
| Classic Movie Zombies | 0.10 | 0.05 | 0.10 |
| Apocalypse Zombies | 0.30 | 0.03 | 0.03 |
| Runner Zombies | 0.45 | 0.08 | 0.08 |
| Viral Zombies | 0.75 | 0.50 | 0.10 |
| Rotter Zombies | 0.18 | 0.15 | 0.70 |
| Custom | 0.20 | 0.06 | 0.05 |

Selecting a preset loads its values into the controls. Beta, gamma, and decay
fraction remain editable for every preset, so presets act as starting templates
rather than locked scenarios. `Custom` provides a neutral starting point for a
fully user-defined outbreak.

## Simulation Controls

The Streamlit sidebar allows the user to select:

* starting human population
* initial zombies
* simulation length from 10 to 365 days
* 100, 500, 1,000, 5,000, or 10,000 Monte Carlo runs
* beta
* gamma
* decay fraction
* an optional random seed

The simulation runs only after the user selects **Run Simulation**. Enabling the
seed makes the results reproducible when the same inputs and seed are used.

## Results

### Outbreak Setup

The app summarizes the starting population, initial infected population,
simulation length, and calculated $R_0$.

### One Possible Outbreak

One stochastic simulation reports the final number of susceptible humans,
active zombies, eliminated zombies, and decayed zombies. A line chart shows all
four groups over time.

### Monte Carlo Summary

Repeated simulations produce four main summary metrics:

* **Zombie extinction probability**: percentage of runs ending with no active
  zombies
* **Apocalypse probability**: percentage of runs in which at least 80% of the
  original population becomes infected
* **Median survivors**: median number of susceptible humans remaining at the
  end of the runs
* **Median peak zombies**: median of the highest active-zombie population
  reached in each run

## Visualizations

### Single Outbreak Curve

Shows susceptible humans, active zombies, eliminated zombies, and decayed
zombies across one possible outbreak.

### Possible Outbreak Range

The user can view Monte Carlo uncertainty for any of the four population
groups. The chart shows:

* the median population by day
* the middle 50% of outcomes, from the 25th to 75th percentile
* the middle 90% of outcomes, from the 5th to 95th percentile

### Final-Survivor Distribution

A histogram shows the number of susceptible humans remaining at the end of
every Monte Carlo run. Reference lines identify the mean and median survivor
counts.

## Project Structure

* `model.py`: stochastic outbreak logic and repeated Monte Carlo simulations
* `plots.py`: Matplotlib visualizations
* `app.py`: Streamlit controls, metrics, and application layout

## Planned Testing

The core MVP is implemented. The next development step is a focused automated
test suite covering:

* population conservation
* nonnegative compartment values
* reproducible results with a fixed seed
* parameter and Monte Carlo trial validation
* extinction and apocalypse outcome logic
