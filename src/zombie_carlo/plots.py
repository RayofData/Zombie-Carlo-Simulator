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



def final_survivors_plot(final_survivors):
    """Plots a histogram of the final survivors for all simulations."""
    fig, ax = plt.subplots()

    ax.hist(final_survivors)

    ax.set_xlabel("Total Number of Survivors at the end of days.")
    ax.set_ylabel("Count")
    ax.set_title("Final Survivors Distribution")
    
    return fig