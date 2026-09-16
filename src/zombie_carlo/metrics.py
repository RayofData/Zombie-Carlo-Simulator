"""Summarizes Monte Carlo results."""

def extinction_probability(results):
    return results["zombie_extinct"].mean() * 100


def apocalypse_probability(results):
    return results["apocalypse"].mean() * 100


def median_survivors(results):
    return results["final_survivors"].median()


def median_peak_zombies(results):
    return results["peak_infected"].median()