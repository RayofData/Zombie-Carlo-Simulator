"""SIR Model for zombie infection spread."""

import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 


class ZombieSIR:
    def __init__(
        self,
        days=100, 
        susceptible=999, 
        infected=1, 
        beta=0.05, 
        gamma=0.01,
        decay_fraction=0.05,
        seed=None
    ):
        if not isinstance(days, int) or days <= 0:
            raise ValueError("Days must be a positive integer.")
        if not isinstance(susceptible, int) or susceptible <= 0:
            raise ValueError("Susceptible population must be a positive integer.")
        if not isinstance(infected, int) or infected <= 0:
            raise ValueError("Infected population must be a positive integer.")
        if not 0 <= beta <= 1:
            raise ValueError("Beta must be between 0 and 1.")
        if not 0 <= gamma <= 1:
            raise ValueError("Gamma must be between 0 and 1.")
        if not 0 <= decay_fraction <= 1:
            raise ValueError("Decay fraction must be between 0 and 1.")
    
        self.days = days
        self.susceptible = susceptible
        self.infected = infected
        self.eliminated = 0
        self.decayed_zombies = 0
        self.beta = beta
        self.gamma = gamma
        self.decay_fraction = decay_fraction
        self.num_individuals = susceptible + infected
        self.results = None
        self.rng = np.random.default_rng(seed)


    def run_simulation(self):
        """Run one stochastic zombie outbreak simulation."""
        S = [self.susceptible]
        I = [self.infected]
        E = [self.eliminated]
        D = [self.decayed_zombies]

        for _ in range(1, self.days):
            infection_probability = self.beta * I[-1] / self.num_individuals
            new_infections = self.rng.binomial(S[-1], infection_probability)

            removed = self.rng.binomial(I[-1], self.gamma)
            new_decayed = self.rng.binomial(removed, self.decay_fraction)
            new_eliminated = removed - new_decayed

            S.append(S[-1] - new_infections)
            I.append(I[-1] + new_infections - removed)
            E.append(E[-1] + new_eliminated)
            D.append(D[-1] + new_decayed)

        self.results = pd.DataFrame(
            {
                "Day": range(len(S)),
                "Susceptible": S,
                "Infected": I,
                "Eliminated": E,
                "Decayed": D
            }
        )


    def run_monte_carlo(self, trials=1000): 
        """Run repeated outbreak simulations and return their outcomes."""

        if not isinstance(trials, int) or trials <= 0:
            raise ValueError("Number of trials must be a positive integer.")  
        outcomes = []

        for _ in range(trials):
            self.run_simulation()

            final_survivors = self.results["Susceptible"].iloc[-1]
            final_infected = self.results["Infected"].iloc[-1]
            final_eliminated = self.results["Eliminated"].iloc[-1]
            final_decayed = self.results["Decayed"].iloc[-1]

            peak_infected = self.results["Infected"].max()

            total_ever_infected = self.num_individuals - final_survivors

            extinct = final_infected == 0

            apocalypse = (total_ever_infected / self.num_individuals >= 0.8)

            outcomes.append(
                {
                    "final_survivors": final_survivors,
                    "final_infected": final_infected,
                    "final_eliminated": final_eliminated,
                    "final_decayed": final_decayed,
                    "total_ever_infected": total_ever_infected,
                    "peak_infected": peak_infected,
                    "extinct": extinct,
                    "apocalypse": apocalypse
                }
            )

        return pd.DataFrame(outcomes)

