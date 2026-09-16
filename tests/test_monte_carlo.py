"""Unit tests for Monte Carlo simulation and summary statistics."""

import pytest
from pandas.testing import assert_frame_equal


from src.zombie_carlo.model import ZombieSIR, SIED

def test_negative_trails_raises_error():
    with pytest.raises(ValueError):
        model = ZombieSIR()
        model.run_monte_carlo(-100)


def test_number_of_trails():
    expected_trials = 100
    days = 365
    expected_days = (days + 1)* expected_trials


    model = ZombieSIR(days=days)
    results, daily_results = model.run_monte_carlo(trials=expected_trials)

    assert len(results) == expected_trials
    assert len(daily_results) == expected_days


def test_same_seed_produces_same_results():
    model1 = ZombieSIR(seed=42)
    model2 = ZombieSIR(seed=42)

    results1, daily_results1 = model1.run_monte_carlo()
    results2, daily_results2 = model2.run_monte_carlo()

    assert_frame_equal(results1, results2)
    assert_frame_equal(daily_results1, daily_results2)