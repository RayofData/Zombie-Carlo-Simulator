"""Create different plots to display Zombie Carlo Simulation results."""

import matplotlib.pyplot as plt 

from src.zombie_carlo.model import SIED

def single_run_plot(results):
    """Plots a single trail run from simulation."""
    fig, ax = plt.subplots(figsize=(8,5))

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

    ax.grid(axis="y", alpha=0.15)
    ax.legend(frameon=False)

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

    fig, ax = plt.subplots()

    days = results_by_day.index 

    ax.fill_between(
        days,
        results_by_day[0.05],
        results_by_day[0.95],
        alpha=0.2,
        label="5th-95th percentile"
    )
    ax.fill_between(
        days,
        results_by_day[0.25],
        results_by_day[0.75],
        alpha=0.4,
        label="25th-75th percentile"
    )

    ax.plot(
        days,
        results_by_day[0.50],
       label="Median"
    )

    ax.set_xlabel("Day")
    ax.set_ylabel(category)
    ax.set_title(f"Possible {category} Outcomes")
    ax.legend()
    fig.tight_layout()

    return fig


def final_survivors_plot(final_survivors):
    """Plots a histogram of the final survivors with Zombie Carlo styling."""
    fig, ax = plt.subplots(figsize=(8,5))

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
        color = "dimgray",
        linestyle = ":",
        linewidth = 2,
        label = f"Median: {median_survivors:.0f}"
    )

    ax.axvline(
        mean_survivors, 
        color = "firebrick",
        linestyle = "--",
        linewidth = 2,
        label = f"Mean: {mean_survivors:.0f}"
    )

    ax.set_xlabel("Humans Remaining")
    ax.set_ylabel("Number of Simulations")
    ax.set_title("Who Survived the Outbreak?")

    ax.grid(
        axis="y",
        alpha=0.15
    )

    ax.legend(frameon=False)

    fig.tight_layout()
    
    return fig