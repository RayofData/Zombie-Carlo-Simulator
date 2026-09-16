"""Unit tests over model parameters."""

import pytest
from pandas.testing import assert_frame_equal

from src.zombie_carlo.model import ZombieSIR, SIED

def test_negative_beta_raises_error():
    with pytest.raises(ValueError):
        ZombieSIR(beta=-0.1)


def test_large_beta_raises_error():
    with pytest.raises(ValueError):
        ZombieSIR(beta=2)


def test_negative_gamma_raises_error():
    with pytest.raises(ValueError):
        ZombieSIR(gamma=-0.1)


def test_large_gamma_raises_error():
    with pytest.raises(ValueError):
        ZombieSIR(gamma=2)


def test_negative_population_raises_error():
    with pytest.raises(ValueError):
        ZombieSIR(humans=-100)


def test_larger_infected_than_population():
    humans=100
    initial_zombies=200

    model = ZombieSIR(humans=humans, initial_zombies=initial_zombies)

    expected_population = humans + initial_zombies

    assert model.population == expected_population
    assert model.population == model.susceptible + model.infected


def test_zero_humans_starting_raises_error():
    with pytest.raises(ValueError):
        ZombieSIR(humans=0)


def test_zero_zombies_starting_raises_error():
    with pytest.raises(ValueError):
        ZombieSIR(initial_zombies=0)


def test_population_is_conserved():
    model = ZombieSIR()
    model.run_simulation()

    results = model.results

    totals = (
        results["Susceptible"]
        + results["Infected"]
        + results["Eliminated"]
        + results["Decayed"]
    )

    assert (totals == model.population).all()


def test_population_are_nonnegative():
    model = ZombieSIR(seed=42)
    model.run_simulation()


    assert (model.results[SIED] >= 0).all().all()


def test_same_seed_produces_same_results():
    model1 = ZombieSIR(seed=42)
    model2 = ZombieSIR(seed=42)

    model1.run_simulation()
    model2.run_simulation()

    assert_frame_equal(model1.results, model2.results)


def test_negative_decay_fraction_raises_error():
    with pytest.raises(ValueError):
        ZombieSIR(decay_fraction=-0.1)


def test_large_decay_fraction_raises_error():
    with pytest.raises(ValueError):
        ZombieSIR(decay_fraction=1.1)