"""Create different plots to display Zombie Carlo Simulation results."""

import matplotlib.pyplot as plt 

def single_run_plot(results):
    """Plots a single trail run from simulation."""
    fig, ax = plt.subplots()

    ax.plot(
        results["Day"], 
        results["Susceptible"],
        label="Susceptible",
        color = "blue"
    )

    ax.plot(
        results["Day"], 
        results["Infected"],
        label="Infected",
        color = "green"
    )

    ax.plot(
        results["Day"],
        results["Eliminated"],
        label="Eliminated",
        color = "grey"
    )

    ax.plot(
        results["Day"],
        results["Decayed"],
        label="Decayed",
        color = "black"
    )
    
    ax.set_xlabel("Day")
    ax.set_ylabel("Population")
    ax.set_title("Single Zombie Outbreak")
    ax.legend()

    
    return fig


def monte_carlo_band_plot(daily_results, category):
    """Plot median active zombies and Monte Carlo percentile bands."""
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
    """Plots a histogram of the final survivors for all simulations."""
    fig, ax = plt.subplots()

    ax.hist(final_survivors)

    ax.set_xlabel("Final Survivors")
    ax.set_ylabel("Number of Simulations")
    ax.set_title("Final Survivors Distribution")
    fig.tight_layout()
    
    return fig