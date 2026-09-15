"""Create different plots to display Zombie Carlo Simulation results."""

import matplotlib.pyplot as plt 

from src.zombie_carlo.model import SIED

def _get_day_tick_step(max_day):
    """Return a readable x-axis tick interval for the simulation length."""
    if max_day <= 75:
        return 5
    if max_day <= 150:
        return 10
    if max_day <= 300:
        return 25
    if max_day <= 600:
        return 50
    
    return 100


def _get_pop_tick_step(population):
    """Return a readable tick interval for the population size."""
    if population <= 150:
        return 10
    if population <= 750:
        return 50
    if population <= 1500:
        return 100
    if population <= 2500:
        return 200
    if population <= 5000:
        return 500

    return 1000

def single_run_plot(results):
    """Plots one trial run from the simulation."""
    fig, ax = plt.subplots(figsize=(8, 5))

    days = results["Day"]
    max_day = days.max()
    tick_step = _get_day_tick_step(max_day)

    ax.plot(
        results["Day"], 
        results["Susceptible"],
        label="Susceptible",
        color="steelblue",
        linewidth=2
    )

    ax.plot(
        results["Day"], 
        results["Infected"],
        label="Infected",
        color="darkseagreen",
        linewidth=2
    )

    ax.plot(
        results["Day"],
        results["Eliminated"],
        label="Eliminated",
        color="dimgrey",
        linewidth=2
    )

    ax.plot(
        results["Day"],
        results["Decayed"],
        label="Decayed",
        color="black",
        linewidth=2
    )
    
    ax.set_xlabel("Day")
    ax.set_ylabel("Population")
    ax.set_title("One Possible Zombie Outbreak")

    ticks = list(range(0, max_day+1, tick_step))

    if max_day not in ticks:
        ticks.append(max_day)

    ax.set_xticks(ticks)

    ax.set_ylim(bottom=0)
    ax.margins(x=0)

    ax.grid(axis="y", alpha=0.15)
    ax.legend(frameon=False)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()

    
    return fig


def monte_carlo_band_plot(daily_results, category):
    """Plot median active zombies and Monte Carlo percentile bands."""
    if category not in SIED:
        raise ValueError("Not a daily reported category.")

    results_by_day = (
        daily_results.groupby("Day")[category]
        .quantile([0.05, 0.25, 0.50, 0.75, 0.95])
        .unstack()
    )

    fig, ax = plt.subplots(figsize=(8,5))

    days = results_by_day.index 
    max_day = days.max()
    tick_step = _get_day_tick_step(max_day)

    ax.fill_between(
        days,
        results_by_day[0.05],
        results_by_day[0.95],
        color="darkseagreen",
        alpha=0.6,
        label="Middle 90%"
    )
    ax.fill_between(
        days,
        results_by_day[0.25],
        results_by_day[0.75],
        color="seagreen",
        alpha=0.5,
        label="Middle 50%"
    )

    ax.plot(
        days,
        results_by_day[0.50],
        color="darkgreen",
        linewidth=2.5,
        label="Median"
    )

    ax.set_xlabel("Day")
    ax.set_ylabel(category)
    ax.set_title(f"Possible {category} Range")

    ticks = list(range(0, max_day+1, tick_step))

    if max_day not in ticks:
        ticks.append(max_day)

    ax.set_xticks(ticks)

    ax.set_ylim(bottom=0)
    ax.margins(x=0)

    ax.grid(axis="y", alpha=0.15)

    ax.legend(frameon=False)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()

    return fig


def final_survivors_plot(final_survivors, population):
    """Plots a histogram of the final survivors with Zombie Carlo styling."""
    fig, ax = plt.subplots(figsize=(8,5))

    tick_step = _get_pop_tick_step(population)

    mean_survivors = final_survivors.mean()
    median_survivors = final_survivors.median()

    ax.hist(
        final_survivors,
        bins=20,
        color="darkseagreen",
        edgecolor="white",
        linewidth=0.8,
        alpha=0.9
    )

    ax.axvline(
        median_survivors, 
        color="dimgray",
        linestyle=":",
        linewidth=2,
        label=f"Median: {median_survivors:.0f}"
    )

    ax.axvline(
        mean_survivors, 
        color="firebrick",
        linestyle="--",
        linewidth=2,
        label=f"Mean: {mean_survivors:.0f}"
    )

    ax.set_xlabel("Humans Remaining")
    ax.set_ylabel("Number of Simulations")
    ax.set_title("Who Survived the Outbreak?")

    ticks = list(range(0, population+1, tick_step))

    if population not in ticks:
        ticks.append(population)

    ax.set_xticks(ticks)

    ax.grid(
        axis="y",
        alpha=0.15
    )

    ax.legend(frameon=False)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.set_ylim(bottom=0)
    ax.margins(x=0)

    fig.tight_layout()
    
    return fig