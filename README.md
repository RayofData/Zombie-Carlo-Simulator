# Zombie Carlo Simulator MVP

An **Streamlit Monte Carlo simulator** for a fictional zombie outbreak using an SIR-style model.

The simulator will run the same outbreak many times with randomness so the user can see a range of possible outcomes instead of one fixed result.

## Core Model

Track four groups:

* `susceptible` = humans who can still become zombies
* `infected` = active zombies spreading the outbreak
* `eliminated` = zombies removed by survivors
* `decayed_zombies` = zombies removed because they decay

`eliminated + decayed_zombies` make up the model's removed population.

The main parameters are:

* **$\beta$ (beta)** = transmission rate, or how quickly zombies create new zombies
* **$\gamma$ (gamma)** = removal rate, or how quickly active zombies stop spreading
* **$R_0$** = estimated number of new zombies one zombie would create when nearly everyone is still susceptible
* **decay fraction** = the share of removed zombies that become `decayed_zombies` instead of `eliminated`

Use:

$$
R_0 = \frac{\beta}{\gamma}
$$

A larger `beta` generally makes the outbreak spread faster. A larger `gamma` removes zombies faster and generally makes the outbreak easier to stop.

`gamma` determines how many active zombies are removed from the outbreak. The `decay fraction` then determines how those removed zombies are split between `eliminated` and `decayed_zombies`.

The simulation should use randomness when deciding how many humans become zombies and how many zombies are removed each day. Running the simulation hundreds or thousands of times will show how much the final outcome can vary even when the starting conditions are identical.

## MVP Features

### Presets

* Classic Movie Zombies
* Apocalypse Zombies
* Black Plague Zombies
* ZOMBIE-19
* Custom

Disease-inspired presets use real disease characteristics only as loose inspiration for fictional zombie parameters.

Each preset has fixed values for:

* `beta`
* `gamma`
* `decay fraction`

For **Custom**, the user can edit all three.

### User Inputs

For all scenarios:

* population
* initial zombies
* simulation days
* Monte Carlo runs

For **Custom** only:

* `beta`
* `gamma`
* `decay fraction`

## Results

Show:

* calculated `R0`
* extinction probability
* apocalypse probability
* median survivors
* peak zombies

An apocalypse is **80% or more of the original population becoming infected**.

## Streamlit Output

Include three main visualizations:

### 1. Single Outbreak Curve

Show one stochastic outbreak from beginning to end.

Plot the number of:

* susceptible humans
* active zombies
* removed zombies

over the simulation period.

This visualization explains how one possible outbreak develops over time.

### 2. Monte Carlo Uncertainty / Percentile Chart

Run the same scenario many times and summarize how the number of active zombies varies across simulations.

Show:

* median number of active zombies over time
* a middle percentile range, such as 25th–75th percentile
* a wider percentile range, such as 5th–95th percentile

This shows that identical starting conditions can produce very different outbreaks because the simulation is stochastic.

### 3. Final-Survivor Distribution

For every Monte Carlo run, record the number of susceptible humans remaining at the end of the simulation.

Display these values as a histogram.

This shows:

* the most common survivor outcomes
* whether outcomes are tightly grouped or highly variable
* how often the outbreak causes severe population loss
* how often the outbreak dies out early

Use this chart alongside summary statistics such as median survivors and apocalypse probability.