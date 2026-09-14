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
        eliminated=0, 
        decayed_zombies=0,
        beta=0.05, 
        gamma=0.01,
        decay_fraction=0.05
    ):
        self.days = days
        self.susceptible = susceptible
        self.infected = infected
        self.eliminated = eliminated
        self.decayed_zombies = decayed_zombies
        self.beta = beta
        self.gamma = gamma
        self.decay_fraction = decay_fraction
        self.num_individuals = (
            susceptible + infected + eliminated + decayed_zombies
        )
        self.results = None
        self.model_run = False


    def run_simulation(self):
        S = [self.susceptible]
        I = [self.infected]
        E = [self.eliminated]
        D = [self.decayed_zombies]

        for _ in range(1, self.days):
            infection_probability = min(
                self.beta * I[-1] / self.num_individuals, 
                1.0
            )
            new_infections = np.random.binomial(S[-1], infection_probability)
            removed = np.random.binomial(I[-1], self.gamma)
            new_decayed = np.random.binomial(removed, self.decay_fraction)
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
            },
            orient="index"
        ).transpose()
        self.model_run = True


    def run_monte_carlo(self, trials=1000):   
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


