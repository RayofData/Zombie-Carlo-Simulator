"""Test summary metrics from Monte Carlo simulations."""

import pandas as pd

from src.zombie_carlo.metrics import (
    extinction_probability,
    apocalypse_probability,
    median_survivors,
    median_peak_zombies
)

def test_extinction_probability():
    results = pd.DataFrame(
        {
            "zombie_extinct": [True, True, False, False]
        }
    )

    assert extinction_probability(results) == 50


def test_apocalypse_probability():
    results = pd.DataFrame(
        {
            "apocalypse": [True, False, False, False]
        }
    )

    assert apocalypse_probability(results) == 25


def test_median_survivors():
    results = pd.DataFrame(
        {
            "final_survivors": [100, 200, 300]
        }
    )

    assert median_survivors(results) == 200


def test_median_peak_zombies():
    results = pd.DataFrame(
        {
            "peak_infected": [50, 100, 150]
        }
    )

    assert median_peak_zombies(results) == 100