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
        E = [self.eliminated ]
        D = [self.decayed_zombies]

        for _ in range(1, self.days):
            infection_probability = min(self.beta * I[-1] / self.num_individuals, 1.0)
            new_infections = np.random.binomial(S[-1], infection_probability)
            removed = np.random.binomial(I[-1], self.gamma)
            new_decayed = np.random.binomial(removed, self.decay_fraction)
            new_eliminated = removed - new_decayed
            S.append(S[-1] - new_infections)
            I.append(I[-1] + new_infections - removed)
            E.append(E[-1] + new_eliminated)
            D.append(D[-1] + new_decayed)

        self.results = pd.DataFrame.from_dict({"Time":list(range(len(S))),
            "Susceptible":S, "Infected":I, "Eliminated":E, "Decayed":D},
            orient="index").transpose()
        self.model_run = True


        
for _ in range(3):
    model = ZombieSIR()
    model.run_simulation()

    print(model.results.iloc[-20])

    totals = (
        model.results["Susceptible"]
        + model.results["Infected"]
        + model.results["Eliminated"]
        + model.results["Decayed"]
    )

    print(totals.min())
    print(totals.max())
    print(model.results.head(10))